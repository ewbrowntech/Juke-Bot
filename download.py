from pytube import YouTube
import re

async def download_command(message):
    # Detect whether a YouTube URL is present within the command
    match = re.search(r'https://www.youtube.com/\S+|https://youtu.be/\S+', message.content)
    if match:
        ytLink = match.group(0)
        print("Found a YouTube link: " + ytLink)
        await message.channel.send('Downloading YouTube video...\n' + ytLink)
    else:
        print("No YouTube URL detected.")
        await message.channel.send('No YouTube URL detected.')


def download_video(url):
    yt = YouTube(url)
    return yt.title