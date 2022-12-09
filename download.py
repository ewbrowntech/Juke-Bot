from pytube import YouTube
import re

async def download_command(message):
    match = re.search(r'https://www.youtube.com/\S+|https://youtu.be/\S+', message.content)
    if match:
        # Extract the YouTube link from the match
        ytLink = match.group(0)

        # Handle the YouTube link as needed
        print("Found a YouTube link: " + ytLink)
    await message.channel.send('Downloading YouTube video...\n' + ytLink)


def download_video(url):
    yt = YouTube(url)
    return yt.title