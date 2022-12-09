from pytube import YouTube
import re

async def download_command(message):
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
    download_video(url)

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
    url = None
    match = re.search(r'https://www.youtube.com/\S+|https://youtu.be/\S+', messageContents)
    if match:
        url = match.group(0)
        print("Found a YouTube link: " + url)
    return url

# Determine if the specified YouTube URL exists and points to a video
def isVideo():
    pass

# Get title of YouTube video at specified URL
def get_title(url):
    return YouTube(url).title

def download_video(url):
    yt = YouTube(url)
    # for stream in yt.streams:
    #     print(stream)
    pass