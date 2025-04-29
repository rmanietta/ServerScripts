#!/bin/sh

printf "Zimit"
printf "URL to Archive: " >&2
read -r URL
printf "Archive File Name: " >&2
read -r file

docker run -rm -v ~/www/zim:/output ghcr.io/openzim/zimit zimit --url $URL --name $file
