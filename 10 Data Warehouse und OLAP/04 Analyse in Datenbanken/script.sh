#!/usr/bin/env bash

# Software:
# - yt-dlp
# - ffmpeg
# - tesseract-ocr

REQUEST=$(date +'%Y-%m-%d_%H-%M-%S')

# Text ist im Kasten mit folgenden Koordinaten
BOX_TL_X="466"
BOX_TL_Y="410"
BOX_SIZE_X="310"
BOX_SIZE_Y="140"

# Abrufen des Twitch Streams
# Bild zuschneiden, Threshold anwenden
# Texterkennung
yt-dlp "https://www.twitch.tv/wienersportstaetten" -f bestvideo/best -o -  |                                                                                                              \
ffmpeg -i - -f lavfi -i color=gray:s=${BOX_SIZE_X}x${BOX_SIZE_Y}:r=1 -f lavfi -i color=black:s=${BOX_SIZE_X}x${BOX_SIZE_Y}:r=1 -f lavfi -i color=white:s=${BOX_SIZE_X}x${BOX_SIZE_Y}:r=1  \
       -filter_complex "[0:v]crop=${BOX_SIZE_X}:${BOX_SIZE_Y}:${BOX_TL_X}:${BOX_TL_Y}[c];[c]negate[n],[n][1:v][2:v][3:v]threshold[f]"                                                     \
       -map "[f]" -y -frames:v 1 -y "$REQUEST.png"
COUNTER=$(tesseract -c tessedit_char_whitelist=0123456789 "$REQUEST.png" -)

# gültige Werte abspeichern
# eigentlich immer, sofern der Stream live ist
if [[ "$COUNTER" =~ ^[0-9]+$ ]]; then
    echo "$REQUEST,$COUNTER" >> "stadthallenbad_wien.csv"
else
    echo "COUNTER ist keine ganze Zahl."
fi
