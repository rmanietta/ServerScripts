#!/bin/sh

## Script can install incus or docker and docker compose as well as setup docker in a rootless mode. Using prompts to complete for alpine linux server.

## Update and Upgrade
doas apk update
doas apk upgrade

#Install Docker
printf 'Install Docker (y/n)? '
read answer1

if [ "$answer1" != "${answer1#[Yy]}" ]; then
doas apk add docker
doas rc-update add docker default
doas service docker start
doas addgroup ${USER} docker
else 
printf 'Setup docker rootless mode (y/n)? '
read answer2

if ["$answer2" != "${answer2#[Yy]}" ]; then
# Docker rootless
doas apk add docker-rootless-extras
doas echo 'rc_cgroup_mode="unified"' >> /etc/rc.conf
doas rc-update add cgroups
doas service cgroups start
else 
printf 'Install Docker Compose (y/n)? '
read answer3
if ["$answer3" != "${answer3#[Yy]}" ]; then
# Install Docker Compose
doas apk add docker-cli-compose
printf 'Install Incus (y/n)? '
read answer4
if ["$answer4" != "${answer4#[Yy]}" ]; then
# Install incus
doas apk add incus
else 
 echo 'Nothing Installed '
 exit
 
