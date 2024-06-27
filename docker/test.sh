#!/bin/bash

# This file should be used to test AGAINST a container. Meaning, it should test a
# container from outside the container and try and get in.
#
# It looks for a `test.json` file in the same directory. That json file should simply contain a list of URIs with preceeding /, followed by
# what it expects as successful output. If you put simply a 3 digit response code, it'll match the HTTP response code against that.
# If you put a string, it will try to do a regex match. If the regex contains a capture group, it'll return teh 1st captured result. If the
# regex does not contain a capture group, it'll return the number of times it matched.


# Colors
NC="\033[0m" # default color
RD="\033[0;31m"
GR="\033[0;32m"
BL="\033[0;34m"
BR="\033[0;33m"
BOLD="\\033[1m"

# Working directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Repo information
REPO=$("$DIR/npm_helper.sh" 'repo')
BRANCH=$("$DIR/npm_helper.sh" 'branch')

# Output function
function out {
	# Shorten $2 and $3 if they're too long
	SHORT_2=$(echo "$2"| awk -v len=40 '{ if (length($0) > len) print substr($0, 1, len-4) "..."; else print; }')
	SHORT_3=$(echo "$3"| awk -v len=40 '{ if (length($0) > len) print substr($0, 1, len-4) "..."; else print; }')

	# Format output
	if [[ $1 == "pass" ]]; then
		printf "${GR}%-5s" "[✓]" && \
		printf "%-2s" "" && \
		printf "${BL}%-40s" "$SHORT_2" && \
		printf "%-2s" "" && \
		printf "${GR}%-40s" "$SHORT_3" && \
		printf "%-2s" "" && \
		printf "${NC}%-0s\n" "$4"
	elif [[ $1 == "fail" ]]; then
		printf "${RD}%-5s" "[✗]" && \
		printf "%-2s" "" && \
		printf "${BL}%-40s" "$SHORT_2" && \
		printf "%-2s" "" && \
		printf "${RD}%-40s" "$SHORT_3" && \
		printf "%-2s" "" && \
		printf "${NC}%-0s\n" "$4"
	elif [[ $1 == "skip" ]]; then
		printf "${BR}%-5s" "[…]" && \
		printf "%-2s" "" && \
		printf "${NC}%-40s" "$SHORT_2"
		printf "%-2s" "" && \
		printf "%-40s" "" && \
		printf "%-2s" "" && \
		printf "%-0s\n" "$3"
	elif [[ $1 == "error" ]]; then
		printf "${RD}%-5s" "!" && \
		printf "%-2s" "" && \
		printf "${RD}%-0s\n" "$2"
		exit 1
	fi
}

# Starting
echo -e "Testing script starting..."

# Get container port
PORT=$(cat "$DIR/Dockerfile" | grep -i '^EXPOSE' | awk '{print $2}')
if [[ $PORT ]]; then
	echo -e "Detected port $PORT"
else
	out "error" "Could not automatically locate a port to test on inside the Dockerfile${NC}"
	exit 1
fi

# Build HOST
if [[ $BRANCH == "master" ]]; then
	HOST="$REPO.widespreadsales.com"
else
	HOST="$BRANCH-$REPO.widespreadsales.com"
fi

# Build URL
URL="http://localhost:$PORT"

# Verify test.json exists
if [[ -f "$DIR/test.json" ]]; then
	echo -e "Found test.json"
	# See if want to skip tests
	if [[ $(grep -q '^disable' "$DIR/test.json"; echo $?) == 0 ]]; then
		echo "Found 'disable' in test.json file. Skipping tests and continuing."
		exit 0
	fi
else
	out "error" "Couldn't locate JSON file"
	exit 1
fi

# Message
echo -e "Starting tests"
echo -e "--------------"
echo -e "${GR}$URL${NC}"
echo -e "--------------"

# Process test routes
while read -r LINE; do

	# Reset variables
	unset STATUS
	unset PATTERN

	# Extract route
	ROUTE=$(echo "$LINE" | pcregrep -o1 -Mi -e '"(.*)"\s*:\s*')

	# Be sure route exists before moving on
	if [[ ! "$ROUTE" ]]; then
		continue
	fi

	# Expect a response code?
	CODE_EXPECT=$(echo "$LINE" | pcregrep -o1 -Mi -e '".*"\s*:\s*([0-9]{3})')

	# Expect a regex match?
	PATTERN=$(echo "$LINE" | pcregrep -o1 -Mi -e '".*"\s*:\s*"([^"]*)"')

	# Process
	if [[ $CODE_EXPECT ]]; then
		# Get response code
		CODE_RESPONSE=$(curl -is -o /dev/null -w '%{http_code}' -H "Host: $HOST" -m 5 "$URL$ROUTE")

		# Fix code for timeouts
		if [[ $CODE_RESPONSE == "000" ]]; then
			CODE_RESPONSE="timeout"
		fi

		# Validate
		if [[ $CODE_RESPONSE -eq $CODE_EXPECT ]]; then
				out "pass" "$CODE_EXPECT" "$CODE_RESPONSE" "$ROUTE"
			else
				out "fail" "$CODE_EXPECT" "$CODE_RESPONSE" "$ROUTE"
				FAIL=true
		fi
	elif [[ "$PATTERN" ]]; then
		# Curl
		HTML=$(curl -is "$URL")

		# Parse REGEX pattern to see if it contains a group match
		GROUP=$(echo "$PATTERN" | sed -E 's/\\\)//' | sed -E 's/\\\(//' | grep -io -E '\([^\)]*\)')

		# If regex tries to match group, behave differently
		if [[ "$GROUP" ]]; then
			# Run REGEX to match capture group
			CAPTURE=$(echo "$HTML" | pcregrep -o1 -Mi -e "$PATTERN" | head -n 1)

			# Validate
			if [[ $CAPTURE ]]; then
				out "pass" "$PATTERN" "$CAPTURE" "$ROUTE"
			else
				out "fail" "$PATTERN" "No group match" "$ROUTE"
				FAIL=true
			fi
		else
			# No capture group in REGEX so run and count number of lines that match
			MATCHES=$(echo "$HTML" | pcregrep -ci -e "$PATTERN")

			# If no group match, then get count of lines that match
			if [[ $MATCHES -gt 0 ]]; then
				out "pass" "$PATTERN" "$MATCHES matches" "$ROUTE"
			else
				out "fail" "$PATTERN" "$MATCHES matches" "$ROUTE"
				FAIL=true
			fi
		fi
	else
		# Detected a route but not a valid check
		out "skip" "Skipping - no expectation." "$ROUTE"
	fi
done < "$DIR/test.json"

# Finished
echo -e "---"

# Exit with proper status code
if [[ $FAIL == true ]]; then
	echo -e "${RD}Some routes failed.${NC}"
	exit 1
else
	echo -e "${GR}All routes passed successuflly.${NC}"
	exit 0
fi
