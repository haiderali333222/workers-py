#!/bin/bash
#
# Helper that can be used by npm commands to return helpful things like current repo, branch, or commit
#

# Be sure at least 1 argument supplied
if [ $# -lt 1 ]; then
	echo "Usage: $0 (repo|branch|commit|ports)"
	exit 1
fi

# Switch
case "$1" in
	'repo')		echo 'amplify-pricing'
				;;

	'branch')	echo $(git branch | grep \\* | awk '{print $2}')
				;;

	'commit')	echo $(git rev-parse HEAD | cut -c 1-7)
				;;

	'ports')	# Determine location of dockerfile
				if [[ -f ./Dockerfile ]]; then
					FILE=./Dockerfile
				elif [[ -f ./docker/Dockerfile ]]; then
					FILE=./docker/Dockerfile
				else
					echo "Couldn't locate a Dockerfile to determine port!"; exit 1
				fi

				# Pull all ports from docker file and assemble port flags
				echo $(grep '^EXPOSE' $FILE | awk '{out=""; for(i=2;i<=NF;i++){out=out"-p "$i":"$i" "}; print out}') || (echo "Error extracting ports from Dockerfile. Be sure Dockerfile uses syntax 'EXPOSE port1 port2 ...'"; exit 1)
				;;

	*)			echo "Invalid option."
				echo "Usage: $0 (repo|branch|commit|port)"
				;;
esac