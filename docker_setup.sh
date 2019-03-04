#!/bin/bash

IMAGE=capstone-docker
CONTAINER=capstone-dev

build_image ()
{
    docker build --rm -t $IMAGE:latest .
}

launch_container ()
{
    docker run -itd --name $CONTAINER $IMAGE
}

interactive_shell ()
{
    docker exec -it $CONTAINER bash
}

usage ()
{
    echo "# script usage:"
    echo "# no args is equivalent to -bl"
    echo "#     -b build the the docker image"
    echo "#     -l launch container"
    echo "#     -i attach to shell of container"
    echo "#     -h print this help message"
    
}

if [[ $# -eq 0 ]]; then
    build_image
    launch_container
fi

while getopts ':bhlih' OPT; do
    case "$OPT" in 
        b)
            build_image
            ;;
       
        l)
            launch_container
            ;;
        i)
            interactive_shell
            ;;
        h)
            usage
            ;;
        ?)
            usage
            ;;
    esac
done
