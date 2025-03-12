#!/bin/sh

printf "Converting & Deleting Original Files... "

for f in *.mkv; do ffmpeg -loglevel quiet -i "${f}" -c:v libvpx-vp9 -c:a libopus "${f%%.*}.webm"; rm "${f}"; done
for f in *.mp4; do ffmpeg -loglevel quiet -i "${f}" -c:v libvpx-vp9 -c:a libopus "${f%%.*}.webm"; rm "${f}"; done
for f in *.avi; do ffmpeg -loglevel quiet -i "${f}" -c:v libvpx-vp9 -c:a libopus "${f%%.*}.webm"; rm "${f}"; done
for f in *.mov; do ffmpeg -loglevel quiet -i "${f}" -c:v libvpx-vp9 -c:a libopus "${f%%.*}.webm"; rm "${f}"; done

printf "Completed... "
