#!/usr/bin/env bash

HOSTNAME='core'
HOST_TYPE='edge'

if [ "$HOSTNAME" != "localhost" ]
then  
	HOST_TYPE='core'
fi

export LOCUST_PORT=8089
export LOCUST_DURATION=360
export LOCUST_USERS=5
export LOCUST_USER_START_INDEX=1
export LOCUST_WAIT_MIN=1000
export LOCUST_WAIT_MAX=1000
export LOCUST_HATCH_RATE=1

export KOALA_ENABLED=1 #set manually, comment the line below!
# export KOALA_ENABLED=$(docker ps | grep -c "koala_1") #check if koala container is running

export PREDEF_PROJECTS='asdf'
export USER_PROJECTS='{"user1": ["project1", "project2"], "user2": ["project1", "project2"], "user3": ["project3"]}'
export PAGE_TASKS='{ "move_and_write": 100, "chat": 20}'
# export PAGE_TASKS='{ "move_and_write": 100, "spell_check": 90, "chat": 20}'
#export PAGE_TASKS='{ "move_and_write": 1, "compile": 5, "show_history": 4}'
export PROJECT_OVERVIEW_TASKS='{"project.Page": 100}'
export LOCUST_LOAD_TYPE=constant

export LOCUST_MEASUREMENT_NAME="${HOST_TYPE}.${LOCUST_DURATION}secs.${LOCUST_USERS}users.${KOALA_ENABLED}koala"
export LOCUST_MEASUREMENT_DESCRIPTION="constant test"

echo "#####EXPERIMENT START########"

# for i in $(seq 1 1); do
#     locust -H http://${HOSTNAME}:8080 -P ${LOCUST_PORT}
# done


# paplay /usr/share/sounds/ubuntu/notifications/Positive.ogg


#
##MOVING PROJECT EXPERIMENT#
#export LOCUST_USERS=1
#EDGE=edge1
#EDGES=(edge1 edge1 edge3 edge3 edge4 edge4)
#
#j=1
#for i in ${EDGES[@]}; do
#	if (($j==3)) ; then
#		j=1
#	fi
#	echo "### ${EDGE} and ${i}, part ${j} ###"
#	LOCUST_MEASUREMENT_NAME="${EDGE}.${i}.u1.${j}"
#    locust -H http://${EDGE}:8080 -P ${LOCUST_PORT}&
#
#	let 'LOCUST_PORT++'
#	let 'LOCUST_USER_START_INDEX++'
#	LOCUST_MEASUREMENT_NAME="${EDGE}.${i}.u2.${j}"
#	locust -H http://${i}:8080 -P ${LOCUST_PORT}
#	LOCUST_USER_START_INDEX=1
#	LOCUST_PORT=8089
#	sleep 2
#	let 'j++'
#done
#echo "### DONE ###"


##PROJECT DISTRIBUTION EXPERIMENT#
LOCUST_DURATION=1200
export LOCUST_WAIT_MIN=3000
export LOCUST_WAIT_MAX=3000
PAGE_TASKS='{ "move_and_write": 50, "chat": 30, "stop": 5}'
LOCUST_USER_START_INDEX=1
EDGES=(edge1 edge3 edge4)
USER_NR=(4 3 3)
UPROJECTS=(
        '{"locust1": ["project1", "project3", "project4"], "locust2": ["project2"], "locust3": ["project3"], "locust4": ["project4", "project7"]}'
        '{"locust5": ["project1", "project5", "project8", "project9"], "locust6": ["project1", "project5", "project6"], "locust7": ["project7"]}'
        '{"locust8": ["project8", "project9", "project10"], "locust9": ["project8", "project9"], "locust10": ["project10"]}')


for (( i=1; i<${#EDGES[@]}+1; i++ ));
do
	echo "### starting ${EDGES[$i-1]} ###"
	LOCUST_USERS=${USER_NR[$i-1]}
	USER_PROJECTS=${UPROJECTS[$i-1]}
	locust -H http://${EDGES[$i-1]}:8080 -P ${LOCUST_PORT}&
    # echo $i " " ${EDGES[$i-1]} " " $LOCUST_USER_START_INDEX " " $LOCUST_USERS  " " $USER_PROJECTS
	
    LOCUST_USER_START_INDEX=$((LOCUST_USER_START_INDEX + USER_NR[$i-1]))
    let 'LOCUST_PORT++'
    sleep 5
done
echo "### DONE ###"