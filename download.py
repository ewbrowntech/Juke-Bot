from pytube import YouTube
import ffmpeg
import discord
import re
import os

'''
download.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 09 DEC 22

Get the URL of a YouTube video from a message and download the associated video
'''

downloadsPath = os.path.join(os.getcwd(), "download_folder")

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
    filepath = await manage_download_process(url, filetype, title, message.channel)
    await upload_file(message.channel, filepath)

# Register the "upload_size" command
def determine_upload_limit(server):
    uploadLimit = server.filesize_limit / 1_048_576  # Return the maximum file upload size in megabytes
    return uploadLimit

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

async def manage_download_process(url, filetype, title, channel):
    global downloadsPath
    yt = YouTube(url)
    streams = yt.streams
    if filetype == "mp3":
        filepath = download_audio(streams, title)
        return filepath
    elif filetype == "mp4":
        await channel.send("This will take a bit...")
        delete_existing_copy(title + ".mp4")
        audioPath = download_audio(streams, title)
        videoPath = download_video(streams)
        filepath = stitch_video(audioPath, videoPath, title)
        return filepath

# Get preferred audio stream and initiate download
def download_audio(streams, title):
    audioStreams = streams.filter(only_audio=True)
    preferredStream = audioStreams.order_by("abr").last() # Get audio stream with the highest bit-rate
    if preferredStream.mime_type == "audio/webm":
        filename = title + ".webm"
        perform_download_operation(preferredStream, filename)
        filepath = os.path.join(os.getcwd() + "\download_folder", filename)
        return filepath
    elif preferredStream.mime_type == "audio/mp4":
        filename = title + ".mp4"
        perform_download_operation(preferredStream, filename)
        filepath = os.path.join(os.getcwd() + "\download_folder", filename)
        return filepath

# Get preferred video stream and initiate download
def download_video(streams):
    videoStreams = streams.filter(only_video=True)
    preferredStream = videoStreams.order_by("resolution").last()  # Get video stream with the highest resolution
    filename = "video.mp4"
    perform_download_operation(preferredStream, filename)
    filepath = os.path.join(os.getcwd() + "\download_folder", filename)
    return filepath

# Perform download of video from YouTube
def perform_download_operation(stream, filename):
    print("Downloading Stream: " + str(stream))
    folderPath = os.getcwd() + "\download_folder\\"
    stream.download(folderPath, filename=filename)
    print("Download complete.")

# Stitch audio and video tracks together
def stitch_video(audioPath, videoPath, title): # Stitch together audio and video streams
    inputAudio = ffmpeg.input(audioPath)
    inputVideo = ffmpeg.input(videoPath)
    outputFilename = title + ".mp4"
    outputPath = os.path.join(os.getcwd() + "\download_folder", outputFilename)
    print("Stitching video...")
    ffmpeg.output(inputVideo, inputAudio, outputPath).run()
    print("Stitching complete.")
    return outputPath

# If a file with a given name exists in the download folder, delete it
def delete_existing_copy(filename):
    global downloadsPath
    hypotheticalFilepath = os.path.join(downloadsPath, filename)
    if os.path.exists(hypotheticalFilepath):
        os.remove(hypotheticalFilepath)

# If file is smaller than the upload limit of the server, send it in a message; otherwise, upload it to the cloud
async def upload_file(channel, filepath):
    server = channel.guild
    uploadLimit = determine_upload_limit(server)
    filesize = os.stat(filepath).st_size / 1_048_576  # Get size of output file in megabytes
    if not filesize > uploadLimit:
        await channel.send("Here you go!", file=discord.File(filepath))
    else:
        await channel.send('File is too big!')