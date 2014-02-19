adb $1 shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > $2

# Use via: ./screencap.sh [-d|-e] file.png
