#!/bin/sh

#Install Docker

doas apk add docker
doas rc-update add docker default
doas service docker start
doas addgroup ${USER} docker

# Docker rootless
doas apk add docker-rootless-extras
doas echo 'rc_cgroup_mode="unified"' >> /etc/rc.conf
doas rc-update add cgroups
doas service cgroups start

# Install Docker Compose
apk add docker-cli-compose
