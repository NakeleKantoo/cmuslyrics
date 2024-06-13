#!/usr/bin/env python
import os
import subprocess
current = subprocess.check_output(["cmus-remote","-Q"]).split(b"\n")
currentfile = b""
user = os.environ['HOME']
for w in current:
    if w.startswith(b"file"):
        currentfile = w.decode()[5:]
def render():
    text = subprocess.check_output(["cmus-remote","-Q"])
    os.system("clear")
    newText = text.split(b"\n")
    file = b""
    title = b""
    artist = b""
    album = b""
    position = 0
    for w in newText:
        if w.startswith(b"file"):
            file = w.decode()[5:]
        elif w.startswith(b"tag title"):
            title = w.decode()[10:]
        elif w.startswith(b"tag artist"):
            artist = w.decode()[11:]
        elif w.startswith(b"tag album"):
            album = w.decode()[10:]
        elif w.startswith(b"position"):
            position = int(w.decode()[9:])
    os.system("ffmpeg -y -i \""+file+"\" -an -vcodec copy "+user+"/cache.png -loglevel quiet")
    titlebar = artist+" - "+album+" - "+title
    twidth = int(subprocess.check_output(["tput","cols"]).decode())
    print(center_string(titlebar,twidth))
    width = twidth//2
    offset = int((width*1.4)-((width*1.4)//2))
    os.system("viu -w "+str(width)+" -x "+str(offset)+" -y 1 "+user+"/cache.png")
    lyrics = subprocess.check_output(["clyrics",artist,title]).decode().split("\n")
    for w in lyrics:
        print(center_string(w,twidth))
    os.system("tput home")

def getTime(pos):
    minutes = 0
    seconds = 0
    while pos>=60:
        minutes+=1
        pos-=60
    seconds = pos
    if seconds<10:
        seconds = "0"+str(seconds)
    if minutes<10:
        minutes = "0"+str(minutes)
    return minutes+":"+seconds

def get_display_width(s):
    """Calculate the display width of a string considering wide characters."""
    width = 0
    for char in s:
        # Wide characters (East Asian) have a width of 2
        if ord(char) > 255:
            width += 2
        else:
            width += 1
    return width

def center_string(s, total_width):
    """Center a string for display considering wide characters."""
    string_width = get_display_width(s)
    if string_width >= total_width:
        return s

    # Calculate padding on both sides
    padding = (total_width - string_width) // 2
    # Create padding string
    padding_str = ' ' * padding
    return padding_str + s + padding_str

while True:
    os.system("sleep 1")
    new = subprocess.check_output(["cmus-remote","-Q"]).split(b"\n")
    newfile = b""
    for w in new:
        if w.startswith(b"file"):
            newfile = w.decode()[5:]
    if newfile != currentfile:
        current = new
        currentfile = newfile
        render()

