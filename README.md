# Youbili

This is a python app which can download youtube videos and subtitles, then translate subtitles into chinese, then add subtitles to viedos.

Author: depplenny@gmail.com

## Install:

$ git clone https://github.com/depplenny/youbili

## Requirements:

1. This app uses microsoft azure translator, create a translator resource and get the authentication key at 
   https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-how-to-signup
   
   Your key would look like 43aab2df00084eda9cf6dfac4f6b0fec. Save it in a file named key.txt inside youbili folder.

2. Install FFmpeg

3. $ python3 -m pip install --upgrade pip

   $ python3 -m pip install translate youtube_dl

## Usage:

Download youtube videos and subtitles, then translate subtitles into chinese

$ python3 youbili.py ["youtube_video_url" or "youtube_list_url"] 

Add subtitles to viedos

$ python3 youbili.py

## FFmpeg:
Cut the video from HH:MM:SS.xxx=00:00:30.0 to HH:MM:SS.xxx=00:00:30.0
$ ffmpeg -ss 00:00:30.0 -i input.mp4 -c copy -t 00:00:30.0 output.mp4




