from pytube import YouTube
import ffmpeg
import re
import os

'''
download.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 09 DEC 22

Get the URL of a YouTube video from a message and download the associated video
'''

async def process_download_command(message):
    filetype = get_filetype(message.content)
    if filetype == None:
        await message.channel.send('No filetype specified.')
        return

    url = get_url(message.content)
    if url == None:
        await message.channel.send('No YouTube URL detected.')
        return

    title = get_title(url)

    await message.channel.send('Downloading ' + "**" + title + "** as " + filetype + '...')
    manage_download_process(url, filetype)

# Get desired filetype from message
def get_filetype(messageContents):
    if " -mp3 " in messageContents:
        filetype = "mp3"
    elif " -mp4 " in messageContents:
        filetype = "mp4"
    else:
        filetype = None
    return filetype

# Find a* YouTube URL within message
def get_url(messageContents):
    match = re.search(r'https://www.youtube.com/\S+|https://youtu.be/\S+', messageContents)
    if match:
        url = match.group(0)
        print("Found a YouTube link: " + url)
    else: url = None
    return url


# Determine if the specified YouTube URL exists and points to a video
def isVideo():
    pass

# Get title of YouTube video at specified URL
def get_title(url):
    return YouTube(url).title

def manage_download_process(url, filetype):
    yt = YouTube(url)
    streams = yt.streams
    if filetype == "mp3":
        download_audio(streams)
    elif filetype == "mp4":
        audioPath = download_audio(streams)
        videoPath = download_video(streams)
        print(audioPath)
        print(videoPath)
        stitch_video(audioPath, videoPath)

# Download audio track
def download_audio(streams):
    audioStreams = streams.filter(only_audio=True)
    preferredStream = audioStreams.order_by("abr").last() # Get audio stream with the highest bit-rate
    if preferredStream.mime_type == "audio/webm":
        perform_download_operation(preferredStream, "audio.webm")
        return os.getcwd() + "\download_folder\\audio.webm"
    elif preferredStream.mime_type == "audio/mp4":
        perform_download_operation(preferredStream, "audio.mp4")
        return os.getcwd() + "\download_folder\\audio.mp4"

# Download video track
def download_video(streams):
    videoStreams = streams.filter(only_video=True)
    preferredStream = videoStreams.order_by("resolution").last()  # Get video stream with the highest resolution
    perform_download_operation(preferredStream, "video.mp4")
    return os.getcwd() + "\download_folder\\video.mp4"

def perform_download_operation(stream, filename):
    print("Downloading Stream: " + str(stream))
    folderPath = os.getcwd() + "\download_folder\\"
    print(folderPath)
    stream.download(folderPath, filename=filename)
    print("Download complete.")

def stitch_video(audioPath, videoPath): # Stitch together audio and video streams
    inputAudio = ffmpeg.input(audioPath)
    inputVideo = ffmpeg.input(videoPath)
    outputPath = os.getcwd() + "\download_folder\stiched.mp4"
    print(outputPath)
    ffmpeg.output(inputVideo, inputAudio, outputPath).run()