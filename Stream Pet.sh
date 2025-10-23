#!/bin/sh
printf '\033c\033]0;%s\a' Stream Pet
base_path="$(dirname "$(realpath "$0")")"
"$base_path/Stream Pet.x86_64" "$@"
