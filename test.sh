#!/bin/bash
IFS=$'\n'
commits=($(git log -n 2 --pretty=%s))
echo "${commits[0]}" 
echo "${commits[1]}"

