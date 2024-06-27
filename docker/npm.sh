#!/bin/bash
#
# This script holds the more complicated NPM run commands.
# In the package.json, simply use ./docker/npm.sh {command_name} {arg1, arg2, etc.}
#

############
## VARIABLES
############
# Colors for terminal
NC="\\033[0m"		# No Color
RD="\\033[0;31m"	# Red
GN="\\033[0;32m"	# Green
BR="\\033[1;33m"	# Brown
LB="\\033[2;33m"	# Light Brown
BL="\\033[0;34m"	# Blue
PK="\\033[0;35m"	# Pink
LG="\\033[0;37m"	# Light Grey
YL="\\033[1;33m"	# Yellow
CY="\\033[0;36m"	# Cyan
CY="\\033[0;36m"	# Cyan

BOLD="\\033[1m"		# BOLD


# Repo details
REPO=$(docker/npm_helper.sh 'repo')
BRANCH=$(docker/npm_helper.sh 'branch')
COMMIT=$(docker/npm_helper.sh 'commit')
PORTS=$(docker/npm_helper.sh 'ports')

# Working directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Server name provided in input?
if [[ $2 == "staging" || $2 == "master" ]]; then
	# Is this repo currently running on server as a docker service?
	COMMAND="docker service ls | grep ${SERVER}_$REPO >/dev/null || exit 1"
	SERVER="$2.widespread.com"

	if [[ $2 == "master" ]]; then
		ssh widespread1@$SERVER -p 1022 "$COMMAND" && \
		SERVICE=true || \
		SERVICE=false
	else
		ssh root@$SERVER -p 1022 "$COMMAND" && \
		SERVICE=true || \
		SERVICE=false
	fi

	# Does this repo have a runcommand (used to run container instead of docker stack YML file.
	if [[ -f "$DIR/runcommand.txt" ]]; then
		RUNCOMMAND=$(echo $(eval echo $(cat "$DIR/runcommand.txt")))
	else
		RUNCOMMAND=false
	fi
fi

############
## FUNCTIONS
############


#####
# Display which step is currently being run
#####
function display_step()
{
	echo -e "\\033[48;5;7m \\033[1m=============== $1 ===============\\033[0m"
}

#####
# Be sure working on branch we think we are
#####
function docker_safety_check()
{
	display_step "${FUNCNAME[0]}"

	# Check that the $1 and $BRANCH are the same
	if [[ "$BRANCH" != "$1" ]]; then
		# Play alert sound to notify user of prompt
		afplay /System/Library/Sounds/Sosumi.aiff

		echo -e "${BR}WARNING: ${NC}Trying to push to ${PK}$1${NC} from the ${BL}$BRANCH${NC} github branch!"
		# Override?
		while true; do
			# Valid answer?
			if [[ $ANSWER == "yes" || $ANSWER == "y" ]]; then
				echo -e "${BR}Ignoring server / branch mismatch. Continuing...${NC}"
				break
			elif [[ $ANSWER == "no" || $ANSWER == "n" ]]; then
				exit 1
			fi

			# Ask if want to override
			echo -n "Ignore warning and continue? (yes|no):"

			# Prompt for answer
			read ANSWER
		done
	else
		echo -e "${GR}SUCCESS: ${NC}Safety checks passed. Attempting to push to ${PK}$1 ${NC}from ${BL}$BRANCH ${NC}branch."
	fi
}

#####
# Builds image based on current repo
#####
function docker_build()
{
	display_step "${FUNCNAME[0]}"
	echo -e "Building ${BL}widespread/$REPO:$BRANCH${NC}"

	# Find dockerfile in either repo/Dockerfile or repo/docker/Dockerfile
	if [[ -f 'docker/Dockerfile' ]]; then
		docker build --no-cache -f docker/Dockerfile -t "widespread/$REPO:$BRANCH" .
	else
		docker build --no-cache -t "widespread/$REPO:$BRANCH" .
	fi

	# Success?
	if [[ $? -eq 0 ]]; then
		echo -e "${GN}SUCCESS: ${NC}Built image ${BL}widespread/$REPO:$BRANCH${NC}."
	else
		echo -e "${RD}ERROR: ${NC}Couldn't build ${BL}widespread/$REPO:$BRANCH${NC}. Stopping."; exit 1
	fi
}

#####
# Pushe image to remote dockerhub repo
#####
function docker_push()
{
	display_step "${FUNCNAME[0]}"
	PUSHCOMMIT=true

	# Verify origin is up to date
	if [[ $(git status | head -n 2 | tail -n 1 | grep -q "Your branch is up to date with 'origin/"; echo $?) -gt 0 ]]; then
		# Play alert sound to notify user of prompt
		afplay /System/Library/Sounds/Sosumi.aiff

		# Warning
		echo -e "${BR}WARNING: ${NC}According to 'git status', you have unpublished work."

		# Flag so we don't push up commit later
		PUSHCOMMIT=false

		# Prompt for override
		while true; do
			# Valid answer?
			if [[ $ANSWER == "yes" || $ANSWER == "y" ]]; then
				echo -e "${BR}Ignoring unpublished github changes. Continuing...${NC}"
				break
			elif [[ $ANSWER == "no" || $ANSWER == "n" ]]; then
				exit 1
			fi

			# Ask if want to override
			echo -n "Ignore warning and continue? (yes|no):"

			# Prompt for answer
			read ANSWER
		done
	fi

	# Message
	echo -e "Pushing ${BL}widespread/$REPO:$BRANCH ${NC}"

	# Tag image with branch name and also commit
	if [[ $PUSHCOMMIT == true ]]; then
		docker tag "widespread/$REPO:$BRANCH" "widespread/$REPO:$BRANCH-$COMMIT"
		docker push "widespread/$REPO:$BRANCH-$COMMIT"

		if [[ $? -eq 0 ]]; then
			echo -e "${GN}SUCCESS: ${NC}Pushed ${BL}widespread/$REPO:$BRANCH-$COMMIT ${NC}"
		else
			echo -e "${RD}ERROR: ${NC}Couldn't push ${BL}widespread/$REPO:$BRANCH-$COMMIT${NC}"
		fi
	fi

	# Push
	docker push "widespread/$REPO:$BRANCH"

	# Success
	if [[ $? -eq 0 ]]; then
		echo -e "${GN}SUCCESS: ${NC}Pushed ${BL}widespread/$REPO:$BRANCH ${NC}"
	else
		echo -e "${RD}ERROR: ${NC}Couldn't push ${BL}widespread/$REPO:$BRANCH${NC}"
	fi
}

#####
# Kill running containers named `npm_$REPO`
#####
function docker_kill()
{
	display_step "${FUNCNAME[0]}"

	# Container running?
	if [[ $(docker ps | grep "npm_$REPO") ]]; then
		docker kill "npm_$REPO$1" >/dev/null
		echo -e "${GN}SUCCESS: ${NC}Killed ${CY}npm_$REPO$1${NC}"
	else
		echo -e "${GR}NOTICE: ${NC}No ${CY}npm_$REPO$1${NC} containers to kill."
	fi
}

#####
# Remove containers named `npm_$REPO`
#####
function docker_rm()
{
	display_step "${FUNCNAME[0]}"

	# Container exists?
	if [[ $(docker ps -a | grep "npm_$REPO$1") ]]; then
		docker rm "npm_$REPO$1" > /dev/null
		echo -e "${GN}SUCCESS: ${NC}Removed ${CY}npm_$REPO$1${NC}"
	else
		echo -e "${GR}NOTICE: ${NC}No ${CY}npm_${REPO}$1${NC} containers to remove."
	fi
}

#####
# Start container
#####
function docker_run()
{
	display_step "${FUNCNAME[0]}"

	# Detached mode?
	if [[ "$1" == '-d' ]]; then
		DETACHED='-d'
		MODE=" in detached mode"
	fi

	# Message
	echo -e "${GN}SUCCESS: ${NC}Starting container ${CY}npm_$REPO$2${NC}$MODE."
	if [[ "$1" == '-d' ]]; then
		echo -e "Streaming logs below...."
		echo -e "Use ctrl + c to stop or ctrl + p + q to detach shell and leave container running."
		echo -e "================================================================================="
	fi

	# Run
	if [[ $(docker ps | grep ":$PORTS" | awk '{print $1}') != "" ]]; then
		# Play alert sound to notify user of prompt
		afplay /System/Library/Sounds/Sosumi.aiff

		# Another container running, prompt for removing it
		echo -e "${BR}WARNING: ${NC}It looks like another container is already running with port $PORTS. Would you like to kill that container and start a new one for this test?)"

		while true; do
			# Valid answer?
			if [[ $ANSWER == "yes" || $ANSWER == "y" ]]; then
				echo -e "${BR}Stopping other container and starting a new one${NC}"
				docker stop $(docker ps | grep "$PORTS" | awk '{print $1}')
				docker run $DETACHED -it $PORTS --name npm_$REPO$2 widespread/$REPO:$BRANCH || (echo -e "${RD}ERROR: ${NC}Couldn't start a container using ${BL}widespread/$REPO:$BRANCH${NC} (or you exited the container with ctrl + c)"; exit 1)
				exit 0
			elif [[ $ANSWER == "no" || $ANSWER == "n" ]]; then
				exit 1
			fi

			# Ask if want to override
			echo -n "Ignore failure and continue? (yes|no):"

			# Prompt for answer
			read ANSWER
		done
	else
		# Start continaer
		docker run $DETACHED -it $PORTS --name npm_$REPO$2 widespread/$REPO:$BRANCH || (echo -e "${RD}ERROR: ${NC}Couldn't start a container using ${BL}widespread/$REPO:$BRANCH${NC} (or you exited the container with ctrl + c)"; exit 1)
	fi
}

#####
# Run automated tests against container
#####
function docker_test()
{
	display_step "${FUNCNAME[0]}"

	# Verify check string is passed
	if [[ $# -lt  1 ]]; then
		echo -e "${RED}ERROR: ${NC}No up message parameter specified. Must pass a string to look for in the container log output to determine when the container is fully 'up'."
		echo "Example: 'Nginx successfully started'"
		echo "Alternatively, you can use 'wait:XX' and indicate a specific number of seconds to wait instead of checking for a value."
		echo "You can also use a value of simply 'disable' to disable tests."
		exit 1
	fi

	# Verify a container is running
	if [[ ! $(docker ps | grep "npm_$REPO$2") ]]; then
		echo -e "${RD}ERROR: ${NC}No container ${CY}npm_$REPO$2 ${NC}running..."
		exit 1
	fi

	# Check to be sure container is finished loading
	if [[ $(echo "$1" | grep -q '^wait:[0-9]+'; echo "$?") == 0 ]]; then
		SLEEP=$(echo "$1" | cut -d: -f2)
		# Wait seconds rather than check for value
		echo -e "Waiting $SLEEP seconds for container to finish starting\c"

		# Wait
		SNORE=1
		while [[ $SNORE -le $SLEEP ]]; do
			echo -e ".\c"
			sleep 1
			((SNORE++))
		done
		echo ""
	elif [[ $1 != "" ]]; then
		## Disable tests?
		if [[ $1 == 'disable' ]]; then
			echo -e "${GN}SKIPPING: ${NC}Found 'disable' in package.json config. Skipping tests."
			exit 0
		fi

		echo -e "Checking for \"${BOLD}$1${NC}\" in container logs to see if it's finished starting..."

		# Set limit & count for checking if container is up
		LIMIT=250
		COUNT=1

		# Check if container up
		while [[ $(docker logs "npm_$REPO$2" 2>/dev/null | grep -m 1 "$1") == "" ]]; do
			# Clear line on subsequent counts
			echo -e "\\033[1K\\033[1G\c"

			# Message
			echo -e "($COUNT/$LIMIT) Checking.\c"

			# Add dots
			DOTS=1
			while [[ $DOTS -lt $COUNT ]]; do
				echo -e ".\c"
				((DOTS++))
			done

			# Reached limit?
			if [[ $COUNT -ge $LIMIT ]]; then
				echo -e "${RD}ERROR: ${NC}Couldn't detect '$1' in container logs to determine that the container is running."
				echo -e "Below are the logs from the container. Perhaps it had an error, or, the 'upmessage' changed and you need to update package.json?"
				echo -e "----------"
				docker logs "npm_$REPO$2"
				echo -e "----------"
				exit 2
			fi

			# Increment
			((COUNT++))

			# Wait
			sleep 1
		done

		# Success
		echo -e "${GN}SUCCESS: ${NC}Found '${BOLD}$1${NC}'. Container ${CY}'npm_$REPO$2' ${NC}started. Continuing..."
	else
		# Default
		echo -e "Wait time or word to check for were not specified. Waiting default 10 seconds for container to start.\c"
		SLEEP=10
		SNORE=1
		while [[ $SNORE -le $SLEEP ]]; do
			echo -e ".\c"
			sleep 1
			((SNORE++))
		done
		echo ""
	fi

	# Run automated tests
	$DIR/test.sh

	# Tests failed?
	if [[ $? != 0 ]]; then
		# Play alert sound to notify user of prompt
		afplay /System/Library/Sounds/Sosumi.aiff

		# Prompt for override unless on master
		if [[ $BRANCH == 'master' ]]; then
			# Failed, stop and output error
			echo -e "${RD}ERROR: ${NC}Some automated tests failed. Stopping. Please resolve failures and try again."
			exit 1
		else
			# Not on master branch and failed, prompt for override
			echo -e "${BR}WARNING: ${NC}Some automated tests failed (see output above for details.)"
			while true; do
				# Valid answer?
				if [[ $ANSWER == "yes" || $ANSWER == "y" ]]; then
					echo -e "${BR}Ignoring failed tests... Continuing...${NC}"
					exit 0
				elif [[ $ANSWER == "no" || $ANSWER == "n" ]]; then
					exit 1
				fi

				# Ask if want to override
				echo -n "Ignore failure and continue? (yes|no):"

				# Prompt for answer
				read ANSWER
			done
		fi
	else
	# Tests passed
		echo -e "${GN}SUCCESS: ${NC}All tests passed."
		exit 0
	fi
}

#####
# Remove old containers and images
# Only affects `npm_$REPO` named containers
#####
function docker_clean()
{
	display_step "${FUNCNAME[0]}"

	# Kill containers
	docker kill $(docker ps | grep "npm_$REPO$1" | awk '{print $1}') 2>/dev/null

	# Remove containers
	docker rm $(docker ps -a | grep "npm_$REPO$1" | awk '{print $1}')
	echo -e "${GN}SUCCESS: ${NC}Cleaned any ${CY}npm_$REPO$1${NC} containers."

	# Remove images
	docker rmi $(docker images | grep "widespread/$REPO" | tail -n +2 | awk '{print $3}')
	echo -e "${GN}SUCCESS: ${NC}Cleaned any ${CY}widespread/$REPO${NC} images."
}

#####
# Deploy to server
#####
function docker_deploy()
{
	# Safety check
	docker_safety_check "$1"

	# Display step after safety check (because safety check displays its step)
	display_step "${FUNCNAME[0]}"

	SERVER_NAME="root@$1.widespread.com"

	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	# Update service
	if [[ $SERVICE == true ]]; then
		ssh $SERVER_NAME -p 1022 << EOF
			docker image pull "widespread/$REPO:$BRANCH"
			docker service update --force --image "widespread/$REPO:$BRANCH" "${1}_$REPO$2" > /dev/null 2>/dev/null \
			&& msg-admin "Successfully updated *${1}_$REPO$2* service." \
			|| (msg-admin "Failed to update *${1}_$REPO$2*! Check logs."; exit 1)
EOF
		# Success?
		if [[ $? -eq 0 ]]; then
			SUCCESS=true
		fi
	# No service running. Do aditional check.
	else
		# Runcommand file exists? (means this repo isn't run as a service)
		if [[ $RUNCOMMAND == false ]]; then
			# Not currently running. Should be started for first time as part of stack with docker repo. Output error.
			echo -e "${RD}ERROR:${NC}The ${CY}\"${1}_$REPO$2\"${NC} service is not currently running on the ${PK}$1 ${NC}server. You should use the docker repo to deploy the entire ${PK}$1 ${NC}stack instead."; exit 1
		else
			# If already running, then stop & remove
			ssh $SERVER_NAME -p 1022 << EOF
				docker image pull "widespread/$REPO:$BRANCH"
				(docker stop $REPO$2 && docker rm $REPO$2)  \
				|| (msg-admin 'Error trying to stop/remove container *$REPO$2*.'; exit 1)

				$RUNCOMMAND >/dev/null 2>/dev/null \
				&& msg-admin 'Container *$REPO$2* successfully deployed.' \
				|| (msg-admin 'Error trying to deploy *$REPO$2* container.'; exit 1)
EOF

			# Success?
			if [[ $? -eq 0 ]]; then
				SUCCESS=true
			fi
		fi
	fi

	# Message
	if [[ $SUCCESS == true ]]; then
		echo -e "${GN}SUCCESS: ${NC}Deployed ${BL}${1}_$REPO$2${NC} to ${PK}$1${NC} server."
		#say -v Daniel "Deployed $REPO repository to $1 server"
	else
		echo -e "${RD}ERROR: ${NC}Couldn't deploy ${BL}${1}_$REPO$2${NC} to ${PK}$1${NC} server."
		#say -v Daniel "Error. Couldn't deploy $REPO repository to $1 server"
	fi
}

#####
# Reload (restarts) running containers without any updates.
#
# Useful for things like www containers which pull API configs when the container starts
#####
function docker_reload()
{
	# Safety check
	docker_safety_check "$1"

	# Display step after safety check (because safety check displays its step)
	display_step "${FUNCNAME[0]}"

	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	#
	ssh $SERVER_NAME -p 1022 docker service update --force ${1}_$REPO

	echo -e "${GN}SUCCESS: ${CY}${1}_$REPO$2${NC} successfully reloaded. Might take a minute or so for containers to finish starting (especially www containers)."
	echo -e "NOTE: You can run 'npm run docker_status' to monitor the status or 'npm run logs${2/_/-}-$1' to monitor the container status."
}

#####
# Roll back container on server to use previous image and then delete the image that was just current
#####
function docker_rollback()
{
	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	docker_safety_check "$1"
	display_step "${FUNCNAME[0]}"
	echo -e "Rolling back ${PK}$1 ${NC}server, ${BL}$REPO ${NC} service, to previous docker image."
	echo -e "This will take longer if there are many containers running for this app"

	# Get current and previous image hashes
	IMAGE_CURR=$(ssh $SERVER_NAME -p 1022 docker images | grep "widespread/$REPO" | head -n 1 | awk '{print $3}')
	IMAGE_PREV=$(ssh $SERVER_NAME -p 1022 docker images | grep" widespread/$REPO" | head -n 2 | tail -n 1 | awk '{print $3}')

	# Update service to use older image, then remove the once-was currently running image
	ssh $SERVER_NAME -p 1022 "docker service update --image widespread/$REPO:$IMAGE_PREV ${1}_$REPO$2 || msg-admin 'Error rolling back *${1}_$REPO$2*!'" \
	&& (ssh $SERVER_NAME -p 1022 "docker rmi $IMAGE_CURR || msg-admin \"Error removing old image *$IMG_CURR*.\"" \
		&& echo -e "${GN}SUCCESS: ${NC}Rolled back service ${CY}${1}_$REPO$2${NC} to previous image ${BOLD}$IMAGE_CURR${NC}. Use npm run logs${2/_/-}-$1 to watch logs." || echo -e "${RD}ERROR: ${NC}An issue occurred while trying to remove previous image ${CY}$IMAGE_CURR${NC}.") \
	|| echo -e "${RD}ERROR: ${NC}An issue occurred while trying to roll back ${BL}${SERVER}_$REPO$2${NC} service on the ${PK}$1 ${NC}server."
}

#####
# Get status output of service and overall docker stats
#####
function docker_status()
{
	display_step "${FUNCNAME[0]}"

	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	# Message
	echo '======================'
	echo -e "==== ${PK}$(echo $REPO$2 | tr /a-z/ /A-Z/) ${NC}CONTAINER(S)"
	echo '======================'
	echo '*Note - some containers running outside the swarm (like router) may have PORTS column empty.'

	# SSH and get running containers
	ssh $SERVER_NAME -p 1022 "docker ps | head -n 1; docker ps | grep widespread/$REPO"
	echo '======================'
	CONTAINERS=$(ssh $SERVER_NAME -p 1022 'docker stats --no-stream $(docker ps --format={{.Names}})')
	if [[ $CONTAINERS == "" ]]; then
		echo -e "${RD}No container $REPO found running!${NC}"
	else
		echo "$CONTAINERS"
	fi
}

#####
# Get status of the stack that's running
#####
function docker_status_containers()
{
	display_step "${FUNCNAME[0]}"

	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	# Message
	echo '======================'
	echo -e "==== ${PK}$(echo $1 | tr /a-z/ /A-Z/) ${NC}CONTAINERS"
	echo '======================'
	echo '*Note - any containers that are not currently running are not shown here'

	# SSH and get running containers
	ssh $SERVER_NAME -p 1022 "docker ps"
	echo '======================'
}

#####
# Get status of the stack that's running
#####
function docker_status_stack()
{
	display_step "${FUNCNAME[0]}"

	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	# Message
	echo '======================'
	echo -e "==== ${PK}$(echo $1 | tr /a-z/ /A-Z/) ${NC}STACK"
	echo '======================'
	echo '*Note - containers like `router` which are not part of the stack are not shown here'

	# SSH and get running containers
	ssh $SERVER_NAME -p 1022 "docker stack services $1"
	echo '======================'
}

#####
# Get aggregated container logs
#####
function docker_logs()
{
	display_step "${FUNCNAME[0]}";

	if [[ $1 == "master" ]]; then
		SERVER_NAME="widespread1@$1.widespread.com"
	else
		SERVER_NAME="root@$1.widespread.com"
	fi

	# Message
	echo -e "Streaming '${1}_$REPO' logs below...."
	echo -e "Use ctrl + c to stop or ctrl + p + q to detach shell and leave container running."
	echo -e "${CY}=================================================================================${NC}"

	# Repo running as a service?
	if [[ $(ssh $SERVER_NAME -p 1022 "docker service ls | grep -q '${1}_$REPO$3' >/dev/null 2>&1"; echo $?) -eq 0 ]]; then
		echo "Trying to stream service logs."
		# YES, Stream from logger file
		ssh $SERVER_NAME -p 1022 "docker service logs -f -t --tail 200 '${1}_$REPO'"
	else
		echo "Trying to stream container logs."
		# NO, Stream from `docker logs`
		ssh $SERVER_NAME -p 1022 "docker logs -f -t --tail 200 $REPO$3"
	fi
}

############
## RUN
############
# Be sure the passed parameter is a function in this script
if [ -n "$(type -t $1)" ] && [ "$(type -t $1)" = function ]; then
	# Run the function
	eval "$1 '$2' '$3' '$4' '$5'"
fi
