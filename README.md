# StreamBot
Project for Hack@WPI 2020

## Setup
1. Install [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html#installing) using the command appropriate for your OS.

2. Install the following dependencies using this command.
```
pip3 install -r requirements.txt
```
3. Install ffmpeg through the following command (if on Ubuntu/Debian).
```
sudo apt install ffmpeg
```

## Running
First, get your discord bot's private key and save it into a file called 'config.txt' in the /streambot directory along with the filepath to store downloads.  

To start testing run
```
python3 streambot/streambot.py
```
Or
```
cd streambot && python3 streambot.py
``` 
