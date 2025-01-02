import requests
import time
import otavreq
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import datetime

# Open and read info from config file so you can edit that instead of re-coding, get IP, PORT, and WINDOW TITLE

endpoint = "http://172.17.251.100:8081/"

title = "ULTRA"
formatted_time = ""
playspot = 1
elapsed = 0
nextlive = 0

# Main Refresh Loop, update root.after value to increase or decrease ticks
def update_list():
    global playspot
    update_playing()
    if playspot >= 4:
        maincanvas.yview_moveto(playspot / 350)
    else:
        maincanvas.yview_moveto(0)
    root.after(1000, update_list)


# Check if list is playing, and update screen accordingly; called by update_list() on every cycle
def update_playing():
    # Formatted_time is global as it is used in multiple functions
    global formatted_time
    global elapsed
    # API call to get info on currently playing clip
    updatetime = otavreq.otavplaystatus(endpoint)
    try:
        elapsed = int(updatetime[2])
    except:
        #print("CRAP")
        elapsed = 0
    # Updates current clip info, and prevents breaking if playback is stopped
    if updatetime[0] != "STOPPED":
        current_clip_status["text"] = updatetime[0]
        formatted_time = "0" + str(datetime.timedelta(seconds=int(updatetime[1])))
        current_duration_clock["text"] = formatted_time
        playlistitems()
    else:
        current_clip_status["text"] = updatetime[0]
        current_duration_clock["text"] = ""
        y = 299
        while y >= 0:
            name_list[y]["text"] = ""
            name_list[y]["bg"] = "#656565"
            index_list[y]["text"] = ""
            index_list[y]["bg"] = "#656565"
            duration_list[y]["text"] = ""
            duration_list[y]["bg"] = "#656565"
            frame_list[y]["bg"] = "#656565"
            frame_list[y]["relief"] = "flat"
            live_list[y]["text"] = ""
            live_list[y]["bg"] = "#656565"
            disabled_list[y]["bg"] = "#656565"
            disabled_list[y]["relief"] = "flat"
            disabled_list[y]["text"] = ""
            live_list[y]["relief"] = "flat"
            y -= 1
        next_live_clock["text"] = "NONE"

# Function to update all info on GUI
def playlistitems():
    global formatted_time
    global playspot
    global nextlive
    global elapsed
    playlist = otavreq.otavgetplaylist(endpoint)
    clipindex = 0
    played = 0
    lives = 0
    for x in playlist[0]:
        name_list[clipindex]["text"] = str(playlist[2][clipindex]) #updates clip titles in playlist
        if "WX" in playlist[2][clipindex] and playlist[1][clipindex] != 3:
            playlist[1][clipindex] = 4
            if int(playlist[9][clipindex]) > int(elapsed) and lives <1:
                nextlive = int(playlist[9][clipindex]) - int(elapsed)
                lives+=1




        if playlist[5][clipindex] == playlist[6]:
            live_list[clipindex]["bg"] = "green"
            frame_list[clipindex]["bg"] = "green"
            name_list[clipindex]["bg"] = "green"
            name_list[clipindex]["fg"] = "#0DFF00"
            index_list[clipindex]["bg"] = "green"
            index_list[clipindex]["fg"] = "#0DFF00"
            duration_list[clipindex]["bg"] = "green"
            duration_list[clipindex]["fg"] = "#0DFF00"
            duration_list[clipindex]["text"] = formatted_time
            frame_list[clipindex]["relief"] = "sunken"
            disabled_list[clipindex]["bg"] = "green"
            disabled_list[clipindex]["relief"] = "flat"
            disabled_list[clipindex]["text"] = ""
            played = clipindex - 1
            playspot = played


        elif playlist[1][clipindex] == 3:
            live_list[clipindex]["bg"] = "purple"
            frame_list[clipindex]["bg"] = "purple"
            name_list[clipindex]["bg"] = "purple"
            name_list[clipindex]["fg"] = "white"
            index_list[clipindex]["bg"] = "purple"
            duration_list[clipindex]["bg"] = "purple"
            duration_list[clipindex]["text"] = ""
            frame_list[clipindex]["relief"] = "sunken"
            disabled_list[clipindex]["bg"] = "purple"
            disabled_list[clipindex]["relief"] = "flat"
            disabled_list[clipindex]["text"] = ""
        else:
            live_list[clipindex]["bg"] = "#adafae"
            frame_list[clipindex]["bg"] = "#adafae"
            name_list[clipindex]["bg"] = "#adafae"
            name_list[clipindex]["fg"] = "black"
            index_list[clipindex]["bg"] = "#adafae"
            index_list[clipindex]["fg"] = "black"
            duration_list[clipindex]["bg"] = "#adafae"
            duration_list[clipindex]["fg"] = "black"
            duration_list[clipindex]["text"] = str(playlist[3][clipindex])
            frame_list[clipindex]["relief"] = "sunken"
            disabled_list[clipindex]["bg"] = "#adafae"
            disabled_list[clipindex]["relief"] = "flat"
            disabled_list[clipindex]["text"] = ""

        if playlist[1][clipindex] == 4:
            live_list[clipindex]["text"] = "LIVE"
            live_list[clipindex]["relief"] = "ridge"
            live_list[clipindex]["bg"] = "white"
        else:
            live_list[clipindex]["text"] = ""
            live_list[clipindex]["relief"] = "flat"

        if playlist[7][clipindex] == 'disabled':
            frame_list[clipindex]["bg"] = 'red'
            live_list[clipindex]["bg"] = "red"
            name_list[clipindex]["bg"] = "red"
            name_list[clipindex]["fg"] = "pink"
            index_list[clipindex]["bg"] = "red"
            index_list[clipindex]["fg"] = "pink"
            duration_list[clipindex]["bg"] = "red"
            duration_list[clipindex]["fg"] = "pink"
            disabled_list[clipindex]["bg"] = "pink"
            disabled_list[clipindex]["relief"] = "sunken"
            disabled_list[clipindex]["text"] = "DISABLED"



        index_list[clipindex]["text"] = str(playlist[4][clipindex])

        clipindex+=1

    #Make sure this is 1 less than number of elements or live countdown will break.
    y = 299
    if played >= 0:
        while played >= 0:
            if live_list[played]["bg"] != "purple":
                live_list[played]["bg"] = "#4C4C4C"
                frame_list[played]["bg"] = "#4C4C4C"
                name_list[played]["bg"] = "#4C4C4C"
                name_list[played]["fg"] = "black"
                index_list[played]["bg"] = "#4C4C4C"
                index_list[played]["fg"] = "black"
                index_list[played]["text"] = ""
                duration_list[played]["bg"] = "#4C4C4C"
                duration_list[played]["fg"] = "black"
                duration_list[played]["text"] = "PLAYED"
                frame_list[played]["relief"] = "sunken"
                disabled_list[played]["bg"] = "#4C4C4C"
                disabled_list[played]["relief"] = "flat"
                disabled_list[played]["text"] = ""
            played -= 1

    while y >= clipindex:
        name_list[y]["text"] = ""
        name_list[y]["bg"] = "#656565"
        index_list[y]["text"] = ""
        index_list[y]["bg"] = "#656565"
        duration_list[y]["text"] = ""
        duration_list[y]["bg"] = "#656565"
        frame_list[y]["bg"] = "#656565"
        frame_list[y]["relief"] = "flat"
        live_list[y]["text"] = ""
        live_list[y]["bg"] = "#656565"
        disabled_list[y]["bg"] = "#656565"
        y -= 1

        next_live_clock["text"] = str(datetime.timedelta(seconds=round(nextlive)))
"""
def testing123():
    for x in name_list:
        x["text"] = "crap"
    for y in index_list:
        y["text"] = "poop"
    for z in duration_list:
        z["text"] = "01:23:45"
"""

# Defines the GUI, and sets most attributes into lists for easy manipulation
root = tk.Tk()
# setting title
root.title(title)
# setting window size
width = 1080
height = 1920
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=True, height=True)
root.configure(bg='#656565')
root.state('zoomed')

mainframe = tk.Frame(root)
mainframe.place(x=0,y=10,height=1920, width=1060)

maincanvas = tk.Canvas(mainframe)
maincanvas["bg"] = "#656565"
maincanvas["highlightbackground"] = "#656565"
maincanvas['scrollregion']=(0,0,1080,13000)
maincanvas.place(x=0, y=0, height=1920, width=1080)
maincanvas.configure(scrollregion=maincanvas.bbox("all"))

maincanvas2 = tk.Canvas(mainframe)
maincanvas2["bg"] = "#656565"
maincanvas2["highlightbackground"] = "#656565"
maincanvas2.place(x=0, y=0, height=120, width=1080)


scrollframe = tk.Frame(maincanvas)
scrollframe['bg']='#656565'
scrollframe.place(x=0,y=0,height=1920, width=1080)

maincanvas.place(x=0, y=0, height=1920, width=1080)


scroller = tk.Scrollbar(root,orient='vertical', command=maincanvas.yview)
scroller.place(x=1060,y=202, width=20, height=1730)
maincanvas.configure(yscrollcommand=scroller.set)


current_clip_frame = tk.Label(root)
current_clip_frame["bg"] = "#bebebe"
ft = tkFont.Font(family='Times', size=16)
current_clip_frame["font"] = ft
current_clip_frame["fg"] = "#333333"
current_clip_frame["justify"] = "center"
current_clip_frame["text"] = ""
current_clip_frame["relief"] = "sunken"
current_clip_frame.place(x=10, y=10, width=520, height=100)

current_clip_header = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=22)
current_clip_header["font"] = ft
current_clip_header["fg"] = "#333333"
current_clip_header["bg"] = "#bebebe"
current_clip_header["justify"] = "left"
current_clip_header["anchor"] = "w"
current_clip_header["text"] = "Current Clip:"
current_clip_header.place(x=20, y=20, width=500, height=30)

current_clip_status = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=22)
current_clip_status["font"] = ft
current_clip_status["fg"] = "#333333"
current_clip_status["bg"] = "#bebebe"
current_clip_status["justify"] = "left"
current_clip_status["anchor"] = "w"
current_clip_status["text"] = "STOPPED"
current_clip_status.place(x=20, y=60, width=500, height=35)


current_duration_frame = tk.Label(root)
current_duration_frame["bg"] = "#bebebe"
ft = tkFont.Font(family='Times', size=16)
current_duration_frame["font"] = ft
current_duration_frame["fg"] = "#333333"
current_duration_frame["justify"] = "center"
current_duration_frame["text"] = ""
current_duration_frame["relief"] = "sunken"
current_duration_frame.place(x=550, y=10, width=520, height=100)

current_duration_header = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=22)
current_duration_header["font"] = ft
current_duration_header["fg"] = "#333333"
current_duration_header["bg"] = "#bebebe"
current_duration_header["justify"] = "left"
current_duration_header["anchor"] = "w"
current_duration_header["text"] = "Time Remaining:"
current_duration_header.place(x=560, y=20, width=500, height=35)

current_duration_clock = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=22)
current_duration_clock["font"] = ft
current_duration_clock["fg"] = "#333333"
current_duration_clock["bg"] = "#bebebe"
current_duration_clock["justify"] = "left"
current_duration_clock["anchor"] = "w"
current_duration_clock["text"] = "0000"
current_duration_clock.place(x=560, y=60, width=300, height=35)

next_live_frame = tk.Label(root)
next_live_frame["bg"] = "pink"
next_live_frame["relief"] = "sunken"
next_live_frame.place(x=10, y=120, width=1060, height=40)

next_live_label = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=22, weight="bold")
next_live_label["font"] = ft
next_live_label["bg"] = "pink"
next_live_label["fg"] = "red"
next_live_label["anchor"] = "w"
next_live_label["text"] = "NEXT LIVE HIT IN: "
next_live_label.place(x=20, y=125, width=500, height=33)

next_live_clock = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=22, weight="bold")
next_live_clock["font"] = ft
next_live_clock["bg"] = "pink"
next_live_clock["fg"] = "red"
next_live_clock["anchor"] = "e"
next_live_clock["text"] = "test"
next_live_clock.place(x=565, y=125, width=500, height=33)

header_bar_frame = tk.Label(root)
header_bar_frame["bg"] = "#adafae"
header_bar_frame["text"] = ""
header_bar_frame["relief"] = "sunken"
header_bar_frame.place(x=10, y=160, width=1060, height=40)

start_time_header = tk.Label(root)
ft = tkFont.Font(family='Proxima', size=16)
start_time_header["font"] = ft
start_time_header["fg"] = "#333333"
start_time_header["bg"] = "#adafae"
start_time_header["justify"] = "left"
start_time_header["anchor"] = "w"
start_time_header["text"] = "Start Time"
start_time_header.place(x=20, y=165, width=139, height=32)

title_header=tk.Label(root)
ft = tkFont.Font(family='Proxima',size=16)
title_header["font"] = ft
title_header["fg"] = "#333333"
title_header["bg"] = "#adafae"
title_header["justify"] = "left"
title_header["anchor"] = "w"
title_header["text"] = "Title"
title_header.place(x=250,y=165,width=70,height=32)

duration_header=tk.Label(root)
ft = tkFont.Font(family='Proxima',size=16)
duration_header["font"] = ft
duration_header["fg"] = "#333333"
duration_header["bg"] = "#adafae"
duration_header["justify"] = "right"
duration_header["anchor"] = "e"
duration_header["text"] = "Duration"
duration_header.place(x=930,y=165,width=100,height=32)

line_1_frame = tk.Label(scrollframe)
line_1_frame["bg"] = "#adafae"
line_1_frame["text"] = ""
line_1_frame["relief"] = "sunken"
line_1_frame.place(x=10, y=200, width=1060, height=40)

line_1_index = tk.Label(scrollframe)
line_1_index["bg"] = "#adafae"
line_1_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_1_index["font"] = ft
line_1_index["justify"] = "left"
line_1_index["anchor"] = "w"
line_1_index.place(x=20, y=205, width=150, height=33)

line_1_name = tk.Label(scrollframe)
line_1_name["bg"] = "#adafae"
line_1_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_1_name["font"] = ft
line_1_name["justify"] = "left"
line_1_name["anchor"] = "w"
line_1_name.place(x=250, y=205, width=500, height=33)

line_1_duration = tk.Label(scrollframe)
line_1_duration["bg"] = "#adafae"
line_1_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_1_duration["font"] = ft
line_1_duration["justify"] = "right"
line_1_duration["anchor"] = "e"
line_1_duration.place(x=910, y=205, width=150, height=33)

line_1_live = tk.Label(scrollframe)
line_1_live["bg"] = "#adafae"
line_1_live["fg"] = "red"
line_1_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_1_live["font"] = ftl
line_1_live["justify"] = "left"
line_1_live["anchor"] = "w"
line_1_live.place(x=800, y=205, width=70, height=33)

line_1_disabled = tk.Label(scrollframe)
line_1_disabled["bg"] = "#adafae"
line_1_disabled["fg"] = "red"
line_1_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_1_disabled["font"] = ftl
line_1_disabled["justify"] = "left"
line_1_disabled["anchor"] = "w"
line_1_disabled["relief"] = "flat"
line_1_disabled.place(x=650, y=205, width=150, height=33)

line_2_frame = tk.Label(scrollframe)
line_2_frame["bg"] = "#adafae"
line_2_frame["text"] = ""
line_2_frame["relief"] = "sunken"
line_2_frame.place(x=10, y=240, width=1060, height=40)

line_2_index = tk.Label(scrollframe)
line_2_index["bg"] = "#adafae"
line_2_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_2_index["font"] = ft
line_2_index["justify"] = "left"
line_2_index["anchor"] = "w"
line_2_index.place(x=20, y=245, width=150, height=33)

line_2_name = tk.Label(scrollframe)
line_2_name["bg"] = "#adafae"
line_2_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_2_name["font"] = ft
line_2_name["justify"] = "left"
line_2_name["anchor"] = "w"
line_2_name.place(x=250, y=245, width=500, height=33)

line_2_duration = tk.Label(scrollframe)
line_2_duration["bg"] = "#adafae"
line_2_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_2_duration["font"] = ft
line_2_duration["justify"] = "right"
line_2_duration["anchor"] = "e"
line_2_duration.place(x=910, y=245, width=150, height=33)

line_2_live = tk.Label(scrollframe)
line_2_live["bg"] = "#adafae"
line_2_live["fg"] = "red"
line_2_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_2_live["font"] = ftl
line_2_live["justify"] = "left"
line_2_live["anchor"] = "w"
line_2_live.place(x=800, y=245, width=70, height=33)

line_2_disabled = tk.Label(scrollframe)
line_2_disabled["bg"] = "#adafae"
line_2_disabled["fg"] = "red"
line_2_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_2_disabled["font"] = ftl
line_2_disabled["justify"] = "left"
line_2_disabled["anchor"] = "w"
line_2_disabled["relief"] = "flat"
line_2_disabled.place(x=650, y=245, width=150, height=33)

line_3_frame = tk.Label(scrollframe)
line_3_frame["bg"] = "#adafae"
line_3_frame["text"] = ""
line_3_frame["relief"] = "sunken"
line_3_frame.place(x=10, y=280, width=1060, height=40)

line_3_index = tk.Label(scrollframe)
line_3_index["bg"] = "#adafae"
line_3_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_3_index["font"] = ft
line_3_index["justify"] = "left"
line_3_index["anchor"] = "w"
line_3_index.place(x=20, y=285, width=150, height=33)

line_3_name = tk.Label(scrollframe)
line_3_name["bg"] = "#adafae"
line_3_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_3_name["font"] = ft
line_3_name["justify"] = "left"
line_3_name["anchor"] = "w"
line_3_name.place(x=250, y=285, width=500, height=33)

line_3_duration = tk.Label(scrollframe)
line_3_duration["bg"] = "#adafae"
line_3_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_3_duration["font"] = ft
line_3_duration["justify"] = "right"
line_3_duration["anchor"] = "e"
line_3_duration.place(x=910, y=285, width=150, height=33)

line_3_live = tk.Label(scrollframe)
line_3_live["bg"] = "#adafae"
line_3_live["fg"] = "red"
line_3_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_3_live["font"] = ftl
line_3_live["justify"] = "left"
line_3_live["anchor"] = "w"
line_3_live.place(x=800, y=285, width=70, height=33)

line_3_disabled = tk.Label(scrollframe)
line_3_disabled["bg"] = "#adafae"
line_3_disabled["fg"] = "red"
line_3_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_3_disabled["font"] = ftl
line_3_disabled["justify"] = "left"
line_3_disabled["anchor"] = "w"
line_3_disabled["relief"] = "flat"
line_3_disabled.place(x=650, y=285, width=150, height=33)

line_4_frame = tk.Label(scrollframe)
line_4_frame["bg"] = "#adafae"
line_4_frame["text"] = ""
line_4_frame["relief"] = "sunken"
line_4_frame.place(x=10, y=320, width=1060, height=40)

line_4_index = tk.Label(scrollframe)
line_4_index["bg"] = "#adafae"
line_4_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_4_index["font"] = ft
line_4_index["justify"] = "left"
line_4_index["anchor"] = "w"
line_4_index.place(x=20, y=325, width=150, height=33)

line_4_name = tk.Label(scrollframe)
line_4_name["bg"] = "#adafae"
line_4_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_4_name["font"] = ft
line_4_name["justify"] = "left"
line_4_name["anchor"] = "w"
line_4_name.place(x=250, y=325, width=500, height=33)

line_4_duration = tk.Label(scrollframe)
line_4_duration["bg"] = "#adafae"
line_4_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_4_duration["font"] = ft
line_4_duration["justify"] = "right"
line_4_duration["anchor"] = "e"
line_4_duration.place(x=910, y=325, width=150, height=33)

line_4_live = tk.Label(scrollframe)
line_4_live["bg"] = "#adafae"
line_4_live["fg"] = "red"
line_4_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_4_live["font"] = ftl
line_4_live["justify"] = "left"
line_4_live["anchor"] = "w"
line_4_live.place(x=800, y=325, width=70, height=33)

line_4_disabled = tk.Label(scrollframe)
line_4_disabled["bg"] = "#adafae"
line_4_disabled["fg"] = "red"
line_4_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_4_disabled["font"] = ftl
line_4_disabled["justify"] = "left"
line_4_disabled["anchor"] = "w"
line_4_disabled["relief"] = "flat"
line_4_disabled.place(x=650, y=325, width=150, height=33)

line_5_frame = tk.Label(scrollframe)
line_5_frame["bg"] = "#adafae"
line_5_frame["text"] = ""
line_5_frame["relief"] = "sunken"
line_5_frame.place(x=10, y=360, width=1060, height=40)

line_5_index = tk.Label(scrollframe)
line_5_index["bg"] = "#adafae"
line_5_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_5_index["font"] = ft
line_5_index["justify"] = "left"
line_5_index["anchor"] = "w"
line_5_index.place(x=20, y=365, width=150, height=33)

line_5_name = tk.Label(scrollframe)
line_5_name["bg"] = "#adafae"
line_5_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_5_name["font"] = ft
line_5_name["justify"] = "left"
line_5_name["anchor"] = "w"
line_5_name.place(x=250, y=365, width=500, height=33)

line_5_duration = tk.Label(scrollframe)
line_5_duration["bg"] = "#adafae"
line_5_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_5_duration["font"] = ft
line_5_duration["justify"] = "right"
line_5_duration["anchor"] = "e"
line_5_duration.place(x=910, y=365, width=150, height=33)

line_5_live = tk.Label(scrollframe)
line_5_live["bg"] = "#adafae"
line_5_live["fg"] = "red"
line_5_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_5_live["font"] = ftl
line_5_live["justify"] = "left"
line_5_live["anchor"] = "w"
line_5_live.place(x=800, y=365, width=70, height=33)

line_5_disabled = tk.Label(scrollframe)
line_5_disabled["bg"] = "#adafae"
line_5_disabled["fg"] = "red"
line_5_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_5_disabled["font"] = ftl
line_5_disabled["justify"] = "left"
line_5_disabled["anchor"] = "w"
line_5_disabled["relief"] = "flat"
line_5_disabled.place(x=650, y=365, width=150, height=33)

line_6_frame = tk.Label(scrollframe)
line_6_frame["bg"] = "#adafae"
line_6_frame["text"] = ""
line_6_frame["relief"] = "sunken"
line_6_frame.place(x=10, y=400, width=1060, height=40)

line_6_index = tk.Label(scrollframe)
line_6_index["bg"] = "#adafae"
line_6_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_6_index["font"] = ft
line_6_index["justify"] = "left"
line_6_index["anchor"] = "w"
line_6_index.place(x=20, y=405, width=150, height=33)

line_6_name = tk.Label(scrollframe)
line_6_name["bg"] = "#adafae"
line_6_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_6_name["font"] = ft
line_6_name["justify"] = "left"
line_6_name["anchor"] = "w"
line_6_name.place(x=250, y=405, width=500, height=33)

line_6_duration = tk.Label(scrollframe)
line_6_duration["bg"] = "#adafae"
line_6_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_6_duration["font"] = ft
line_6_duration["justify"] = "right"
line_6_duration["anchor"] = "e"
line_6_duration.place(x=910, y=405, width=150, height=33)

line_6_live = tk.Label(scrollframe)
line_6_live["bg"] = "#adafae"
line_6_live["fg"] = "red"
line_6_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_6_live["font"] = ftl
line_6_live["justify"] = "left"
line_6_live["anchor"] = "w"
line_6_live.place(x=800, y=405, width=70, height=33)

line_6_disabled = tk.Label(scrollframe)
line_6_disabled["bg"] = "#adafae"
line_6_disabled["fg"] = "red"
line_6_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_6_disabled["font"] = ftl
line_6_disabled["justify"] = "left"
line_6_disabled["anchor"] = "w"
line_6_disabled["relief"] = "flat"
line_6_disabled.place(x=650, y=405, width=150, height=33)

line_7_frame = tk.Label(scrollframe)
line_7_frame["bg"] = "#adafae"
line_7_frame["text"] = ""
line_7_frame["relief"] = "sunken"
line_7_frame.place(x=10, y=440, width=1060, height=40)

line_7_index = tk.Label(scrollframe)
line_7_index["bg"] = "#adafae"
line_7_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_7_index["font"] = ft
line_7_index["justify"] = "left"
line_7_index["anchor"] = "w"
line_7_index.place(x=20, y=445, width=150, height=33)

line_7_name = tk.Label(scrollframe)
line_7_name["bg"] = "#adafae"
line_7_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_7_name["font"] = ft
line_7_name["justify"] = "left"
line_7_name["anchor"] = "w"
line_7_name.place(x=250, y=445, width=500, height=33)

line_7_duration = tk.Label(scrollframe)
line_7_duration["bg"] = "#adafae"
line_7_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_7_duration["font"] = ft
line_7_duration["justify"] = "right"
line_7_duration["anchor"] = "e"
line_7_duration.place(x=910, y=445, width=150, height=33)

line_7_live = tk.Label(scrollframe)
line_7_live["bg"] = "#adafae"
line_7_live["fg"] = "red"
line_7_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_7_live["font"] = ftl
line_7_live["justify"] = "left"
line_7_live["anchor"] = "w"
line_7_live.place(x=800, y=445, width=70, height=33)

line_7_disabled = tk.Label(scrollframe)
line_7_disabled["bg"] = "#adafae"
line_7_disabled["fg"] = "red"
line_7_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_7_disabled["font"] = ftl
line_7_disabled["justify"] = "left"
line_7_disabled["anchor"] = "w"
line_7_disabled["relief"] = "flat"
line_7_disabled.place(x=650, y=445, width=150, height=33)

line_8_frame = tk.Label(scrollframe)
line_8_frame["bg"] = "#adafae"
line_8_frame["text"] = ""
line_8_frame["relief"] = "sunken"
line_8_frame.place(x=10, y=480, width=1060, height=40)

line_8_index = tk.Label(scrollframe)
line_8_index["bg"] = "#adafae"
line_8_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_8_index["font"] = ft
line_8_index["justify"] = "left"
line_8_index["anchor"] = "w"
line_8_index.place(x=20, y=485, width=150, height=33)

line_8_name = tk.Label(scrollframe)
line_8_name["bg"] = "#adafae"
line_8_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_8_name["font"] = ft
line_8_name["justify"] = "left"
line_8_name["anchor"] = "w"
line_8_name.place(x=250, y=485, width=500, height=33)

line_8_duration = tk.Label(scrollframe)
line_8_duration["bg"] = "#adafae"
line_8_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_8_duration["font"] = ft
line_8_duration["justify"] = "right"
line_8_duration["anchor"] = "e"
line_8_duration.place(x=910, y=485, width=150, height=33)

line_8_live = tk.Label(scrollframe)
line_8_live["bg"] = "#adafae"
line_8_live["fg"] = "red"
line_8_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_8_live["font"] = ftl
line_8_live["justify"] = "left"
line_8_live["anchor"] = "w"
line_8_live.place(x=800, y=485, width=70, height=33)

line_8_disabled = tk.Label(scrollframe)
line_8_disabled["bg"] = "#adafae"
line_8_disabled["fg"] = "red"
line_8_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_8_disabled["font"] = ftl
line_8_disabled["justify"] = "left"
line_8_disabled["anchor"] = "w"
line_8_disabled["relief"] = "flat"
line_8_disabled.place(x=650, y=485, width=150, height=33)

line_9_frame = tk.Label(scrollframe)
line_9_frame["bg"] = "#adafae"
line_9_frame["text"] = ""
line_9_frame["relief"] = "sunken"
line_9_frame.place(x=10, y=520, width=1060, height=40)

line_9_index = tk.Label(scrollframe)
line_9_index["bg"] = "#adafae"
line_9_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_9_index["font"] = ft
line_9_index["justify"] = "left"
line_9_index["anchor"] = "w"
line_9_index.place(x=20, y=525, width=480, height=33)

line_9_name = tk.Label(scrollframe)
line_9_name["bg"] = "#adafae"
line_9_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_9_name["font"] = ft
line_9_name["justify"] = "left"
line_9_name["anchor"] = "w"
line_9_name.place(x=250, y=525, width=500, height=33)

line_9_duration = tk.Label(scrollframe)
line_9_duration["bg"] = "#adafae"
line_9_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_9_duration["font"] = ft
line_9_duration["justify"] = "right"
line_9_duration["anchor"] = "e"
line_9_duration.place(x=910, y=525, width=150, height=33)

line_9_live = tk.Label(scrollframe)
line_9_live["bg"] = "#adafae"
line_9_live["fg"] = "red"
line_9_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_9_live["font"] = ftl
line_9_live["justify"] = "left"
line_9_live["anchor"] = "w"
line_9_live.place(x=800, y=525, width=70, height=33)

line_9_disabled = tk.Label(scrollframe)
line_9_disabled["bg"] = "#adafae"
line_9_disabled["fg"] = "red"
line_9_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_9_disabled["font"] = ftl
line_9_disabled["justify"] = "left"
line_9_disabled["anchor"] = "w"
line_9_disabled["relief"] = "flat"
line_9_disabled.place(x=650, y=525, width=150, height=33)

line_10_frame = tk.Label(scrollframe)
line_10_frame["bg"] = "#adafae"
line_10_frame["text"] = ""
line_10_frame["relief"] = "sunken"
line_10_frame.place(x=10, y=560, width=1060, height=40)

line_10_index = tk.Label(scrollframe)
line_10_index["bg"] = "#adafae"
line_10_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_10_index["font"] = ft
line_10_index["justify"] = "left"
line_10_index["anchor"] = "w"
line_10_index.place(x=20, y=565, width=150, height=33)

line_10_name = tk.Label(scrollframe)
line_10_name["bg"] = "#adafae"
line_10_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_10_name["font"] = ft
line_10_name["justify"] = "left"
line_10_name["anchor"] = "w"
line_10_name.place(x=250, y=565, width=500, height=33)

line_10_duration = tk.Label(scrollframe)
line_10_duration["bg"] = "#adafae"
line_10_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_10_duration["font"] = ft
line_10_duration["justify"] = "right"
line_10_duration["anchor"] = "e"
line_10_duration.place(x=910, y=565, width=150, height=33)

line_10_live = tk.Label(scrollframe)
line_10_live["bg"] = "#adafae"
line_10_live["fg"] = "red"
line_10_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_10_live["font"] = ftl
line_10_live["justify"] = "left"
line_10_live["anchor"] = "w"
line_10_live.place(x=800, y=565, width=70, height=33)

line_10_disabled = tk.Label(scrollframe)
line_10_disabled["bg"] = "#adafae"
line_10_disabled["fg"] = "red"
line_10_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_10_disabled["font"] = ftl
line_10_disabled["justify"] = "left"
line_10_disabled["anchor"] = "w"
line_10_disabled["relief"] = "flat"
line_10_disabled.place(x=650, y=565, width=150, height=33)

line_11_frame = tk.Label(scrollframe)
line_11_frame["bg"] = "#adafae"
line_11_frame["text"] = ""
line_11_frame["relief"] = "sunken"
line_11_frame.place(x=10, y=600, width=1060, height=40)

line_11_index = tk.Label(scrollframe)
line_11_index["bg"] = "#adafae"
line_11_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_11_index["font"] = ft
line_11_index["justify"] = "left"
line_11_index["anchor"] = "w"
line_11_index.place(x=20, y=605, width=150, height=33)

line_11_name = tk.Label(scrollframe)
line_11_name["bg"] = "#adafae"
line_11_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_11_name["font"] = ft
line_11_name["justify"] = "left"
line_11_name["anchor"] = "w"
line_11_name.place(x=250, y=605, width=500, height=33)

line_11_duration = tk.Label(scrollframe)
line_11_duration["bg"] = "#adafae"
line_11_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_11_duration["font"] = ft
line_11_duration["justify"] = "right"
line_11_duration["anchor"] = "e"
line_11_duration.place(x=910, y=605, width=150, height=33)

line_11_live = tk.Label(scrollframe)
line_11_live["bg"] = "#adafae"
line_11_live["fg"] = "red"
line_11_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_11_live["font"] = ftl
line_11_live["justify"] = "left"
line_11_live["anchor"] = "w"
line_11_live.place(x=800, y=605, width=70, height=33)

line_11_disabled = tk.Label(scrollframe)
line_11_disabled["bg"] = "#adafae"
line_11_disabled["fg"] = "red"
line_11_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_11_disabled["font"] = ftl
line_11_disabled["justify"] = "left"
line_11_disabled["anchor"] = "w"
line_11_disabled["relief"] = "flat"
line_11_disabled.place(x=650, y=605, width=150, height=33)

line_12_frame = tk.Label(scrollframe)
line_12_frame["bg"] = "#adafae"
line_12_frame["text"] = ""
line_12_frame["relief"] = "sunken"
line_12_frame.place(x=10, y=640, width=1060, height=40)

line_12_index = tk.Label(scrollframe)
line_12_index["bg"] = "#adafae"
line_12_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_12_index["font"] = ft
line_12_index["justify"] = "left"
line_12_index["anchor"] = "w"
line_12_index.place(x=20, y=645, width=150, height=33)

line_12_name = tk.Label(scrollframe)
line_12_name["bg"] = "#adafae"
line_12_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_12_name["font"] = ft
line_12_name["justify"] = "left"
line_12_name["anchor"] = "w"
line_12_name.place(x=250, y=645, width=500, height=33)

line_12_duration = tk.Label(scrollframe)
line_12_duration["bg"] = "#adafae"
line_12_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_12_duration["font"] = ft
line_12_duration["justify"] = "right"
line_12_duration["anchor"] = "e"
line_12_duration.place(x=910, y=645, width=150, height=33)

line_12_live = tk.Label(scrollframe)
line_12_live["bg"] = "#adafae"
line_12_live["fg"] = "red"
line_12_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_12_live["font"] = ftl
line_12_live["justify"] = "left"
line_12_live["anchor"] = "w"
line_12_live.place(x=800, y=645, width=70, height=33)

line_12_disabled = tk.Label(scrollframe)
line_12_disabled["bg"] = "#adafae"
line_12_disabled["fg"] = "red"
line_12_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_12_disabled["font"] = ftl
line_12_disabled["justify"] = "left"
line_12_disabled["anchor"] = "w"
line_12_disabled["relief"] = "flat"
line_12_disabled.place(x=650, y=645, width=150, height=33)

line_13_frame = tk.Label(scrollframe)
line_13_frame["bg"] = "#adafae"
line_13_frame["text"] = ""
line_13_frame["relief"] = "sunken"
line_13_frame.place(x=10, y=680, width=1060, height=40)

line_13_index = tk.Label(scrollframe)
line_13_index["bg"] = "#adafae"
line_13_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_13_index["font"] = ft
line_13_index["justify"] = "left"
line_13_index["anchor"] = "w"
line_13_index.place(x=20, y=685, width=150, height=33)

line_13_name = tk.Label(scrollframe)
line_13_name["bg"] = "#adafae"
line_13_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_13_name["font"] = ft
line_13_name["justify"] = "left"
line_13_name["anchor"] = "w"
line_13_name.place(x=250, y=685, width=500, height=33)

line_13_duration = tk.Label(scrollframe)
line_13_duration["bg"] = "#adafae"
line_13_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_13_duration["font"] = ft
line_13_duration["justify"] = "right"
line_13_duration["anchor"] = "e"
line_13_duration.place(x=910, y=685, width=150, height=33)

line_13_live = tk.Label(scrollframe)
line_13_live["bg"] = "#adafae"
line_13_live["fg"] = "red"
line_13_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_13_live["font"] = ftl
line_13_live["justify"] = "left"
line_13_live["anchor"] = "w"
line_13_live.place(x=800, y=685, width=70, height=33)

line_13_disabled = tk.Label(scrollframe)
line_13_disabled["bg"] = "#adafae"
line_13_disabled["fg"] = "red"
line_13_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_13_disabled["font"] = ftl
line_13_disabled["justify"] = "left"
line_13_disabled["anchor"] = "w"
line_13_disabled["relief"] = "flat"
line_13_disabled.place(x=650, y=685, width=150, height=33)

line_14_frame = tk.Label(scrollframe)
line_14_frame["bg"] = "#adafae"
line_14_frame["text"] = ""
line_14_frame["relief"] = "sunken"
line_14_frame.place(x=10, y=720, width=1060, height=40)

line_14_index = tk.Label(scrollframe)
line_14_index["bg"] = "#adafae"
line_14_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_14_index["font"] = ft
line_14_index["justify"] = "left"
line_14_index["anchor"] = "w"
line_14_index.place(x=20, y=725, width=150, height=33)

line_14_name = tk.Label(scrollframe)
line_14_name["bg"] = "#adafae"
line_14_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_14_name["font"] = ft
line_14_name["justify"] = "left"
line_14_name["anchor"] = "w"
line_14_name.place(x=250, y=725, width=500, height=33)

line_14_duration = tk.Label(scrollframe)
line_14_duration["bg"] = "#adafae"
line_14_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_14_duration["font"] = ft
line_14_duration["justify"] = "right"
line_14_duration["anchor"] = "e"
line_14_duration.place(x=910, y=725, width=150, height=33)

line_14_live = tk.Label(scrollframe)
line_14_live["bg"] = "#adafae"
line_14_live["fg"] = "red"
line_14_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_14_live["font"] = ftl
line_14_live["justify"] = "left"
line_14_live["anchor"] = "w"
line_14_live.place(x=800, y=725, width=70, height=33)

line_14_disabled = tk.Label(scrollframe)
line_14_disabled["bg"] = "#adafae"
line_14_disabled["fg"] = "red"
line_14_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_14_disabled["font"] = ftl
line_14_disabled["justify"] = "left"
line_14_disabled["anchor"] = "w"
line_14_disabled["relief"] = "flat"
line_14_disabled.place(x=650, y=725, width=150, height=33)

line_15_frame = tk.Label(scrollframe)
line_15_frame["bg"] = "#adafae"
line_15_frame["text"] = ""
line_15_frame["relief"] = "sunken"
line_15_frame.place(x=10, y=760, width=1060, height=40)

line_15_index = tk.Label(scrollframe)
line_15_index["bg"] = "#adafae"
line_15_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_15_index["font"] = ft
line_15_index["justify"] = "left"
line_15_index["anchor"] = "w"
line_15_index.place(x=20, y=765, width=150, height=33)

line_15_name = tk.Label(scrollframe)
line_15_name["bg"] = "#adafae"
line_15_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_15_name["font"] = ft
line_15_name["justify"] = "left"
line_15_name["anchor"] = "w"
line_15_name.place(x=250, y=765, width=500, height=33)

line_15_duration = tk.Label(scrollframe)
line_15_duration["bg"] = "#adafae"
line_15_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_15_duration["font"] = ft
line_15_duration["justify"] = "right"
line_15_duration["anchor"] = "e"
line_15_duration.place(x=910, y=765, width=150, height=33)

line_15_live = tk.Label(scrollframe)
line_15_live["bg"] = "#adafae"
line_15_live["fg"] = "red"
line_15_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_15_live["font"] = ftl
line_15_live["justify"] = "left"
line_15_live["anchor"] = "w"
line_15_live.place(x=800, y=765, width=70, height=33)

line_15_disabled = tk.Label(scrollframe)
line_15_disabled["bg"] = "#adafae"
line_15_disabled["fg"] = "red"
line_15_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_15_disabled["font"] = ftl
line_15_disabled["justify"] = "left"
line_15_disabled["anchor"] = "w"
line_15_disabled["relief"] = "flat"
line_15_disabled.place(x=650, y=765, width=150, height=33)

line_16_frame = tk.Label(scrollframe)
line_16_frame["bg"] = "#adafae"
line_16_frame["text"] = ""
line_16_frame["relief"] = "sunken"
line_16_frame.place(x=10, y=800, width=1060, height=40)

line_16_index = tk.Label(scrollframe)
line_16_index["bg"] = "#adafae"
line_16_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_16_index["font"] = ft
line_16_index["justify"] = "left"
line_16_index["anchor"] = "w"
line_16_index.place(x=20, y=805, width=150, height=33)

line_16_name = tk.Label(scrollframe)
line_16_name["bg"] = "#adafae"
line_16_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_16_name["font"] = ft
line_16_name["justify"] = "left"
line_16_name["anchor"] = "w"
line_16_name.place(x=250, y=805, width=500, height=33)

line_16_duration = tk.Label(scrollframe)
line_16_duration["bg"] = "#adafae"
line_16_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_16_duration["font"] = ft
line_16_duration["justify"] = "right"
line_16_duration["anchor"] = "e"
line_16_duration.place(x=910, y=805, width=150, height=33)

line_16_live = tk.Label(scrollframe)
line_16_live["bg"] = "#adafae"
line_16_live["fg"] = "red"
line_16_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_16_live["font"] = ftl
line_16_live["justify"] = "left"
line_16_live["anchor"] = "w"
line_16_live.place(x=800, y=805, width=70, height=33)

line_16_disabled = tk.Label(scrollframe)
line_16_disabled["bg"] = "#adafae"
line_16_disabled["fg"] = "red"
line_16_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_16_disabled["font"] = ftl
line_16_disabled["justify"] = "left"
line_16_disabled["anchor"] = "w"
line_16_disabled["relief"] = "flat"
line_16_disabled.place(x=650, y=805, width=150, height=33)

line_17_frame = tk.Label(scrollframe)
line_17_frame["bg"] = "#adafae"
line_17_frame["text"] = ""
line_17_frame["relief"] = "sunken"
line_17_frame.place(x=10, y=840, width=1060, height=40)

line_17_index = tk.Label(scrollframe)
line_17_index["bg"] = "#adafae"
line_17_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_17_index["font"] = ft
line_17_index["justify"] = "left"
line_17_index["anchor"] = "w"
line_17_index.place(x=20, y=845, width=150, height=33)

line_17_name = tk.Label(scrollframe)
line_17_name["bg"] = "#adafae"
line_17_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_17_name["font"] = ft
line_17_name["justify"] = "left"
line_17_name["anchor"] = "w"
line_17_name.place(x=250, y=845, width=500, height=33)

line_17_duration = tk.Label(scrollframe)
line_17_duration["bg"] = "#adafae"
line_17_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_17_duration["font"] = ft
line_17_duration["justify"] = "right"
line_17_duration["anchor"] = "e"
line_17_duration.place(x=910, y=845, width=150, height=33)

line_17_live = tk.Label(scrollframe)
line_17_live["bg"] = "#adafae"
line_17_live["fg"] = "red"
line_17_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_17_live["font"] = ftl
line_17_live["justify"] = "left"
line_17_live["anchor"] = "w"
line_17_live.place(x=800, y=845, width=70, height=33)

line_17_disabled = tk.Label(scrollframe)
line_17_disabled["bg"] = "#adafae"
line_17_disabled["fg"] = "red"
line_17_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_17_disabled["font"] = ftl
line_17_disabled["justify"] = "left"
line_17_disabled["anchor"] = "w"
line_17_disabled["relief"] = "flat"
line_17_disabled.place(x=650, y=845, width=150, height=33)

line_18_frame = tk.Label(scrollframe)
line_18_frame["bg"] = "#adafae"
line_18_frame["text"] = ""
line_18_frame["relief"] = "sunken"
line_18_frame.place(x=10, y=880, width=1060, height=40)

line_18_index = tk.Label(scrollframe)
line_18_index["bg"] = "#adafae"
line_18_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_18_index["font"] = ft
line_18_index["justify"] = "left"
line_18_index["anchor"] = "w"
line_18_index.place(x=20, y=885, width=150, height=33)

line_18_name = tk.Label(scrollframe)
line_18_name["bg"] = "#adafae"
line_18_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_18_name["font"] = ft
line_18_name["justify"] = "left"
line_18_name["anchor"] = "w"
line_18_name.place(x=250, y=885, width=500, height=33)

line_18_duration = tk.Label(scrollframe)
line_18_duration["bg"] = "#adafae"
line_18_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_18_duration["font"] = ft
line_18_duration["justify"] = "right"
line_18_duration["anchor"] = "e"
line_18_duration.place(x=910, y=885, width=150, height=33)

line_18_live = tk.Label(scrollframe)
line_18_live["bg"] = "#adafae"
line_18_live["fg"] = "red"
line_18_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_18_live["font"] = ftl
line_18_live["justify"] = "left"
line_18_live["anchor"] = "w"
line_18_live.place(x=800, y=885, width=70, height=33)

line_18_disabled = tk.Label(scrollframe)
line_18_disabled["bg"] = "#adafae"
line_18_disabled["fg"] = "red"
line_18_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_18_disabled["font"] = ftl
line_18_disabled["justify"] = "left"
line_18_disabled["anchor"] = "w"
line_18_disabled["relief"] = "flat"
line_18_disabled.place(x=650, y=885, width=150, height=33)

line_19_frame = tk.Label(scrollframe)
line_19_frame["bg"] = "#adafae"
line_19_frame["text"] = ""
line_19_frame["relief"] = "sunken"
line_19_frame.place(x=10, y=920, width=1060, height=40)

line_19_index = tk.Label(scrollframe)
line_19_index["bg"] = "#adafae"
line_19_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_19_index["font"] = ft
line_19_index["justify"] = "left"
line_19_index["anchor"] = "w"
line_19_index.place(x=20, y=925, width=150, height=33)

line_19_name = tk.Label(scrollframe)
line_19_name["bg"] = "#adafae"
line_19_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_19_name["font"] = ft
line_19_name["justify"] = "left"
line_19_name["anchor"] = "w"
line_19_name.place(x=250, y=925, width=500, height=33)

line_19_duration = tk.Label(scrollframe)
line_19_duration["bg"] = "#adafae"
line_19_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_19_duration["font"] = ft
line_19_duration["justify"] = "right"
line_19_duration["anchor"] = "e"
line_19_duration.place(x=910, y=925, width=150, height=33)

line_19_live = tk.Label(scrollframe)
line_19_live["bg"] = "#adafae"
line_19_live["fg"] = "red"
line_19_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_19_live["font"] = ftl
line_19_live["justify"] = "left"
line_19_live["anchor"] = "w"
line_19_live.place(x=800, y=925, width=70, height=33)

line_19_disabled = tk.Label(scrollframe)
line_19_disabled["bg"] = "#adafae"
line_19_disabled["fg"] = "red"
line_19_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_19_disabled["font"] = ftl
line_19_disabled["justify"] = "left"
line_19_disabled["anchor"] = "w"
line_19_disabled["relief"] = "flat"
line_19_disabled.place(x=650, y=925, width=150, height=33)

line_20_frame = tk.Label(scrollframe)
line_20_frame["bg"] = "#adafae"
line_20_frame["text"] = ""
line_20_frame["relief"] = "sunken"
line_20_frame.place(x=10, y=960, width=1060, height=40)

line_20_index = tk.Label(scrollframe)
line_20_index["bg"] = "#adafae"
line_20_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_20_index["font"] = ft
line_20_index["justify"] = "left"
line_20_index["anchor"] = "w"
line_20_index.place(x=20, y=965, width=150, height=33)

line_20_name = tk.Label(scrollframe)
line_20_name["bg"] = "#adafae"
line_20_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_20_name["font"] = ft
line_20_name["justify"] = "left"
line_20_name["anchor"] = "w"
line_20_name.place(x=250, y=965, width=500, height=33)

line_20_duration = tk.Label(scrollframe)
line_20_duration["bg"] = "#adafae"
line_20_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_20_duration["font"] = ft
line_20_duration["justify"] = "right"
line_20_duration["anchor"] = "e"
line_20_duration.place(x=910, y=965, width=150, height=33)

line_20_live = tk.Label(scrollframe)
line_20_live["bg"] = "#adafae"
line_20_live["fg"] = "red"
line_20_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_20_live["font"] = ftl
line_20_live["justify"] = "left"
line_20_live["anchor"] = "w"
line_20_live.place(x=800, y=965, width=70, height=33)

line_20_disabled = tk.Label(scrollframe)
line_20_disabled["bg"] = "#adafae"
line_20_disabled["fg"] = "red"
line_20_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_20_disabled["font"] = ftl
line_20_disabled["justify"] = "left"
line_20_disabled["anchor"] = "w"
line_20_disabled["relief"] = "flat"
line_20_disabled.place(x=650, y=965, width=150, height=33)

line_21_frame = tk.Label(scrollframe)
line_21_frame["bg"] = "#adafae"
line_21_frame["text"] = ""
line_21_frame["relief"] = "sunken"
line_21_frame.place(x=10, y=1000, width=1060, height=40)

line_21_index = tk.Label(scrollframe)
line_21_index["bg"] = "#adafae"
line_21_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_21_index["font"] = ft
line_21_index["justify"] = "left"
line_21_index["anchor"] = "w"
line_21_index.place(x=20, y=1005, width=150, height=33)

line_21_name = tk.Label(scrollframe)
line_21_name["bg"] = "#adafae"
line_21_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_21_name["font"] = ft
line_21_name["justify"] = "left"
line_21_name["anchor"] = "w"
line_21_name.place(x=250, y=1005, width=500, height=33)

line_21_duration = tk.Label(scrollframe)
line_21_duration["bg"] = "#adafae"
line_21_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_21_duration["font"] = ft
line_21_duration["justify"] = "right"
line_21_duration["anchor"] = "e"
line_21_duration.place(x=910, y=1005, width=150, height=33)

line_21_live = tk.Label(scrollframe)
line_21_live["bg"] = "#adafae"
line_21_live["fg"] = "red"
line_21_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_21_live["font"] = ftl
line_21_live["justify"] = "left"
line_21_live["anchor"] = "w"
line_21_live.place(x=800, y=1005, width=70, height=33)

line_21_disabled = tk.Label(scrollframe)
line_21_disabled["bg"] = "#adafae"
line_21_disabled["fg"] = "red"
line_21_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_21_disabled["font"] = ftl
line_21_disabled["justify"] = "left"
line_21_disabled["anchor"] = "w"
line_21_disabled["relief"] = "flat"
line_21_disabled.place(x=650, y=1005, width=150, height=33)

line_22_frame = tk.Label(scrollframe)
line_22_frame["bg"] = "#adafae"
line_22_frame["text"] = ""
line_22_frame["relief"] = "sunken"
line_22_frame.place(x=10, y=1040, width=1060, height=40)

line_22_index = tk.Label(scrollframe)
line_22_index["bg"] = "#adafae"
line_22_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_22_index["font"] = ft
line_22_index["justify"] = "left"
line_22_index["anchor"] = "w"
line_22_index.place(x=20, y=1045, width=150, height=33)

line_22_name = tk.Label(scrollframe)
line_22_name["bg"] = "#adafae"
line_22_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_22_name["font"] = ft
line_22_name["justify"] = "left"
line_22_name["anchor"] = "w"
line_22_name.place(x=250, y=1045, width=500, height=33)

line_22_duration = tk.Label(scrollframe)
line_22_duration["bg"] = "#adafae"
line_22_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_22_duration["font"] = ft
line_22_duration["justify"] = "right"
line_22_duration["anchor"] = "e"
line_22_duration.place(x=910, y=1045, width=150, height=33)

line_22_live = tk.Label(scrollframe)
line_22_live["bg"] = "#adafae"
line_22_live["fg"] = "red"
line_22_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_22_live["font"] = ftl
line_22_live["justify"] = "left"
line_22_live["anchor"] = "w"
line_22_live.place(x=800, y=1045, width=70, height=33)

line_22_disabled = tk.Label(scrollframe)
line_22_disabled["bg"] = "#adafae"
line_22_disabled["fg"] = "red"
line_22_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_22_disabled["font"] = ftl
line_22_disabled["justify"] = "left"
line_22_disabled["anchor"] = "w"
line_22_disabled["relief"] = "flat"
line_22_disabled.place(x=650, y=1045, width=150, height=33)

line_23_frame = tk.Label(scrollframe)
line_23_frame["bg"] = "#adafae"
line_23_frame["text"] = ""
line_23_frame["relief"] = "sunken"
line_23_frame.place(x=10, y=1080, width=1060, height=40)

line_23_index = tk.Label(scrollframe)
line_23_index["bg"] = "#adafae"
line_23_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_23_index["font"] = ft
line_23_index["justify"] = "left"
line_23_index["anchor"] = "w"
line_23_index.place(x=20, y=1085, width=150, height=33)

line_23_name = tk.Label(scrollframe)
line_23_name["bg"] = "#adafae"
line_23_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_23_name["font"] = ft
line_23_name["justify"] = "left"
line_23_name["anchor"] = "w"
line_23_name.place(x=250, y=1085, width=500, height=33)

line_23_duration = tk.Label(scrollframe)
line_23_duration["bg"] = "#adafae"
line_23_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_23_duration["font"] = ft
line_23_duration["justify"] = "right"
line_23_duration["anchor"] = "e"
line_23_duration.place(x=910, y=1085, width=150, height=33)

line_23_live = tk.Label(scrollframe)
line_23_live["bg"] = "#adafae"
line_23_live["fg"] = "red"
line_23_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_23_live["font"] = ftl
line_23_live["justify"] = "left"
line_23_live["anchor"] = "w"
line_23_live.place(x=800, y=1085, width=70, height=33)

line_23_disabled = tk.Label(scrollframe)
line_23_disabled["bg"] = "#adafae"
line_23_disabled["fg"] = "red"
line_23_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_23_disabled["font"] = ftl
line_23_disabled["justify"] = "left"
line_23_disabled["anchor"] = "w"
line_23_disabled["relief"] = "flat"
line_23_disabled.place(x=650, y=1085, width=150, height=33)

line_24_frame = tk.Label(scrollframe)
line_24_frame["bg"] = "#adafae"
line_24_frame["text"] = ""
line_24_frame["relief"] = "sunken"
line_24_frame.place(x=10, y=1120, width=1060, height=40)

line_24_index = tk.Label(scrollframe)
line_24_index["bg"] = "#adafae"
line_24_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_24_index["font"] = ft
line_24_index["justify"] = "left"
line_24_index["anchor"] = "w"
line_24_index.place(x=20, y=1125, width=150, height=33)

line_24_name = tk.Label(scrollframe)
line_24_name["bg"] = "#adafae"
line_24_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_24_name["font"] = ft
line_24_name["justify"] = "left"
line_24_name["anchor"] = "w"
line_24_name.place(x=250, y=1125, width=500, height=33)

line_24_duration = tk.Label(scrollframe)
line_24_duration["bg"] = "#adafae"
line_24_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_24_duration["font"] = ft
line_24_duration["justify"] = "right"
line_24_duration["anchor"] = "e"
line_24_duration.place(x=910, y=1125, width=150, height=33)

line_24_live = tk.Label(scrollframe)
line_24_live["bg"] = "#adafae"
line_24_live["fg"] = "red"
line_24_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_24_live["font"] = ftl
line_24_live["justify"] = "left"
line_24_live["anchor"] = "w"
line_24_live.place(x=800, y=1125, width=70, height=33)

line_24_disabled = tk.Label(scrollframe)
line_24_disabled["bg"] = "#adafae"
line_24_disabled["fg"] = "red"
line_24_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_24_disabled["font"] = ftl
line_24_disabled["justify"] = "left"
line_24_disabled["anchor"] = "w"
line_24_disabled["relief"] = "flat"
line_24_disabled.place(x=650, y=1125, width=150, height=33)

line_25_frame = tk.Label(scrollframe)
line_25_frame["bg"] = "#adafae"
line_25_frame["text"] = ""
line_25_frame["relief"] = "sunken"
line_25_frame.place(x=10, y=1160, width=1060, height=40)

line_25_index = tk.Label(scrollframe)
line_25_index["bg"] = "#adafae"
line_25_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_25_index["font"] = ft
line_25_index["justify"] = "left"
line_25_index["anchor"] = "w"
line_25_index.place(x=20, y=1165, width=150, height=33)

line_25_name = tk.Label(scrollframe)
line_25_name["bg"] = "#adafae"
line_25_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_25_name["font"] = ft
line_25_name["justify"] = "left"
line_25_name["anchor"] = "w"
line_25_name.place(x=250, y=1165, width=500, height=33)

line_25_duration = tk.Label(scrollframe)
line_25_duration["bg"] = "#adafae"
line_25_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_25_duration["font"] = ft
line_25_duration["justify"] = "right"
line_25_duration["anchor"] = "e"
line_25_duration.place(x=910, y=1165, width=150, height=33)

line_25_live = tk.Label(scrollframe)
line_25_live["bg"] = "#adafae"
line_25_live["fg"] = "red"
line_25_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_25_live["font"] = ftl
line_25_live["justify"] = "left"
line_25_live["anchor"] = "w"
line_25_live.place(x=800, y=1165, width=70, height=33)

line_25_disabled = tk.Label(scrollframe)
line_25_disabled["bg"] = "#adafae"
line_25_disabled["fg"] = "red"
line_25_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_25_disabled["font"] = ftl
line_25_disabled["justify"] = "left"
line_25_disabled["anchor"] = "w"
line_25_disabled["relief"] = "flat"
line_25_disabled.place(x=650, y=1165, width=150, height=33)

line_26_frame = tk.Label(scrollframe)
line_26_frame["bg"] = "#adafae"
line_26_frame["text"] = ""
line_26_frame["relief"] = "sunken"
line_26_frame.place(x=10, y=1200, width=1060, height=40)

line_26_index = tk.Label(scrollframe)
line_26_index["bg"] = "#adafae"
line_26_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_26_index["font"] = ft
line_26_index["justify"] = "left"
line_26_index["anchor"] = "w"
line_26_index.place(x=20, y=1205, width=150, height=33)

line_26_name = tk.Label(scrollframe)
line_26_name["bg"] = "#adafae"
line_26_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_26_name["font"] = ft
line_26_name["justify"] = "left"
line_26_name["anchor"] = "w"
line_26_name.place(x=250, y=1205, width=500, height=33)

line_26_duration = tk.Label(scrollframe)
line_26_duration["bg"] = "#adafae"
line_26_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_26_duration["font"] = ft
line_26_duration["justify"] = "right"
line_26_duration["anchor"] = "e"
line_26_duration.place(x=910, y=1205, width=150, height=33)

line_26_live = tk.Label(scrollframe)
line_26_live["bg"] = "#adafae"
line_26_live["fg"] = "red"
line_26_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_26_live["font"] = ftl
line_26_live["justify"] = "left"
line_26_live["anchor"] = "w"
line_26_live.place(x=800, y=1205, width=70, height=33)

line_26_disabled = tk.Label(scrollframe)
line_26_disabled["bg"] = "#adafae"
line_26_disabled["fg"] = "red"
line_26_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_26_disabled["font"] = ftl
line_26_disabled["justify"] = "left"
line_26_disabled["anchor"] = "w"
line_26_disabled["relief"] = "flat"
line_26_disabled.place(x=650, y=1205, width=150, height=33)

line_27_frame = tk.Label(scrollframe)
line_27_frame["bg"] = "#adafae"
line_27_frame["text"] = ""
line_27_frame["relief"] = "sunken"
line_27_frame.place(x=10, y=1240, width=1060, height=40)

line_27_index = tk.Label(scrollframe)
line_27_index["bg"] = "#adafae"
line_27_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_27_index["font"] = ft
line_27_index["justify"] = "left"
line_27_index["anchor"] = "w"
line_27_index.place(x=20, y=1245, width=150, height=33)

line_27_name = tk.Label(scrollframe)
line_27_name["bg"] = "#adafae"
line_27_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_27_name["font"] = ft
line_27_name["justify"] = "left"
line_27_name["anchor"] = "w"
line_27_name.place(x=250, y=1245, width=500, height=33)

line_27_duration = tk.Label(scrollframe)
line_27_duration["bg"] = "#adafae"
line_27_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_27_duration["font"] = ft
line_27_duration["justify"] = "right"
line_27_duration["anchor"] = "e"
line_27_duration.place(x=910, y=1245, width=150, height=33)

line_27_live = tk.Label(scrollframe)
line_27_live["bg"] = "#adafae"
line_27_live["fg"] = "red"
line_27_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_27_live["font"] = ftl
line_27_live["justify"] = "left"
line_27_live["anchor"] = "w"
line_27_live.place(x=800, y=1245, width=70, height=33)

line_27_disabled = tk.Label(scrollframe)
line_27_disabled["bg"] = "#adafae"
line_27_disabled["fg"] = "red"
line_27_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_27_disabled["font"] = ftl
line_27_disabled["justify"] = "left"
line_27_disabled["anchor"] = "w"
line_27_disabled["relief"] = "flat"
line_27_disabled.place(x=650, y=1245, width=150, height=33)

line_28_frame = tk.Label(scrollframe)
line_28_frame["bg"] = "#adafae"
line_28_frame["text"] = ""
line_28_frame["relief"] = "sunken"
line_28_frame.place(x=10, y=1280, width=1060, height=40)

line_28_index = tk.Label(scrollframe)
line_28_index["bg"] = "#adafae"
line_28_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_28_index["font"] = ft
line_28_index["justify"] = "left"
line_28_index["anchor"] = "w"
line_28_index.place(x=20, y=1285, width=150, height=33)

line_28_name = tk.Label(scrollframe)
line_28_name["bg"] = "#adafae"
line_28_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_28_name["font"] = ft
line_28_name["justify"] = "left"
line_28_name["anchor"] = "w"
line_28_name.place(x=250, y=1285, width=500, height=33)

line_28_duration = tk.Label(scrollframe)
line_28_duration["bg"] = "#adafae"
line_28_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_28_duration["font"] = ft
line_28_duration["justify"] = "right"
line_28_duration["anchor"] = "e"
line_28_duration.place(x=910, y=1285, width=150, height=33)

line_28_live = tk.Label(scrollframe)
line_28_live["bg"] = "#adafae"
line_28_live["fg"] = "red"
line_28_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_28_live["font"] = ftl
line_28_live["justify"] = "left"
line_28_live["anchor"] = "w"
line_28_live.place(x=800, y=1285, width=70, height=33)

line_28_disabled = tk.Label(scrollframe)
line_28_disabled["bg"] = "#adafae"
line_28_disabled["fg"] = "red"
line_28_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_28_disabled["font"] = ftl
line_28_disabled["justify"] = "left"
line_28_disabled["anchor"] = "w"
line_28_disabled["relief"] = "flat"
line_28_disabled.place(x=650, y=1285, width=150, height=33)

line_29_frame = tk.Label(scrollframe)
line_29_frame["bg"] = "#adafae"
line_29_frame["text"] = ""
line_29_frame["relief"] = "sunken"
line_29_frame.place(x=10, y=1320, width=1060, height=40)

line_29_index = tk.Label(scrollframe)
line_29_index["bg"] = "#adafae"
line_29_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_29_index["font"] = ft
line_29_index["justify"] = "left"
line_29_index["anchor"] = "w"
line_29_index.place(x=20, y=1325, width=150, height=33)

line_29_name = tk.Label(scrollframe)
line_29_name["bg"] = "#adafae"
line_29_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_29_name["font"] = ft
line_29_name["justify"] = "left"
line_29_name["anchor"] = "w"
line_29_name.place(x=250, y=1325, width=500, height=33)

line_29_duration = tk.Label(scrollframe)
line_29_duration["bg"] = "#adafae"
line_29_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_29_duration["font"] = ft
line_29_duration["justify"] = "right"
line_29_duration["anchor"] = "e"
line_29_duration.place(x=910, y=1325, width=150, height=33)

line_29_live = tk.Label(scrollframe)
line_29_live["bg"] = "#adafae"
line_29_live["fg"] = "red"
line_29_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_29_live["font"] = ftl
line_29_live["justify"] = "left"
line_29_live["anchor"] = "w"
line_29_live.place(x=800, y=1325, width=70, height=33)

line_29_disabled = tk.Label(scrollframe)
line_29_disabled["bg"] = "#adafae"
line_29_disabled["fg"] = "red"
line_29_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_29_disabled["font"] = ftl
line_29_disabled["justify"] = "left"
line_29_disabled["anchor"] = "w"
line_29_disabled["relief"] = "flat"
line_29_disabled.place(x=650, y=1325, width=150, height=33)

line_30_frame = tk.Label(scrollframe)
line_30_frame["bg"] = "#adafae"
line_30_frame["text"] = ""
line_30_frame["relief"] = "sunken"
line_30_frame.place(x=10, y=1360, width=1060, height=40)

line_30_index = tk.Label(scrollframe)
line_30_index["bg"] = "#adafae"
line_30_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_30_index["font"] = ft
line_30_index["justify"] = "left"
line_30_index["anchor"] = "w"
line_30_index.place(x=20, y=1365, width=150, height=33)

line_30_name = tk.Label(scrollframe)
line_30_name["bg"] = "#adafae"
line_30_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_30_name["font"] = ft
line_30_name["justify"] = "left"
line_30_name["anchor"] = "w"
line_30_name.place(x=250, y=1365, width=500, height=33)

line_30_duration = tk.Label(scrollframe)
line_30_duration["bg"] = "#adafae"
line_30_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_30_duration["font"] = ft
line_30_duration["justify"] = "right"
line_30_duration["anchor"] = "e"
line_30_duration.place(x=910, y=1365, width=150, height=33)

line_30_live = tk.Label(scrollframe)
line_30_live["bg"] = "#adafae"
line_30_live["fg"] = "red"
line_30_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_30_live["font"] = ftl
line_30_live["justify"] = "left"
line_30_live["anchor"] = "w"
line_30_live.place(x=800, y=1365, width=70, height=33)

line_30_disabled = tk.Label(scrollframe)
line_30_disabled["bg"] = "#adafae"
line_30_disabled["fg"] = "red"
line_30_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_30_disabled["font"] = ftl
line_30_disabled["justify"] = "left"
line_30_disabled["anchor"] = "w"
line_30_disabled["relief"] = "flat"
line_30_disabled.place(x=650, y=1365, width=150, height=33)

line_31_frame = tk.Label(scrollframe)
line_31_frame["bg"] = "#adafae"
line_31_frame["text"] = ""
line_31_frame["relief"] = "sunken"
line_31_frame.place(x=10, y=1400, width=1060, height=40)

line_31_index = tk.Label(scrollframe)
line_31_index["bg"] = "#adafae"
line_31_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_31_index["font"] = ft
line_31_index["justify"] = "left"
line_31_index["anchor"] = "w"
line_31_index.place(x=20, y=1405, width=150, height=33)

line_31_name = tk.Label(scrollframe)
line_31_name["bg"] = "#adafae"
line_31_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_31_name["font"] = ft
line_31_name["justify"] = "left"
line_31_name["anchor"] = "w"
line_31_name.place(x=250, y=1405, width=500, height=33)

line_31_duration = tk.Label(scrollframe)
line_31_duration["bg"] = "#adafae"
line_31_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_31_duration["font"] = ft
line_31_duration["justify"] = "right"
line_31_duration["anchor"] = "e"
line_31_duration.place(x=910, y=1405, width=150, height=33)

line_31_live = tk.Label(scrollframe)
line_31_live["bg"] = "#adafae"
line_31_live["fg"] = "red"
line_31_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_31_live["font"] = ftl
line_31_live["justify"] = "left"
line_31_live["anchor"] = "w"
line_31_live.place(x=800, y=1405, width=70, height=33)

line_31_disabled = tk.Label(scrollframe)
line_31_disabled["bg"] = "#adafae"
line_31_disabled["fg"] = "red"
line_31_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_31_disabled["font"] = ftl
line_31_disabled["justify"] = "left"
line_31_disabled["anchor"] = "w"
line_31_disabled["relief"] = "flat"
line_31_disabled.place(x=650, y=1405, width=150, height=33)

line_32_frame = tk.Label(scrollframe)
line_32_frame["bg"] = "#adafae"
line_32_frame["text"] = ""
line_32_frame["relief"] = "sunken"
line_32_frame.place(x=10, y=1440, width=1060, height=40)

line_32_index = tk.Label(scrollframe)
line_32_index["bg"] = "#adafae"
line_32_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_32_index["font"] = ft
line_32_index["justify"] = "left"
line_32_index["anchor"] = "w"
line_32_index.place(x=20, y=1445, width=150, height=33)

line_32_name = tk.Label(scrollframe)
line_32_name["bg"] = "#adafae"
line_32_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_32_name["font"] = ft
line_32_name["justify"] = "left"
line_32_name["anchor"] = "w"
line_32_name.place(x=250, y=1445, width=500, height=33)

line_32_duration = tk.Label(scrollframe)
line_32_duration["bg"] = "#adafae"
line_32_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_32_duration["font"] = ft
line_32_duration["justify"] = "right"
line_32_duration["anchor"] = "e"
line_32_duration.place(x=910, y=1445, width=150, height=33)

line_32_live = tk.Label(scrollframe)
line_32_live["bg"] = "#adafae"
line_32_live["fg"] = "red"
line_32_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_32_live["font"] = ftl
line_32_live["justify"] = "left"
line_32_live["anchor"] = "w"
line_32_live.place(x=800, y=1445, width=70, height=33)

line_32_disabled = tk.Label(scrollframe)
line_32_disabled["bg"] = "#adafae"
line_32_disabled["fg"] = "red"
line_32_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_32_disabled["font"] = ftl
line_32_disabled["justify"] = "left"
line_32_disabled["anchor"] = "w"
line_32_disabled["relief"] = "flat"
line_32_disabled.place(x=650, y=1445, width=150, height=33)

line_33_frame = tk.Label(scrollframe)
line_33_frame["bg"] = "#adafae"
line_33_frame["text"] = ""
line_33_frame["relief"] = "sunken"
line_33_frame.place(x=10, y=1480, width=1060, height=40)

line_33_index = tk.Label(scrollframe)
line_33_index["bg"] = "#adafae"
line_33_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_33_index["font"] = ft
line_33_index["justify"] = "left"
line_33_index["anchor"] = "w"
line_33_index.place(x=20, y=1485, width=150, height=33)

line_33_name = tk.Label(scrollframe)
line_33_name["bg"] = "#adafae"
line_33_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_33_name["font"] = ft
line_33_name["justify"] = "left"
line_33_name["anchor"] = "w"
line_33_name.place(x=250, y=1485, width=500, height=33)

line_33_duration = tk.Label(scrollframe)
line_33_duration["bg"] = "#adafae"
line_33_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_33_duration["font"] = ft
line_33_duration["justify"] = "right"
line_33_duration["anchor"] = "e"
line_33_duration.place(x=910, y=1485, width=150, height=33)

line_33_live = tk.Label(scrollframe)
line_33_live["bg"] = "#adafae"
line_33_live["fg"] = "red"
line_33_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_33_live["font"] = ftl
line_33_live["justify"] = "left"
line_33_live["anchor"] = "w"
line_33_live.place(x=800, y=1485, width=70, height=33)

line_33_disabled = tk.Label(scrollframe)
line_33_disabled["bg"] = "#adafae"
line_33_disabled["fg"] = "red"
line_33_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_33_disabled["font"] = ftl
line_33_disabled["justify"] = "left"
line_33_disabled["anchor"] = "w"
line_33_disabled["relief"] = "flat"
line_33_disabled.place(x=650, y=1485, width=150, height=33)

line_34_frame = tk.Label(scrollframe)
line_34_frame["bg"] = "#adafae"
line_34_frame["text"] = ""
line_34_frame["relief"] = "sunken"
line_34_frame.place(x=10, y=1520, width=1060, height=40)

line_34_index = tk.Label(scrollframe)
line_34_index["bg"] = "#adafae"
line_34_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_34_index["font"] = ft
line_34_index["justify"] = "left"
line_34_index["anchor"] = "w"
line_34_index.place(x=20, y=1525, width=150, height=33)

line_34_name = tk.Label(scrollframe)
line_34_name["bg"] = "#adafae"
line_34_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_34_name["font"] = ft
line_34_name["justify"] = "left"
line_34_name["anchor"] = "w"
line_34_name.place(x=250, y=1525, width=500, height=33)

line_34_duration = tk.Label(scrollframe)
line_34_duration["bg"] = "#adafae"
line_34_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_34_duration["font"] = ft
line_34_duration["justify"] = "right"
line_34_duration["anchor"] = "e"
line_34_duration.place(x=910, y=1525, width=150, height=33)

line_34_live = tk.Label(scrollframe)
line_34_live["bg"] = "#adafae"
line_34_live["fg"] = "red"
line_34_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_34_live["font"] = ftl
line_34_live["justify"] = "left"
line_34_live["anchor"] = "w"
line_34_live.place(x=800, y=1525, width=70, height=33)

line_34_disabled = tk.Label(scrollframe)
line_34_disabled["bg"] = "#adafae"
line_34_disabled["fg"] = "red"
line_34_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_34_disabled["font"] = ftl
line_34_disabled["justify"] = "left"
line_34_disabled["anchor"] = "w"
line_34_disabled["relief"] = "flat"
line_34_disabled.place(x=650, y=1525, width=150, height=33)

line_35_frame = tk.Label(scrollframe)
line_35_frame["bg"] = "#adafae"
line_35_frame["text"] = ""
line_35_frame["relief"] = "sunken"
line_35_frame.place(x=10, y=1560, width=1060, height=40)

line_35_index = tk.Label(scrollframe)
line_35_index["bg"] = "#adafae"
line_35_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_35_index["font"] = ft
line_35_index["justify"] = "left"
line_35_index["anchor"] = "w"
line_35_index.place(x=20, y=1565, width=150, height=33)

line_35_name = tk.Label(scrollframe)
line_35_name["bg"] = "#adafae"
line_35_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_35_name["font"] = ft
line_35_name["justify"] = "left"
line_35_name["anchor"] = "w"
line_35_name.place(x=250, y=1565, width=500, height=33)

line_35_duration = tk.Label(scrollframe)
line_35_duration["bg"] = "#adafae"
line_35_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_35_duration["font"] = ft
line_35_duration["justify"] = "right"
line_35_duration["anchor"] = "e"
line_35_duration.place(x=910, y=1565, width=150, height=33)

line_35_live = tk.Label(scrollframe)
line_35_live["bg"] = "#adafae"
line_35_live["fg"] = "red"
line_35_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_35_live["font"] = ftl
line_35_live["justify"] = "left"
line_35_live["anchor"] = "w"
line_35_live.place(x=800, y=1565, width=70, height=33)

line_35_disabled = tk.Label(scrollframe)
line_35_disabled["bg"] = "#adafae"
line_35_disabled["fg"] = "red"
line_35_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_35_disabled["font"] = ftl
line_35_disabled["justify"] = "left"
line_35_disabled["anchor"] = "w"
line_35_disabled["relief"] = "flat"
line_35_disabled.place(x=650, y=1565, width=150, height=33)

line_36_frame = tk.Label(scrollframe)
line_36_frame["bg"] = "#adafae"
line_36_frame["text"] = ""
line_36_frame["relief"] = "sunken"
line_36_frame.place(x=10, y=1600, width=1060, height=40)

line_36_index = tk.Label(scrollframe)
line_36_index["bg"] = "#adafae"
line_36_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_36_index["font"] = ft
line_36_index["justify"] = "left"
line_36_index["anchor"] = "w"
line_36_index.place(x=20, y=1605, width=150, height=33)

line_36_name = tk.Label(scrollframe)
line_36_name["bg"] = "#adafae"
line_36_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_36_name["font"] = ft
line_36_name["justify"] = "left"
line_36_name["anchor"] = "w"
line_36_name.place(x=250, y=1605, width=500, height=33)

line_36_duration = tk.Label(scrollframe)
line_36_duration["bg"] = "#adafae"
line_36_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_36_duration["font"] = ft
line_36_duration["justify"] = "right"
line_36_duration["anchor"] = "e"
line_36_duration.place(x=910, y=1605, width=150, height=33)

line_36_live = tk.Label(scrollframe)
line_36_live["bg"] = "#adafae"
line_36_live["fg"] = "red"
line_36_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_36_live["font"] = ftl
line_36_live["justify"] = "left"
line_36_live["anchor"] = "w"
line_36_live.place(x=800, y=1605, width=70, height=33)

line_36_disabled = tk.Label(scrollframe)
line_36_disabled["bg"] = "#adafae"
line_36_disabled["fg"] = "red"
line_36_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_36_disabled["font"] = ftl
line_36_disabled["justify"] = "left"
line_36_disabled["anchor"] = "w"
line_36_disabled["relief"] = "flat"
line_36_disabled.place(x=650, y=1605, width=150, height=33)

line_37_frame = tk.Label(scrollframe)
line_37_frame["bg"] = "#adafae"
line_37_frame["text"] = ""
line_37_frame["relief"] = "sunken"
line_37_frame.place(x=10, y=1640, width=1060, height=40)

line_37_index = tk.Label(scrollframe)
line_37_index["bg"] = "#adafae"
line_37_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_37_index["font"] = ft
line_37_index["justify"] = "left"
line_37_index["anchor"] = "w"
line_37_index.place(x=20, y=1645, width=150, height=33)

line_37_name = tk.Label(scrollframe)
line_37_name["bg"] = "#adafae"
line_37_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_37_name["font"] = ft
line_37_name["justify"] = "left"
line_37_name["anchor"] = "w"
line_37_name.place(x=250, y=1645, width=500, height=33)

line_37_duration = tk.Label(scrollframe)
line_37_duration["bg"] = "#adafae"
line_37_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_37_duration["font"] = ft
line_37_duration["justify"] = "right"
line_37_duration["anchor"] = "e"
line_37_duration.place(x=910, y=1645, width=150, height=33)

line_37_live = tk.Label(scrollframe)
line_37_live["bg"] = "#adafae"
line_37_live["fg"] = "red"
line_37_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_37_live["font"] = ftl
line_37_live["justify"] = "left"
line_37_live["anchor"] = "w"
line_37_live.place(x=800, y=1645, width=70, height=33)

line_37_disabled = tk.Label(scrollframe)
line_37_disabled["bg"] = "#adafae"
line_37_disabled["fg"] = "red"
line_37_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_37_disabled["font"] = ftl
line_37_disabled["justify"] = "left"
line_37_disabled["anchor"] = "w"
line_37_disabled["relief"] = "flat"
line_37_disabled.place(x=650, y=1645, width=150, height=33)

line_38_frame = tk.Label(scrollframe)
line_38_frame["bg"] = "#adafae"
line_38_frame["text"] = ""
line_38_frame["relief"] = "sunken"
line_38_frame.place(x=10, y=1680, width=1060, height=40)

line_38_index = tk.Label(scrollframe)
line_38_index["bg"] = "#adafae"
line_38_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_38_index["font"] = ft
line_38_index["justify"] = "left"
line_38_index["anchor"] = "w"
line_38_index.place(x=20, y=1685, width=150, height=33)

line_38_name = tk.Label(scrollframe)
line_38_name["bg"] = "#adafae"
line_38_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_38_name["font"] = ft
line_38_name["justify"] = "left"
line_38_name["anchor"] = "w"
line_38_name.place(x=250, y=1685, width=500, height=33)

line_38_duration = tk.Label(scrollframe)
line_38_duration["bg"] = "#adafae"
line_38_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_38_duration["font"] = ft
line_38_duration["justify"] = "right"
line_38_duration["anchor"] = "e"
line_38_duration.place(x=910, y=1685, width=150, height=33)

line_38_live = tk.Label(scrollframe)
line_38_live["bg"] = "#adafae"
line_38_live["fg"] = "red"
line_38_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_38_live["font"] = ftl
line_38_live["justify"] = "left"
line_38_live["anchor"] = "w"
line_38_live.place(x=800, y=1685, width=70, height=33)

line_38_disabled = tk.Label(scrollframe)
line_38_disabled["bg"] = "#adafae"
line_38_disabled["fg"] = "red"
line_38_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_38_disabled["font"] = ftl
line_38_disabled["justify"] = "left"
line_38_disabled["anchor"] = "w"
line_38_disabled["relief"] = "flat"
line_38_disabled.place(x=650, y=1685, width=150, height=33)

line_39_frame = tk.Label(scrollframe)
line_39_frame["bg"] = "#adafae"
line_39_frame["text"] = ""
line_39_frame["relief"] = "sunken"
line_39_frame.place(x=10, y=1720, width=1060, height=40)

line_39_index = tk.Label(scrollframe)
line_39_index["bg"] = "#adafae"
line_39_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_39_index["font"] = ft
line_39_index["justify"] = "left"
line_39_index["anchor"] = "w"
line_39_index.place(x=20, y=1725, width=150, height=33)

line_39_name = tk.Label(scrollframe)
line_39_name["bg"] = "#adafae"
line_39_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_39_name["font"] = ft
line_39_name["justify"] = "left"
line_39_name["anchor"] = "w"
line_39_name.place(x=250, y=1725, width=500, height=33)

line_39_duration = tk.Label(scrollframe)
line_39_duration["bg"] = "#adafae"
line_39_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_39_duration["font"] = ft
line_39_duration["justify"] = "right"
line_39_duration["anchor"] = "e"
line_39_duration.place(x=910, y=1725, width=150, height=33)

line_39_live = tk.Label(scrollframe)
line_39_live["bg"] = "#adafae"
line_39_live["fg"] = "red"
line_39_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_39_live["font"] = ftl
line_39_live["justify"] = "left"
line_39_live["anchor"] = "w"
line_39_live.place(x=800, y=1725, width=70, height=33)

line_39_disabled = tk.Label(scrollframe)
line_39_disabled["bg"] = "#adafae"
line_39_disabled["fg"] = "red"
line_39_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_39_disabled["font"] = ftl
line_39_disabled["justify"] = "left"
line_39_disabled["anchor"] = "w"
line_39_disabled["relief"] = "flat"
line_39_disabled.place(x=650, y=1725, width=150, height=33)

line_40_frame = tk.Label(scrollframe)
line_40_frame["bg"] = "#adafae"
line_40_frame["text"] = ""
line_40_frame["relief"] = "sunken"
line_40_frame.place(x=10, y=1760, width=1060, height=40)

line_40_index = tk.Label(scrollframe)
line_40_index["bg"] = "#adafae"
line_40_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_40_index["font"] = ft
line_40_index["justify"] = "left"
line_40_index["anchor"] = "w"
line_40_index.place(x=20, y=1765, width=150, height=33)

line_40_name = tk.Label(scrollframe)
line_40_name["bg"] = "#adafae"
line_40_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_40_name["font"] = ft
line_40_name["justify"] = "left"
line_40_name["anchor"] = "w"
line_40_name.place(x=250, y=1765, width=500, height=33)

line_40_duration = tk.Label(scrollframe)
line_40_duration["bg"] = "#adafae"
line_40_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_40_duration["font"] = ft
line_40_duration["justify"] = "right"
line_40_duration["anchor"] = "e"
line_40_duration.place(x=910, y=1765, width=150, height=33)

line_40_live = tk.Label(scrollframe)
line_40_live["bg"] = "#adafae"
line_40_live["fg"] = "red"
line_40_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_40_live["font"] = ftl
line_40_live["justify"] = "left"
line_40_live["anchor"] = "w"
line_40_live.place(x=800, y=1765, width=70, height=33)

line_40_disabled = tk.Label(scrollframe)
line_40_disabled["bg"] = "#adafae"
line_40_disabled["fg"] = "red"
line_40_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_40_disabled["font"] = ftl
line_40_disabled["justify"] = "left"
line_40_disabled["anchor"] = "w"
line_40_disabled["relief"] = "flat"
line_40_disabled.place(x=650, y=1765, width=150, height=33)

line_41_frame = tk.Label(scrollframe)
line_41_frame["bg"] = "#adafae"
line_41_frame["text"] = ""
line_41_frame["relief"] = "sunken"
line_41_frame.place(x=10, y=1800, width=1060, height=40)

line_41_index = tk.Label(scrollframe)
line_41_index["bg"] = "#adafae"
line_41_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_41_index["font"] = ft
line_41_index["justify"] = "left"
line_41_index["anchor"] = "w"
line_41_index.place(x=20, y=1805, width=150, height=33)

line_41_name = tk.Label(scrollframe)
line_41_name["bg"] = "#adafae"
line_41_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_41_name["font"] = ft
line_41_name["justify"] = "left"
line_41_name["anchor"] = "w"
line_41_name.place(x=250, y=1805, width=500, height=33)

line_41_duration = tk.Label(scrollframe)
line_41_duration["bg"] = "#adafae"
line_41_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_41_duration["font"] = ft
line_41_duration["justify"] = "right"
line_41_duration["anchor"] = "e"
line_41_duration.place(x=910, y=1805, width=150, height=33)

line_41_live = tk.Label(scrollframe)
line_41_live["bg"] = "#adafae"
line_41_live["fg"] = "red"
line_41_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_41_live["font"] = ftl
line_41_live["justify"] = "left"
line_41_live["anchor"] = "w"
line_41_live["relief"] = "flat"
line_41_live.place(x=800, y=1805, width=70, height=33)

line_41_disabled = tk.Label(scrollframe)
line_41_disabled["bg"] = "#adafae"
line_41_disabled["fg"] = "red"
line_41_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_41_disabled["font"] = ftl
line_41_disabled["justify"] = "left"
line_41_disabled["anchor"] = "w"
line_41_disabled["relief"] = "flat"
line_41_disabled.place(x=650, y=1805, width=150, height=33)

line_42_frame = tk.Label(scrollframe)
line_42_frame["bg"] = "#adafae"
line_42_frame["text"] = ""
line_42_frame["relief"] = "sunken"
line_42_frame.place(x=10, y=1840, width=1060, height=40)

line_42_index = tk.Label(scrollframe)
line_42_index["bg"] = "#adafae"
line_42_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_42_index["font"] = ft
line_42_index["justify"] = "left"
line_42_index["anchor"] = "w"
line_42_index.place(x=20, y=1845, width=150, height=33)

line_42_name = tk.Label(scrollframe)
line_42_name["bg"] = "#adafae"
line_42_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_42_name["font"] = ft
line_42_name["justify"] = "left"
line_42_name["anchor"] = "w"
line_42_name.place(x=250, y=1845, width=500, height=33)

line_42_duration = tk.Label(scrollframe)
line_42_duration["bg"] = "#adafae"
line_42_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_42_duration["font"] = ft
line_42_duration["justify"] = "right"
line_42_duration["anchor"] = "e"
line_42_duration.place(x=910, y=1845, width=150, height=33)

line_42_live = tk.Label(scrollframe)
line_42_live["bg"] = "#adafae"
line_42_live["fg"] = "red"
line_42_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_42_live["font"] = ftl
line_42_live["justify"] = "left"
line_42_live["anchor"] = "w"
line_42_live["relief"] = "flat"
line_42_live.place(x=800, y=1845, width=70, height=33)

line_42_disabled = tk.Label(scrollframe)
line_42_disabled["bg"] = "#adafae"
line_42_disabled["fg"] = "red"
line_42_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_42_disabled["font"] = ftl
line_42_disabled["justify"] = "left"
line_42_disabled["anchor"] = "w"
line_42_disabled["relief"] = "flat"
line_42_disabled.place(x=650, y=1845, width=150, height=33)

line_43_frame = tk.Label(scrollframe)
line_43_frame["bg"] = "#adafae"
line_43_frame["text"] = ""
line_43_frame["relief"] = "sunken"
line_43_frame.place(x=10, y=1880, width=1060, height=40)

line_43_index = tk.Label(scrollframe)
line_43_index["bg"] = "#adafae"
line_43_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_43_index["font"] = ft
line_43_index["justify"] = "left"
line_43_index["anchor"] = "w"
line_43_index.place(x=20, y=1885, width=150, height=33)

line_43_name = tk.Label(scrollframe)
line_43_name["bg"] = "#adafae"
line_43_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_43_name["font"] = ft
line_43_name["justify"] = "left"
line_43_name["anchor"] = "w"
line_43_name.place(x=250, y=1885, width=500, height=33)

line_43_duration = tk.Label(scrollframe)
line_43_duration["bg"] = "#adafae"
line_43_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_43_duration["font"] = ft
line_43_duration["justify"] = "right"
line_43_duration["anchor"] = "e"
line_43_duration.place(x=910, y=1885, width=150, height=33)

line_43_live = tk.Label(scrollframe)
line_43_live["bg"] = "#adafae"
line_43_live["fg"] = "red"
line_43_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_43_live["font"] = ftl
line_43_live["justify"] = "left"
line_43_live["anchor"] = "w"
line_43_live["relief"] = "flat"
line_43_live.place(x=800, y=1885, width=70, height=33)

line_43_disabled = tk.Label(scrollframe)
line_43_disabled["bg"] = "#adafae"
line_43_disabled["fg"] = "red"
line_43_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_43_disabled["font"] = ftl
line_43_disabled["justify"] = "left"
line_43_disabled["anchor"] = "w"
line_43_disabled["relief"] = "flat"
line_43_disabled.place(x=650, y=1885, width=150, height=33)

line_44_frame = tk.Label(scrollframe)
line_44_frame["bg"] = "#adafae"
line_44_frame["text"] = ""
line_44_frame["relief"] = "sunken"
line_44_frame.place(x=10, y=1920, width=1060, height=40)

line_44_index = tk.Label(scrollframe)
line_44_index["bg"] = "#adafae"
line_44_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_44_index["font"] = ft
line_44_index["justify"] = "left"
line_44_index["anchor"] = "w"
line_44_index.place(x=20, y=1925, width=150, height=33)

line_44_name = tk.Label(scrollframe)
line_44_name["bg"] = "#adafae"
line_44_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_44_name["font"] = ft
line_44_name["justify"] = "left"
line_44_name["anchor"] = "w"
line_44_name.place(x=250, y=1925, width=500, height=33)

line_44_duration = tk.Label(scrollframe)
line_44_duration["bg"] = "#adafae"
line_44_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_44_duration["font"] = ft
line_44_duration["justify"] = "right"
line_44_duration["anchor"] = "e"
line_44_duration.place(x=910, y=1925, width=150, height=33)

line_44_live = tk.Label(scrollframe)
line_44_live["bg"] = "#adafae"
line_44_live["fg"] = "red"
line_44_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_44_live["font"] = ftl
line_44_live["justify"] = "left"
line_44_live["anchor"] = "w"
line_44_live["relief"] = "flat"
line_44_live.place(x=800, y=1925, width=70, height=33)

line_44_disabled = tk.Label(scrollframe)
line_44_disabled["bg"] = "#adafae"
line_44_disabled["fg"] = "red"
line_44_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_44_disabled["font"] = ftl
line_44_disabled["justify"] = "left"
line_44_disabled["anchor"] = "w"
line_44_disabled["relief"] = "flat"
line_44_disabled.place(x=650, y=1925, width=150, height=33)

line_45_frame = tk.Label(scrollframe)
line_45_frame["bg"] = "#adafae"
line_45_frame["text"] = ""
line_45_frame["relief"] = "sunken"
line_45_frame.place(x=10, y=1960, width=1060, height=40)

line_45_index = tk.Label(scrollframe)
line_45_index["bg"] = "#adafae"
line_45_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_45_index["font"] = ft
line_45_index["justify"] = "left"
line_45_index["anchor"] = "w"
line_45_index.place(x=20, y=1965, width=150, height=33)

line_45_name = tk.Label(scrollframe)
line_45_name["bg"] = "#adafae"
line_45_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_45_name["font"] = ft
line_45_name["justify"] = "left"
line_45_name["anchor"] = "w"
line_45_name.place(x=250, y=1965, width=500, height=33)

line_45_duration = tk.Label(scrollframe)
line_45_duration["bg"] = "#adafae"
line_45_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_45_duration["font"] = ft
line_45_duration["justify"] = "right"
line_45_duration["anchor"] = "e"
line_45_duration.place(x=910, y=1965, width=150, height=33)

line_45_live = tk.Label(scrollframe)
line_45_live["bg"] = "#adafae"
line_45_live["fg"] = "red"
line_45_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_45_live["font"] = ftl
line_45_live["justify"] = "left"
line_45_live["anchor"] = "w"
line_45_live["relief"] = "flat"
line_45_live.place(x=800, y=1965, width=70, height=33)

line_45_disabled = tk.Label(scrollframe)
line_45_disabled["bg"] = "#adafae"
line_45_disabled["fg"] = "red"
line_45_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_45_disabled["font"] = ftl
line_45_disabled["justify"] = "left"
line_45_disabled["anchor"] = "w"
line_45_disabled["relief"] = "flat"
line_45_disabled.place(x=650, y=1965, width=150, height=33)

line_46_frame = tk.Label(scrollframe)
line_46_frame["bg"] = "#adafae"
line_46_frame["text"] = ""
line_46_frame["relief"] = "sunken"
line_46_frame.place(x=10, y=2000, width=1060, height=40)

line_46_index = tk.Label(scrollframe)
line_46_index["bg"] = "#adafae"
line_46_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_46_index["font"] = ft
line_46_index["justify"] = "left"
line_46_index["anchor"] = "w"
line_46_index.place(x=20, y=2005, width=150, height=33)

line_46_name = tk.Label(scrollframe)
line_46_name["bg"] = "#adafae"
line_46_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_46_name["font"] = ft
line_46_name["justify"] = "left"
line_46_name["anchor"] = "w"
line_46_name.place(x=250, y=2005, width=500, height=33)

line_46_duration = tk.Label(scrollframe)
line_46_duration["bg"] = "#adafae"
line_46_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_46_duration["font"] = ft
line_46_duration["justify"] = "right"
line_46_duration["anchor"] = "e"
line_46_duration.place(x=910, y=2005, width=150, height=33)

line_46_live = tk.Label(scrollframe)
line_46_live["bg"] = "#adafae"
line_46_live["fg"] = "red"
line_46_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_46_live["font"] = ftl
line_46_live["justify"] = "left"
line_46_live["anchor"] = "w"
line_46_live["relief"] = "flat"
line_46_live.place(x=800, y=2005, width=70, height=33)

line_46_disabled = tk.Label(scrollframe)
line_46_disabled["bg"] = "#adafae"
line_46_disabled["fg"] = "red"
line_46_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_46_disabled["font"] = ftl
line_46_disabled["justify"] = "left"
line_46_disabled["anchor"] = "w"
line_46_disabled["relief"] = "flat"
line_46_disabled.place(x=650, y=2005, width=150, height=33)

line_47_frame = tk.Label(scrollframe)
line_47_frame["bg"] = "#adafae"
line_47_frame["text"] = ""
line_47_frame["relief"] = "sunken"
line_47_frame.place(x=10, y=2040, width=1060, height=40)

line_47_index = tk.Label(scrollframe)
line_47_index["bg"] = "#adafae"
line_47_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_47_index["font"] = ft
line_47_index["justify"] = "left"
line_47_index["anchor"] = "w"
line_47_index.place(x=20, y=2045, width=150, height=33)

line_47_name = tk.Label(scrollframe)
line_47_name["bg"] = "#adafae"
line_47_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_47_name["font"] = ft
line_47_name["justify"] = "left"
line_47_name["anchor"] = "w"
line_47_name.place(x=250, y=2045, width=500, height=33)

line_47_duration = tk.Label(scrollframe)
line_47_duration["bg"] = "#adafae"
line_47_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_47_duration["font"] = ft
line_47_duration["justify"] = "right"
line_47_duration["anchor"] = "e"
line_47_duration.place(x=910, y=2045, width=150, height=33)

line_47_live = tk.Label(scrollframe)
line_47_live["bg"] = "#adafae"
line_47_live["fg"] = "red"
line_47_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_47_live["font"] = ftl
line_47_live["justify"] = "left"
line_47_live["anchor"] = "w"
line_47_live["relief"] = "flat"
line_47_live.place(x=800, y=2045, width=70, height=33)

line_47_disabled = tk.Label(scrollframe)
line_47_disabled["bg"] = "#adafae"
line_47_disabled["fg"] = "red"
line_47_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_47_disabled["font"] = ftl
line_47_disabled["justify"] = "left"
line_47_disabled["anchor"] = "w"
line_47_disabled["relief"] = "flat"
line_47_disabled.place(x=650, y=2045, width=150, height=33)

line_48_frame = tk.Label(scrollframe)
line_48_frame["bg"] = "#adafae"
line_48_frame["text"] = ""
line_48_frame["relief"] = "sunken"
line_48_frame.place(x=10, y=2080, width=1060, height=40)

line_48_index = tk.Label(scrollframe)
line_48_index["bg"] = "#adafae"
line_48_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_48_index["font"] = ft
line_48_index["justify"] = "left"
line_48_index["anchor"] = "w"
line_48_index.place(x=20, y=2085, width=150, height=33)

line_48_name = tk.Label(scrollframe)
line_48_name["bg"] = "#adafae"
line_48_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_48_name["font"] = ft
line_48_name["justify"] = "left"
line_48_name["anchor"] = "w"
line_48_name.place(x=250, y=2085, width=500, height=33)

line_48_duration = tk.Label(scrollframe)
line_48_duration["bg"] = "#adafae"
line_48_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_48_duration["font"] = ft
line_48_duration["justify"] = "right"
line_48_duration["anchor"] = "e"
line_48_duration.place(x=910, y=2085, width=150, height=33)

line_48_live = tk.Label(scrollframe)
line_48_live["bg"] = "#adafae"
line_48_live["fg"] = "red"
line_48_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_48_live["font"] = ftl
line_48_live["justify"] = "left"
line_48_live["anchor"] = "w"
line_48_live["relief"] = "flat"
line_48_live.place(x=800, y=2085, width=70, height=33)

line_48_disabled = tk.Label(scrollframe)
line_48_disabled["bg"] = "#adafae"
line_48_disabled["fg"] = "red"
line_48_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_48_disabled["font"] = ftl
line_48_disabled["justify"] = "left"
line_48_disabled["anchor"] = "w"
line_48_disabled["relief"] = "flat"
line_48_disabled.place(x=650, y=2085, width=150, height=33)

line_49_frame = tk.Label(scrollframe)
line_49_frame["bg"] = "#adafae"
line_49_frame["text"] = ""
line_49_frame["relief"] = "sunken"
line_49_frame.place(x=10, y=2120, width=1060, height=40)

line_49_index = tk.Label(scrollframe)
line_49_index["bg"] = "#adafae"
line_49_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_49_index["font"] = ft
line_49_index["justify"] = "left"
line_49_index["anchor"] = "w"
line_49_index.place(x=20, y=2125, width=150, height=33)

line_49_name = tk.Label(scrollframe)
line_49_name["bg"] = "#adafae"
line_49_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_49_name["font"] = ft
line_49_name["justify"] = "left"
line_49_name["anchor"] = "w"
line_49_name.place(x=250, y=2125, width=500, height=33)

line_49_duration = tk.Label(scrollframe)
line_49_duration["bg"] = "#adafae"
line_49_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_49_duration["font"] = ft
line_49_duration["justify"] = "right"
line_49_duration["anchor"] = "e"
line_49_duration.place(x=910, y=2125, width=150, height=33)

line_49_live = tk.Label(scrollframe)
line_49_live["bg"] = "#adafae"
line_49_live["fg"] = "red"
line_49_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_49_live["font"] = ftl
line_49_live["justify"] = "left"
line_49_live["anchor"] = "w"
line_49_live["relief"] = "flat"
line_49_live.place(x=800, y=2125, width=70, height=33)

line_49_disabled = tk.Label(scrollframe)
line_49_disabled["bg"] = "#adafae"
line_49_disabled["fg"] = "red"
line_49_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_49_disabled["font"] = ftl
line_49_disabled["justify"] = "left"
line_49_disabled["anchor"] = "w"
line_49_disabled["relief"] = "flat"
line_49_disabled.place(x=650, y=2125, width=150, height=33)

line_50_frame = tk.Label(scrollframe)
line_50_frame["bg"] = "#adafae"
line_50_frame["text"] = ""
line_50_frame["relief"] = "sunken"
line_50_frame.place(x=10, y=2160, width=1060, height=40)

line_50_index = tk.Label(scrollframe)
line_50_index["bg"] = "#adafae"
line_50_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_50_index["font"] = ft
line_50_index["justify"] = "left"
line_50_index["anchor"] = "w"
line_50_index.place(x=20, y=2165, width=150, height=33)

line_50_name = tk.Label(scrollframe)
line_50_name["bg"] = "#adafae"
line_50_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_50_name["font"] = ft
line_50_name["justify"] = "left"
line_50_name["anchor"] = "w"
line_50_name.place(x=250, y=2165, width=500, height=33)

line_50_duration = tk.Label(scrollframe)
line_50_duration["bg"] = "#adafae"
line_50_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_50_duration["font"] = ft
line_50_duration["justify"] = "right"
line_50_duration["anchor"] = "e"
line_50_duration.place(x=910, y=2165, width=150, height=33)

line_50_live = tk.Label(scrollframe)
line_50_live["bg"] = "#adafae"
line_50_live["fg"] = "red"
line_50_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_50_live["font"] = ftl
line_50_live["justify"] = "left"
line_50_live["anchor"] = "w"
line_50_live["relief"] = "flat"
line_50_live.place(x=800, y=2165, width=70, height=33)

line_50_disabled = tk.Label(scrollframe)
line_50_disabled["bg"] = "#adafae"
line_50_disabled["fg"] = "red"
line_50_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_50_disabled["font"] = ftl
line_50_disabled["justify"] = "left"
line_50_disabled["anchor"] = "w"
line_50_disabled["relief"] = "flat"
line_50_disabled.place(x=650, y=2165, width=150, height=33)

line_51_frame = tk.Label(scrollframe)
line_51_frame["bg"] = "#adafae"
line_51_frame["text"] = ""
line_51_frame["relief"] = "sunken"
line_51_frame.place(x=10, y=2200, width=1060, height=40)

line_51_index = tk.Label(scrollframe)
line_51_index["bg"] = "#adafae"
line_51_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_51_index["font"] = ft
line_51_index["justify"] = "left"
line_51_index["anchor"] = "w"
line_51_index.place(x=20, y=2205, width=150, height=33)

line_51_name = tk.Label(scrollframe)
line_51_name["bg"] = "#adafae"
line_51_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_51_name["font"] = ft
line_51_name["justify"] = "left"
line_51_name["anchor"] = "w"
line_51_name.place(x=250, y=2205, width=500, height=33)

line_51_duration = tk.Label(scrollframe)
line_51_duration["bg"] = "#adafae"
line_51_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_51_duration["font"] = ft
line_51_duration["justify"] = "right"
line_51_duration["anchor"] = "e"
line_51_duration.place(x=910, y=2205, width=150, height=33)

line_51_live = tk.Label(scrollframe)
line_51_live["bg"] = "#adafae"
line_51_live["fg"] = "red"
line_51_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_51_live["font"] = ftl
line_51_live["justify"] = "left"
line_51_live["anchor"] = "w"
line_51_live["relief"] = "flat"
line_51_live.place(x=800, y=2205, width=70, height=33)

line_51_disabled = tk.Label(scrollframe)
line_51_disabled["bg"] = "#adafae"
line_51_disabled["fg"] = "red"
line_51_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_51_disabled["font"] = ftl
line_51_disabled["justify"] = "left"
line_51_disabled["anchor"] = "w"
line_51_disabled["relief"] = "flat"
line_51_disabled.place(x=650, y=2205, width=150, height=33)

line_52_frame = tk.Label(scrollframe)
line_52_frame["bg"] = "#adafae"
line_52_frame["text"] = ""
line_52_frame["relief"] = "sunken"
line_52_frame.place(x=10, y=2240, width=1060, height=40)

line_52_index = tk.Label(scrollframe)
line_52_index["bg"] = "#adafae"
line_52_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_52_index["font"] = ft
line_52_index["justify"] = "left"
line_52_index["anchor"] = "w"
line_52_index.place(x=20, y=2245, width=150, height=33)

line_52_name = tk.Label(scrollframe)
line_52_name["bg"] = "#adafae"
line_52_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_52_name["font"] = ft
line_52_name["justify"] = "left"
line_52_name["anchor"] = "w"
line_52_name.place(x=250, y=2245, width=500, height=33)

line_52_duration = tk.Label(scrollframe)
line_52_duration["bg"] = "#adafae"
line_52_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_52_duration["font"] = ft
line_52_duration["justify"] = "right"
line_52_duration["anchor"] = "e"
line_52_duration.place(x=910, y=2245, width=150, height=33)

line_52_live = tk.Label(scrollframe)
line_52_live["bg"] = "#adafae"
line_52_live["fg"] = "red"
line_52_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_52_live["font"] = ftl
line_52_live["justify"] = "left"
line_52_live["anchor"] = "w"
line_52_live["relief"] = "flat"
line_52_live.place(x=800, y=2245, width=70, height=33)

line_52_disabled = tk.Label(scrollframe)
line_52_disabled["bg"] = "#adafae"
line_52_disabled["fg"] = "red"
line_52_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_52_disabled["font"] = ftl
line_52_disabled["justify"] = "left"
line_52_disabled["anchor"] = "w"
line_52_disabled["relief"] = "flat"
line_52_disabled.place(x=650, y=2245, width=150, height=33)

line_53_frame = tk.Label(scrollframe)
line_53_frame["bg"] = "#adafae"
line_53_frame["text"] = ""
line_53_frame["relief"] = "sunken"
line_53_frame.place(x=10, y=2280, width=1060, height=40)

line_53_index = tk.Label(scrollframe)
line_53_index["bg"] = "#adafae"
line_53_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_53_index["font"] = ft
line_53_index["justify"] = "left"
line_53_index["anchor"] = "w"
line_53_index.place(x=20, y=2285, width=150, height=33)

line_53_name = tk.Label(scrollframe)
line_53_name["bg"] = "#adafae"
line_53_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_53_name["font"] = ft
line_53_name["justify"] = "left"
line_53_name["anchor"] = "w"
line_53_name.place(x=250, y=2285, width=500, height=33)

line_53_duration = tk.Label(scrollframe)
line_53_duration["bg"] = "#adafae"
line_53_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_53_duration["font"] = ft
line_53_duration["justify"] = "right"
line_53_duration["anchor"] = "e"
line_53_duration.place(x=910, y=2285, width=150, height=33)

line_53_live = tk.Label(scrollframe)
line_53_live["bg"] = "#adafae"
line_53_live["fg"] = "red"
line_53_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_53_live["font"] = ftl
line_53_live["justify"] = "left"
line_53_live["anchor"] = "w"
line_53_live["relief"] = "flat"
line_53_live.place(x=800, y=2285, width=70, height=33)

line_53_disabled = tk.Label(scrollframe)
line_53_disabled["bg"] = "#adafae"
line_53_disabled["fg"] = "red"
line_53_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_53_disabled["font"] = ftl
line_53_disabled["justify"] = "left"
line_53_disabled["anchor"] = "w"
line_53_disabled["relief"] = "flat"
line_53_disabled.place(x=650, y=2285, width=150, height=33)

line_54_frame = tk.Label(scrollframe)
line_54_frame["bg"] = "#adafae"
line_54_frame["text"] = ""
line_54_frame["relief"] = "sunken"
line_54_frame.place(x=10, y=2320, width=1060, height=40)

line_54_index = tk.Label(scrollframe)
line_54_index["bg"] = "#adafae"
line_54_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_54_index["font"] = ft
line_54_index["justify"] = "left"
line_54_index["anchor"] = "w"
line_54_index.place(x=20, y=2325, width=150, height=33)

line_54_name = tk.Label(scrollframe)
line_54_name["bg"] = "#adafae"
line_54_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_54_name["font"] = ft
line_54_name["justify"] = "left"
line_54_name["anchor"] = "w"
line_54_name.place(x=250, y=2325, width=500, height=33)

line_54_duration = tk.Label(scrollframe)
line_54_duration["bg"] = "#adafae"
line_54_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_54_duration["font"] = ft
line_54_duration["justify"] = "right"
line_54_duration["anchor"] = "e"
line_54_duration.place(x=910, y=2325, width=150, height=33)

line_54_live = tk.Label(scrollframe)
line_54_live["bg"] = "#adafae"
line_54_live["fg"] = "red"
line_54_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_54_live["font"] = ftl
line_54_live["justify"] = "left"
line_54_live["anchor"] = "w"
line_54_live["relief"] = "flat"
line_54_live.place(x=800, y=2325, width=70, height=33)

line_54_disabled = tk.Label(scrollframe)
line_54_disabled["bg"] = "#adafae"
line_54_disabled["fg"] = "red"
line_54_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_54_disabled["font"] = ftl
line_54_disabled["justify"] = "left"
line_54_disabled["anchor"] = "w"
line_54_disabled["relief"] = "flat"
line_54_disabled.place(x=650, y=2325, width=150, height=33)

line_55_frame = tk.Label(scrollframe)
line_55_frame["bg"] = "#adafae"
line_55_frame["text"] = ""
line_55_frame["relief"] = "sunken"
line_55_frame.place(x=10, y=2360, width=1060, height=40)

line_55_index = tk.Label(scrollframe)
line_55_index["bg"] = "#adafae"
line_55_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_55_index["font"] = ft
line_55_index["justify"] = "left"
line_55_index["anchor"] = "w"
line_55_index.place(x=20, y=2365, width=150, height=33)

line_55_name = tk.Label(scrollframe)
line_55_name["bg"] = "#adafae"
line_55_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_55_name["font"] = ft
line_55_name["justify"] = "left"
line_55_name["anchor"] = "w"
line_55_name.place(x=250, y=2365, width=500, height=33)

line_55_duration = tk.Label(scrollframe)
line_55_duration["bg"] = "#adafae"
line_55_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_55_duration["font"] = ft
line_55_duration["justify"] = "right"
line_55_duration["anchor"] = "e"
line_55_duration.place(x=910, y=2365, width=150, height=33)

line_55_live = tk.Label(scrollframe)
line_55_live["bg"] = "#adafae"
line_55_live["fg"] = "red"
line_55_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_55_live["font"] = ftl
line_55_live["justify"] = "left"
line_55_live["anchor"] = "w"
line_55_live["relief"] = "flat"
line_55_live.place(x=800, y=2365, width=70, height=33)

line_55_disabled = tk.Label(scrollframe)
line_55_disabled["bg"] = "#adafae"
line_55_disabled["fg"] = "red"
line_55_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_55_disabled["font"] = ftl
line_55_disabled["justify"] = "left"
line_55_disabled["anchor"] = "w"
line_55_disabled["relief"] = "flat"
line_55_disabled.place(x=650, y=2365, width=150, height=33)

line_56_frame = tk.Label(scrollframe)
line_56_frame["bg"] = "#adafae"
line_56_frame["text"] = ""
line_56_frame["relief"] = "sunken"
line_56_frame.place(x=10, y=2400, width=1060, height=40)

line_56_index = tk.Label(scrollframe)
line_56_index["bg"] = "#adafae"
line_56_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_56_index["font"] = ft
line_56_index["justify"] = "left"
line_56_index["anchor"] = "w"
line_56_index.place(x=20, y=2405, width=150, height=33)

line_56_name = tk.Label(scrollframe)
line_56_name["bg"] = "#adafae"
line_56_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_56_name["font"] = ft
line_56_name["justify"] = "left"
line_56_name["anchor"] = "w"
line_56_name.place(x=250, y=2405, width=500, height=33)

line_56_duration = tk.Label(scrollframe)
line_56_duration["bg"] = "#adafae"
line_56_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_56_duration["font"] = ft
line_56_duration["justify"] = "right"
line_56_duration["anchor"] = "e"
line_56_duration.place(x=910, y=2405, width=150, height=33)

line_56_live = tk.Label(scrollframe)
line_56_live["bg"] = "#adafae"
line_56_live["fg"] = "red"
line_56_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_56_live["font"] = ftl
line_56_live["justify"] = "left"
line_56_live["anchor"] = "w"
line_56_live["relief"] = "flat"
line_56_live.place(x=800, y=2405, width=70, height=33)

line_56_disabled = tk.Label(scrollframe)
line_56_disabled["bg"] = "#adafae"
line_56_disabled["fg"] = "red"
line_56_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_56_disabled["font"] = ftl
line_56_disabled["justify"] = "left"
line_56_disabled["anchor"] = "w"
line_56_disabled["relief"] = "flat"
line_56_disabled.place(x=650, y=2405, width=150, height=33)

line_57_frame = tk.Label(scrollframe)
line_57_frame["bg"] = "#adafae"
line_57_frame["text"] = ""
line_57_frame["relief"] = "sunken"
line_57_frame.place(x=10, y=2440, width=1060, height=40)

line_57_index = tk.Label(scrollframe)
line_57_index["bg"] = "#adafae"
line_57_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_57_index["font"] = ft
line_57_index["justify"] = "left"
line_57_index["anchor"] = "w"
line_57_index.place(x=20, y=2445, width=150, height=33)

line_57_name = tk.Label(scrollframe)
line_57_name["bg"] = "#adafae"
line_57_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_57_name["font"] = ft
line_57_name["justify"] = "left"
line_57_name["anchor"] = "w"
line_57_name.place(x=250, y=2445, width=500, height=33)

line_57_duration = tk.Label(scrollframe)
line_57_duration["bg"] = "#adafae"
line_57_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_57_duration["font"] = ft
line_57_duration["justify"] = "right"
line_57_duration["anchor"] = "e"
line_57_duration.place(x=910, y=2445, width=150, height=33)

line_57_live = tk.Label(scrollframe)
line_57_live["bg"] = "#adafae"
line_57_live["fg"] = "red"
line_57_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_57_live["font"] = ftl
line_57_live["justify"] = "left"
line_57_live["anchor"] = "w"
line_57_live["relief"] = "flat"
line_57_live.place(x=800, y=2445, width=70, height=33)

line_57_disabled = tk.Label(scrollframe)
line_57_disabled["bg"] = "#adafae"
line_57_disabled["fg"] = "red"
line_57_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_57_disabled["font"] = ftl
line_57_disabled["justify"] = "left"
line_57_disabled["anchor"] = "w"
line_57_disabled["relief"] = "flat"
line_57_disabled.place(x=650, y=2445, width=150, height=33)

line_58_frame = tk.Label(scrollframe)
line_58_frame["bg"] = "#adafae"
line_58_frame["text"] = ""
line_58_frame["relief"] = "sunken"
line_58_frame.place(x=10, y=2480, width=1060, height=40)

line_58_index = tk.Label(scrollframe)
line_58_index["bg"] = "#adafae"
line_58_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_58_index["font"] = ft
line_58_index["justify"] = "left"
line_58_index["anchor"] = "w"
line_58_index.place(x=20, y=2485, width=150, height=33)

line_58_name = tk.Label(scrollframe)
line_58_name["bg"] = "#adafae"
line_58_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_58_name["font"] = ft
line_58_name["justify"] = "left"
line_58_name["anchor"] = "w"
line_58_name.place(x=250, y=2485, width=500, height=33)

line_58_duration = tk.Label(scrollframe)
line_58_duration["bg"] = "#adafae"
line_58_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_58_duration["font"] = ft
line_58_duration["justify"] = "right"
line_58_duration["anchor"] = "e"
line_58_duration.place(x=910, y=2485, width=150, height=33)

line_58_live = tk.Label(scrollframe)
line_58_live["bg"] = "#adafae"
line_58_live["fg"] = "red"
line_58_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_58_live["font"] = ftl
line_58_live["justify"] = "left"
line_58_live["anchor"] = "w"
line_58_live["relief"] = "flat"
line_58_live.place(x=800, y=2485, width=70, height=33)

line_58_disabled = tk.Label(scrollframe)
line_58_disabled["bg"] = "#adafae"
line_58_disabled["fg"] = "red"
line_58_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_58_disabled["font"] = ftl
line_58_disabled["justify"] = "left"
line_58_disabled["anchor"] = "w"
line_58_disabled["relief"] = "flat"
line_58_disabled.place(x=650, y=2485, width=150, height=33)

line_59_frame = tk.Label(scrollframe)
line_59_frame["bg"] = "#adafae"
line_59_frame["text"] = ""
line_59_frame["relief"] = "sunken"
line_59_frame.place(x=10, y=2520, width=1060, height=40)

line_59_index = tk.Label(scrollframe)
line_59_index["bg"] = "#adafae"
line_59_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_59_index["font"] = ft
line_59_index["justify"] = "left"
line_59_index["anchor"] = "w"
line_59_index.place(x=20, y=2525, width=150, height=33)

line_59_name = tk.Label(scrollframe)
line_59_name["bg"] = "#adafae"
line_59_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_59_name["font"] = ft
line_59_name["justify"] = "left"
line_59_name["anchor"] = "w"
line_59_name.place(x=250, y=2525, width=500, height=33)

line_59_duration = tk.Label(scrollframe)
line_59_duration["bg"] = "#adafae"
line_59_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_59_duration["font"] = ft
line_59_duration["justify"] = "right"
line_59_duration["anchor"] = "e"
line_59_duration.place(x=910, y=2525, width=150, height=33)

line_59_live = tk.Label(scrollframe)
line_59_live["bg"] = "#adafae"
line_59_live["fg"] = "red"
line_59_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_59_live["font"] = ftl
line_59_live["justify"] = "left"
line_59_live["anchor"] = "w"
line_59_live["relief"] = "flat"
line_59_live.place(x=800, y=2525, width=70, height=33)

line_59_disabled = tk.Label(scrollframe)
line_59_disabled["bg"] = "#adafae"
line_59_disabled["fg"] = "red"
line_59_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_59_disabled["font"] = ftl
line_59_disabled["justify"] = "left"
line_59_disabled["anchor"] = "w"
line_59_disabled["relief"] = "flat"
line_59_disabled.place(x=650, y=2525, width=150, height=33)

line_60_frame = tk.Label(scrollframe)
line_60_frame["bg"] = "#adafae"
line_60_frame["text"] = ""
line_60_frame["relief"] = "sunken"
line_60_frame.place(x=10, y=2560, width=1060, height=40)

line_60_index = tk.Label(scrollframe)
line_60_index["bg"] = "#adafae"
line_60_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_60_index["font"] = ft
line_60_index["justify"] = "left"
line_60_index["anchor"] = "w"
line_60_index.place(x=20, y=2565, width=150, height=33)

line_60_name = tk.Label(scrollframe)
line_60_name["bg"] = "#adafae"
line_60_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_60_name["font"] = ft
line_60_name["justify"] = "left"
line_60_name["anchor"] = "w"
line_60_name.place(x=250, y=2565, width=500, height=33)

line_60_duration = tk.Label(scrollframe)
line_60_duration["bg"] = "#adafae"
line_60_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_60_duration["font"] = ft
line_60_duration["justify"] = "right"
line_60_duration["anchor"] = "e"
line_60_duration.place(x=910, y=2565, width=150, height=33)

line_60_live = tk.Label(scrollframe)
line_60_live["bg"] = "#adafae"
line_60_live["fg"] = "red"
line_60_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_60_live["font"] = ftl
line_60_live["justify"] = "left"
line_60_live["anchor"] = "w"
line_60_live["relief"] = "flat"
line_60_live.place(x=800, y=2565, width=70, height=33)

line_60_disabled = tk.Label(scrollframe)
line_60_disabled["bg"] = "#adafae"
line_60_disabled["fg"] = "red"
line_60_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_60_disabled["font"] = ftl
line_60_disabled["justify"] = "left"
line_60_disabled["anchor"] = "w"
line_60_disabled["relief"] = "flat"
line_60_disabled.place(x=650, y=2565, width=150, height=33)

line_61_frame = tk.Label(scrollframe)
line_61_frame["bg"] = "#adafae"
line_61_frame["text"] = ""
line_61_frame["relief"] = "sunken"
line_61_frame.place(x=10, y=2600, width=1060, height=40)

line_61_index = tk.Label(scrollframe)
line_61_index["bg"] = "#adafae"
line_61_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_61_index["font"] = ft
line_61_index["justify"] = "left"
line_61_index["anchor"] = "w"
line_61_index.place(x=20, y=2605, width=150, height=33)

line_61_name = tk.Label(scrollframe)
line_61_name["bg"] = "#adafae"
line_61_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_61_name["font"] = ft
line_61_name["justify"] = "left"
line_61_name["anchor"] = "w"
line_61_name.place(x=250, y=2605, width=500, height=33)

line_61_duration = tk.Label(scrollframe)
line_61_duration["bg"] = "#adafae"
line_61_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_61_duration["font"] = ft
line_61_duration["justify"] = "right"
line_61_duration["anchor"] = "e"
line_61_duration.place(x=910, y=2605, width=150, height=33)

line_61_live = tk.Label(scrollframe)
line_61_live["bg"] = "#adafae"
line_61_live["fg"] = "red"
line_61_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_61_live["font"] = ftl
line_61_live["justify"] = "left"
line_61_live["anchor"] = "w"
line_61_live["relief"] = "flat"
line_61_live.place(x=800, y=2605, width=70, height=33)

line_61_disabled = tk.Label(scrollframe)
line_61_disabled["bg"] = "#adafae"
line_61_disabled["fg"] = "red"
line_61_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_61_disabled["font"] = ftl
line_61_disabled["justify"] = "left"
line_61_disabled["anchor"] = "w"
line_61_disabled["relief"] = "flat"
line_61_disabled.place(x=650, y=2605, width=150, height=33)

line_62_frame = tk.Label(scrollframe)
line_62_frame["bg"] = "#adafae"
line_62_frame["text"] = ""
line_62_frame["relief"] = "sunken"
line_62_frame.place(x=10, y=2640, width=1060, height=40)

line_62_index = tk.Label(scrollframe)
line_62_index["bg"] = "#adafae"
line_62_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_62_index["font"] = ft
line_62_index["justify"] = "left"
line_62_index["anchor"] = "w"
line_62_index.place(x=20, y=2645, width=150, height=33)

line_62_name = tk.Label(scrollframe)
line_62_name["bg"] = "#adafae"
line_62_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_62_name["font"] = ft
line_62_name["justify"] = "left"
line_62_name["anchor"] = "w"
line_62_name.place(x=250, y=2645, width=500, height=33)

line_62_duration = tk.Label(scrollframe)
line_62_duration["bg"] = "#adafae"
line_62_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_62_duration["font"] = ft
line_62_duration["justify"] = "right"
line_62_duration["anchor"] = "e"
line_62_duration.place(x=910, y=2645, width=150, height=33)

line_62_live = tk.Label(scrollframe)
line_62_live["bg"] = "#adafae"
line_62_live["fg"] = "red"
line_62_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_62_live["font"] = ftl
line_62_live["justify"] = "left"
line_62_live["anchor"] = "w"
line_62_live["relief"] = "flat"
line_62_live.place(x=800, y=2645, width=70, height=33)

line_62_disabled = tk.Label(scrollframe)
line_62_disabled["bg"] = "#adafae"
line_62_disabled["fg"] = "red"
line_62_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_62_disabled["font"] = ftl
line_62_disabled["justify"] = "left"
line_62_disabled["anchor"] = "w"
line_62_disabled["relief"] = "flat"
line_62_disabled.place(x=650, y=2645, width=150, height=33)

line_63_frame = tk.Label(scrollframe)
line_63_frame["bg"] = "#adafae"
line_63_frame["text"] = ""
line_63_frame["relief"] = "sunken"
line_63_frame.place(x=10, y=2680, width=1060, height=40)

line_63_index = tk.Label(scrollframe)
line_63_index["bg"] = "#adafae"
line_63_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_63_index["font"] = ft
line_63_index["justify"] = "left"
line_63_index["anchor"] = "w"
line_63_index.place(x=20, y=2685, width=150, height=33)

line_63_name = tk.Label(scrollframe)
line_63_name["bg"] = "#adafae"
line_63_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_63_name["font"] = ft
line_63_name["justify"] = "left"
line_63_name["anchor"] = "w"
line_63_name.place(x=250, y=2685, width=500, height=33)

line_63_duration = tk.Label(scrollframe)
line_63_duration["bg"] = "#adafae"
line_63_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_63_duration["font"] = ft
line_63_duration["justify"] = "right"
line_63_duration["anchor"] = "e"
line_63_duration.place(x=910, y=2685, width=150, height=33)

line_63_live = tk.Label(scrollframe)
line_63_live["bg"] = "#adafae"
line_63_live["fg"] = "red"
line_63_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_63_live["font"] = ftl
line_63_live["justify"] = "left"
line_63_live["anchor"] = "w"
line_63_live["relief"] = "flat"
line_63_live.place(x=800, y=2685, width=70, height=33)

line_63_disabled = tk.Label(scrollframe)
line_63_disabled["bg"] = "#adafae"
line_63_disabled["fg"] = "red"
line_63_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_63_disabled["font"] = ftl
line_63_disabled["justify"] = "left"
line_63_disabled["anchor"] = "w"
line_63_disabled["relief"] = "flat"
line_63_disabled.place(x=650, y=2685, width=150, height=33)

line_64_frame = tk.Label(scrollframe)
line_64_frame["bg"] = "#adafae"
line_64_frame["text"] = ""
line_64_frame["relief"] = "sunken"
line_64_frame.place(x=10, y=2720, width=1060, height=40)

line_64_index = tk.Label(scrollframe)
line_64_index["bg"] = "#adafae"
line_64_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_64_index["font"] = ft
line_64_index["justify"] = "left"
line_64_index["anchor"] = "w"
line_64_index.place(x=20, y=2725, width=150, height=33)

line_64_name = tk.Label(scrollframe)
line_64_name["bg"] = "#adafae"
line_64_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_64_name["font"] = ft
line_64_name["justify"] = "left"
line_64_name["anchor"] = "w"
line_64_name.place(x=250, y=2725, width=500, height=33)

line_64_duration = tk.Label(scrollframe)
line_64_duration["bg"] = "#adafae"
line_64_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_64_duration["font"] = ft
line_64_duration["justify"] = "right"
line_64_duration["anchor"] = "e"
line_64_duration.place(x=910, y=2725, width=150, height=33)

line_64_live = tk.Label(scrollframe)
line_64_live["bg"] = "#adafae"
line_64_live["fg"] = "red"
line_64_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_64_live["font"] = ftl
line_64_live["justify"] = "left"
line_64_live["anchor"] = "w"
line_64_live["relief"] = "flat"
line_64_live.place(x=800, y=2725, width=70, height=33)

line_64_disabled = tk.Label(scrollframe)
line_64_disabled["bg"] = "#adafae"
line_64_disabled["fg"] = "red"
line_64_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_64_disabled["font"] = ftl
line_64_disabled["justify"] = "left"
line_64_disabled["anchor"] = "w"
line_64_disabled["relief"] = "flat"
line_64_disabled.place(x=650, y=2725, width=150, height=33)

line_65_frame = tk.Label(scrollframe)
line_65_frame["bg"] = "#adafae"
line_65_frame["text"] = ""
line_65_frame["relief"] = "sunken"
line_65_frame.place(x=10, y=2760, width=1060, height=40)

line_65_index = tk.Label(scrollframe)
line_65_index["bg"] = "#adafae"
line_65_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_65_index["font"] = ft
line_65_index["justify"] = "left"
line_65_index["anchor"] = "w"
line_65_index.place(x=20, y=2765, width=150, height=33)

line_65_name = tk.Label(scrollframe)
line_65_name["bg"] = "#adafae"
line_65_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_65_name["font"] = ft
line_65_name["justify"] = "left"
line_65_name["anchor"] = "w"
line_65_name.place(x=250, y=2765, width=500, height=33)

line_65_duration = tk.Label(scrollframe)
line_65_duration["bg"] = "#adafae"
line_65_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_65_duration["font"] = ft
line_65_duration["justify"] = "right"
line_65_duration["anchor"] = "e"
line_65_duration.place(x=910, y=2765, width=150, height=33)

line_65_live = tk.Label(scrollframe)
line_65_live["bg"] = "#adafae"
line_65_live["fg"] = "red"
line_65_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_65_live["font"] = ftl
line_65_live["justify"] = "left"
line_65_live["anchor"] = "w"
line_65_live["relief"] = "flat"
line_65_live.place(x=800, y=2765, width=70, height=33)

line_65_disabled = tk.Label(scrollframe)
line_65_disabled["bg"] = "#adafae"
line_65_disabled["fg"] = "red"
line_65_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_65_disabled["font"] = ftl
line_65_disabled["justify"] = "left"
line_65_disabled["anchor"] = "w"
line_65_disabled["relief"] = "flat"
line_65_disabled.place(x=650, y=2765, width=150, height=33)

line_66_frame = tk.Label(scrollframe)
line_66_frame["bg"] = "#adafae"
line_66_frame["text"] = ""
line_66_frame["relief"] = "sunken"
line_66_frame.place(x=10, y=2800, width=1060, height=40)

line_66_index = tk.Label(scrollframe)
line_66_index["bg"] = "#adafae"
line_66_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_66_index["font"] = ft
line_66_index["justify"] = "left"
line_66_index["anchor"] = "w"
line_66_index.place(x=20, y=2805, width=150, height=33)

line_66_name = tk.Label(scrollframe)
line_66_name["bg"] = "#adafae"
line_66_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_66_name["font"] = ft
line_66_name["justify"] = "left"
line_66_name["anchor"] = "w"
line_66_name.place(x=250, y=2805, width=500, height=33)

line_66_duration = tk.Label(scrollframe)
line_66_duration["bg"] = "#adafae"
line_66_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_66_duration["font"] = ft
line_66_duration["justify"] = "right"
line_66_duration["anchor"] = "e"
line_66_duration.place(x=910, y=2805, width=150, height=33)

line_66_live = tk.Label(scrollframe)
line_66_live["bg"] = "#adafae"
line_66_live["fg"] = "red"
line_66_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_66_live["font"] = ftl
line_66_live["justify"] = "left"
line_66_live["anchor"] = "w"
line_66_live["relief"] = "flat"
line_66_live.place(x=800, y=2805, width=70, height=33)

line_66_disabled = tk.Label(scrollframe)
line_66_disabled["bg"] = "#adafae"
line_66_disabled["fg"] = "red"
line_66_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_66_disabled["font"] = ftl
line_66_disabled["justify"] = "left"
line_66_disabled["anchor"] = "w"
line_66_disabled["relief"] = "flat"
line_66_disabled.place(x=650, y=2805, width=150, height=33)

line_67_frame = tk.Label(scrollframe)
line_67_frame["bg"] = "#adafae"
line_67_frame["text"] = ""
line_67_frame["relief"] = "sunken"
line_67_frame.place(x=10, y=2840, width=1060, height=40)

line_67_index = tk.Label(scrollframe)
line_67_index["bg"] = "#adafae"
line_67_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_67_index["font"] = ft
line_67_index["justify"] = "left"
line_67_index["anchor"] = "w"
line_67_index.place(x=20, y=2845, width=150, height=33)

line_67_name = tk.Label(scrollframe)
line_67_name["bg"] = "#adafae"
line_67_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_67_name["font"] = ft
line_67_name["justify"] = "left"
line_67_name["anchor"] = "w"
line_67_name.place(x=250, y=2845, width=500, height=33)

line_67_duration = tk.Label(scrollframe)
line_67_duration["bg"] = "#adafae"
line_67_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_67_duration["font"] = ft
line_67_duration["justify"] = "right"
line_67_duration["anchor"] = "e"
line_67_duration.place(x=910, y=2845, width=150, height=33)

line_67_live = tk.Label(scrollframe)
line_67_live["bg"] = "#adafae"
line_67_live["fg"] = "red"
line_67_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_67_live["font"] = ftl
line_67_live["justify"] = "left"
line_67_live["anchor"] = "w"
line_67_live["relief"] = "flat"
line_67_live.place(x=800, y=2845, width=70, height=33)

line_67_disabled = tk.Label(scrollframe)
line_67_disabled["bg"] = "#adafae"
line_67_disabled["fg"] = "red"
line_67_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_67_disabled["font"] = ftl
line_67_disabled["justify"] = "left"
line_67_disabled["anchor"] = "w"
line_67_disabled["relief"] = "flat"
line_67_disabled.place(x=650, y=2845, width=150, height=33)

line_68_frame = tk.Label(scrollframe)
line_68_frame["bg"] = "#adafae"
line_68_frame["text"] = ""
line_68_frame["relief"] = "sunken"
line_68_frame.place(x=10, y=2880, width=1060, height=40)

line_68_index = tk.Label(scrollframe)
line_68_index["bg"] = "#adafae"
line_68_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_68_index["font"] = ft
line_68_index["justify"] = "left"
line_68_index["anchor"] = "w"
line_68_index.place(x=20, y=2885, width=150, height=33)

line_68_name = tk.Label(scrollframe)
line_68_name["bg"] = "#adafae"
line_68_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_68_name["font"] = ft
line_68_name["justify"] = "left"
line_68_name["anchor"] = "w"
line_68_name.place(x=250, y=2885, width=500, height=33)

line_68_duration = tk.Label(scrollframe)
line_68_duration["bg"] = "#adafae"
line_68_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_68_duration["font"] = ft
line_68_duration["justify"] = "right"
line_68_duration["anchor"] = "e"
line_68_duration.place(x=910, y=2885, width=150, height=33)

line_68_live = tk.Label(scrollframe)
line_68_live["bg"] = "#adafae"
line_68_live["fg"] = "red"
line_68_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_68_live["font"] = ftl
line_68_live["justify"] = "left"
line_68_live["anchor"] = "w"
line_68_live["relief"] = "flat"
line_68_live.place(x=800, y=2885, width=70, height=33)

line_68_disabled = tk.Label(scrollframe)
line_68_disabled["bg"] = "#adafae"
line_68_disabled["fg"] = "red"
line_68_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_68_disabled["font"] = ftl
line_68_disabled["justify"] = "left"
line_68_disabled["anchor"] = "w"
line_68_disabled["relief"] = "flat"
line_68_disabled.place(x=650, y=2885, width=150, height=33)

line_69_frame = tk.Label(scrollframe)
line_69_frame["bg"] = "#adafae"
line_69_frame["text"] = ""
line_69_frame["relief"] = "sunken"
line_69_frame.place(x=10, y=2920, width=1060, height=40)

line_69_index = tk.Label(scrollframe)
line_69_index["bg"] = "#adafae"
line_69_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_69_index["font"] = ft
line_69_index["justify"] = "left"
line_69_index["anchor"] = "w"
line_69_index.place(x=20, y=2925, width=150, height=33)

line_69_name = tk.Label(scrollframe)
line_69_name["bg"] = "#adafae"
line_69_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_69_name["font"] = ft
line_69_name["justify"] = "left"
line_69_name["anchor"] = "w"
line_69_name.place(x=250, y=2925, width=500, height=33)

line_69_duration = tk.Label(scrollframe)
line_69_duration["bg"] = "#adafae"
line_69_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_69_duration["font"] = ft
line_69_duration["justify"] = "right"
line_69_duration["anchor"] = "e"
line_69_duration.place(x=910, y=2925, width=150, height=33)

line_69_live = tk.Label(scrollframe)
line_69_live["bg"] = "#adafae"
line_69_live["fg"] = "red"
line_69_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_69_live["font"] = ftl
line_69_live["justify"] = "left"
line_69_live["anchor"] = "w"
line_69_live["relief"] = "flat"
line_69_live.place(x=800, y=2925, width=70, height=33)

line_69_disabled = tk.Label(scrollframe)
line_69_disabled["bg"] = "#adafae"
line_69_disabled["fg"] = "red"
line_69_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_69_disabled["font"] = ftl
line_69_disabled["justify"] = "left"
line_69_disabled["anchor"] = "w"
line_69_disabled["relief"] = "flat"
line_69_disabled.place(x=650, y=2925, width=150, height=33)

line_70_frame = tk.Label(scrollframe)
line_70_frame["bg"] = "#adafae"
line_70_frame["text"] = ""
line_70_frame["relief"] = "sunken"
line_70_frame.place(x=10, y=2960, width=1060, height=40)

line_70_index = tk.Label(scrollframe)
line_70_index["bg"] = "#adafae"
line_70_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_70_index["font"] = ft
line_70_index["justify"] = "left"
line_70_index["anchor"] = "w"
line_70_index.place(x=20, y=2965, width=150, height=33)

line_70_name = tk.Label(scrollframe)
line_70_name["bg"] = "#adafae"
line_70_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_70_name["font"] = ft
line_70_name["justify"] = "left"
line_70_name["anchor"] = "w"
line_70_name.place(x=250, y=2965, width=500, height=33)

line_70_duration = tk.Label(scrollframe)
line_70_duration["bg"] = "#adafae"
line_70_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_70_duration["font"] = ft
line_70_duration["justify"] = "right"
line_70_duration["anchor"] = "e"
line_70_duration.place(x=910, y=2965, width=150, height=33)

line_70_live = tk.Label(scrollframe)
line_70_live["bg"] = "#adafae"
line_70_live["fg"] = "red"
line_70_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_70_live["font"] = ftl
line_70_live["justify"] = "left"
line_70_live["anchor"] = "w"
line_70_live["relief"] = "flat"
line_70_live.place(x=800, y=2965, width=70, height=33)

line_70_disabled = tk.Label(scrollframe)
line_70_disabled["bg"] = "#adafae"
line_70_disabled["fg"] = "red"
line_70_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_70_disabled["font"] = ftl
line_70_disabled["justify"] = "left"
line_70_disabled["anchor"] = "w"
line_70_disabled["relief"] = "flat"
line_70_disabled.place(x=650, y=2965, width=150, height=33)

line_71_frame = tk.Label(scrollframe)
line_71_frame["bg"] = "#adafae"
line_71_frame["text"] = ""
line_71_frame["relief"] = "sunken"
line_71_frame.place(x=10, y=3000, width=1060, height=40)

line_71_index = tk.Label(scrollframe)
line_71_index["bg"] = "#adafae"
line_71_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_71_index["font"] = ft
line_71_index["justify"] = "left"
line_71_index["anchor"] = "w"
line_71_index.place(x=20, y=3005, width=150, height=33)

line_71_name = tk.Label(scrollframe)
line_71_name["bg"] = "#adafae"
line_71_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_71_name["font"] = ft
line_71_name["justify"] = "left"
line_71_name["anchor"] = "w"
line_71_name.place(x=250, y=3005, width=500, height=33)

line_71_duration = tk.Label(scrollframe)
line_71_duration["bg"] = "#adafae"
line_71_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_71_duration["font"] = ft
line_71_duration["justify"] = "right"
line_71_duration["anchor"] = "e"
line_71_duration.place(x=910, y=3005, width=150, height=33)

line_71_live = tk.Label(scrollframe)
line_71_live["bg"] = "#adafae"
line_71_live["fg"] = "red"
line_71_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_71_live["font"] = ftl
line_71_live["justify"] = "left"
line_71_live["anchor"] = "w"
line_71_live["relief"] = "flat"
line_71_live.place(x=800, y=3005, width=70, height=33)

line_71_disabled = tk.Label(scrollframe)
line_71_disabled["bg"] = "#adafae"
line_71_disabled["fg"] = "red"
line_71_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_71_disabled["font"] = ftl
line_71_disabled["justify"] = "left"
line_71_disabled["anchor"] = "w"
line_71_disabled["relief"] = "flat"
line_71_disabled.place(x=650, y=3005, width=150, height=33)

line_72_frame = tk.Label(scrollframe)
line_72_frame["bg"] = "#adafae"
line_72_frame["text"] = ""
line_72_frame["relief"] = "sunken"
line_72_frame.place(x=10, y=3040, width=1060, height=40)

line_72_index = tk.Label(scrollframe)
line_72_index["bg"] = "#adafae"
line_72_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_72_index["font"] = ft
line_72_index["justify"] = "left"
line_72_index["anchor"] = "w"
line_72_index.place(x=20, y=3045, width=150, height=33)

line_72_name = tk.Label(scrollframe)
line_72_name["bg"] = "#adafae"
line_72_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_72_name["font"] = ft
line_72_name["justify"] = "left"
line_72_name["anchor"] = "w"
line_72_name.place(x=250, y=3045, width=500, height=33)

line_72_duration = tk.Label(scrollframe)
line_72_duration["bg"] = "#adafae"
line_72_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_72_duration["font"] = ft
line_72_duration["justify"] = "right"
line_72_duration["anchor"] = "e"
line_72_duration.place(x=910, y=3045, width=150, height=33)

line_72_live = tk.Label(scrollframe)
line_72_live["bg"] = "#adafae"
line_72_live["fg"] = "red"
line_72_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_72_live["font"] = ftl
line_72_live["justify"] = "left"
line_72_live["anchor"] = "w"
line_72_live["relief"] = "flat"
line_72_live.place(x=800, y=3045, width=70, height=33)

line_72_disabled = tk.Label(scrollframe)
line_72_disabled["bg"] = "#adafae"
line_72_disabled["fg"] = "red"
line_72_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_72_disabled["font"] = ftl
line_72_disabled["justify"] = "left"
line_72_disabled["anchor"] = "w"
line_72_disabled["relief"] = "flat"
line_72_disabled.place(x=650, y=3045, width=150, height=33)

line_73_frame = tk.Label(scrollframe)
line_73_frame["bg"] = "#adafae"
line_73_frame["text"] = ""
line_73_frame["relief"] = "sunken"
line_73_frame.place(x=10, y=3080, width=1060, height=40)

line_73_index = tk.Label(scrollframe)
line_73_index["bg"] = "#adafae"
line_73_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_73_index["font"] = ft
line_73_index["justify"] = "left"
line_73_index["anchor"] = "w"
line_73_index.place(x=20, y=3085, width=150, height=33)

line_73_name = tk.Label(scrollframe)
line_73_name["bg"] = "#adafae"
line_73_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_73_name["font"] = ft
line_73_name["justify"] = "left"
line_73_name["anchor"] = "w"
line_73_name.place(x=250, y=3085, width=500, height=33)

line_73_duration = tk.Label(scrollframe)
line_73_duration["bg"] = "#adafae"
line_73_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_73_duration["font"] = ft
line_73_duration["justify"] = "right"
line_73_duration["anchor"] = "e"
line_73_duration.place(x=910, y=3085, width=150, height=33)

line_73_live = tk.Label(scrollframe)
line_73_live["bg"] = "#adafae"
line_73_live["fg"] = "red"
line_73_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_73_live["font"] = ftl
line_73_live["justify"] = "left"
line_73_live["anchor"] = "w"
line_73_live["relief"] = "flat"
line_73_live.place(x=800, y=3085, width=70, height=33)

line_73_disabled = tk.Label(scrollframe)
line_73_disabled["bg"] = "#adafae"
line_73_disabled["fg"] = "red"
line_73_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_73_disabled["font"] = ftl
line_73_disabled["justify"] = "left"
line_73_disabled["anchor"] = "w"
line_73_disabled["relief"] = "flat"
line_73_disabled.place(x=650, y=3085, width=150, height=33)

line_74_frame = tk.Label(scrollframe)
line_74_frame["bg"] = "#adafae"
line_74_frame["text"] = ""
line_74_frame["relief"] = "sunken"
line_74_frame.place(x=10, y=3120, width=1060, height=40)

line_74_index = tk.Label(scrollframe)
line_74_index["bg"] = "#adafae"
line_74_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_74_index["font"] = ft
line_74_index["justify"] = "left"
line_74_index["anchor"] = "w"
line_74_index.place(x=20, y=3125, width=150, height=33)

line_74_name = tk.Label(scrollframe)
line_74_name["bg"] = "#adafae"
line_74_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_74_name["font"] = ft
line_74_name["justify"] = "left"
line_74_name["anchor"] = "w"
line_74_name.place(x=250, y=3125, width=500, height=33)

line_74_duration = tk.Label(scrollframe)
line_74_duration["bg"] = "#adafae"
line_74_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_74_duration["font"] = ft
line_74_duration["justify"] = "right"
line_74_duration["anchor"] = "e"
line_74_duration.place(x=910, y=3125, width=150, height=33)

line_74_live = tk.Label(scrollframe)
line_74_live["bg"] = "#adafae"
line_74_live["fg"] = "red"
line_74_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_74_live["font"] = ftl
line_74_live["justify"] = "left"
line_74_live["anchor"] = "w"
line_74_live["relief"] = "flat"
line_74_live.place(x=800, y=3125, width=70, height=33)

line_74_disabled = tk.Label(scrollframe)
line_74_disabled["bg"] = "#adafae"
line_74_disabled["fg"] = "red"
line_74_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_74_disabled["font"] = ftl
line_74_disabled["justify"] = "left"
line_74_disabled["anchor"] = "w"
line_74_disabled["relief"] = "flat"
line_74_disabled.place(x=650, y=3125, width=150, height=33)

line_75_frame = tk.Label(scrollframe)
line_75_frame["bg"] = "#adafae"
line_75_frame["text"] = ""
line_75_frame["relief"] = "sunken"
line_75_frame.place(x=10, y=3160, width=1060, height=40)

line_75_index = tk.Label(scrollframe)
line_75_index["bg"] = "#adafae"
line_75_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_75_index["font"] = ft
line_75_index["justify"] = "left"
line_75_index["anchor"] = "w"
line_75_index.place(x=20, y=3165, width=150, height=33)

line_75_name = tk.Label(scrollframe)
line_75_name["bg"] = "#adafae"
line_75_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_75_name["font"] = ft
line_75_name["justify"] = "left"
line_75_name["anchor"] = "w"
line_75_name.place(x=250, y=3165, width=500, height=33)

line_75_duration = tk.Label(scrollframe)
line_75_duration["bg"] = "#adafae"
line_75_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_75_duration["font"] = ft
line_75_duration["justify"] = "right"
line_75_duration["anchor"] = "e"
line_75_duration.place(x=910, y=3165, width=150, height=33)

line_75_live = tk.Label(scrollframe)
line_75_live["bg"] = "#adafae"
line_75_live["fg"] = "red"
line_75_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_75_live["font"] = ftl
line_75_live["justify"] = "left"
line_75_live["anchor"] = "w"
line_75_live["relief"] = "flat"
line_75_live.place(x=800, y=3165, width=70, height=33)

line_75_disabled = tk.Label(scrollframe)
line_75_disabled["bg"] = "#adafae"
line_75_disabled["fg"] = "red"
line_75_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_75_disabled["font"] = ftl
line_75_disabled["justify"] = "left"
line_75_disabled["anchor"] = "w"
line_75_disabled["relief"] = "flat"
line_75_disabled.place(x=650, y=3165, width=150, height=33)

line_76_frame = tk.Label(scrollframe)
line_76_frame["bg"] = "#adafae"
line_76_frame["text"] = ""
line_76_frame["relief"] = "sunken"
line_76_frame.place(x=10, y=3200, width=1060, height=40)

line_76_index = tk.Label(scrollframe)
line_76_index["bg"] = "#adafae"
line_76_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_76_index["font"] = ft
line_76_index["justify"] = "left"
line_76_index["anchor"] = "w"
line_76_index.place(x=20, y=3205, width=150, height=33)

line_76_name = tk.Label(scrollframe)
line_76_name["bg"] = "#adafae"
line_76_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_76_name["font"] = ft
line_76_name["justify"] = "left"
line_76_name["anchor"] = "w"
line_76_name.place(x=250, y=3205, width=500, height=33)

line_76_duration = tk.Label(scrollframe)
line_76_duration["bg"] = "#adafae"
line_76_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_76_duration["font"] = ft
line_76_duration["justify"] = "right"
line_76_duration["anchor"] = "e"
line_76_duration.place(x=910, y=3205, width=150, height=33)

line_76_live = tk.Label(scrollframe)
line_76_live["bg"] = "#adafae"
line_76_live["fg"] = "red"
line_76_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_76_live["font"] = ftl
line_76_live["justify"] = "left"
line_76_live["anchor"] = "w"
line_76_live["relief"] = "flat"
line_76_live.place(x=800, y=3205, width=70, height=33)

line_76_disabled = tk.Label(scrollframe)
line_76_disabled["bg"] = "#adafae"
line_76_disabled["fg"] = "red"
line_76_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_76_disabled["font"] = ftl
line_76_disabled["justify"] = "left"
line_76_disabled["anchor"] = "w"
line_76_disabled["relief"] = "flat"
line_76_disabled.place(x=650, y=3205, width=150, height=33)

line_77_frame = tk.Label(scrollframe)
line_77_frame["bg"] = "#adafae"
line_77_frame["text"] = ""
line_77_frame["relief"] = "sunken"
line_77_frame.place(x=10, y=3240, width=1060, height=40)

line_77_index = tk.Label(scrollframe)
line_77_index["bg"] = "#adafae"
line_77_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_77_index["font"] = ft
line_77_index["justify"] = "left"
line_77_index["anchor"] = "w"
line_77_index.place(x=20, y=3245, width=150, height=33)

line_77_name = tk.Label(scrollframe)
line_77_name["bg"] = "#adafae"
line_77_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_77_name["font"] = ft
line_77_name["justify"] = "left"
line_77_name["anchor"] = "w"
line_77_name.place(x=250, y=3245, width=500, height=33)

line_77_duration = tk.Label(scrollframe)
line_77_duration["bg"] = "#adafae"
line_77_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_77_duration["font"] = ft
line_77_duration["justify"] = "right"
line_77_duration["anchor"] = "e"
line_77_duration.place(x=910, y=3245, width=150, height=33)

line_77_live = tk.Label(scrollframe)
line_77_live["bg"] = "#adafae"
line_77_live["fg"] = "red"
line_77_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_77_live["font"] = ftl
line_77_live["justify"] = "left"
line_77_live["anchor"] = "w"
line_77_live["relief"] = "flat"
line_77_live.place(x=800, y=3245, width=70, height=33)

line_77_disabled = tk.Label(scrollframe)
line_77_disabled["bg"] = "#adafae"
line_77_disabled["fg"] = "red"
line_77_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_77_disabled["font"] = ftl
line_77_disabled["justify"] = "left"
line_77_disabled["anchor"] = "w"
line_77_disabled["relief"] = "flat"
line_77_disabled.place(x=650, y=3245, width=150, height=33)

line_78_frame = tk.Label(scrollframe)
line_78_frame["bg"] = "#adafae"
line_78_frame["text"] = ""
line_78_frame["relief"] = "sunken"
line_78_frame.place(x=10, y=3280, width=1060, height=40)

line_78_index = tk.Label(scrollframe)
line_78_index["bg"] = "#adafae"
line_78_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_78_index["font"] = ft
line_78_index["justify"] = "left"
line_78_index["anchor"] = "w"
line_78_index.place(x=20, y=3285, width=150, height=33)

line_78_name = tk.Label(scrollframe)
line_78_name["bg"] = "#adafae"
line_78_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_78_name["font"] = ft
line_78_name["justify"] = "left"
line_78_name["anchor"] = "w"
line_78_name.place(x=250, y=3285, width=500, height=33)

line_78_duration = tk.Label(scrollframe)
line_78_duration["bg"] = "#adafae"
line_78_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_78_duration["font"] = ft
line_78_duration["justify"] = "right"
line_78_duration["anchor"] = "e"
line_78_duration.place(x=910, y=3285, width=150, height=33)

line_78_live = tk.Label(scrollframe)
line_78_live["bg"] = "#adafae"
line_78_live["fg"] = "red"
line_78_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_78_live["font"] = ftl
line_78_live["justify"] = "left"
line_78_live["anchor"] = "w"
line_78_live["relief"] = "flat"
line_78_live.place(x=800, y=3285, width=70, height=33)

line_78_disabled = tk.Label(scrollframe)
line_78_disabled["bg"] = "#adafae"
line_78_disabled["fg"] = "red"
line_78_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_78_disabled["font"] = ftl
line_78_disabled["justify"] = "left"
line_78_disabled["anchor"] = "w"
line_78_disabled["relief"] = "flat"
line_78_disabled.place(x=650, y=3285, width=150, height=33)

line_79_frame = tk.Label(scrollframe)
line_79_frame["bg"] = "#adafae"
line_79_frame["text"] = ""
line_79_frame["relief"] = "sunken"
line_79_frame.place(x=10, y=3320, width=1060, height=40)

line_79_index = tk.Label(scrollframe)
line_79_index["bg"] = "#adafae"
line_79_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_79_index["font"] = ft
line_79_index["justify"] = "left"
line_79_index["anchor"] = "w"
line_79_index.place(x=20, y=3325, width=150, height=33)

line_79_name = tk.Label(scrollframe)
line_79_name["bg"] = "#adafae"
line_79_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_79_name["font"] = ft
line_79_name["justify"] = "left"
line_79_name["anchor"] = "w"
line_79_name.place(x=250, y=3325, width=500, height=33)

line_79_duration = tk.Label(scrollframe)
line_79_duration["bg"] = "#adafae"
line_79_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_79_duration["font"] = ft
line_79_duration["justify"] = "right"
line_79_duration["anchor"] = "e"
line_79_duration.place(x=910, y=3325, width=150, height=33)

line_79_live = tk.Label(scrollframe)
line_79_live["bg"] = "#adafae"
line_79_live["fg"] = "red"
line_79_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_79_live["font"] = ftl
line_79_live["justify"] = "left"
line_79_live["anchor"] = "w"
line_79_live["relief"] = "flat"
line_79_live.place(x=800, y=3325, width=70, height=33)

line_79_disabled = tk.Label(scrollframe)
line_79_disabled["bg"] = "#adafae"
line_79_disabled["fg"] = "red"
line_79_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_79_disabled["font"] = ftl
line_79_disabled["justify"] = "left"
line_79_disabled["anchor"] = "w"
line_79_disabled["relief"] = "flat"
line_79_disabled.place(x=650, y=3325, width=150, height=33)

line_80_frame = tk.Label(scrollframe)
line_80_frame["bg"] = "#adafae"
line_80_frame["text"] = ""
line_80_frame["relief"] = "sunken"
line_80_frame.place(x=10, y=3360, width=1060, height=40)

line_80_index = tk.Label(scrollframe)
line_80_index["bg"] = "#adafae"
line_80_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_80_index["font"] = ft
line_80_index["justify"] = "left"
line_80_index["anchor"] = "w"
line_80_index.place(x=20, y=3365, width=150, height=33)

line_80_name = tk.Label(scrollframe)
line_80_name["bg"] = "#adafae"
line_80_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_80_name["font"] = ft
line_80_name["justify"] = "left"
line_80_name["anchor"] = "w"
line_80_name.place(x=250, y=3365, width=500, height=33)

line_80_duration = tk.Label(scrollframe)
line_80_duration["bg"] = "#adafae"
line_80_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_80_duration["font"] = ft
line_80_duration["justify"] = "right"
line_80_duration["anchor"] = "e"
line_80_duration.place(x=910, y=3365, width=150, height=33)

line_80_live = tk.Label(scrollframe)
line_80_live["bg"] = "#adafae"
line_80_live["fg"] = "red"
line_80_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_80_live["font"] = ftl
line_80_live["justify"] = "left"
line_80_live["anchor"] = "w"
line_80_live["relief"] = "flat"
line_80_live.place(x=800, y=3365, width=70, height=33)

line_80_disabled = tk.Label(scrollframe)
line_80_disabled["bg"] = "#adafae"
line_80_disabled["fg"] = "red"
line_80_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_80_disabled["font"] = ftl
line_80_disabled["justify"] = "left"
line_80_disabled["anchor"] = "w"
line_80_disabled["relief"] = "flat"
line_80_disabled.place(x=650, y=3365, width=150, height=33)

line_81_frame = tk.Label(scrollframe)
line_81_frame["bg"] = "#adafae"
line_81_frame["text"] = ""
line_81_frame["relief"] = "sunken"
line_81_frame.place(x=10, y=3400, width=1060, height=40)

line_81_index = tk.Label(scrollframe)
line_81_index["bg"] = "#adafae"
line_81_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_81_index["font"] = ft
line_81_index["justify"] = "left"
line_81_index["anchor"] = "w"
line_81_index.place(x=20, y=3405, width=150, height=33)

line_81_name = tk.Label(scrollframe)
line_81_name["bg"] = "#adafae"
line_81_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_81_name["font"] = ft
line_81_name["justify"] = "left"
line_81_name["anchor"] = "w"
line_81_name.place(x=250, y=3405, width=500, height=33)

line_81_duration = tk.Label(scrollframe)
line_81_duration["bg"] = "#adafae"
line_81_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_81_duration["font"] = ft
line_81_duration["justify"] = "right"
line_81_duration["anchor"] = "e"
line_81_duration.place(x=910, y=3405, width=150, height=33)

line_81_live = tk.Label(scrollframe)
line_81_live["bg"] = "#adafae"
line_81_live["fg"] = "red"
line_81_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_81_live["font"] = ftl
line_81_live["justify"] = "left"
line_81_live["anchor"] = "w"
line_81_live["relief"] = "flat"
line_81_live.place(x=800, y=3405, width=70, height=33)

line_81_disabled = tk.Label(scrollframe)
line_81_disabled["bg"] = "#adafae"
line_81_disabled["fg"] = "red"
line_81_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_81_disabled["font"] = ftl
line_81_disabled["justify"] = "left"
line_81_disabled["anchor"] = "w"
line_81_disabled["relief"] = "flat"
line_81_disabled.place(x=650, y=3405, width=150, height=33)

line_82_frame = tk.Label(scrollframe)
line_82_frame["bg"] = "#adafae"
line_82_frame["text"] = ""
line_82_frame["relief"] = "sunken"
line_82_frame.place(x=10, y=3440, width=1060, height=40)

line_82_index = tk.Label(scrollframe)
line_82_index["bg"] = "#adafae"
line_82_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_82_index["font"] = ft
line_82_index["justify"] = "left"
line_82_index["anchor"] = "w"
line_82_index.place(x=20, y=3445, width=150, height=33)

line_82_name = tk.Label(scrollframe)
line_82_name["bg"] = "#adafae"
line_82_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_82_name["font"] = ft
line_82_name["justify"] = "left"
line_82_name["anchor"] = "w"
line_82_name.place(x=250, y=3445, width=500, height=33)

line_82_duration = tk.Label(scrollframe)
line_82_duration["bg"] = "#adafae"
line_82_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_82_duration["font"] = ft
line_82_duration["justify"] = "right"
line_82_duration["anchor"] = "e"
line_82_duration.place(x=910, y=3445, width=150, height=33)

line_82_live = tk.Label(scrollframe)
line_82_live["bg"] = "#adafae"
line_82_live["fg"] = "red"
line_82_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_82_live["font"] = ftl
line_82_live["justify"] = "left"
line_82_live["anchor"] = "w"
line_82_live["relief"] = "flat"
line_82_live.place(x=800, y=3445, width=70, height=33)

line_82_disabled = tk.Label(scrollframe)
line_82_disabled["bg"] = "#adafae"
line_82_disabled["fg"] = "red"
line_82_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_82_disabled["font"] = ftl
line_82_disabled["justify"] = "left"
line_82_disabled["anchor"] = "w"
line_82_disabled["relief"] = "flat"
line_82_disabled.place(x=650, y=3445, width=150, height=33)

line_83_frame = tk.Label(scrollframe)
line_83_frame["bg"] = "#adafae"
line_83_frame["text"] = ""
line_83_frame["relief"] = "sunken"
line_83_frame.place(x=10, y=3480, width=1060, height=40)

line_83_index = tk.Label(scrollframe)
line_83_index["bg"] = "#adafae"
line_83_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_83_index["font"] = ft
line_83_index["justify"] = "left"
line_83_index["anchor"] = "w"
line_83_index.place(x=20, y=3485, width=150, height=33)

line_83_name = tk.Label(scrollframe)
line_83_name["bg"] = "#adafae"
line_83_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_83_name["font"] = ft
line_83_name["justify"] = "left"
line_83_name["anchor"] = "w"
line_83_name.place(x=250, y=3485, width=500, height=33)

line_83_duration = tk.Label(scrollframe)
line_83_duration["bg"] = "#adafae"
line_83_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_83_duration["font"] = ft
line_83_duration["justify"] = "right"
line_83_duration["anchor"] = "e"
line_83_duration.place(x=910, y=3485, width=150, height=33)

line_83_live = tk.Label(scrollframe)
line_83_live["bg"] = "#adafae"
line_83_live["fg"] = "red"
line_83_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_83_live["font"] = ftl
line_83_live["justify"] = "left"
line_83_live["anchor"] = "w"
line_83_live["relief"] = "flat"
line_83_live.place(x=800, y=3485, width=70, height=33)

line_83_disabled = tk.Label(scrollframe)
line_83_disabled["bg"] = "#adafae"
line_83_disabled["fg"] = "red"
line_83_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_83_disabled["font"] = ftl
line_83_disabled["justify"] = "left"
line_83_disabled["anchor"] = "w"
line_83_disabled["relief"] = "flat"
line_83_disabled.place(x=650, y=3485, width=150, height=33)

line_84_frame = tk.Label(scrollframe)
line_84_frame["bg"] = "#adafae"
line_84_frame["text"] = ""
line_84_frame["relief"] = "sunken"
line_84_frame.place(x=10, y=3520, width=1060, height=40)

line_84_index = tk.Label(scrollframe)
line_84_index["bg"] = "#adafae"
line_84_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_84_index["font"] = ft
line_84_index["justify"] = "left"
line_84_index["anchor"] = "w"
line_84_index.place(x=20, y=3525, width=150, height=33)

line_84_name = tk.Label(scrollframe)
line_84_name["bg"] = "#adafae"
line_84_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_84_name["font"] = ft
line_84_name["justify"] = "left"
line_84_name["anchor"] = "w"
line_84_name.place(x=250, y=3525, width=500, height=33)

line_84_duration = tk.Label(scrollframe)
line_84_duration["bg"] = "#adafae"
line_84_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_84_duration["font"] = ft
line_84_duration["justify"] = "right"
line_84_duration["anchor"] = "e"
line_84_duration.place(x=910, y=3525, width=150, height=33)

line_84_live = tk.Label(scrollframe)
line_84_live["bg"] = "#adafae"
line_84_live["fg"] = "red"
line_84_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_84_live["font"] = ftl
line_84_live["justify"] = "left"
line_84_live["anchor"] = "w"
line_84_live["relief"] = "flat"
line_84_live.place(x=800, y=3525, width=70, height=33)

line_84_disabled = tk.Label(scrollframe)
line_84_disabled["bg"] = "#adafae"
line_84_disabled["fg"] = "red"
line_84_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_84_disabled["font"] = ftl
line_84_disabled["justify"] = "left"
line_84_disabled["anchor"] = "w"
line_84_disabled["relief"] = "flat"
line_84_disabled.place(x=650, y=3525, width=150, height=33)

line_85_frame = tk.Label(scrollframe)
line_85_frame["bg"] = "#adafae"
line_85_frame["text"] = ""
line_85_frame["relief"] = "sunken"
line_85_frame.place(x=10, y=3560, width=1060, height=40)

line_85_index = tk.Label(scrollframe)
line_85_index["bg"] = "#adafae"
line_85_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_85_index["font"] = ft
line_85_index["justify"] = "left"
line_85_index["anchor"] = "w"
line_85_index.place(x=20, y=3565, width=150, height=33)

line_85_name = tk.Label(scrollframe)
line_85_name["bg"] = "#adafae"
line_85_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_85_name["font"] = ft
line_85_name["justify"] = "left"
line_85_name["anchor"] = "w"
line_85_name.place(x=250, y=3565, width=500, height=33)

line_85_duration = tk.Label(scrollframe)
line_85_duration["bg"] = "#adafae"
line_85_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_85_duration["font"] = ft
line_85_duration["justify"] = "right"
line_85_duration["anchor"] = "e"
line_85_duration.place(x=910, y=3565, width=150, height=33)

line_85_live = tk.Label(scrollframe)
line_85_live["bg"] = "#adafae"
line_85_live["fg"] = "red"
line_85_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_85_live["font"] = ftl
line_85_live["justify"] = "left"
line_85_live["anchor"] = "w"
line_85_live["relief"] = "flat"
line_85_live.place(x=800, y=3565, width=70, height=33)

line_85_disabled = tk.Label(scrollframe)
line_85_disabled["bg"] = "#adafae"
line_85_disabled["fg"] = "red"
line_85_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_85_disabled["font"] = ftl
line_85_disabled["justify"] = "left"
line_85_disabled["anchor"] = "w"
line_85_disabled["relief"] = "flat"
line_85_disabled.place(x=650, y=3565, width=150, height=33)

line_86_frame = tk.Label(scrollframe)
line_86_frame["bg"] = "#adafae"
line_86_frame["text"] = ""
line_86_frame["relief"] = "sunken"
line_86_frame.place(x=10, y=3600, width=1060, height=40)

line_86_index = tk.Label(scrollframe)
line_86_index["bg"] = "#adafae"
line_86_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_86_index["font"] = ft
line_86_index["justify"] = "left"
line_86_index["anchor"] = "w"
line_86_index.place(x=20, y=3605, width=150, height=33)

line_86_name = tk.Label(scrollframe)
line_86_name["bg"] = "#adafae"
line_86_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_86_name["font"] = ft
line_86_name["justify"] = "left"
line_86_name["anchor"] = "w"
line_86_name.place(x=250, y=3605, width=500, height=33)

line_86_duration = tk.Label(scrollframe)
line_86_duration["bg"] = "#adafae"
line_86_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_86_duration["font"] = ft
line_86_duration["justify"] = "right"
line_86_duration["anchor"] = "e"
line_86_duration.place(x=910, y=3605, width=150, height=33)

line_86_live = tk.Label(scrollframe)
line_86_live["bg"] = "#adafae"
line_86_live["fg"] = "red"
line_86_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_86_live["font"] = ftl
line_86_live["justify"] = "left"
line_86_live["anchor"] = "w"
line_86_live["relief"] = "flat"
line_86_live.place(x=800, y=3605, width=70, height=33)

line_86_disabled = tk.Label(scrollframe)
line_86_disabled["bg"] = "#adafae"
line_86_disabled["fg"] = "red"
line_86_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_86_disabled["font"] = ftl
line_86_disabled["justify"] = "left"
line_86_disabled["anchor"] = "w"
line_86_disabled["relief"] = "flat"
line_86_disabled.place(x=650, y=3605, width=150, height=33)

line_87_frame = tk.Label(scrollframe)
line_87_frame["bg"] = "#adafae"
line_87_frame["text"] = ""
line_87_frame["relief"] = "sunken"
line_87_frame.place(x=10, y=3640, width=1060, height=40)

line_87_index = tk.Label(scrollframe)
line_87_index["bg"] = "#adafae"
line_87_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_87_index["font"] = ft
line_87_index["justify"] = "left"
line_87_index["anchor"] = "w"
line_87_index.place(x=20, y=3645, width=150, height=33)

line_87_name = tk.Label(scrollframe)
line_87_name["bg"] = "#adafae"
line_87_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_87_name["font"] = ft
line_87_name["justify"] = "left"
line_87_name["anchor"] = "w"
line_87_name.place(x=250, y=3645, width=500, height=33)

line_87_duration = tk.Label(scrollframe)
line_87_duration["bg"] = "#adafae"
line_87_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_87_duration["font"] = ft
line_87_duration["justify"] = "right"
line_87_duration["anchor"] = "e"
line_87_duration.place(x=910, y=3645, width=150, height=33)

line_87_live = tk.Label(scrollframe)
line_87_live["bg"] = "#adafae"
line_87_live["fg"] = "red"
line_87_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_87_live["font"] = ftl
line_87_live["justify"] = "left"
line_87_live["anchor"] = "w"
line_87_live["relief"] = "flat"
line_87_live.place(x=800, y=3645, width=70, height=33)

line_87_disabled = tk.Label(scrollframe)
line_87_disabled["bg"] = "#adafae"
line_87_disabled["fg"] = "red"
line_87_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_87_disabled["font"] = ftl
line_87_disabled["justify"] = "left"
line_87_disabled["anchor"] = "w"
line_87_disabled["relief"] = "flat"
line_87_disabled.place(x=650, y=3645, width=150, height=33)

line_88_frame = tk.Label(scrollframe)
line_88_frame["bg"] = "#adafae"
line_88_frame["text"] = ""
line_88_frame["relief"] = "sunken"
line_88_frame.place(x=10, y=3680, width=1060, height=40)

line_88_index = tk.Label(scrollframe)
line_88_index["bg"] = "#adafae"
line_88_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_88_index["font"] = ft
line_88_index["justify"] = "left"
line_88_index["anchor"] = "w"
line_88_index.place(x=20, y=3685, width=150, height=33)

line_88_name = tk.Label(scrollframe)
line_88_name["bg"] = "#adafae"
line_88_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_88_name["font"] = ft
line_88_name["justify"] = "left"
line_88_name["anchor"] = "w"
line_88_name.place(x=250, y=3685, width=500, height=33)

line_88_duration = tk.Label(scrollframe)
line_88_duration["bg"] = "#adafae"
line_88_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_88_duration["font"] = ft
line_88_duration["justify"] = "right"
line_88_duration["anchor"] = "e"
line_88_duration.place(x=910, y=3685, width=150, height=33)

line_88_live = tk.Label(scrollframe)
line_88_live["bg"] = "#adafae"
line_88_live["fg"] = "red"
line_88_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_88_live["font"] = ftl
line_88_live["justify"] = "left"
line_88_live["anchor"] = "w"
line_88_live["relief"] = "flat"
line_88_live.place(x=800, y=3685, width=70, height=33)

line_88_disabled = tk.Label(scrollframe)
line_88_disabled["bg"] = "#adafae"
line_88_disabled["fg"] = "red"
line_88_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_88_disabled["font"] = ftl
line_88_disabled["justify"] = "left"
line_88_disabled["anchor"] = "w"
line_88_disabled["relief"] = "flat"
line_88_disabled.place(x=650, y=3685, width=150, height=33)

line_89_frame = tk.Label(scrollframe)
line_89_frame["bg"] = "#adafae"
line_89_frame["text"] = ""
line_89_frame["relief"] = "sunken"
line_89_frame.place(x=10, y=3720, width=1060, height=40)

line_89_index = tk.Label(scrollframe)
line_89_index["bg"] = "#adafae"
line_89_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_89_index["font"] = ft
line_89_index["justify"] = "left"
line_89_index["anchor"] = "w"
line_89_index.place(x=20, y=3725, width=150, height=33)

line_89_name = tk.Label(scrollframe)
line_89_name["bg"] = "#adafae"
line_89_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_89_name["font"] = ft
line_89_name["justify"] = "left"
line_89_name["anchor"] = "w"
line_89_name.place(x=250, y=3725, width=500, height=33)

line_89_duration = tk.Label(scrollframe)
line_89_duration["bg"] = "#adafae"
line_89_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_89_duration["font"] = ft
line_89_duration["justify"] = "right"
line_89_duration["anchor"] = "e"
line_89_duration.place(x=910, y=3725, width=150, height=33)

line_89_live = tk.Label(scrollframe)
line_89_live["bg"] = "#adafae"
line_89_live["fg"] = "red"
line_89_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_89_live["font"] = ftl
line_89_live["justify"] = "left"
line_89_live["anchor"] = "w"
line_89_live["relief"] = "flat"
line_89_live.place(x=800, y=3725, width=70, height=33)

line_89_disabled = tk.Label(scrollframe)
line_89_disabled["bg"] = "#adafae"
line_89_disabled["fg"] = "red"
line_89_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_89_disabled["font"] = ftl
line_89_disabled["justify"] = "left"
line_89_disabled["anchor"] = "w"
line_89_disabled["relief"] = "flat"
line_89_disabled.place(x=650, y=3725, width=150, height=33)

line_90_frame = tk.Label(scrollframe)
line_90_frame["bg"] = "#adafae"
line_90_frame["text"] = ""
line_90_frame["relief"] = "sunken"
line_90_frame.place(x=10, y=3760, width=1060, height=40)

line_90_index = tk.Label(scrollframe)
line_90_index["bg"] = "#adafae"
line_90_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_90_index["font"] = ft
line_90_index["justify"] = "left"
line_90_index["anchor"] = "w"
line_90_index.place(x=20, y=3765, width=150, height=33)

line_90_name = tk.Label(scrollframe)
line_90_name["bg"] = "#adafae"
line_90_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_90_name["font"] = ft
line_90_name["justify"] = "left"
line_90_name["anchor"] = "w"
line_90_name.place(x=250, y=3765, width=500, height=33)

line_90_duration = tk.Label(scrollframe)
line_90_duration["bg"] = "#adafae"
line_90_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_90_duration["font"] = ft
line_90_duration["justify"] = "right"
line_90_duration["anchor"] = "e"
line_90_duration.place(x=910, y=3765, width=150, height=33)

line_90_live = tk.Label(scrollframe)
line_90_live["bg"] = "#adafae"
line_90_live["fg"] = "red"
line_90_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_90_live["font"] = ftl
line_90_live["justify"] = "left"
line_90_live["anchor"] = "w"
line_90_live["relief"] = "flat"
line_90_live.place(x=800, y=3765, width=70, height=33)

line_90_disabled = tk.Label(scrollframe)
line_90_disabled["bg"] = "#adafae"
line_90_disabled["fg"] = "red"
line_90_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_90_disabled["font"] = ftl
line_90_disabled["justify"] = "left"
line_90_disabled["anchor"] = "w"
line_90_disabled["relief"] = "flat"
line_90_disabled.place(x=650, y=3765, width=150, height=33)

line_91_frame = tk.Label(scrollframe)
line_91_frame["bg"] = "#adafae"
line_91_frame["text"] = ""
line_91_frame["relief"] = "sunken"
line_91_frame.place(x=10, y=3800, width=1060, height=40)

line_91_index = tk.Label(scrollframe)
line_91_index["bg"] = "#adafae"
line_91_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_91_index["font"] = ft
line_91_index["justify"] = "left"
line_91_index["anchor"] = "w"
line_91_index.place(x=20, y=3805, width=150, height=33)

line_91_name = tk.Label(scrollframe)
line_91_name["bg"] = "#adafae"
line_91_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_91_name["font"] = ft
line_91_name["justify"] = "left"
line_91_name["anchor"] = "w"
line_91_name.place(x=250, y=3805, width=500, height=33)

line_91_duration = tk.Label(scrollframe)
line_91_duration["bg"] = "#adafae"
line_91_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_91_duration["font"] = ft
line_91_duration["justify"] = "right"
line_91_duration["anchor"] = "e"
line_91_duration.place(x=910, y=3805, width=150, height=33)

line_91_live = tk.Label(scrollframe)
line_91_live["bg"] = "#adafae"
line_91_live["fg"] = "red"
line_91_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_91_live["font"] = ftl
line_91_live["justify"] = "left"
line_91_live["anchor"] = "w"
line_91_live["relief"] = "flat"
line_91_live.place(x=800, y=3805, width=70, height=33)

line_91_disabled = tk.Label(scrollframe)
line_91_disabled["bg"] = "#adafae"
line_91_disabled["fg"] = "red"
line_91_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_91_disabled["font"] = ftl
line_91_disabled["justify"] = "left"
line_91_disabled["anchor"] = "w"
line_91_disabled["relief"] = "flat"
line_91_disabled.place(x=650, y=3805, width=150, height=33)

line_92_frame = tk.Label(scrollframe)
line_92_frame["bg"] = "#adafae"
line_92_frame["text"] = ""
line_92_frame["relief"] = "sunken"
line_92_frame.place(x=10, y=3840, width=1060, height=40)

line_92_index = tk.Label(scrollframe)
line_92_index["bg"] = "#adafae"
line_92_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_92_index["font"] = ft
line_92_index["justify"] = "left"
line_92_index["anchor"] = "w"
line_92_index.place(x=20, y=3845, width=150, height=33)

line_92_name = tk.Label(scrollframe)
line_92_name["bg"] = "#adafae"
line_92_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_92_name["font"] = ft
line_92_name["justify"] = "left"
line_92_name["anchor"] = "w"
line_92_name.place(x=250, y=3845, width=500, height=33)

line_92_duration = tk.Label(scrollframe)
line_92_duration["bg"] = "#adafae"
line_92_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_92_duration["font"] = ft
line_92_duration["justify"] = "right"
line_92_duration["anchor"] = "e"
line_92_duration.place(x=910, y=3845, width=150, height=33)

line_92_live = tk.Label(scrollframe)
line_92_live["bg"] = "#adafae"
line_92_live["fg"] = "red"
line_92_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_92_live["font"] = ftl
line_92_live["justify"] = "left"
line_92_live["anchor"] = "w"
line_92_live["relief"] = "flat"
line_92_live.place(x=800, y=3845, width=70, height=33)

line_92_disabled = tk.Label(scrollframe)
line_92_disabled["bg"] = "#adafae"
line_92_disabled["fg"] = "red"
line_92_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_92_disabled["font"] = ftl
line_92_disabled["justify"] = "left"
line_92_disabled["anchor"] = "w"
line_92_disabled["relief"] = "flat"
line_92_disabled.place(x=650, y=3845, width=150, height=33)

line_93_frame = tk.Label(scrollframe)
line_93_frame["bg"] = "#adafae"
line_93_frame["text"] = ""
line_93_frame["relief"] = "sunken"
line_93_frame.place(x=10, y=3880, width=1060, height=40)

line_93_index = tk.Label(scrollframe)
line_93_index["bg"] = "#adafae"
line_93_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_93_index["font"] = ft
line_93_index["justify"] = "left"
line_93_index["anchor"] = "w"
line_93_index.place(x=20, y=3885, width=150, height=33)

line_93_name = tk.Label(scrollframe)
line_93_name["bg"] = "#adafae"
line_93_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_93_name["font"] = ft
line_93_name["justify"] = "left"
line_93_name["anchor"] = "w"
line_93_name.place(x=250, y=3885, width=500, height=33)

line_93_duration = tk.Label(scrollframe)
line_93_duration["bg"] = "#adafae"
line_93_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_93_duration["font"] = ft
line_93_duration["justify"] = "right"
line_93_duration["anchor"] = "e"
line_93_duration.place(x=910, y=3885, width=150, height=33)

line_93_live = tk.Label(scrollframe)
line_93_live["bg"] = "#adafae"
line_93_live["fg"] = "red"
line_93_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_93_live["font"] = ftl
line_93_live["justify"] = "left"
line_93_live["anchor"] = "w"
line_93_live["relief"] = "flat"
line_93_live.place(x=800, y=3885, width=70, height=33)

line_93_disabled = tk.Label(scrollframe)
line_93_disabled["bg"] = "#adafae"
line_93_disabled["fg"] = "red"
line_93_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_93_disabled["font"] = ftl
line_93_disabled["justify"] = "left"
line_93_disabled["anchor"] = "w"
line_93_disabled["relief"] = "flat"
line_93_disabled.place(x=650, y=3885, width=150, height=33)

line_94_frame = tk.Label(scrollframe)
line_94_frame["bg"] = "#adafae"
line_94_frame["text"] = ""
line_94_frame["relief"] = "sunken"
line_94_frame.place(x=10, y=3920, width=1060, height=40)

line_94_index = tk.Label(scrollframe)
line_94_index["bg"] = "#adafae"
line_94_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_94_index["font"] = ft
line_94_index["justify"] = "left"
line_94_index["anchor"] = "w"
line_94_index.place(x=20, y=3925, width=150, height=33)

line_94_name = tk.Label(scrollframe)
line_94_name["bg"] = "#adafae"
line_94_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_94_name["font"] = ft
line_94_name["justify"] = "left"
line_94_name["anchor"] = "w"
line_94_name.place(x=250, y=3925, width=500, height=33)

line_94_duration = tk.Label(scrollframe)
line_94_duration["bg"] = "#adafae"
line_94_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_94_duration["font"] = ft
line_94_duration["justify"] = "right"
line_94_duration["anchor"] = "e"
line_94_duration.place(x=910, y=3925, width=150, height=33)

line_94_live = tk.Label(scrollframe)
line_94_live["bg"] = "#adafae"
line_94_live["fg"] = "red"
line_94_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_94_live["font"] = ftl
line_94_live["justify"] = "left"
line_94_live["anchor"] = "w"
line_94_live["relief"] = "flat"
line_94_live.place(x=800, y=3925, width=70, height=33)

line_94_disabled = tk.Label(scrollframe)
line_94_disabled["bg"] = "#adafae"
line_94_disabled["fg"] = "red"
line_94_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_94_disabled["font"] = ftl
line_94_disabled["justify"] = "left"
line_94_disabled["anchor"] = "w"
line_94_disabled["relief"] = "flat"
line_94_disabled.place(x=650, y=3925, width=150, height=33)

line_95_frame = tk.Label(scrollframe)
line_95_frame["bg"] = "#adafae"
line_95_frame["text"] = ""
line_95_frame["relief"] = "sunken"
line_95_frame.place(x=10, y=3960, width=1060, height=40)

line_95_index = tk.Label(scrollframe)
line_95_index["bg"] = "#adafae"
line_95_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_95_index["font"] = ft
line_95_index["justify"] = "left"
line_95_index["anchor"] = "w"
line_95_index.place(x=20, y=3965, width=150, height=33)

line_95_name = tk.Label(scrollframe)
line_95_name["bg"] = "#adafae"
line_95_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_95_name["font"] = ft
line_95_name["justify"] = "left"
line_95_name["anchor"] = "w"
line_95_name.place(x=250, y=3965, width=500, height=33)

line_95_duration = tk.Label(scrollframe)
line_95_duration["bg"] = "#adafae"
line_95_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_95_duration["font"] = ft
line_95_duration["justify"] = "right"
line_95_duration["anchor"] = "e"
line_95_duration.place(x=910, y=3965, width=150, height=33)

line_95_live = tk.Label(scrollframe)
line_95_live["bg"] = "#adafae"
line_95_live["fg"] = "red"
line_95_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_95_live["font"] = ftl
line_95_live["justify"] = "left"
line_95_live["anchor"] = "w"
line_95_live["relief"] = "flat"
line_95_live.place(x=800, y=3965, width=70, height=33)

line_95_disabled = tk.Label(scrollframe)
line_95_disabled["bg"] = "#adafae"
line_95_disabled["fg"] = "red"
line_95_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_95_disabled["font"] = ftl
line_95_disabled["justify"] = "left"
line_95_disabled["anchor"] = "w"
line_95_disabled["relief"] = "flat"
line_95_disabled.place(x=650, y=3965, width=150, height=33)

line_96_frame = tk.Label(scrollframe)
line_96_frame["bg"] = "#adafae"
line_96_frame["text"] = ""
line_96_frame["relief"] = "sunken"
line_96_frame.place(x=10, y=4000, width=1060, height=40)

line_96_index = tk.Label(scrollframe)
line_96_index["bg"] = "#adafae"
line_96_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_96_index["font"] = ft
line_96_index["justify"] = "left"
line_96_index["anchor"] = "w"
line_96_index.place(x=20, y=4005, width=150, height=33)

line_96_name = tk.Label(scrollframe)
line_96_name["bg"] = "#adafae"
line_96_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_96_name["font"] = ft
line_96_name["justify"] = "left"
line_96_name["anchor"] = "w"
line_96_name.place(x=250, y=4005, width=500, height=33)

line_96_duration = tk.Label(scrollframe)
line_96_duration["bg"] = "#adafae"
line_96_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_96_duration["font"] = ft
line_96_duration["justify"] = "right"
line_96_duration["anchor"] = "e"
line_96_duration.place(x=910, y=4005, width=150, height=33)

line_96_live = tk.Label(scrollframe)
line_96_live["bg"] = "#adafae"
line_96_live["fg"] = "red"
line_96_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_96_live["font"] = ftl
line_96_live["justify"] = "left"
line_96_live["anchor"] = "w"
line_96_live["relief"] = "flat"
line_96_live.place(x=800, y=4005, width=70, height=33)

line_96_disabled = tk.Label(scrollframe)
line_96_disabled["bg"] = "#adafae"
line_96_disabled["fg"] = "red"
line_96_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_96_disabled["font"] = ftl
line_96_disabled["justify"] = "left"
line_96_disabled["anchor"] = "w"
line_96_disabled["relief"] = "flat"
line_96_disabled.place(x=650, y=4005, width=150, height=33)

line_97_frame = tk.Label(scrollframe)
line_97_frame["bg"] = "#adafae"
line_97_frame["text"] = ""
line_97_frame["relief"] = "sunken"
line_97_frame.place(x=10, y=4040, width=1060, height=40)

line_97_index = tk.Label(scrollframe)
line_97_index["bg"] = "#adafae"
line_97_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_97_index["font"] = ft
line_97_index["justify"] = "left"
line_97_index["anchor"] = "w"
line_97_index.place(x=20, y=4045, width=150, height=33)

line_97_name = tk.Label(scrollframe)
line_97_name["bg"] = "#adafae"
line_97_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_97_name["font"] = ft
line_97_name["justify"] = "left"
line_97_name["anchor"] = "w"
line_97_name.place(x=250, y=4045, width=500, height=33)

line_97_duration = tk.Label(scrollframe)
line_97_duration["bg"] = "#adafae"
line_97_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_97_duration["font"] = ft
line_97_duration["justify"] = "right"
line_97_duration["anchor"] = "e"
line_97_duration.place(x=910, y=4045, width=150, height=33)

line_97_live = tk.Label(scrollframe)
line_97_live["bg"] = "#adafae"
line_97_live["fg"] = "red"
line_97_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_97_live["font"] = ftl
line_97_live["justify"] = "left"
line_97_live["anchor"] = "w"
line_97_live["relief"] = "flat"
line_97_live.place(x=800, y=4045, width=70, height=33)

line_97_disabled = tk.Label(scrollframe)
line_97_disabled["bg"] = "#adafae"
line_97_disabled["fg"] = "red"
line_97_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_97_disabled["font"] = ftl
line_97_disabled["justify"] = "left"
line_97_disabled["anchor"] = "w"
line_97_disabled["relief"] = "flat"
line_97_disabled.place(x=650, y=4045, width=150, height=33)

line_98_frame = tk.Label(scrollframe)
line_98_frame["bg"] = "#adafae"
line_98_frame["text"] = ""
line_98_frame["relief"] = "sunken"
line_98_frame.place(x=10, y=4080, width=1060, height=40)

line_98_index = tk.Label(scrollframe)
line_98_index["bg"] = "#adafae"
line_98_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_98_index["font"] = ft
line_98_index["justify"] = "left"
line_98_index["anchor"] = "w"
line_98_index.place(x=20, y=4085, width=150, height=33)

line_98_name = tk.Label(scrollframe)
line_98_name["bg"] = "#adafae"
line_98_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_98_name["font"] = ft
line_98_name["justify"] = "left"
line_98_name["anchor"] = "w"
line_98_name.place(x=250, y=4085, width=500, height=33)

line_98_duration = tk.Label(scrollframe)
line_98_duration["bg"] = "#adafae"
line_98_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_98_duration["font"] = ft
line_98_duration["justify"] = "right"
line_98_duration["anchor"] = "e"
line_98_duration.place(x=910, y=4085, width=150, height=33)

line_98_live = tk.Label(scrollframe)
line_98_live["bg"] = "#adafae"
line_98_live["fg"] = "red"
line_98_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_98_live["font"] = ftl
line_98_live["justify"] = "left"
line_98_live["anchor"] = "w"
line_98_live["relief"] = "flat"
line_98_live.place(x=800, y=4085, width=70, height=33)

line_98_disabled = tk.Label(scrollframe)
line_98_disabled["bg"] = "#adafae"
line_98_disabled["fg"] = "red"
line_98_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_98_disabled["font"] = ftl
line_98_disabled["justify"] = "left"
line_98_disabled["anchor"] = "w"
line_98_disabled["relief"] = "flat"
line_98_disabled.place(x=650, y=4085, width=150, height=33)

line_99_frame = tk.Label(scrollframe)
line_99_frame["bg"] = "#adafae"
line_99_frame["text"] = ""
line_99_frame["relief"] = "sunken"
line_99_frame.place(x=10, y=4120, width=1060, height=40)

line_99_index = tk.Label(scrollframe)
line_99_index["bg"] = "#adafae"
line_99_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_99_index["font"] = ft
line_99_index["justify"] = "left"
line_99_index["anchor"] = "w"
line_99_index.place(x=20, y=4125, width=150, height=33)

line_99_name = tk.Label(scrollframe)
line_99_name["bg"] = "#adafae"
line_99_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_99_name["font"] = ft
line_99_name["justify"] = "left"
line_99_name["anchor"] = "w"
line_99_name.place(x=250, y=4125, width=500, height=33)

line_99_duration = tk.Label(scrollframe)
line_99_duration["bg"] = "#adafae"
line_99_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_99_duration["font"] = ft
line_99_duration["justify"] = "right"
line_99_duration["anchor"] = "e"
line_99_duration.place(x=910, y=4125, width=150, height=33)

line_99_live = tk.Label(scrollframe)
line_99_live["bg"] = "#adafae"
line_99_live["fg"] = "red"
line_99_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_99_live["font"] = ftl
line_99_live["justify"] = "left"
line_99_live["anchor"] = "w"
line_99_live["relief"] = "flat"
line_99_live.place(x=800, y=4125, width=70, height=33)

line_99_disabled = tk.Label(scrollframe)
line_99_disabled["bg"] = "#adafae"
line_99_disabled["fg"] = "red"
line_99_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_99_disabled["font"] = ftl
line_99_disabled["justify"] = "left"
line_99_disabled["anchor"] = "w"
line_99_disabled["relief"] = "flat"
line_99_disabled.place(x=650, y=4125, width=150, height=33)

line_100_frame = tk.Label(scrollframe)
line_100_frame["bg"] = "#adafae"
line_100_frame["text"] = ""
line_100_frame["relief"] = "sunken"
line_100_frame.place(x=10, y=4160, width=1060, height=40)

line_100_index = tk.Label(scrollframe)
line_100_index["bg"] = "#adafae"
line_100_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_100_index["font"] = ft
line_100_index["justify"] = "left"
line_100_index["anchor"] = "w"
line_100_index.place(x=20, y=4165, width=150, height=33)

line_100_name = tk.Label(scrollframe)
line_100_name["bg"] = "#adafae"
line_100_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_100_name["font"] = ft
line_100_name["justify"] = "left"
line_100_name["anchor"] = "w"
line_100_name.place(x=250, y=4165, width=500, height=33)

line_100_duration = tk.Label(scrollframe)
line_100_duration["bg"] = "#adafae"
line_100_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_100_duration["font"] = ft
line_100_duration["justify"] = "right"
line_100_duration["anchor"] = "e"
line_100_duration.place(x=910, y=4165, width=150, height=33)

line_100_live = tk.Label(scrollframe)
line_100_live["bg"] = "#adafae"
line_100_live["fg"] = "red"
line_100_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_100_live["font"] = ftl
line_100_live["justify"] = "left"
line_100_live["anchor"] = "w"
line_100_live["relief"] = "flat"
line_100_live.place(x=800, y=4165, width=70, height=33)

line_100_disabled = tk.Label(scrollframe)
line_100_disabled["bg"] = "#adafae"
line_100_disabled["fg"] = "red"
line_100_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_100_disabled["font"] = ftl
line_100_disabled["justify"] = "left"
line_100_disabled["anchor"] = "w"
line_100_disabled["relief"] = "flat"
line_100_disabled.place(x=650, y=4165, width=150, height=33)

line_101_frame = tk.Label(maincanvas)
line_101_frame["bg"] = "#adafae"
line_101_frame["text"] = ""
line_101_frame["relief"] = "sunken"
line_101_frame.place(x=10, y=4200, width=1060, height=40)

line_101_index = tk.Label(maincanvas)
line_101_index["bg"] = "#adafae"
line_101_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_101_index["font"] = ft
line_101_index["justify"] = "left"
line_101_index["anchor"] = "w"
line_101_index.place(x=20, y=4205, width=150, height=33)

line_101_name = tk.Label(maincanvas)
line_101_name["bg"] = "#adafae"
line_101_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_101_name["font"] = ft
line_101_name["justify"] = "left"
line_101_name["anchor"] = "w"
line_101_name.place(x=250, y=4205, width=500, height=33)

line_101_duration = tk.Label(maincanvas)
line_101_duration["bg"] = "#adafae"
line_101_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_101_duration["font"] = ft
line_101_duration["justify"] = "right"
line_101_duration["anchor"] = "e"
line_101_duration.place(x=910, y=4205, width=150, height=33)

line_101_live = tk.Label(maincanvas)
line_101_live["bg"] = "#adafae"
line_101_live["fg"] = "red"
line_101_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_101_live["font"] = ftl
line_101_live["justify"] = "left"
line_101_live["anchor"] = "w"
line_101_live["relief"] = "flat"
line_101_live.place(x=800, y=4205, width=70, height=33)

line_101_disabled = tk.Label(maincanvas)
line_101_disabled["bg"] = "#adafae"
line_101_disabled["fg"] = "red"
line_101_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_101_disabled["font"] = ftl
line_101_disabled["justify"] = "left"
line_101_disabled["anchor"] = "w"
line_101_disabled["relief"] = "flat"
line_101_disabled.place(x=650, y=4205, width=150, height=33)

line_102_frame = tk.Label(maincanvas)
line_102_frame["bg"] = "#adafae"
line_102_frame["text"] = ""
line_102_frame["relief"] = "sunken"
line_102_frame.place(x=10, y=4240, width=1060, height=40)

line_102_index = tk.Label(maincanvas)
line_102_index["bg"] = "#adafae"
line_102_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_102_index["font"] = ft
line_102_index["justify"] = "left"
line_102_index["anchor"] = "w"
line_102_index.place(x=20, y=4245, width=150, height=33)

line_102_name = tk.Label(maincanvas)
line_102_name["bg"] = "#adafae"
line_102_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_102_name["font"] = ft
line_102_name["justify"] = "left"
line_102_name["anchor"] = "w"
line_102_name.place(x=250, y=4245, width=500, height=33)

line_102_duration = tk.Label(maincanvas)
line_102_duration["bg"] = "#adafae"
line_102_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_102_duration["font"] = ft
line_102_duration["justify"] = "right"
line_102_duration["anchor"] = "e"
line_102_duration.place(x=910, y=4245, width=150, height=33)

line_102_live = tk.Label(maincanvas)
line_102_live["bg"] = "#adafae"
line_102_live["fg"] = "red"
line_102_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_102_live["font"] = ftl
line_102_live["justify"] = "left"
line_102_live["anchor"] = "w"
line_102_live["relief"] = "flat"
line_102_live.place(x=800, y=4245, width=70, height=33)

line_102_disabled = tk.Label(maincanvas)
line_102_disabled["bg"] = "#adafae"
line_102_disabled["fg"] = "red"
line_102_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_102_disabled["font"] = ftl
line_102_disabled["justify"] = "left"
line_102_disabled["anchor"] = "w"
line_102_disabled["relief"] = "flat"
line_102_disabled.place(x=650, y=4245, width=150, height=33)

line_103_frame = tk.Label(maincanvas)
line_103_frame["bg"] = "#adafae"
line_103_frame["text"] = ""
line_103_frame["relief"] = "sunken"
line_103_frame.place(x=10, y=4280, width=1060, height=40)

line_103_index = tk.Label(maincanvas)
line_103_index["bg"] = "#adafae"
line_103_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_103_index["font"] = ft
line_103_index["justify"] = "left"
line_103_index["anchor"] = "w"
line_103_index.place(x=20, y=4285, width=150, height=33)

line_103_name = tk.Label(maincanvas)
line_103_name["bg"] = "#adafae"
line_103_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_103_name["font"] = ft
line_103_name["justify"] = "left"
line_103_name["anchor"] = "w"
line_103_name.place(x=250, y=4285, width=500, height=33)

line_103_duration = tk.Label(maincanvas)
line_103_duration["bg"] = "#adafae"
line_103_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_103_duration["font"] = ft
line_103_duration["justify"] = "right"
line_103_duration["anchor"] = "e"
line_103_duration.place(x=910, y=4285, width=150, height=33)

line_103_live = tk.Label(maincanvas)
line_103_live["bg"] = "#adafae"
line_103_live["fg"] = "red"
line_103_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_103_live["font"] = ftl
line_103_live["justify"] = "left"
line_103_live["anchor"] = "w"
line_103_live["relief"] = "flat"
line_103_live.place(x=800, y=4285, width=70, height=33)

line_103_disabled = tk.Label(maincanvas)
line_103_disabled["bg"] = "#adafae"
line_103_disabled["fg"] = "red"
line_103_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_103_disabled["font"] = ftl
line_103_disabled["justify"] = "left"
line_103_disabled["anchor"] = "w"
line_103_disabled["relief"] = "flat"
line_103_disabled.place(x=650, y=4285, width=150, height=33)

line_104_frame = tk.Label(maincanvas)
line_104_frame["bg"] = "#adafae"
line_104_frame["text"] = ""
line_104_frame["relief"] = "sunken"
line_104_frame.place(x=10, y=4320, width=1060, height=40)

line_104_index = tk.Label(maincanvas)
line_104_index["bg"] = "#adafae"
line_104_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_104_index["font"] = ft
line_104_index["justify"] = "left"
line_104_index["anchor"] = "w"
line_104_index.place(x=20, y=4325, width=150, height=33)

line_104_name = tk.Label(maincanvas)
line_104_name["bg"] = "#adafae"
line_104_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_104_name["font"] = ft
line_104_name["justify"] = "left"
line_104_name["anchor"] = "w"
line_104_name.place(x=250, y=4325, width=500, height=33)

line_104_duration = tk.Label(maincanvas)
line_104_duration["bg"] = "#adafae"
line_104_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_104_duration["font"] = ft
line_104_duration["justify"] = "right"
line_104_duration["anchor"] = "e"
line_104_duration.place(x=910, y=4325, width=150, height=33)

line_104_live = tk.Label(maincanvas)
line_104_live["bg"] = "#adafae"
line_104_live["fg"] = "red"
line_104_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_104_live["font"] = ftl
line_104_live["justify"] = "left"
line_104_live["anchor"] = "w"
line_104_live["relief"] = "flat"
line_104_live.place(x=800, y=4325, width=70, height=33)

line_104_disabled = tk.Label(maincanvas)
line_104_disabled["bg"] = "#adafae"
line_104_disabled["fg"] = "red"
line_104_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_104_disabled["font"] = ftl
line_104_disabled["justify"] = "left"
line_104_disabled["anchor"] = "w"
line_104_disabled["relief"] = "flat"
line_104_disabled.place(x=650, y=4325, width=150, height=33)

line_105_frame = tk.Label(maincanvas)
line_105_frame["bg"] = "#adafae"
line_105_frame["text"] = ""
line_105_frame["relief"] = "sunken"
line_105_frame.place(x=10, y=4360, width=1060, height=40)

line_105_index = tk.Label(maincanvas)
line_105_index["bg"] = "#adafae"
line_105_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_105_index["font"] = ft
line_105_index["justify"] = "left"
line_105_index["anchor"] = "w"
line_105_index.place(x=20, y=4365, width=150, height=33)

line_105_name = tk.Label(maincanvas)
line_105_name["bg"] = "#adafae"
line_105_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_105_name["font"] = ft
line_105_name["justify"] = "left"
line_105_name["anchor"] = "w"
line_105_name.place(x=250, y=4365, width=500, height=33)

line_105_duration = tk.Label(maincanvas)
line_105_duration["bg"] = "#adafae"
line_105_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_105_duration["font"] = ft
line_105_duration["justify"] = "right"
line_105_duration["anchor"] = "e"
line_105_duration.place(x=910, y=4365, width=150, height=33)

line_105_live = tk.Label(maincanvas)
line_105_live["bg"] = "#adafae"
line_105_live["fg"] = "red"
line_105_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_105_live["font"] = ftl
line_105_live["justify"] = "left"
line_105_live["anchor"] = "w"
line_105_live["relief"] = "flat"
line_105_live.place(x=800, y=4365, width=70, height=33)

line_105_disabled = tk.Label(maincanvas)
line_105_disabled["bg"] = "#adafae"
line_105_disabled["fg"] = "red"
line_105_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_105_disabled["font"] = ftl
line_105_disabled["justify"] = "left"
line_105_disabled["anchor"] = "w"
line_105_disabled["relief"] = "flat"
line_105_disabled.place(x=650, y=4365, width=150, height=33)

line_106_frame = tk.Label(maincanvas)
line_106_frame["bg"] = "#adafae"
line_106_frame["text"] = ""
line_106_frame["relief"] = "sunken"
line_106_frame.place(x=10, y=4400, width=1060, height=40)

line_106_index = tk.Label(maincanvas)
line_106_index["bg"] = "#adafae"
line_106_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_106_index["font"] = ft
line_106_index["justify"] = "left"
line_106_index["anchor"] = "w"
line_106_index.place(x=20, y=4405, width=150, height=33)

line_106_name = tk.Label(maincanvas)
line_106_name["bg"] = "#adafae"
line_106_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_106_name["font"] = ft
line_106_name["justify"] = "left"
line_106_name["anchor"] = "w"
line_106_name.place(x=250, y=4405, width=500, height=33)

line_106_duration = tk.Label(maincanvas)
line_106_duration["bg"] = "#adafae"
line_106_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_106_duration["font"] = ft
line_106_duration["justify"] = "right"
line_106_duration["anchor"] = "e"
line_106_duration.place(x=910, y=4405, width=150, height=33)

line_106_live = tk.Label(maincanvas)
line_106_live["bg"] = "#adafae"
line_106_live["fg"] = "red"
line_106_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_106_live["font"] = ftl
line_106_live["justify"] = "left"
line_106_live["anchor"] = "w"
line_106_live["relief"] = "flat"
line_106_live.place(x=800, y=4405, width=70, height=33)

line_106_disabled = tk.Label(maincanvas)
line_106_disabled["bg"] = "#adafae"
line_106_disabled["fg"] = "red"
line_106_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_106_disabled["font"] = ftl
line_106_disabled["justify"] = "left"
line_106_disabled["anchor"] = "w"
line_106_disabled["relief"] = "flat"
line_106_disabled.place(x=650, y=4405, width=150, height=33)

line_107_frame = tk.Label(maincanvas)
line_107_frame["bg"] = "#adafae"
line_107_frame["text"] = ""
line_107_frame["relief"] = "sunken"
line_107_frame.place(x=10, y=4440, width=1060, height=40)

line_107_index = tk.Label(maincanvas)
line_107_index["bg"] = "#adafae"
line_107_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_107_index["font"] = ft
line_107_index["justify"] = "left"
line_107_index["anchor"] = "w"
line_107_index.place(x=20, y=4445, width=150, height=33)

line_107_name = tk.Label(maincanvas)
line_107_name["bg"] = "#adafae"
line_107_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_107_name["font"] = ft
line_107_name["justify"] = "left"
line_107_name["anchor"] = "w"
line_107_name.place(x=250, y=4445, width=500, height=33)

line_107_duration = tk.Label(maincanvas)
line_107_duration["bg"] = "#adafae"
line_107_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_107_duration["font"] = ft
line_107_duration["justify"] = "right"
line_107_duration["anchor"] = "e"
line_107_duration.place(x=910, y=4445, width=150, height=33)

line_107_live = tk.Label(maincanvas)
line_107_live["bg"] = "#adafae"
line_107_live["fg"] = "red"
line_107_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_107_live["font"] = ftl
line_107_live["justify"] = "left"
line_107_live["anchor"] = "w"
line_107_live["relief"] = "flat"
line_107_live.place(x=800, y=4445, width=70, height=33)

line_107_disabled = tk.Label(maincanvas)
line_107_disabled["bg"] = "#adafae"
line_107_disabled["fg"] = "red"
line_107_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_107_disabled["font"] = ftl
line_107_disabled["justify"] = "left"
line_107_disabled["anchor"] = "w"
line_107_disabled["relief"] = "flat"
line_107_disabled.place(x=650, y=4445, width=150, height=33)

line_108_frame = tk.Label(maincanvas)
line_108_frame["bg"] = "#adafae"
line_108_frame["text"] = ""
line_108_frame["relief"] = "sunken"
line_108_frame.place(x=10, y=4480, width=1060, height=40)

line_108_index = tk.Label(maincanvas)
line_108_index["bg"] = "#adafae"
line_108_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_108_index["font"] = ft
line_108_index["justify"] = "left"
line_108_index["anchor"] = "w"
line_108_index.place(x=20, y=4485, width=150, height=33)

line_108_name = tk.Label(maincanvas)
line_108_name["bg"] = "#adafae"
line_108_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_108_name["font"] = ft
line_108_name["justify"] = "left"
line_108_name["anchor"] = "w"
line_108_name.place(x=250, y=4485, width=500, height=33)

line_108_duration = tk.Label(maincanvas)
line_108_duration["bg"] = "#adafae"
line_108_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_108_duration["font"] = ft
line_108_duration["justify"] = "right"
line_108_duration["anchor"] = "e"
line_108_duration.place(x=910, y=4485, width=150, height=33)

line_108_live = tk.Label(maincanvas)
line_108_live["bg"] = "#adafae"
line_108_live["fg"] = "red"
line_108_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_108_live["font"] = ftl
line_108_live["justify"] = "left"
line_108_live["anchor"] = "w"
line_108_live["relief"] = "flat"
line_108_live.place(x=800, y=4485, width=70, height=33)

line_108_disabled = tk.Label(maincanvas)
line_108_disabled["bg"] = "#adafae"
line_108_disabled["fg"] = "red"
line_108_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_108_disabled["font"] = ftl
line_108_disabled["justify"] = "left"
line_108_disabled["anchor"] = "w"
line_108_disabled["relief"] = "flat"
line_108_disabled.place(x=650, y=4485, width=150, height=33)

line_109_frame = tk.Label(maincanvas)
line_109_frame["bg"] = "#adafae"
line_109_frame["text"] = ""
line_109_frame["relief"] = "sunken"
line_109_frame.place(x=10, y=4520, width=1060, height=40)

line_109_index = tk.Label(maincanvas)
line_109_index["bg"] = "#adafae"
line_109_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_109_index["font"] = ft
line_109_index["justify"] = "left"
line_109_index["anchor"] = "w"
line_109_index.place(x=20, y=4525, width=150, height=33)

line_109_name = tk.Label(maincanvas)
line_109_name["bg"] = "#adafae"
line_109_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_109_name["font"] = ft
line_109_name["justify"] = "left"
line_109_name["anchor"] = "w"
line_109_name.place(x=250, y=4525, width=500, height=33)

line_109_duration = tk.Label(maincanvas)
line_109_duration["bg"] = "#adafae"
line_109_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_109_duration["font"] = ft
line_109_duration["justify"] = "right"
line_109_duration["anchor"] = "e"
line_109_duration.place(x=910, y=4525, width=150, height=33)

line_109_live = tk.Label(maincanvas)
line_109_live["bg"] = "#adafae"
line_109_live["fg"] = "red"
line_109_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_109_live["font"] = ftl
line_109_live["justify"] = "left"
line_109_live["anchor"] = "w"
line_109_live["relief"] = "flat"
line_109_live.place(x=800, y=4525, width=70, height=33)

line_109_disabled = tk.Label(maincanvas)
line_109_disabled["bg"] = "#adafae"
line_109_disabled["fg"] = "red"
line_109_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_109_disabled["font"] = ftl
line_109_disabled["justify"] = "left"
line_109_disabled["anchor"] = "w"
line_109_disabled["relief"] = "flat"
line_109_disabled.place(x=650, y=4525, width=150, height=33)

line_110_frame = tk.Label(maincanvas)
line_110_frame["bg"] = "#adafae"
line_110_frame["text"] = ""
line_110_frame["relief"] = "sunken"
line_110_frame.place(x=10, y=4560, width=1060, height=40)

line_110_index = tk.Label(maincanvas)
line_110_index["bg"] = "#adafae"
line_110_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_110_index["font"] = ft
line_110_index["justify"] = "left"
line_110_index["anchor"] = "w"
line_110_index.place(x=20, y=4565, width=150, height=33)

line_110_name = tk.Label(maincanvas)
line_110_name["bg"] = "#adafae"
line_110_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_110_name["font"] = ft
line_110_name["justify"] = "left"
line_110_name["anchor"] = "w"
line_110_name.place(x=250, y=4565, width=500, height=33)

line_110_duration = tk.Label(maincanvas)
line_110_duration["bg"] = "#adafae"
line_110_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_110_duration["font"] = ft
line_110_duration["justify"] = "right"
line_110_duration["anchor"] = "e"
line_110_duration.place(x=910, y=4565, width=150, height=33)

line_110_live = tk.Label(maincanvas)
line_110_live["bg"] = "#adafae"
line_110_live["fg"] = "red"
line_110_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_110_live["font"] = ftl
line_110_live["justify"] = "left"
line_110_live["anchor"] = "w"
line_110_live["relief"] = "flat"
line_110_live.place(x=800, y=4565, width=70, height=33)

line_110_disabled = tk.Label(maincanvas)
line_110_disabled["bg"] = "#adafae"
line_110_disabled["fg"] = "red"
line_110_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_110_disabled["font"] = ftl
line_110_disabled["justify"] = "left"
line_110_disabled["anchor"] = "w"
line_110_disabled["relief"] = "flat"
line_110_disabled.place(x=650, y=4565, width=150, height=33)

line_111_frame = tk.Label(maincanvas)
line_111_frame["bg"] = "#adafae"
line_111_frame["text"] = ""
line_111_frame["relief"] = "sunken"
line_111_frame.place(x=10, y=4600, width=1060, height=40)

line_111_index = tk.Label(maincanvas)
line_111_index["bg"] = "#adafae"
line_111_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_111_index["font"] = ft
line_111_index["justify"] = "left"
line_111_index["anchor"] = "w"
line_111_index.place(x=20, y=4605, width=150, height=33)

line_111_name = tk.Label(maincanvas)
line_111_name["bg"] = "#adafae"
line_111_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_111_name["font"] = ft
line_111_name["justify"] = "left"
line_111_name["anchor"] = "w"
line_111_name.place(x=250, y=4605, width=500, height=33)

line_111_duration = tk.Label(maincanvas)
line_111_duration["bg"] = "#adafae"
line_111_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_111_duration["font"] = ft
line_111_duration["justify"] = "right"
line_111_duration["anchor"] = "e"
line_111_duration.place(x=910, y=4605, width=150, height=33)

line_111_live = tk.Label(maincanvas)
line_111_live["bg"] = "#adafae"
line_111_live["fg"] = "red"
line_111_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_111_live["font"] = ftl
line_111_live["justify"] = "left"
line_111_live["anchor"] = "w"
line_111_live["relief"] = "flat"
line_111_live.place(x=800, y=4605, width=70, height=33)

line_111_disabled = tk.Label(maincanvas)
line_111_disabled["bg"] = "#adafae"
line_111_disabled["fg"] = "red"
line_111_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_111_disabled["font"] = ftl
line_111_disabled["justify"] = "left"
line_111_disabled["anchor"] = "w"
line_111_disabled["relief"] = "flat"
line_111_disabled.place(x=650, y=4605, width=150, height=33)

line_112_frame = tk.Label(maincanvas)
line_112_frame["bg"] = "#adafae"
line_112_frame["text"] = ""
line_112_frame["relief"] = "sunken"
line_112_frame.place(x=10, y=4640, width=1060, height=40)

line_112_index = tk.Label(maincanvas)
line_112_index["bg"] = "#adafae"
line_112_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_112_index["font"] = ft
line_112_index["justify"] = "left"
line_112_index["anchor"] = "w"
line_112_index.place(x=20, y=4645, width=150, height=33)

line_112_name = tk.Label(maincanvas)
line_112_name["bg"] = "#adafae"
line_112_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_112_name["font"] = ft
line_112_name["justify"] = "left"
line_112_name["anchor"] = "w"
line_112_name.place(x=250, y=4645, width=500, height=33)

line_112_duration = tk.Label(maincanvas)
line_112_duration["bg"] = "#adafae"
line_112_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_112_duration["font"] = ft
line_112_duration["justify"] = "right"
line_112_duration["anchor"] = "e"
line_112_duration.place(x=910, y=4645, width=150, height=33)

line_112_live = tk.Label(maincanvas)
line_112_live["bg"] = "#adafae"
line_112_live["fg"] = "red"
line_112_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_112_live["font"] = ftl
line_112_live["justify"] = "left"
line_112_live["anchor"] = "w"
line_112_live["relief"] = "flat"
line_112_live.place(x=800, y=4645, width=70, height=33)

line_112_disabled = tk.Label(maincanvas)
line_112_disabled["bg"] = "#adafae"
line_112_disabled["fg"] = "red"
line_112_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_112_disabled["font"] = ftl
line_112_disabled["justify"] = "left"
line_112_disabled["anchor"] = "w"
line_112_disabled["relief"] = "flat"
line_112_disabled.place(x=650, y=4645, width=150, height=33)

line_113_frame = tk.Label(maincanvas)
line_113_frame["bg"] = "#adafae"
line_113_frame["text"] = ""
line_113_frame["relief"] = "sunken"
line_113_frame.place(x=10, y=4680, width=1060, height=40)

line_113_index = tk.Label(maincanvas)
line_113_index["bg"] = "#adafae"
line_113_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_113_index["font"] = ft
line_113_index["justify"] = "left"
line_113_index["anchor"] = "w"
line_113_index.place(x=20, y=4685, width=150, height=33)

line_113_name = tk.Label(maincanvas)
line_113_name["bg"] = "#adafae"
line_113_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_113_name["font"] = ft
line_113_name["justify"] = "left"
line_113_name["anchor"] = "w"
line_113_name.place(x=250, y=4685, width=500, height=33)

line_113_duration = tk.Label(maincanvas)
line_113_duration["bg"] = "#adafae"
line_113_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_113_duration["font"] = ft
line_113_duration["justify"] = "right"
line_113_duration["anchor"] = "e"
line_113_duration.place(x=910, y=4685, width=150, height=33)

line_113_live = tk.Label(maincanvas)
line_113_live["bg"] = "#adafae"
line_113_live["fg"] = "red"
line_113_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_113_live["font"] = ftl
line_113_live["justify"] = "left"
line_113_live["anchor"] = "w"
line_113_live["relief"] = "flat"
line_113_live.place(x=800, y=4685, width=70, height=33)

line_113_disabled = tk.Label(maincanvas)
line_113_disabled["bg"] = "#adafae"
line_113_disabled["fg"] = "red"
line_113_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_113_disabled["font"] = ftl
line_113_disabled["justify"] = "left"
line_113_disabled["anchor"] = "w"
line_113_disabled["relief"] = "flat"
line_113_disabled.place(x=650, y=4685, width=150, height=33)

line_114_frame = tk.Label(maincanvas)
line_114_frame["bg"] = "#adafae"
line_114_frame["text"] = ""
line_114_frame["relief"] = "sunken"
line_114_frame.place(x=10, y=4720, width=1060, height=40)

line_114_index = tk.Label(maincanvas)
line_114_index["bg"] = "#adafae"
line_114_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_114_index["font"] = ft
line_114_index["justify"] = "left"
line_114_index["anchor"] = "w"
line_114_index.place(x=20, y=4725, width=150, height=33)

line_114_name = tk.Label(maincanvas)
line_114_name["bg"] = "#adafae"
line_114_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_114_name["font"] = ft
line_114_name["justify"] = "left"
line_114_name["anchor"] = "w"
line_114_name.place(x=250, y=4725, width=500, height=33)

line_114_duration = tk.Label(maincanvas)
line_114_duration["bg"] = "#adafae"
line_114_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_114_duration["font"] = ft
line_114_duration["justify"] = "right"
line_114_duration["anchor"] = "e"
line_114_duration.place(x=910, y=4725, width=150, height=33)

line_114_live = tk.Label(maincanvas)
line_114_live["bg"] = "#adafae"
line_114_live["fg"] = "red"
line_114_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_114_live["font"] = ftl
line_114_live["justify"] = "left"
line_114_live["anchor"] = "w"
line_114_live["relief"] = "flat"
line_114_live.place(x=800, y=4725, width=70, height=33)

line_114_disabled = tk.Label(maincanvas)
line_114_disabled["bg"] = "#adafae"
line_114_disabled["fg"] = "red"
line_114_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_114_disabled["font"] = ftl
line_114_disabled["justify"] = "left"
line_114_disabled["anchor"] = "w"
line_114_disabled["relief"] = "flat"
line_114_disabled.place(x=650, y=4725, width=150, height=33)

line_115_frame = tk.Label(maincanvas)
line_115_frame["bg"] = "#adafae"
line_115_frame["text"] = ""
line_115_frame["relief"] = "sunken"
line_115_frame.place(x=10, y=4760, width=1060, height=40)

line_115_index = tk.Label(maincanvas)
line_115_index["bg"] = "#adafae"
line_115_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_115_index["font"] = ft
line_115_index["justify"] = "left"
line_115_index["anchor"] = "w"
line_115_index.place(x=20, y=4765, width=150, height=33)

line_115_name = tk.Label(maincanvas)
line_115_name["bg"] = "#adafae"
line_115_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_115_name["font"] = ft
line_115_name["justify"] = "left"
line_115_name["anchor"] = "w"
line_115_name.place(x=250, y=4765, width=500, height=33)

line_115_duration = tk.Label(maincanvas)
line_115_duration["bg"] = "#adafae"
line_115_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_115_duration["font"] = ft
line_115_duration["justify"] = "right"
line_115_duration["anchor"] = "e"
line_115_duration.place(x=910, y=4765, width=150, height=33)

line_115_live = tk.Label(maincanvas)
line_115_live["bg"] = "#adafae"
line_115_live["fg"] = "red"
line_115_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_115_live["font"] = ftl
line_115_live["justify"] = "left"
line_115_live["anchor"] = "w"
line_115_live["relief"] = "flat"
line_115_live.place(x=800, y=4765, width=70, height=33)

line_115_disabled = tk.Label(maincanvas)
line_115_disabled["bg"] = "#adafae"
line_115_disabled["fg"] = "red"
line_115_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_115_disabled["font"] = ftl
line_115_disabled["justify"] = "left"
line_115_disabled["anchor"] = "w"
line_115_disabled["relief"] = "flat"
line_115_disabled.place(x=650, y=4765, width=150, height=33)

line_116_frame = tk.Label(maincanvas)
line_116_frame["bg"] = "#adafae"
line_116_frame["text"] = ""
line_116_frame["relief"] = "sunken"
line_116_frame.place(x=10, y=4800, width=1060, height=40)

line_116_index = tk.Label(maincanvas)
line_116_index["bg"] = "#adafae"
line_116_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_116_index["font"] = ft
line_116_index["justify"] = "left"
line_116_index["anchor"] = "w"
line_116_index.place(x=20, y=4805, width=150, height=33)

line_116_name = tk.Label(maincanvas)
line_116_name["bg"] = "#adafae"
line_116_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_116_name["font"] = ft
line_116_name["justify"] = "left"
line_116_name["anchor"] = "w"
line_116_name.place(x=250, y=4805, width=500, height=33)

line_116_duration = tk.Label(maincanvas)
line_116_duration["bg"] = "#adafae"
line_116_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_116_duration["font"] = ft
line_116_duration["justify"] = "right"
line_116_duration["anchor"] = "e"
line_116_duration.place(x=910, y=4805, width=150, height=33)

line_116_live = tk.Label(maincanvas)
line_116_live["bg"] = "#adafae"
line_116_live["fg"] = "red"
line_116_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_116_live["font"] = ftl
line_116_live["justify"] = "left"
line_116_live["anchor"] = "w"
line_116_live["relief"] = "flat"
line_116_live.place(x=800, y=4805, width=70, height=33)

line_116_disabled = tk.Label(maincanvas)
line_116_disabled["bg"] = "#adafae"
line_116_disabled["fg"] = "red"
line_116_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_116_disabled["font"] = ftl
line_116_disabled["justify"] = "left"
line_116_disabled["anchor"] = "w"
line_116_disabled["relief"] = "flat"
line_116_disabled.place(x=650, y=4805, width=150, height=33)

line_117_frame = tk.Label(maincanvas)
line_117_frame["bg"] = "#adafae"
line_117_frame["text"] = ""
line_117_frame["relief"] = "sunken"
line_117_frame.place(x=10, y=4840, width=1060, height=40)

line_117_index = tk.Label(maincanvas)
line_117_index["bg"] = "#adafae"
line_117_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_117_index["font"] = ft
line_117_index["justify"] = "left"
line_117_index["anchor"] = "w"
line_117_index.place(x=20, y=4845, width=150, height=33)

line_117_name = tk.Label(maincanvas)
line_117_name["bg"] = "#adafae"
line_117_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_117_name["font"] = ft
line_117_name["justify"] = "left"
line_117_name["anchor"] = "w"
line_117_name.place(x=250, y=4845, width=500, height=33)

line_117_duration = tk.Label(maincanvas)
line_117_duration["bg"] = "#adafae"
line_117_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_117_duration["font"] = ft
line_117_duration["justify"] = "right"
line_117_duration["anchor"] = "e"
line_117_duration.place(x=910, y=4845, width=150, height=33)

line_117_live = tk.Label(maincanvas)
line_117_live["bg"] = "#adafae"
line_117_live["fg"] = "red"
line_117_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_117_live["font"] = ftl
line_117_live["justify"] = "left"
line_117_live["anchor"] = "w"
line_117_live["relief"] = "flat"
line_117_live.place(x=800, y=4845, width=70, height=33)

line_117_disabled = tk.Label(maincanvas)
line_117_disabled["bg"] = "#adafae"
line_117_disabled["fg"] = "red"
line_117_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_117_disabled["font"] = ftl
line_117_disabled["justify"] = "left"
line_117_disabled["anchor"] = "w"
line_117_disabled["relief"] = "flat"
line_117_disabled.place(x=650, y=4845, width=150, height=33)

line_118_frame = tk.Label(maincanvas)
line_118_frame["bg"] = "#adafae"
line_118_frame["text"] = ""
line_118_frame["relief"] = "sunken"
line_118_frame.place(x=10, y=4880, width=1060, height=40)

line_118_index = tk.Label(maincanvas)
line_118_index["bg"] = "#adafae"
line_118_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_118_index["font"] = ft
line_118_index["justify"] = "left"
line_118_index["anchor"] = "w"
line_118_index.place(x=20, y=4885, width=150, height=33)

line_118_name = tk.Label(maincanvas)
line_118_name["bg"] = "#adafae"
line_118_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_118_name["font"] = ft
line_118_name["justify"] = "left"
line_118_name["anchor"] = "w"
line_118_name.place(x=250, y=4885, width=500, height=33)

line_118_duration = tk.Label(maincanvas)
line_118_duration["bg"] = "#adafae"
line_118_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_118_duration["font"] = ft
line_118_duration["justify"] = "right"
line_118_duration["anchor"] = "e"
line_118_duration.place(x=910, y=4885, width=150, height=33)

line_118_live = tk.Label(maincanvas)
line_118_live["bg"] = "#adafae"
line_118_live["fg"] = "red"
line_118_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_118_live["font"] = ftl
line_118_live["justify"] = "left"
line_118_live["anchor"] = "w"
line_118_live["relief"] = "flat"
line_118_live.place(x=800, y=4885, width=70, height=33)

line_118_disabled = tk.Label(maincanvas)
line_118_disabled["bg"] = "#adafae"
line_118_disabled["fg"] = "red"
line_118_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_118_disabled["font"] = ftl
line_118_disabled["justify"] = "left"
line_118_disabled["anchor"] = "w"
line_118_disabled["relief"] = "flat"
line_118_disabled.place(x=650, y=4885, width=150, height=33)

line_119_frame = tk.Label(maincanvas)
line_119_frame["bg"] = "#adafae"
line_119_frame["text"] = ""
line_119_frame["relief"] = "sunken"
line_119_frame.place(x=10, y=4920, width=1060, height=40)

line_119_index = tk.Label(maincanvas)
line_119_index["bg"] = "#adafae"
line_119_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_119_index["font"] = ft
line_119_index["justify"] = "left"
line_119_index["anchor"] = "w"
line_119_index.place(x=20, y=4925, width=150, height=33)

line_119_name = tk.Label(maincanvas)
line_119_name["bg"] = "#adafae"
line_119_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_119_name["font"] = ft
line_119_name["justify"] = "left"
line_119_name["anchor"] = "w"
line_119_name.place(x=250, y=4925, width=500, height=33)

line_119_duration = tk.Label(maincanvas)
line_119_duration["bg"] = "#adafae"
line_119_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_119_duration["font"] = ft
line_119_duration["justify"] = "right"
line_119_duration["anchor"] = "e"
line_119_duration.place(x=910, y=4925, width=150, height=33)

line_119_live = tk.Label(maincanvas)
line_119_live["bg"] = "#adafae"
line_119_live["fg"] = "red"
line_119_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_119_live["font"] = ftl
line_119_live["justify"] = "left"
line_119_live["anchor"] = "w"
line_119_live["relief"] = "flat"
line_119_live.place(x=800, y=4925, width=70, height=33)

line_119_disabled = tk.Label(maincanvas)
line_119_disabled["bg"] = "#adafae"
line_119_disabled["fg"] = "red"
line_119_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_119_disabled["font"] = ftl
line_119_disabled["justify"] = "left"
line_119_disabled["anchor"] = "w"
line_119_disabled["relief"] = "flat"
line_119_disabled.place(x=650, y=4925, width=150, height=33)

line_120_frame = tk.Label(maincanvas)
line_120_frame["bg"] = "#adafae"
line_120_frame["text"] = ""
line_120_frame["relief"] = "sunken"
line_120_frame.place(x=10, y=4960, width=1060, height=40)

line_120_index = tk.Label(maincanvas)
line_120_index["bg"] = "#adafae"
line_120_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_120_index["font"] = ft
line_120_index["justify"] = "left"
line_120_index["anchor"] = "w"
line_120_index.place(x=20, y=4965, width=150, height=33)

line_120_name = tk.Label(maincanvas)
line_120_name["bg"] = "#adafae"
line_120_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_120_name["font"] = ft
line_120_name["justify"] = "left"
line_120_name["anchor"] = "w"
line_120_name.place(x=250, y=4965, width=500, height=33)

line_120_duration = tk.Label(maincanvas)
line_120_duration["bg"] = "#adafae"
line_120_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_120_duration["font"] = ft
line_120_duration["justify"] = "right"
line_120_duration["anchor"] = "e"
line_120_duration.place(x=910, y=4965, width=150, height=33)

line_120_live = tk.Label(maincanvas)
line_120_live["bg"] = "#adafae"
line_120_live["fg"] = "red"
line_120_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_120_live["font"] = ftl
line_120_live["justify"] = "left"
line_120_live["anchor"] = "w"
line_120_live["relief"] = "flat"
line_120_live.place(x=800, y=4965, width=70, height=33)

line_120_disabled = tk.Label(maincanvas)
line_120_disabled["bg"] = "#adafae"
line_120_disabled["fg"] = "red"
line_120_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_120_disabled["font"] = ftl
line_120_disabled["justify"] = "left"
line_120_disabled["anchor"] = "w"
line_120_disabled["relief"] = "flat"
line_120_disabled.place(x=650, y=4965, width=150, height=33)

line_121_frame = tk.Label(maincanvas)
line_121_frame["bg"] = "#adafae"
line_121_frame["text"] = ""
line_121_frame["relief"] = "sunken"
line_121_frame.place(x=10, y=5000, width=1060, height=40)

line_121_index = tk.Label(maincanvas)
line_121_index["bg"] = "#adafae"
line_121_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_121_index["font"] = ft
line_121_index["justify"] = "left"
line_121_index["anchor"] = "w"
line_121_index.place(x=20, y=5005, width=150, height=33)

line_121_name = tk.Label(maincanvas)
line_121_name["bg"] = "#adafae"
line_121_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_121_name["font"] = ft
line_121_name["justify"] = "left"
line_121_name["anchor"] = "w"
line_121_name.place(x=250, y=5005, width=500, height=33)

line_121_duration = tk.Label(maincanvas)
line_121_duration["bg"] = "#adafae"
line_121_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_121_duration["font"] = ft
line_121_duration["justify"] = "right"
line_121_duration["anchor"] = "e"
line_121_duration.place(x=910, y=5005, width=150, height=33)

line_121_live = tk.Label(maincanvas)
line_121_live["bg"] = "#adafae"
line_121_live["fg"] = "red"
line_121_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_121_live["font"] = ftl
line_121_live["justify"] = "left"
line_121_live["anchor"] = "w"
line_121_live["relief"] = "flat"
line_121_live.place(x=800, y=5005, width=70, height=33)

line_121_disabled = tk.Label(maincanvas)
line_121_disabled["bg"] = "#adafae"
line_121_disabled["fg"] = "red"
line_121_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_121_disabled["font"] = ftl
line_121_disabled["justify"] = "left"
line_121_disabled["anchor"] = "w"
line_121_disabled["relief"] = "flat"
line_121_disabled.place(x=650, y=5005, width=150, height=33)

line_122_frame = tk.Label(maincanvas)
line_122_frame["bg"] = "#adafae"
line_122_frame["text"] = ""
line_122_frame["relief"] = "sunken"
line_122_frame.place(x=10, y=5040, width=1060, height=40)

line_122_index = tk.Label(maincanvas)
line_122_index["bg"] = "#adafae"
line_122_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_122_index["font"] = ft
line_122_index["justify"] = "left"
line_122_index["anchor"] = "w"
line_122_index.place(x=20, y=5045, width=150, height=33)

line_122_name = tk.Label(maincanvas)
line_122_name["bg"] = "#adafae"
line_122_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_122_name["font"] = ft
line_122_name["justify"] = "left"
line_122_name["anchor"] = "w"
line_122_name.place(x=250, y=5045, width=500, height=33)

line_122_duration = tk.Label(maincanvas)
line_122_duration["bg"] = "#adafae"
line_122_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_122_duration["font"] = ft
line_122_duration["justify"] = "right"
line_122_duration["anchor"] = "e"
line_122_duration.place(x=910, y=5045, width=150, height=33)

line_122_live = tk.Label(maincanvas)
line_122_live["bg"] = "#adafae"
line_122_live["fg"] = "red"
line_122_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_122_live["font"] = ftl
line_122_live["justify"] = "left"
line_122_live["anchor"] = "w"
line_122_live["relief"] = "flat"
line_122_live.place(x=800, y=5045, width=70, height=33)

line_122_disabled = tk.Label(maincanvas)
line_122_disabled["bg"] = "#adafae"
line_122_disabled["fg"] = "red"
line_122_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_122_disabled["font"] = ftl
line_122_disabled["justify"] = "left"
line_122_disabled["anchor"] = "w"
line_122_disabled["relief"] = "flat"
line_122_disabled.place(x=650, y=5045, width=150, height=33)

line_123_frame = tk.Label(maincanvas)
line_123_frame["bg"] = "#adafae"
line_123_frame["text"] = ""
line_123_frame["relief"] = "sunken"
line_123_frame.place(x=10, y=5080, width=1060, height=40)

line_123_index = tk.Label(maincanvas)
line_123_index["bg"] = "#adafae"
line_123_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_123_index["font"] = ft
line_123_index["justify"] = "left"
line_123_index["anchor"] = "w"
line_123_index.place(x=20, y=5085, width=150, height=33)

line_123_name = tk.Label(maincanvas)
line_123_name["bg"] = "#adafae"
line_123_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_123_name["font"] = ft
line_123_name["justify"] = "left"
line_123_name["anchor"] = "w"
line_123_name.place(x=250, y=5085, width=500, height=33)

line_123_duration = tk.Label(maincanvas)
line_123_duration["bg"] = "#adafae"
line_123_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_123_duration["font"] = ft
line_123_duration["justify"] = "right"
line_123_duration["anchor"] = "e"
line_123_duration.place(x=910, y=5085, width=150, height=33)

line_123_live = tk.Label(maincanvas)
line_123_live["bg"] = "#adafae"
line_123_live["fg"] = "red"
line_123_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_123_live["font"] = ftl
line_123_live["justify"] = "left"
line_123_live["anchor"] = "w"
line_123_live["relief"] = "flat"
line_123_live.place(x=800, y=5085, width=70, height=33)

line_123_disabled = tk.Label(maincanvas)
line_123_disabled["bg"] = "#adafae"
line_123_disabled["fg"] = "red"
line_123_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_123_disabled["font"] = ftl
line_123_disabled["justify"] = "left"
line_123_disabled["anchor"] = "w"
line_123_disabled["relief"] = "flat"
line_123_disabled.place(x=650, y=5085, width=150, height=33)

line_124_frame = tk.Label(maincanvas)
line_124_frame["bg"] = "#adafae"
line_124_frame["text"] = ""
line_124_frame["relief"] = "sunken"
line_124_frame.place(x=10, y=5120, width=1060, height=40)

line_124_index = tk.Label(maincanvas)
line_124_index["bg"] = "#adafae"
line_124_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_124_index["font"] = ft
line_124_index["justify"] = "left"
line_124_index["anchor"] = "w"
line_124_index.place(x=20, y=5125, width=150, height=33)

line_124_name = tk.Label(maincanvas)
line_124_name["bg"] = "#adafae"
line_124_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_124_name["font"] = ft
line_124_name["justify"] = "left"
line_124_name["anchor"] = "w"
line_124_name.place(x=250, y=5125, width=500, height=33)

line_124_duration = tk.Label(maincanvas)
line_124_duration["bg"] = "#adafae"
line_124_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_124_duration["font"] = ft
line_124_duration["justify"] = "right"
line_124_duration["anchor"] = "e"
line_124_duration.place(x=910, y=5125, width=150, height=33)

line_124_live = tk.Label(maincanvas)
line_124_live["bg"] = "#adafae"
line_124_live["fg"] = "red"
line_124_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_124_live["font"] = ftl
line_124_live["justify"] = "left"
line_124_live["anchor"] = "w"
line_124_live["relief"] = "flat"
line_124_live.place(x=800, y=5125, width=70, height=33)

line_124_disabled = tk.Label(maincanvas)
line_124_disabled["bg"] = "#adafae"
line_124_disabled["fg"] = "red"
line_124_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_124_disabled["font"] = ftl
line_124_disabled["justify"] = "left"
line_124_disabled["anchor"] = "w"
line_124_disabled["relief"] = "flat"
line_124_disabled.place(x=650, y=5125, width=150, height=33)

line_125_frame = tk.Label(maincanvas)
line_125_frame["bg"] = "#adafae"
line_125_frame["text"] = ""
line_125_frame["relief"] = "sunken"
line_125_frame.place(x=10, y=5160, width=1060, height=40)

line_125_index = tk.Label(maincanvas)
line_125_index["bg"] = "#adafae"
line_125_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_125_index["font"] = ft
line_125_index["justify"] = "left"
line_125_index["anchor"] = "w"
line_125_index.place(x=20, y=5165, width=150, height=33)

line_125_name = tk.Label(maincanvas)
line_125_name["bg"] = "#adafae"
line_125_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_125_name["font"] = ft
line_125_name["justify"] = "left"
line_125_name["anchor"] = "w"
line_125_name.place(x=250, y=5165, width=500, height=33)

line_125_duration = tk.Label(maincanvas)
line_125_duration["bg"] = "#adafae"
line_125_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_125_duration["font"] = ft
line_125_duration["justify"] = "right"
line_125_duration["anchor"] = "e"
line_125_duration.place(x=910, y=5165, width=150, height=33)

line_125_live = tk.Label(maincanvas)
line_125_live["bg"] = "#adafae"
line_125_live["fg"] = "red"
line_125_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_125_live["font"] = ftl
line_125_live["justify"] = "left"
line_125_live["anchor"] = "w"
line_125_live["relief"] = "flat"
line_125_live.place(x=800, y=5165, width=70, height=33)

line_125_disabled = tk.Label(maincanvas)
line_125_disabled["bg"] = "#adafae"
line_125_disabled["fg"] = "red"
line_125_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_125_disabled["font"] = ftl
line_125_disabled["justify"] = "left"
line_125_disabled["anchor"] = "w"
line_125_disabled["relief"] = "flat"
line_125_disabled.place(x=650, y=5165, width=150, height=33)

line_126_frame = tk.Label(maincanvas)
line_126_frame["bg"] = "#adafae"
line_126_frame["text"] = ""
line_126_frame["relief"] = "sunken"
line_126_frame.place(x=10, y=5200, width=1060, height=40)

line_126_index = tk.Label(maincanvas)
line_126_index["bg"] = "#adafae"
line_126_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_126_index["font"] = ft
line_126_index["justify"] = "left"
line_126_index["anchor"] = "w"
line_126_index.place(x=20, y=5205, width=150, height=33)

line_126_name = tk.Label(maincanvas)
line_126_name["bg"] = "#adafae"
line_126_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_126_name["font"] = ft
line_126_name["justify"] = "left"
line_126_name["anchor"] = "w"
line_126_name.place(x=250, y=5205, width=500, height=33)

line_126_duration = tk.Label(maincanvas)
line_126_duration["bg"] = "#adafae"
line_126_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_126_duration["font"] = ft
line_126_duration["justify"] = "right"
line_126_duration["anchor"] = "e"
line_126_duration.place(x=910, y=5205, width=150, height=33)

line_126_live = tk.Label(maincanvas)
line_126_live["bg"] = "#adafae"
line_126_live["fg"] = "red"
line_126_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_126_live["font"] = ftl
line_126_live["justify"] = "left"
line_126_live["anchor"] = "w"
line_126_live["relief"] = "flat"
line_126_live.place(x=800, y=5205, width=70, height=33)

line_126_disabled = tk.Label(maincanvas)
line_126_disabled["bg"] = "#adafae"
line_126_disabled["fg"] = "red"
line_126_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_126_disabled["font"] = ftl
line_126_disabled["justify"] = "left"
line_126_disabled["anchor"] = "w"
line_126_disabled["relief"] = "flat"
line_126_disabled.place(x=650, y=5205, width=150, height=33)

line_127_frame = tk.Label(maincanvas)
line_127_frame["bg"] = "#adafae"
line_127_frame["text"] = ""
line_127_frame["relief"] = "sunken"
line_127_frame.place(x=10, y=5240, width=1060, height=40)

line_127_index = tk.Label(maincanvas)
line_127_index["bg"] = "#adafae"
line_127_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_127_index["font"] = ft
line_127_index["justify"] = "left"
line_127_index["anchor"] = "w"
line_127_index.place(x=20, y=5245, width=150, height=33)

line_127_name = tk.Label(maincanvas)
line_127_name["bg"] = "#adafae"
line_127_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_127_name["font"] = ft
line_127_name["justify"] = "left"
line_127_name["anchor"] = "w"
line_127_name.place(x=250, y=5245, width=500, height=33)

line_127_duration = tk.Label(maincanvas)
line_127_duration["bg"] = "#adafae"
line_127_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_127_duration["font"] = ft
line_127_duration["justify"] = "right"
line_127_duration["anchor"] = "e"
line_127_duration.place(x=910, y=5245, width=150, height=33)

line_127_live = tk.Label(maincanvas)
line_127_live["bg"] = "#adafae"
line_127_live["fg"] = "red"
line_127_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_127_live["font"] = ftl
line_127_live["justify"] = "left"
line_127_live["anchor"] = "w"
line_127_live["relief"] = "flat"
line_127_live.place(x=800, y=5245, width=70, height=33)

line_127_disabled = tk.Label(maincanvas)
line_127_disabled["bg"] = "#adafae"
line_127_disabled["fg"] = "red"
line_127_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_127_disabled["font"] = ftl
line_127_disabled["justify"] = "left"
line_127_disabled["anchor"] = "w"
line_127_disabled["relief"] = "flat"
line_127_disabled.place(x=650, y=5245, width=150, height=33)

line_128_frame = tk.Label(maincanvas)
line_128_frame["bg"] = "#adafae"
line_128_frame["text"] = ""
line_128_frame["relief"] = "sunken"
line_128_frame.place(x=10, y=5280, width=1060, height=40)

line_128_index = tk.Label(maincanvas)
line_128_index["bg"] = "#adafae"
line_128_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_128_index["font"] = ft
line_128_index["justify"] = "left"
line_128_index["anchor"] = "w"
line_128_index.place(x=20, y=5285, width=150, height=33)

line_128_name = tk.Label(maincanvas)
line_128_name["bg"] = "#adafae"
line_128_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_128_name["font"] = ft
line_128_name["justify"] = "left"
line_128_name["anchor"] = "w"
line_128_name.place(x=250, y=5285, width=500, height=33)

line_128_duration = tk.Label(maincanvas)
line_128_duration["bg"] = "#adafae"
line_128_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_128_duration["font"] = ft
line_128_duration["justify"] = "right"
line_128_duration["anchor"] = "e"
line_128_duration.place(x=910, y=5285, width=150, height=33)

line_128_live = tk.Label(maincanvas)
line_128_live["bg"] = "#adafae"
line_128_live["fg"] = "red"
line_128_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_128_live["font"] = ftl
line_128_live["justify"] = "left"
line_128_live["anchor"] = "w"
line_128_live["relief"] = "flat"
line_128_live.place(x=800, y=5285, width=70, height=33)

line_128_disabled = tk.Label(maincanvas)
line_128_disabled["bg"] = "#adafae"
line_128_disabled["fg"] = "red"
line_128_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_128_disabled["font"] = ftl
line_128_disabled["justify"] = "left"
line_128_disabled["anchor"] = "w"
line_128_disabled["relief"] = "flat"
line_128_disabled.place(x=650, y=5285, width=150, height=33)

line_129_frame = tk.Label(maincanvas)
line_129_frame["bg"] = "#adafae"
line_129_frame["text"] = ""
line_129_frame["relief"] = "sunken"
line_129_frame.place(x=10, y=5320, width=1060, height=40)

line_129_index = tk.Label(maincanvas)
line_129_index["bg"] = "#adafae"
line_129_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_129_index["font"] = ft
line_129_index["justify"] = "left"
line_129_index["anchor"] = "w"
line_129_index.place(x=20, y=5325, width=150, height=33)

line_129_name = tk.Label(maincanvas)
line_129_name["bg"] = "#adafae"
line_129_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_129_name["font"] = ft
line_129_name["justify"] = "left"
line_129_name["anchor"] = "w"
line_129_name.place(x=250, y=5325, width=500, height=33)

line_129_duration = tk.Label(maincanvas)
line_129_duration["bg"] = "#adafae"
line_129_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_129_duration["font"] = ft
line_129_duration["justify"] = "right"
line_129_duration["anchor"] = "e"
line_129_duration.place(x=910, y=5325, width=150, height=33)

line_129_live = tk.Label(maincanvas)
line_129_live["bg"] = "#adafae"
line_129_live["fg"] = "red"
line_129_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_129_live["font"] = ftl
line_129_live["justify"] = "left"
line_129_live["anchor"] = "w"
line_129_live["relief"] = "flat"
line_129_live.place(x=800, y=5325, width=70, height=33)

line_129_disabled = tk.Label(maincanvas)
line_129_disabled["bg"] = "#adafae"
line_129_disabled["fg"] = "red"
line_129_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_129_disabled["font"] = ftl
line_129_disabled["justify"] = "left"
line_129_disabled["anchor"] = "w"
line_129_disabled["relief"] = "flat"
line_129_disabled.place(x=650, y=5325, width=150, height=33)

line_130_frame = tk.Label(maincanvas)
line_130_frame["bg"] = "#adafae"
line_130_frame["text"] = ""
line_130_frame["relief"] = "sunken"
line_130_frame.place(x=10, y=5360, width=1060, height=40)

line_130_index = tk.Label(maincanvas)
line_130_index["bg"] = "#adafae"
line_130_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_130_index["font"] = ft
line_130_index["justify"] = "left"
line_130_index["anchor"] = "w"
line_130_index.place(x=20, y=5365, width=150, height=33)

line_130_name = tk.Label(maincanvas)
line_130_name["bg"] = "#adafae"
line_130_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_130_name["font"] = ft
line_130_name["justify"] = "left"
line_130_name["anchor"] = "w"
line_130_name.place(x=250, y=5365, width=500, height=33)

line_130_duration = tk.Label(maincanvas)
line_130_duration["bg"] = "#adafae"
line_130_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_130_duration["font"] = ft
line_130_duration["justify"] = "right"
line_130_duration["anchor"] = "e"
line_130_duration.place(x=910, y=5365, width=150, height=33)

line_130_live = tk.Label(maincanvas)
line_130_live["bg"] = "#adafae"
line_130_live["fg"] = "red"
line_130_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_130_live["font"] = ftl
line_130_live["justify"] = "left"
line_130_live["anchor"] = "w"
line_130_live["relief"] = "flat"
line_130_live.place(x=800, y=5365, width=70, height=33)

line_130_disabled = tk.Label(maincanvas)
line_130_disabled["bg"] = "#adafae"
line_130_disabled["fg"] = "red"
line_130_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_130_disabled["font"] = ftl
line_130_disabled["justify"] = "left"
line_130_disabled["anchor"] = "w"
line_130_disabled["relief"] = "flat"
line_130_disabled.place(x=650, y=5365, width=150, height=33)

line_131_frame = tk.Label(maincanvas)
line_131_frame["bg"] = "#adafae"
line_131_frame["text"] = ""
line_131_frame["relief"] = "sunken"
line_131_frame.place(x=10, y=5400, width=1060, height=40)

line_131_index = tk.Label(maincanvas)
line_131_index["bg"] = "#adafae"
line_131_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_131_index["font"] = ft
line_131_index["justify"] = "left"
line_131_index["anchor"] = "w"
line_131_index.place(x=20, y=5405, width=150, height=33)

line_131_name = tk.Label(maincanvas)
line_131_name["bg"] = "#adafae"
line_131_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_131_name["font"] = ft
line_131_name["justify"] = "left"
line_131_name["anchor"] = "w"
line_131_name.place(x=250, y=5405, width=500, height=33)

line_131_duration = tk.Label(maincanvas)
line_131_duration["bg"] = "#adafae"
line_131_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_131_duration["font"] = ft
line_131_duration["justify"] = "right"
line_131_duration["anchor"] = "e"
line_131_duration.place(x=910, y=5405, width=150, height=33)

line_131_live = tk.Label(maincanvas)
line_131_live["bg"] = "#adafae"
line_131_live["fg"] = "red"
line_131_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_131_live["font"] = ftl
line_131_live["justify"] = "left"
line_131_live["anchor"] = "w"
line_131_live["relief"] = "flat"
line_131_live.place(x=800, y=5405, width=70, height=33)

line_131_disabled = tk.Label(maincanvas)
line_131_disabled["bg"] = "#adafae"
line_131_disabled["fg"] = "red"
line_131_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_131_disabled["font"] = ftl
line_131_disabled["justify"] = "left"
line_131_disabled["anchor"] = "w"
line_131_disabled["relief"] = "flat"
line_131_disabled.place(x=650, y=5405, width=150, height=33)

line_132_frame = tk.Label(maincanvas)
line_132_frame["bg"] = "#adafae"
line_132_frame["text"] = ""
line_132_frame["relief"] = "sunken"
line_132_frame.place(x=10, y=5440, width=1060, height=40)

line_132_index = tk.Label(maincanvas)
line_132_index["bg"] = "#adafae"
line_132_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_132_index["font"] = ft
line_132_index["justify"] = "left"
line_132_index["anchor"] = "w"
line_132_index.place(x=20, y=5445, width=150, height=33)

line_132_name = tk.Label(maincanvas)
line_132_name["bg"] = "#adafae"
line_132_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_132_name["font"] = ft
line_132_name["justify"] = "left"
line_132_name["anchor"] = "w"
line_132_name.place(x=250, y=5445, width=500, height=33)

line_132_duration = tk.Label(maincanvas)
line_132_duration["bg"] = "#adafae"
line_132_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_132_duration["font"] = ft
line_132_duration["justify"] = "right"
line_132_duration["anchor"] = "e"
line_132_duration.place(x=910, y=5445, width=150, height=33)

line_132_live = tk.Label(maincanvas)
line_132_live["bg"] = "#adafae"
line_132_live["fg"] = "red"
line_132_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_132_live["font"] = ftl
line_132_live["justify"] = "left"
line_132_live["anchor"] = "w"
line_132_live["relief"] = "flat"
line_132_live.place(x=800, y=5445, width=70, height=33)

line_132_disabled = tk.Label(maincanvas)
line_132_disabled["bg"] = "#adafae"
line_132_disabled["fg"] = "red"
line_132_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_132_disabled["font"] = ftl
line_132_disabled["justify"] = "left"
line_132_disabled["anchor"] = "w"
line_132_disabled["relief"] = "flat"
line_132_disabled.place(x=650, y=5445, width=150, height=33)

line_133_frame = tk.Label(maincanvas)
line_133_frame["bg"] = "#adafae"
line_133_frame["text"] = ""
line_133_frame["relief"] = "sunken"
line_133_frame.place(x=10, y=5480, width=1060, height=40)

line_133_index = tk.Label(maincanvas)
line_133_index["bg"] = "#adafae"
line_133_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_133_index["font"] = ft
line_133_index["justify"] = "left"
line_133_index["anchor"] = "w"
line_133_index.place(x=20, y=5485, width=150, height=33)

line_133_name = tk.Label(maincanvas)
line_133_name["bg"] = "#adafae"
line_133_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_133_name["font"] = ft
line_133_name["justify"] = "left"
line_133_name["anchor"] = "w"
line_133_name.place(x=250, y=5485, width=500, height=33)

line_133_duration = tk.Label(maincanvas)
line_133_duration["bg"] = "#adafae"
line_133_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_133_duration["font"] = ft
line_133_duration["justify"] = "right"
line_133_duration["anchor"] = "e"
line_133_duration.place(x=910, y=5485, width=150, height=33)

line_133_live = tk.Label(maincanvas)
line_133_live["bg"] = "#adafae"
line_133_live["fg"] = "red"
line_133_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_133_live["font"] = ftl
line_133_live["justify"] = "left"
line_133_live["anchor"] = "w"
line_133_live["relief"] = "flat"
line_133_live.place(x=800, y=5485, width=70, height=33)

line_133_disabled = tk.Label(maincanvas)
line_133_disabled["bg"] = "#adafae"
line_133_disabled["fg"] = "red"
line_133_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_133_disabled["font"] = ftl
line_133_disabled["justify"] = "left"
line_133_disabled["anchor"] = "w"
line_133_disabled["relief"] = "flat"
line_133_disabled.place(x=650, y=5485, width=150, height=33)

line_134_frame = tk.Label(maincanvas)
line_134_frame["bg"] = "#adafae"
line_134_frame["text"] = ""
line_134_frame["relief"] = "sunken"
line_134_frame.place(x=10, y=5520, width=1060, height=40)

line_134_index = tk.Label(maincanvas)
line_134_index["bg"] = "#adafae"
line_134_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_134_index["font"] = ft
line_134_index["justify"] = "left"
line_134_index["anchor"] = "w"
line_134_index.place(x=20, y=5525, width=150, height=33)

line_134_name = tk.Label(maincanvas)
line_134_name["bg"] = "#adafae"
line_134_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_134_name["font"] = ft
line_134_name["justify"] = "left"
line_134_name["anchor"] = "w"
line_134_name.place(x=250, y=5525, width=500, height=33)

line_134_duration = tk.Label(maincanvas)
line_134_duration["bg"] = "#adafae"
line_134_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_134_duration["font"] = ft
line_134_duration["justify"] = "right"
line_134_duration["anchor"] = "e"
line_134_duration.place(x=910, y=5525, width=150, height=33)

line_134_live = tk.Label(maincanvas)
line_134_live["bg"] = "#adafae"
line_134_live["fg"] = "red"
line_134_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_134_live["font"] = ftl
line_134_live["justify"] = "left"
line_134_live["anchor"] = "w"
line_134_live["relief"] = "flat"
line_134_live.place(x=800, y=5525, width=70, height=33)

line_134_disabled = tk.Label(maincanvas)
line_134_disabled["bg"] = "#adafae"
line_134_disabled["fg"] = "red"
line_134_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_134_disabled["font"] = ftl
line_134_disabled["justify"] = "left"
line_134_disabled["anchor"] = "w"
line_134_disabled["relief"] = "flat"
line_134_disabled.place(x=650, y=5525, width=150, height=33)

line_135_frame = tk.Label(maincanvas)
line_135_frame["bg"] = "#adafae"
line_135_frame["text"] = ""
line_135_frame["relief"] = "sunken"
line_135_frame.place(x=10, y=5560, width=1060, height=40)

line_135_index = tk.Label(maincanvas)
line_135_index["bg"] = "#adafae"
line_135_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_135_index["font"] = ft
line_135_index["justify"] = "left"
line_135_index["anchor"] = "w"
line_135_index.place(x=20, y=5565, width=150, height=33)

line_135_name = tk.Label(maincanvas)
line_135_name["bg"] = "#adafae"
line_135_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_135_name["font"] = ft
line_135_name["justify"] = "left"
line_135_name["anchor"] = "w"
line_135_name.place(x=250, y=5565, width=500, height=33)

line_135_duration = tk.Label(maincanvas)
line_135_duration["bg"] = "#adafae"
line_135_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_135_duration["font"] = ft
line_135_duration["justify"] = "right"
line_135_duration["anchor"] = "e"
line_135_duration.place(x=910, y=5565, width=150, height=33)

line_135_live = tk.Label(maincanvas)
line_135_live["bg"] = "#adafae"
line_135_live["fg"] = "red"
line_135_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_135_live["font"] = ftl
line_135_live["justify"] = "left"
line_135_live["anchor"] = "w"
line_135_live["relief"] = "flat"
line_135_live.place(x=800, y=5565, width=70, height=33)

line_135_disabled = tk.Label(maincanvas)
line_135_disabled["bg"] = "#adafae"
line_135_disabled["fg"] = "red"
line_135_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_135_disabled["font"] = ftl
line_135_disabled["justify"] = "left"
line_135_disabled["anchor"] = "w"
line_135_disabled["relief"] = "flat"
line_135_disabled.place(x=650, y=5565, width=150, height=33)

line_136_frame = tk.Label(maincanvas)
line_136_frame["bg"] = "#adafae"
line_136_frame["text"] = ""
line_136_frame["relief"] = "sunken"
line_136_frame.place(x=10, y=5600, width=1060, height=40)

line_136_index = tk.Label(maincanvas)
line_136_index["bg"] = "#adafae"
line_136_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_136_index["font"] = ft
line_136_index["justify"] = "left"
line_136_index["anchor"] = "w"
line_136_index.place(x=20, y=5605, width=150, height=33)

line_136_name = tk.Label(maincanvas)
line_136_name["bg"] = "#adafae"
line_136_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_136_name["font"] = ft
line_136_name["justify"] = "left"
line_136_name["anchor"] = "w"
line_136_name.place(x=250, y=5605, width=500, height=33)

line_136_duration = tk.Label(maincanvas)
line_136_duration["bg"] = "#adafae"
line_136_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_136_duration["font"] = ft
line_136_duration["justify"] = "right"
line_136_duration["anchor"] = "e"
line_136_duration.place(x=910, y=5605, width=150, height=33)

line_136_live = tk.Label(maincanvas)
line_136_live["bg"] = "#adafae"
line_136_live["fg"] = "red"
line_136_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_136_live["font"] = ftl
line_136_live["justify"] = "left"
line_136_live["anchor"] = "w"
line_136_live["relief"] = "flat"
line_136_live.place(x=800, y=5605, width=70, height=33)

line_136_disabled = tk.Label(maincanvas)
line_136_disabled["bg"] = "#adafae"
line_136_disabled["fg"] = "red"
line_136_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_136_disabled["font"] = ftl
line_136_disabled["justify"] = "left"
line_136_disabled["anchor"] = "w"
line_136_disabled["relief"] = "flat"
line_136_disabled.place(x=650, y=5605, width=150, height=33)

line_137_frame = tk.Label(maincanvas)
line_137_frame["bg"] = "#adafae"
line_137_frame["text"] = ""
line_137_frame["relief"] = "sunken"
line_137_frame.place(x=10, y=5640, width=1060, height=40)

line_137_index = tk.Label(maincanvas)
line_137_index["bg"] = "#adafae"
line_137_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_137_index["font"] = ft
line_137_index["justify"] = "left"
line_137_index["anchor"] = "w"
line_137_index.place(x=20, y=5645, width=150, height=33)

line_137_name = tk.Label(maincanvas)
line_137_name["bg"] = "#adafae"
line_137_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_137_name["font"] = ft
line_137_name["justify"] = "left"
line_137_name["anchor"] = "w"
line_137_name.place(x=250, y=5645, width=500, height=33)

line_137_duration = tk.Label(maincanvas)
line_137_duration["bg"] = "#adafae"
line_137_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_137_duration["font"] = ft
line_137_duration["justify"] = "right"
line_137_duration["anchor"] = "e"
line_137_duration.place(x=910, y=5645, width=150, height=33)

line_137_live = tk.Label(maincanvas)
line_137_live["bg"] = "#adafae"
line_137_live["fg"] = "red"
line_137_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_137_live["font"] = ftl
line_137_live["justify"] = "left"
line_137_live["anchor"] = "w"
line_137_live["relief"] = "flat"
line_137_live.place(x=800, y=5645, width=70, height=33)

line_137_disabled = tk.Label(maincanvas)
line_137_disabled["bg"] = "#adafae"
line_137_disabled["fg"] = "red"
line_137_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_137_disabled["font"] = ftl
line_137_disabled["justify"] = "left"
line_137_disabled["anchor"] = "w"
line_137_disabled["relief"] = "flat"
line_137_disabled.place(x=650, y=5645, width=150, height=33)

line_138_frame = tk.Label(maincanvas)
line_138_frame["bg"] = "#adafae"
line_138_frame["text"] = ""
line_138_frame["relief"] = "sunken"
line_138_frame.place(x=10, y=5680, width=1060, height=40)

line_138_index = tk.Label(maincanvas)
line_138_index["bg"] = "#adafae"
line_138_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_138_index["font"] = ft
line_138_index["justify"] = "left"
line_138_index["anchor"] = "w"
line_138_index.place(x=20, y=5685, width=150, height=33)

line_138_name = tk.Label(maincanvas)
line_138_name["bg"] = "#adafae"
line_138_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_138_name["font"] = ft
line_138_name["justify"] = "left"
line_138_name["anchor"] = "w"
line_138_name.place(x=250, y=5685, width=500, height=33)

line_138_duration = tk.Label(maincanvas)
line_138_duration["bg"] = "#adafae"
line_138_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_138_duration["font"] = ft
line_138_duration["justify"] = "right"
line_138_duration["anchor"] = "e"
line_138_duration.place(x=910, y=5685, width=150, height=33)

line_138_live = tk.Label(maincanvas)
line_138_live["bg"] = "#adafae"
line_138_live["fg"] = "red"
line_138_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_138_live["font"] = ftl
line_138_live["justify"] = "left"
line_138_live["anchor"] = "w"
line_138_live["relief"] = "flat"
line_138_live.place(x=800, y=5685, width=70, height=33)

line_138_disabled = tk.Label(maincanvas)
line_138_disabled["bg"] = "#adafae"
line_138_disabled["fg"] = "red"
line_138_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_138_disabled["font"] = ftl
line_138_disabled["justify"] = "left"
line_138_disabled["anchor"] = "w"
line_138_disabled["relief"] = "flat"
line_138_disabled.place(x=650, y=5685, width=150, height=33)

line_139_frame = tk.Label(maincanvas)
line_139_frame["bg"] = "#adafae"
line_139_frame["text"] = ""
line_139_frame["relief"] = "sunken"
line_139_frame.place(x=10, y=5720, width=1060, height=40)

line_139_index = tk.Label(maincanvas)
line_139_index["bg"] = "#adafae"
line_139_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_139_index["font"] = ft
line_139_index["justify"] = "left"
line_139_index["anchor"] = "w"
line_139_index.place(x=20, y=5725, width=150, height=33)

line_139_name = tk.Label(maincanvas)
line_139_name["bg"] = "#adafae"
line_139_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_139_name["font"] = ft
line_139_name["justify"] = "left"
line_139_name["anchor"] = "w"
line_139_name.place(x=250, y=5725, width=500, height=33)

line_139_duration = tk.Label(maincanvas)
line_139_duration["bg"] = "#adafae"
line_139_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_139_duration["font"] = ft
line_139_duration["justify"] = "right"
line_139_duration["anchor"] = "e"
line_139_duration.place(x=910, y=5725, width=150, height=33)

line_139_live = tk.Label(maincanvas)
line_139_live["bg"] = "#adafae"
line_139_live["fg"] = "red"
line_139_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_139_live["font"] = ftl
line_139_live["justify"] = "left"
line_139_live["anchor"] = "w"
line_139_live["relief"] = "flat"
line_139_live.place(x=800, y=5725, width=70, height=33)

line_139_disabled = tk.Label(maincanvas)
line_139_disabled["bg"] = "#adafae"
line_139_disabled["fg"] = "red"
line_139_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_139_disabled["font"] = ftl
line_139_disabled["justify"] = "left"
line_139_disabled["anchor"] = "w"
line_139_disabled["relief"] = "flat"
line_139_disabled.place(x=650, y=5725, width=150, height=33)

line_140_frame = tk.Label(maincanvas)
line_140_frame["bg"] = "#adafae"
line_140_frame["text"] = ""
line_140_frame["relief"] = "sunken"
line_140_frame.place(x=10, y=5760, width=1060, height=40)

line_140_index = tk.Label(maincanvas)
line_140_index["bg"] = "#adafae"
line_140_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_140_index["font"] = ft
line_140_index["justify"] = "left"
line_140_index["anchor"] = "w"
line_140_index.place(x=20, y=5765, width=150, height=33)

line_140_name = tk.Label(maincanvas)
line_140_name["bg"] = "#adafae"
line_140_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_140_name["font"] = ft
line_140_name["justify"] = "left"
line_140_name["anchor"] = "w"
line_140_name.place(x=250, y=5765, width=500, height=33)

line_140_duration = tk.Label(maincanvas)
line_140_duration["bg"] = "#adafae"
line_140_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_140_duration["font"] = ft
line_140_duration["justify"] = "right"
line_140_duration["anchor"] = "e"
line_140_duration.place(x=910, y=5765, width=150, height=33)

line_140_live = tk.Label(maincanvas)
line_140_live["bg"] = "#adafae"
line_140_live["fg"] = "red"
line_140_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_140_live["font"] = ftl
line_140_live["justify"] = "left"
line_140_live["anchor"] = "w"
line_140_live["relief"] = "flat"
line_140_live.place(x=800, y=5765, width=70, height=33)

line_140_disabled = tk.Label(maincanvas)
line_140_disabled["bg"] = "#adafae"
line_140_disabled["fg"] = "red"
line_140_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_140_disabled["font"] = ftl
line_140_disabled["justify"] = "left"
line_140_disabled["anchor"] = "w"
line_140_disabled["relief"] = "flat"
line_140_disabled.place(x=650, y=5765, width=150, height=33)

line_141_frame = tk.Label(maincanvas)
line_141_frame["bg"] = "#adafae"
line_141_frame["text"] = ""
line_141_frame["relief"] = "sunken"
line_141_frame.place(x=10, y=5800, width=1060, height=40)

line_141_index = tk.Label(maincanvas)
line_141_index["bg"] = "#adafae"
line_141_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_141_index["font"] = ft
line_141_index["justify"] = "left"
line_141_index["anchor"] = "w"
line_141_index.place(x=20, y=5805, width=150, height=33)

line_141_name = tk.Label(maincanvas)
line_141_name["bg"] = "#adafae"
line_141_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_141_name["font"] = ft
line_141_name["justify"] = "left"
line_141_name["anchor"] = "w"
line_141_name.place(x=250, y=5805, width=500, height=33)

line_141_duration = tk.Label(maincanvas)
line_141_duration["bg"] = "#adafae"
line_141_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_141_duration["font"] = ft
line_141_duration["justify"] = "right"
line_141_duration["anchor"] = "e"
line_141_duration.place(x=910, y=5805, width=150, height=33)

line_141_live = tk.Label(maincanvas)
line_141_live["bg"] = "#adafae"
line_141_live["fg"] = "red"
line_141_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_141_live["font"] = ftl
line_141_live["justify"] = "left"
line_141_live["anchor"] = "w"
line_141_live["relief"] = "flat"
line_141_live.place(x=800, y=5805, width=70, height=33)

line_141_disabled = tk.Label(maincanvas)
line_141_disabled["bg"] = "#adafae"
line_141_disabled["fg"] = "red"
line_141_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_141_disabled["font"] = ftl
line_141_disabled["justify"] = "left"
line_141_disabled["anchor"] = "w"
line_141_disabled["relief"] = "flat"
line_141_disabled.place(x=650, y=5805, width=150, height=33)

line_142_frame = tk.Label(maincanvas)
line_142_frame["bg"] = "#adafae"
line_142_frame["text"] = ""
line_142_frame["relief"] = "sunken"
line_142_frame.place(x=10, y=5840, width=1060, height=40)

line_142_index = tk.Label(maincanvas)
line_142_index["bg"] = "#adafae"
line_142_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_142_index["font"] = ft
line_142_index["justify"] = "left"
line_142_index["anchor"] = "w"
line_142_index.place(x=20, y=5845, width=150, height=33)

line_142_name = tk.Label(maincanvas)
line_142_name["bg"] = "#adafae"
line_142_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_142_name["font"] = ft
line_142_name["justify"] = "left"
line_142_name["anchor"] = "w"
line_142_name.place(x=250, y=5845, width=500, height=33)

line_142_duration = tk.Label(maincanvas)
line_142_duration["bg"] = "#adafae"
line_142_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_142_duration["font"] = ft
line_142_duration["justify"] = "right"
line_142_duration["anchor"] = "e"
line_142_duration.place(x=910, y=5845, width=150, height=33)

line_142_live = tk.Label(maincanvas)
line_142_live["bg"] = "#adafae"
line_142_live["fg"] = "red"
line_142_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_142_live["font"] = ftl
line_142_live["justify"] = "left"
line_142_live["anchor"] = "w"
line_142_live["relief"] = "flat"
line_142_live.place(x=800, y=5845, width=70, height=33)

line_142_disabled = tk.Label(maincanvas)
line_142_disabled["bg"] = "#adafae"
line_142_disabled["fg"] = "red"
line_142_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_142_disabled["font"] = ftl
line_142_disabled["justify"] = "left"
line_142_disabled["anchor"] = "w"
line_142_disabled["relief"] = "flat"
line_142_disabled.place(x=650, y=5845, width=150, height=33)

line_143_frame = tk.Label(maincanvas)
line_143_frame["bg"] = "#adafae"
line_143_frame["text"] = ""
line_143_frame["relief"] = "sunken"
line_143_frame.place(x=10, y=5880, width=1060, height=40)

line_143_index = tk.Label(maincanvas)
line_143_index["bg"] = "#adafae"
line_143_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_143_index["font"] = ft
line_143_index["justify"] = "left"
line_143_index["anchor"] = "w"
line_143_index.place(x=20, y=5885, width=150, height=33)

line_143_name = tk.Label(maincanvas)
line_143_name["bg"] = "#adafae"
line_143_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_143_name["font"] = ft
line_143_name["justify"] = "left"
line_143_name["anchor"] = "w"
line_143_name.place(x=250, y=5885, width=500, height=33)

line_143_duration = tk.Label(maincanvas)
line_143_duration["bg"] = "#adafae"
line_143_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_143_duration["font"] = ft
line_143_duration["justify"] = "right"
line_143_duration["anchor"] = "e"
line_143_duration.place(x=910, y=5885, width=150, height=33)

line_143_live = tk.Label(maincanvas)
line_143_live["bg"] = "#adafae"
line_143_live["fg"] = "red"
line_143_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_143_live["font"] = ftl
line_143_live["justify"] = "left"
line_143_live["anchor"] = "w"
line_143_live["relief"] = "flat"
line_143_live.place(x=800, y=5885, width=70, height=33)

line_143_disabled = tk.Label(maincanvas)
line_143_disabled["bg"] = "#adafae"
line_143_disabled["fg"] = "red"
line_143_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_143_disabled["font"] = ftl
line_143_disabled["justify"] = "left"
line_143_disabled["anchor"] = "w"
line_143_disabled["relief"] = "flat"
line_143_disabled.place(x=650, y=5885, width=150, height=33)

line_144_frame = tk.Label(maincanvas)
line_144_frame["bg"] = "#adafae"
line_144_frame["text"] = ""
line_144_frame["relief"] = "sunken"
line_144_frame.place(x=10, y=5920, width=1060, height=40)

line_144_index = tk.Label(maincanvas)
line_144_index["bg"] = "#adafae"
line_144_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_144_index["font"] = ft
line_144_index["justify"] = "left"
line_144_index["anchor"] = "w"
line_144_index.place(x=20, y=5925, width=150, height=33)

line_144_name = tk.Label(maincanvas)
line_144_name["bg"] = "#adafae"
line_144_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_144_name["font"] = ft
line_144_name["justify"] = "left"
line_144_name["anchor"] = "w"
line_144_name.place(x=250, y=5925, width=500, height=33)

line_144_duration = tk.Label(maincanvas)
line_144_duration["bg"] = "#adafae"
line_144_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_144_duration["font"] = ft
line_144_duration["justify"] = "right"
line_144_duration["anchor"] = "e"
line_144_duration.place(x=910, y=5925, width=150, height=33)

line_144_live = tk.Label(maincanvas)
line_144_live["bg"] = "#adafae"
line_144_live["fg"] = "red"
line_144_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_144_live["font"] = ftl
line_144_live["justify"] = "left"
line_144_live["anchor"] = "w"
line_144_live["relief"] = "flat"
line_144_live.place(x=800, y=5925, width=70, height=33)

line_144_disabled = tk.Label(maincanvas)
line_144_disabled["bg"] = "#adafae"
line_144_disabled["fg"] = "red"
line_144_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_144_disabled["font"] = ftl
line_144_disabled["justify"] = "left"
line_144_disabled["anchor"] = "w"
line_144_disabled["relief"] = "flat"
line_144_disabled.place(x=650, y=5925, width=150, height=33)

line_145_frame = tk.Label(maincanvas)
line_145_frame["bg"] = "#adafae"
line_145_frame["text"] = ""
line_145_frame["relief"] = "sunken"
line_145_frame.place(x=10, y=5960, width=1060, height=40)

line_145_index = tk.Label(maincanvas)
line_145_index["bg"] = "#adafae"
line_145_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_145_index["font"] = ft
line_145_index["justify"] = "left"
line_145_index["anchor"] = "w"
line_145_index.place(x=20, y=5965, width=150, height=33)

line_145_name = tk.Label(maincanvas)
line_145_name["bg"] = "#adafae"
line_145_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_145_name["font"] = ft
line_145_name["justify"] = "left"
line_145_name["anchor"] = "w"
line_145_name.place(x=250, y=5965, width=500, height=33)

line_145_duration = tk.Label(maincanvas)
line_145_duration["bg"] = "#adafae"
line_145_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_145_duration["font"] = ft
line_145_duration["justify"] = "right"
line_145_duration["anchor"] = "e"
line_145_duration.place(x=910, y=5965, width=150, height=33)

line_145_live = tk.Label(maincanvas)
line_145_live["bg"] = "#adafae"
line_145_live["fg"] = "red"
line_145_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_145_live["font"] = ftl
line_145_live["justify"] = "left"
line_145_live["anchor"] = "w"
line_145_live["relief"] = "flat"
line_145_live.place(x=800, y=5965, width=70, height=33)

line_145_disabled = tk.Label(maincanvas)
line_145_disabled["bg"] = "#adafae"
line_145_disabled["fg"] = "red"
line_145_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_145_disabled["font"] = ftl
line_145_disabled["justify"] = "left"
line_145_disabled["anchor"] = "w"
line_145_disabled["relief"] = "flat"
line_145_disabled.place(x=650, y=5965, width=150, height=33)

line_146_frame = tk.Label(maincanvas)
line_146_frame["bg"] = "#adafae"
line_146_frame["text"] = ""
line_146_frame["relief"] = "sunken"
line_146_frame.place(x=10, y=6000, width=1060, height=40)

line_146_index = tk.Label(maincanvas)
line_146_index["bg"] = "#adafae"
line_146_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_146_index["font"] = ft
line_146_index["justify"] = "left"
line_146_index["anchor"] = "w"
line_146_index.place(x=20, y=6005, width=150, height=33)

line_146_name = tk.Label(maincanvas)
line_146_name["bg"] = "#adafae"
line_146_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_146_name["font"] = ft
line_146_name["justify"] = "left"
line_146_name["anchor"] = "w"
line_146_name.place(x=250, y=6005, width=500, height=33)

line_146_duration = tk.Label(maincanvas)
line_146_duration["bg"] = "#adafae"
line_146_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_146_duration["font"] = ft
line_146_duration["justify"] = "right"
line_146_duration["anchor"] = "e"
line_146_duration.place(x=910, y=6005, width=150, height=33)

line_146_live = tk.Label(maincanvas)
line_146_live["bg"] = "#adafae"
line_146_live["fg"] = "red"
line_146_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_146_live["font"] = ftl
line_146_live["justify"] = "left"
line_146_live["anchor"] = "w"
line_146_live["relief"] = "flat"
line_146_live.place(x=800, y=6005, width=70, height=33)

line_146_disabled = tk.Label(maincanvas)
line_146_disabled["bg"] = "#adafae"
line_146_disabled["fg"] = "red"
line_146_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_146_disabled["font"] = ftl
line_146_disabled["justify"] = "left"
line_146_disabled["anchor"] = "w"
line_146_disabled["relief"] = "flat"
line_146_disabled.place(x=650, y=6005, width=150, height=33)

line_147_frame = tk.Label(maincanvas)
line_147_frame["bg"] = "#adafae"
line_147_frame["text"] = ""
line_147_frame["relief"] = "sunken"
line_147_frame.place(x=10, y=6040, width=1060, height=40)

line_147_index = tk.Label(maincanvas)
line_147_index["bg"] = "#adafae"
line_147_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_147_index["font"] = ft
line_147_index["justify"] = "left"
line_147_index["anchor"] = "w"
line_147_index.place(x=20, y=6045, width=150, height=33)

line_147_name = tk.Label(maincanvas)
line_147_name["bg"] = "#adafae"
line_147_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_147_name["font"] = ft
line_147_name["justify"] = "left"
line_147_name["anchor"] = "w"
line_147_name.place(x=250, y=6045, width=500, height=33)

line_147_duration = tk.Label(maincanvas)
line_147_duration["bg"] = "#adafae"
line_147_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_147_duration["font"] = ft
line_147_duration["justify"] = "right"
line_147_duration["anchor"] = "e"
line_147_duration.place(x=910, y=6045, width=150, height=33)

line_147_live = tk.Label(maincanvas)
line_147_live["bg"] = "#adafae"
line_147_live["fg"] = "red"
line_147_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_147_live["font"] = ftl
line_147_live["justify"] = "left"
line_147_live["anchor"] = "w"
line_147_live["relief"] = "flat"
line_147_live.place(x=800, y=6045, width=70, height=33)

line_147_disabled = tk.Label(maincanvas)
line_147_disabled["bg"] = "#adafae"
line_147_disabled["fg"] = "red"
line_147_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_147_disabled["font"] = ftl
line_147_disabled["justify"] = "left"
line_147_disabled["anchor"] = "w"
line_147_disabled["relief"] = "flat"
line_147_disabled.place(x=650, y=6045, width=150, height=33)

line_148_frame = tk.Label(maincanvas)
line_148_frame["bg"] = "#adafae"
line_148_frame["text"] = ""
line_148_frame["relief"] = "sunken"
line_148_frame.place(x=10, y=6080, width=1060, height=40)

line_148_index = tk.Label(maincanvas)
line_148_index["bg"] = "#adafae"
line_148_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_148_index["font"] = ft
line_148_index["justify"] = "left"
line_148_index["anchor"] = "w"
line_148_index.place(x=20, y=6085, width=150, height=33)

line_148_name = tk.Label(maincanvas)
line_148_name["bg"] = "#adafae"
line_148_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_148_name["font"] = ft
line_148_name["justify"] = "left"
line_148_name["anchor"] = "w"
line_148_name.place(x=250, y=6085, width=500, height=33)

line_148_duration = tk.Label(maincanvas)
line_148_duration["bg"] = "#adafae"
line_148_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_148_duration["font"] = ft
line_148_duration["justify"] = "right"
line_148_duration["anchor"] = "e"
line_148_duration.place(x=910, y=6085, width=150, height=33)

line_148_live = tk.Label(maincanvas)
line_148_live["bg"] = "#adafae"
line_148_live["fg"] = "red"
line_148_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_148_live["font"] = ftl
line_148_live["justify"] = "left"
line_148_live["anchor"] = "w"
line_148_live["relief"] = "flat"
line_148_live.place(x=800, y=6085, width=70, height=33)

line_148_disabled = tk.Label(maincanvas)
line_148_disabled["bg"] = "#adafae"
line_148_disabled["fg"] = "red"
line_148_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_148_disabled["font"] = ftl
line_148_disabled["justify"] = "left"
line_148_disabled["anchor"] = "w"
line_148_disabled["relief"] = "flat"
line_148_disabled.place(x=650, y=6085, width=150, height=33)

line_149_frame = tk.Label(maincanvas)
line_149_frame["bg"] = "#adafae"
line_149_frame["text"] = ""
line_149_frame["relief"] = "sunken"
line_149_frame.place(x=10, y=6120, width=1060, height=40)

line_149_index = tk.Label(maincanvas)
line_149_index["bg"] = "#adafae"
line_149_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_149_index["font"] = ft
line_149_index["justify"] = "left"
line_149_index["anchor"] = "w"
line_149_index.place(x=20, y=6125, width=150, height=33)

line_149_name = tk.Label(maincanvas)
line_149_name["bg"] = "#adafae"
line_149_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_149_name["font"] = ft
line_149_name["justify"] = "left"
line_149_name["anchor"] = "w"
line_149_name.place(x=250, y=6125, width=500, height=33)

line_149_duration = tk.Label(maincanvas)
line_149_duration["bg"] = "#adafae"
line_149_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_149_duration["font"] = ft
line_149_duration["justify"] = "right"
line_149_duration["anchor"] = "e"
line_149_duration.place(x=910, y=6125, width=150, height=33)

line_149_live = tk.Label(maincanvas)
line_149_live["bg"] = "#adafae"
line_149_live["fg"] = "red"
line_149_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_149_live["font"] = ftl
line_149_live["justify"] = "left"
line_149_live["anchor"] = "w"
line_149_live["relief"] = "flat"
line_149_live.place(x=800, y=6125, width=70, height=33)

line_149_disabled = tk.Label(maincanvas)
line_149_disabled["bg"] = "#adafae"
line_149_disabled["fg"] = "red"
line_149_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_149_disabled["font"] = ftl
line_149_disabled["justify"] = "left"
line_149_disabled["anchor"] = "w"
line_149_disabled["relief"] = "flat"
line_149_disabled.place(x=650, y=6125, width=150, height=33)

line_150_frame = tk.Label(maincanvas)
line_150_frame["bg"] = "#adafae"
line_150_frame["text"] = ""
line_150_frame["relief"] = "sunken"
line_150_frame.place(x=10, y=6160, width=1060, height=40)

line_150_index = tk.Label(maincanvas)
line_150_index["bg"] = "#adafae"
line_150_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_150_index["font"] = ft
line_150_index["justify"] = "left"
line_150_index["anchor"] = "w"
line_150_index.place(x=20, y=6165, width=150, height=33)

line_150_name = tk.Label(maincanvas)
line_150_name["bg"] = "#adafae"
line_150_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_150_name["font"] = ft
line_150_name["justify"] = "left"
line_150_name["anchor"] = "w"
line_150_name.place(x=250, y=6165, width=500, height=33)

line_150_duration = tk.Label(maincanvas)
line_150_duration["bg"] = "#adafae"
line_150_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_150_duration["font"] = ft
line_150_duration["justify"] = "right"
line_150_duration["anchor"] = "e"
line_150_duration.place(x=910, y=6165, width=150, height=33)

line_150_live = tk.Label(maincanvas)
line_150_live["bg"] = "#adafae"
line_150_live["fg"] = "red"
line_150_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_150_live["font"] = ftl
line_150_live["justify"] = "left"
line_150_live["anchor"] = "w"
line_150_live["relief"] = "flat"
line_150_live.place(x=800, y=6165, width=70, height=33)

line_150_disabled = tk.Label(maincanvas)
line_150_disabled["bg"] = "#adafae"
line_150_disabled["fg"] = "red"
line_150_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_150_disabled["font"] = ftl
line_150_disabled["justify"] = "left"
line_150_disabled["anchor"] = "w"
line_150_disabled["relief"] = "flat"
line_150_disabled.place(x=650, y=6165, width=150, height=33)

line_151_frame = tk.Label(maincanvas)
line_151_frame["bg"] = "#adafae"
line_151_frame["text"] = ""
line_151_frame["relief"] = "sunken"
line_151_frame.place(x=10, y=6200, width=1060, height=40)

line_151_index = tk.Label(maincanvas)
line_151_index["bg"] = "#adafae"
line_151_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_151_index["font"] = ft
line_151_index["justify"] = "left"
line_151_index["anchor"] = "w"
line_151_index.place(x=20, y=6205, width=150, height=33)

line_151_name = tk.Label(maincanvas)
line_151_name["bg"] = "#adafae"
line_151_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_151_name["font"] = ft
line_151_name["justify"] = "left"
line_151_name["anchor"] = "w"
line_151_name.place(x=250, y=6205, width=500, height=33)

line_151_duration = tk.Label(maincanvas)
line_151_duration["bg"] = "#adafae"
line_151_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_151_duration["font"] = ft
line_151_duration["justify"] = "right"
line_151_duration["anchor"] = "e"
line_151_duration.place(x=910, y=6205, width=150, height=33)

line_151_live = tk.Label(maincanvas)
line_151_live["bg"] = "#adafae"
line_151_live["fg"] = "red"
line_151_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_151_live["font"] = ftl
line_151_live["justify"] = "left"
line_151_live["anchor"] = "w"
line_151_live["relief"] = "flat"
line_151_live.place(x=8000, y=6205, width=70, height=33)

line_151_disabled = tk.Label(maincanvas)
line_151_disabled["bg"] = "#adafae"
line_151_disabled["fg"] = "red"
line_151_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_151_disabled["font"] = ftl
line_151_disabled["justify"] = "left"
line_151_disabled["anchor"] = "w"
line_151_disabled["relief"] = "flat"
line_151_disabled.place(x=650, y=6205, width=150, height=33)

line_152_frame = tk.Label(maincanvas)
line_152_frame["bg"] = "#adafae"
line_152_frame["text"] = ""
line_152_frame["relief"] = "sunken"
line_152_frame.place(x=10, y=6240, width=1060, height=40)

line_152_index = tk.Label(maincanvas)
line_152_index["bg"] = "#adafae"
line_152_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_152_index["font"] = ft
line_152_index["justify"] = "left"
line_152_index["anchor"] = "w"
line_152_index.place(x=20, y=6245, width=150, height=33)

line_152_name = tk.Label(maincanvas)
line_152_name["bg"] = "#adafae"
line_152_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_152_name["font"] = ft
line_152_name["justify"] = "left"
line_152_name["anchor"] = "w"
line_152_name.place(x=250, y=6245, width=500, height=33)

line_152_duration = tk.Label(maincanvas)
line_152_duration["bg"] = "#adafae"
line_152_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_152_duration["font"] = ft
line_152_duration["justify"] = "right"
line_152_duration["anchor"] = "e"
line_152_duration.place(x=910, y=6245, width=150, height=33)

line_152_live = tk.Label(maincanvas)
line_152_live["bg"] = "#adafae"
line_152_live["fg"] = "red"
line_152_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_152_live["font"] = ftl
line_152_live["justify"] = "left"
line_152_live["anchor"] = "w"
line_152_live["relief"] = "flat"
line_152_live.place(x=8000, y=6245, width=70, height=33)

line_152_disabled = tk.Label(maincanvas)
line_152_disabled["bg"] = "#adafae"
line_152_disabled["fg"] = "red"
line_152_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_152_disabled["font"] = ftl
line_152_disabled["justify"] = "left"
line_152_disabled["anchor"] = "w"
line_152_disabled["relief"] = "flat"
line_152_disabled.place(x=650, y=6245, width=150, height=33)

line_153_frame = tk.Label(maincanvas)
line_153_frame["bg"] = "#adafae"
line_153_frame["text"] = ""
line_153_frame["relief"] = "sunken"
line_153_frame.place(x=10, y=6280, width=1060, height=40)

line_153_index = tk.Label(maincanvas)
line_153_index["bg"] = "#adafae"
line_153_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_153_index["font"] = ft
line_153_index["justify"] = "left"
line_153_index["anchor"] = "w"
line_153_index.place(x=20, y=6285, width=150, height=33)

line_153_name = tk.Label(maincanvas)
line_153_name["bg"] = "#adafae"
line_153_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_153_name["font"] = ft
line_153_name["justify"] = "left"
line_153_name["anchor"] = "w"
line_153_name.place(x=250, y=6285, width=500, height=33)

line_153_duration = tk.Label(maincanvas)
line_153_duration["bg"] = "#adafae"
line_153_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_153_duration["font"] = ft
line_153_duration["justify"] = "right"
line_153_duration["anchor"] = "e"
line_153_duration.place(x=910, y=6285, width=150, height=33)

line_153_live = tk.Label(maincanvas)
line_153_live["bg"] = "#adafae"
line_153_live["fg"] = "red"
line_153_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_153_live["font"] = ftl
line_153_live["justify"] = "left"
line_153_live["anchor"] = "w"
line_153_live["relief"] = "flat"
line_153_live.place(x=8000, y=6285, width=70, height=33)

line_153_disabled = tk.Label(maincanvas)
line_153_disabled["bg"] = "#adafae"
line_153_disabled["fg"] = "red"
line_153_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_153_disabled["font"] = ftl
line_153_disabled["justify"] = "left"
line_153_disabled["anchor"] = "w"
line_153_disabled["relief"] = "flat"
line_153_disabled.place(x=650, y=6285, width=150, height=33)

line_154_frame = tk.Label(maincanvas)
line_154_frame["bg"] = "#adafae"
line_154_frame["text"] = ""
line_154_frame["relief"] = "sunken"
line_154_frame.place(x=10, y=6320, width=1060, height=40)

line_154_index = tk.Label(maincanvas)
line_154_index["bg"] = "#adafae"
line_154_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_154_index["font"] = ft
line_154_index["justify"] = "left"
line_154_index["anchor"] = "w"
line_154_index.place(x=20, y=6325, width=150, height=33)

line_154_name = tk.Label(maincanvas)
line_154_name["bg"] = "#adafae"
line_154_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_154_name["font"] = ft
line_154_name["justify"] = "left"
line_154_name["anchor"] = "w"
line_154_name.place(x=250, y=6325, width=500, height=33)

line_154_duration = tk.Label(maincanvas)
line_154_duration["bg"] = "#adafae"
line_154_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_154_duration["font"] = ft
line_154_duration["justify"] = "right"
line_154_duration["anchor"] = "e"
line_154_duration.place(x=910, y=6325, width=150, height=33)

line_154_live = tk.Label(maincanvas)
line_154_live["bg"] = "#adafae"
line_154_live["fg"] = "red"
line_154_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_154_live["font"] = ftl
line_154_live["justify"] = "left"
line_154_live["anchor"] = "w"
line_154_live["relief"] = "flat"
line_154_live.place(x=8000, y=6325, width=70, height=33)

line_154_disabled = tk.Label(maincanvas)
line_154_disabled["bg"] = "#adafae"
line_154_disabled["fg"] = "red"
line_154_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_154_disabled["font"] = ftl
line_154_disabled["justify"] = "left"
line_154_disabled["anchor"] = "w"
line_154_disabled["relief"] = "flat"
line_154_disabled.place(x=650, y=6325, width=150, height=33)

line_155_frame = tk.Label(maincanvas)
line_155_frame["bg"] = "#adafae"
line_155_frame["text"] = ""
line_155_frame["relief"] = "sunken"
line_155_frame.place(x=10, y=6360, width=1060, height=40)

line_155_index = tk.Label(maincanvas)
line_155_index["bg"] = "#adafae"
line_155_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_155_index["font"] = ft
line_155_index["justify"] = "left"
line_155_index["anchor"] = "w"
line_155_index.place(x=20, y=6365, width=150, height=33)

line_155_name = tk.Label(maincanvas)
line_155_name["bg"] = "#adafae"
line_155_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_155_name["font"] = ft
line_155_name["justify"] = "left"
line_155_name["anchor"] = "w"
line_155_name.place(x=250, y=6365, width=500, height=33)

line_155_duration = tk.Label(maincanvas)
line_155_duration["bg"] = "#adafae"
line_155_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_155_duration["font"] = ft
line_155_duration["justify"] = "right"
line_155_duration["anchor"] = "e"
line_155_duration.place(x=910, y=6365, width=150, height=33)

line_155_live = tk.Label(maincanvas)
line_155_live["bg"] = "#adafae"
line_155_live["fg"] = "red"
line_155_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_155_live["font"] = ftl
line_155_live["justify"] = "left"
line_155_live["anchor"] = "w"
line_155_live["relief"] = "flat"
line_155_live.place(x=8000, y=6365, width=70, height=33)

line_155_disabled = tk.Label(maincanvas)
line_155_disabled["bg"] = "#adafae"
line_155_disabled["fg"] = "red"
line_155_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_155_disabled["font"] = ftl
line_155_disabled["justify"] = "left"
line_155_disabled["anchor"] = "w"
line_155_disabled["relief"] = "flat"
line_155_disabled.place(x=650, y=6365, width=150, height=33)

line_156_frame = tk.Label(maincanvas)
line_156_frame["bg"] = "#adafae"
line_156_frame["text"] = ""
line_156_frame["relief"] = "sunken"
line_156_frame.place(x=10, y=6400, width=1060, height=40)

line_156_index = tk.Label(maincanvas)
line_156_index["bg"] = "#adafae"
line_156_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_156_index["font"] = ft
line_156_index["justify"] = "left"
line_156_index["anchor"] = "w"
line_156_index.place(x=20, y=6405, width=150, height=33)

line_156_name = tk.Label(maincanvas)
line_156_name["bg"] = "#adafae"
line_156_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_156_name["font"] = ft
line_156_name["justify"] = "left"
line_156_name["anchor"] = "w"
line_156_name.place(x=250, y=6405, width=500, height=33)

line_156_duration = tk.Label(maincanvas)
line_156_duration["bg"] = "#adafae"
line_156_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_156_duration["font"] = ft
line_156_duration["justify"] = "right"
line_156_duration["anchor"] = "e"
line_156_duration.place(x=910, y=6405, width=150, height=33)

line_156_live = tk.Label(maincanvas)
line_156_live["bg"] = "#adafae"
line_156_live["fg"] = "red"
line_156_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_156_live["font"] = ftl
line_156_live["justify"] = "left"
line_156_live["anchor"] = "w"
line_156_live["relief"] = "flat"
line_156_live.place(x=8000, y=6405, width=70, height=33)

line_156_disabled = tk.Label(maincanvas)
line_156_disabled["bg"] = "#adafae"
line_156_disabled["fg"] = "red"
line_156_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_156_disabled["font"] = ftl
line_156_disabled["justify"] = "left"
line_156_disabled["anchor"] = "w"
line_156_disabled["relief"] = "flat"
line_156_disabled.place(x=650, y=6405, width=150, height=33)

line_157_frame = tk.Label(maincanvas)
line_157_frame["bg"] = "#adafae"
line_157_frame["text"] = ""
line_157_frame["relief"] = "sunken"
line_157_frame.place(x=10, y=6440, width=1060, height=40)

line_157_index = tk.Label(maincanvas)
line_157_index["bg"] = "#adafae"
line_157_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_157_index["font"] = ft
line_157_index["justify"] = "left"
line_157_index["anchor"] = "w"
line_157_index.place(x=20, y=6445, width=150, height=33)

line_157_name = tk.Label(maincanvas)
line_157_name["bg"] = "#adafae"
line_157_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_157_name["font"] = ft
line_157_name["justify"] = "left"
line_157_name["anchor"] = "w"
line_157_name.place(x=250, y=6445, width=500, height=33)

line_157_duration = tk.Label(maincanvas)
line_157_duration["bg"] = "#adafae"
line_157_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_157_duration["font"] = ft
line_157_duration["justify"] = "right"
line_157_duration["anchor"] = "e"
line_157_duration.place(x=910, y=6445, width=150, height=33)

line_157_live = tk.Label(maincanvas)
line_157_live["bg"] = "#adafae"
line_157_live["fg"] = "red"
line_157_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_157_live["font"] = ftl
line_157_live["justify"] = "left"
line_157_live["anchor"] = "w"
line_157_live["relief"] = "flat"
line_157_live.place(x=8000, y=6445, width=70, height=33)

line_157_disabled = tk.Label(maincanvas)
line_157_disabled["bg"] = "#adafae"
line_157_disabled["fg"] = "red"
line_157_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_157_disabled["font"] = ftl
line_157_disabled["justify"] = "left"
line_157_disabled["anchor"] = "w"
line_157_disabled["relief"] = "flat"
line_157_disabled.place(x=650, y=6445, width=150, height=33)

line_158_frame = tk.Label(maincanvas)
line_158_frame["bg"] = "#adafae"
line_158_frame["text"] = ""
line_158_frame["relief"] = "sunken"
line_158_frame.place(x=10, y=6480, width=1060, height=40)

line_158_index = tk.Label(maincanvas)
line_158_index["bg"] = "#adafae"
line_158_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_158_index["font"] = ft
line_158_index["justify"] = "left"
line_158_index["anchor"] = "w"
line_158_index.place(x=20, y=6485, width=150, height=33)

line_158_name = tk.Label(maincanvas)
line_158_name["bg"] = "#adafae"
line_158_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_158_name["font"] = ft
line_158_name["justify"] = "left"
line_158_name["anchor"] = "w"
line_158_name.place(x=250, y=6485, width=500, height=33)

line_158_duration = tk.Label(maincanvas)
line_158_duration["bg"] = "#adafae"
line_158_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_158_duration["font"] = ft
line_158_duration["justify"] = "right"
line_158_duration["anchor"] = "e"
line_158_duration.place(x=910, y=6485, width=150, height=33)

line_158_live = tk.Label(maincanvas)
line_158_live["bg"] = "#adafae"
line_158_live["fg"] = "red"
line_158_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_158_live["font"] = ftl
line_158_live["justify"] = "left"
line_158_live["anchor"] = "w"
line_158_live["relief"] = "flat"
line_158_live.place(x=8000, y=6485, width=70, height=33)

line_158_disabled = tk.Label(maincanvas)
line_158_disabled["bg"] = "#adafae"
line_158_disabled["fg"] = "red"
line_158_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_158_disabled["font"] = ftl
line_158_disabled["justify"] = "left"
line_158_disabled["anchor"] = "w"
line_158_disabled["relief"] = "flat"
line_158_disabled.place(x=650, y=6485, width=150, height=33)

line_159_frame = tk.Label(maincanvas)
line_159_frame["bg"] = "#adafae"
line_159_frame["text"] = ""
line_159_frame["relief"] = "sunken"
line_159_frame.place(x=10, y=6520, width=1060, height=40)

line_159_index = tk.Label(maincanvas)
line_159_index["bg"] = "#adafae"
line_159_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_159_index["font"] = ft
line_159_index["justify"] = "left"
line_159_index["anchor"] = "w"
line_159_index.place(x=20, y=6525, width=150, height=33)

line_159_name = tk.Label(maincanvas)
line_159_name["bg"] = "#adafae"
line_159_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_159_name["font"] = ft
line_159_name["justify"] = "left"
line_159_name["anchor"] = "w"
line_159_name.place(x=250, y=6525, width=500, height=33)

line_159_duration = tk.Label(maincanvas)
line_159_duration["bg"] = "#adafae"
line_159_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_159_duration["font"] = ft
line_159_duration["justify"] = "right"
line_159_duration["anchor"] = "e"
line_159_duration.place(x=910, y=6525, width=150, height=33)

line_159_live = tk.Label(maincanvas)
line_159_live["bg"] = "#adafae"
line_159_live["fg"] = "red"
line_159_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_159_live["font"] = ftl
line_159_live["justify"] = "left"
line_159_live["anchor"] = "w"
line_159_live["relief"] = "flat"
line_159_live.place(x=8000, y=6525, width=70, height=33)

line_159_disabled = tk.Label(maincanvas)
line_159_disabled["bg"] = "#adafae"
line_159_disabled["fg"] = "red"
line_159_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_159_disabled["font"] = ftl
line_159_disabled["justify"] = "left"
line_159_disabled["anchor"] = "w"
line_159_disabled["relief"] = "flat"
line_159_disabled.place(x=650, y=6525, width=150, height=33)

line_160_frame = tk.Label(maincanvas)
line_160_frame["bg"] = "#adafae"
line_160_frame["text"] = ""
line_160_frame["relief"] = "sunken"
line_160_frame.place(x=10, y=6560, width=1060, height=40)

line_160_index = tk.Label(maincanvas)
line_160_index["bg"] = "#adafae"
line_160_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_160_index["font"] = ft
line_160_index["justify"] = "left"
line_160_index["anchor"] = "w"
line_160_index.place(x=20, y=6565, width=150, height=33)

line_160_name = tk.Label(maincanvas)
line_160_name["bg"] = "#adafae"
line_160_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_160_name["font"] = ft
line_160_name["justify"] = "left"
line_160_name["anchor"] = "w"
line_160_name.place(x=250, y=6565, width=500, height=33)

line_160_duration = tk.Label(maincanvas)
line_160_duration["bg"] = "#adafae"
line_160_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_160_duration["font"] = ft
line_160_duration["justify"] = "right"
line_160_duration["anchor"] = "e"
line_160_duration.place(x=910, y=6565, width=150, height=33)

line_160_live = tk.Label(maincanvas)
line_160_live["bg"] = "#adafae"
line_160_live["fg"] = "red"
line_160_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_160_live["font"] = ftl
line_160_live["justify"] = "left"
line_160_live["anchor"] = "w"
line_160_live["relief"] = "flat"
line_160_live.place(x=8000, y=6565, width=70, height=33)

line_160_disabled = tk.Label(maincanvas)
line_160_disabled["bg"] = "#adafae"
line_160_disabled["fg"] = "red"
line_160_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_160_disabled["font"] = ftl
line_160_disabled["justify"] = "left"
line_160_disabled["anchor"] = "w"
line_160_disabled["relief"] = "flat"
line_160_disabled.place(x=650, y=6565, width=150, height=33)

line_161_frame = tk.Label(maincanvas)
line_161_frame["bg"] = "#adafae"
line_161_frame["text"] = ""
line_161_frame["relief"] = "sunken"
line_161_frame.place(x=10, y=6600, width=1060, height=40)

line_161_index = tk.Label(maincanvas)
line_161_index["bg"] = "#adafae"
line_161_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_161_index["font"] = ft
line_161_index["justify"] = "left"
line_161_index["anchor"] = "w"
line_161_index.place(x=20, y=6605, width=150, height=33)

line_161_name = tk.Label(maincanvas)
line_161_name["bg"] = "#adafae"
line_161_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_161_name["font"] = ft
line_161_name["justify"] = "left"
line_161_name["anchor"] = "w"
line_161_name.place(x=250, y=6605, width=500, height=33)

line_161_duration = tk.Label(maincanvas)
line_161_duration["bg"] = "#adafae"
line_161_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_161_duration["font"] = ft
line_161_duration["justify"] = "right"
line_161_duration["anchor"] = "e"
line_161_duration.place(x=910, y=6605, width=150, height=33)

line_161_live = tk.Label(maincanvas)
line_161_live["bg"] = "#adafae"
line_161_live["fg"] = "red"
line_161_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_161_live["font"] = ftl
line_161_live["justify"] = "left"
line_161_live["anchor"] = "w"
line_161_live["relief"] = "flat"
line_161_live.place(x=8000, y=6605, width=70, height=33)

line_161_disabled = tk.Label(maincanvas)
line_161_disabled["bg"] = "#adafae"
line_161_disabled["fg"] = "red"
line_161_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_161_disabled["font"] = ftl
line_161_disabled["justify"] = "left"
line_161_disabled["anchor"] = "w"
line_161_disabled["relief"] = "flat"
line_161_disabled.place(x=650, y=6605, width=150, height=33)

line_162_frame = tk.Label(maincanvas)
line_162_frame["bg"] = "#adafae"
line_162_frame["text"] = ""
line_162_frame["relief"] = "sunken"
line_162_frame.place(x=10, y=6640, width=1060, height=40)

line_162_index = tk.Label(maincanvas)
line_162_index["bg"] = "#adafae"
line_162_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_162_index["font"] = ft
line_162_index["justify"] = "left"
line_162_index["anchor"] = "w"
line_162_index.place(x=20, y=6645, width=150, height=33)

line_162_name = tk.Label(maincanvas)
line_162_name["bg"] = "#adafae"
line_162_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_162_name["font"] = ft
line_162_name["justify"] = "left"
line_162_name["anchor"] = "w"
line_162_name.place(x=250, y=6645, width=500, height=33)

line_162_duration = tk.Label(maincanvas)
line_162_duration["bg"] = "#adafae"
line_162_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_162_duration["font"] = ft
line_162_duration["justify"] = "right"
line_162_duration["anchor"] = "e"
line_162_duration.place(x=910, y=6645, width=150, height=33)

line_162_live = tk.Label(maincanvas)
line_162_live["bg"] = "#adafae"
line_162_live["fg"] = "red"
line_162_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_162_live["font"] = ftl
line_162_live["justify"] = "left"
line_162_live["anchor"] = "w"
line_162_live["relief"] = "flat"
line_162_live.place(x=8000, y=6645, width=70, height=33)

line_162_disabled = tk.Label(maincanvas)
line_162_disabled["bg"] = "#adafae"
line_162_disabled["fg"] = "red"
line_162_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_162_disabled["font"] = ftl
line_162_disabled["justify"] = "left"
line_162_disabled["anchor"] = "w"
line_162_disabled["relief"] = "flat"
line_162_disabled.place(x=650, y=6645, width=150, height=33)

line_163_frame = tk.Label(maincanvas)
line_163_frame["bg"] = "#adafae"
line_163_frame["text"] = ""
line_163_frame["relief"] = "sunken"
line_163_frame.place(x=10, y=6680, width=1060, height=40)

line_163_index = tk.Label(maincanvas)
line_163_index["bg"] = "#adafae"
line_163_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_163_index["font"] = ft
line_163_index["justify"] = "left"
line_163_index["anchor"] = "w"
line_163_index.place(x=20, y=6685, width=150, height=33)

line_163_name = tk.Label(maincanvas)
line_163_name["bg"] = "#adafae"
line_163_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_163_name["font"] = ft
line_163_name["justify"] = "left"
line_163_name["anchor"] = "w"
line_163_name.place(x=250, y=6685, width=500, height=33)

line_163_duration = tk.Label(maincanvas)
line_163_duration["bg"] = "#adafae"
line_163_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_163_duration["font"] = ft
line_163_duration["justify"] = "right"
line_163_duration["anchor"] = "e"
line_163_duration.place(x=910, y=6685, width=150, height=33)

line_163_live = tk.Label(maincanvas)
line_163_live["bg"] = "#adafae"
line_163_live["fg"] = "red"
line_163_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_163_live["font"] = ftl
line_163_live["justify"] = "left"
line_163_live["anchor"] = "w"
line_163_live["relief"] = "flat"
line_163_live.place(x=8000, y=6685, width=70, height=33)

line_163_disabled = tk.Label(maincanvas)
line_163_disabled["bg"] = "#adafae"
line_163_disabled["fg"] = "red"
line_163_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_163_disabled["font"] = ftl
line_163_disabled["justify"] = "left"
line_163_disabled["anchor"] = "w"
line_163_disabled["relief"] = "flat"
line_163_disabled.place(x=650, y=6685, width=150, height=33)

line_164_frame = tk.Label(maincanvas)
line_164_frame["bg"] = "#adafae"
line_164_frame["text"] = ""
line_164_frame["relief"] = "sunken"
line_164_frame.place(x=10, y=6720, width=1060, height=40)

line_164_index = tk.Label(maincanvas)
line_164_index["bg"] = "#adafae"
line_164_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_164_index["font"] = ft
line_164_index["justify"] = "left"
line_164_index["anchor"] = "w"
line_164_index.place(x=20, y=6725, width=150, height=33)

line_164_name = tk.Label(maincanvas)
line_164_name["bg"] = "#adafae"
line_164_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_164_name["font"] = ft
line_164_name["justify"] = "left"
line_164_name["anchor"] = "w"
line_164_name.place(x=250, y=6725, width=500, height=33)

line_164_duration = tk.Label(maincanvas)
line_164_duration["bg"] = "#adafae"
line_164_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_164_duration["font"] = ft
line_164_duration["justify"] = "right"
line_164_duration["anchor"] = "e"
line_164_duration.place(x=910, y=6725, width=150, height=33)

line_164_live = tk.Label(maincanvas)
line_164_live["bg"] = "#adafae"
line_164_live["fg"] = "red"
line_164_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_164_live["font"] = ftl
line_164_live["justify"] = "left"
line_164_live["anchor"] = "w"
line_164_live["relief"] = "flat"
line_164_live.place(x=8000, y=6725, width=70, height=33)

line_164_disabled = tk.Label(maincanvas)
line_164_disabled["bg"] = "#adafae"
line_164_disabled["fg"] = "red"
line_164_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_164_disabled["font"] = ftl
line_164_disabled["justify"] = "left"
line_164_disabled["anchor"] = "w"
line_164_disabled["relief"] = "flat"
line_164_disabled.place(x=650, y=6725, width=150, height=33)

line_165_frame = tk.Label(maincanvas)
line_165_frame["bg"] = "#adafae"
line_165_frame["text"] = ""
line_165_frame["relief"] = "sunken"
line_165_frame.place(x=10, y=6760, width=1060, height=40)

line_165_index = tk.Label(maincanvas)
line_165_index["bg"] = "#adafae"
line_165_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_165_index["font"] = ft
line_165_index["justify"] = "left"
line_165_index["anchor"] = "w"
line_165_index.place(x=20, y=6765, width=150, height=33)

line_165_name = tk.Label(maincanvas)
line_165_name["bg"] = "#adafae"
line_165_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_165_name["font"] = ft
line_165_name["justify"] = "left"
line_165_name["anchor"] = "w"
line_165_name.place(x=250, y=6765, width=500, height=33)

line_165_duration = tk.Label(maincanvas)
line_165_duration["bg"] = "#adafae"
line_165_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_165_duration["font"] = ft
line_165_duration["justify"] = "right"
line_165_duration["anchor"] = "e"
line_165_duration.place(x=910, y=6765, width=150, height=33)

line_165_live = tk.Label(maincanvas)
line_165_live["bg"] = "#adafae"
line_165_live["fg"] = "red"
line_165_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_165_live["font"] = ftl
line_165_live["justify"] = "left"
line_165_live["anchor"] = "w"
line_165_live["relief"] = "flat"
line_165_live.place(x=8000, y=6765, width=70, height=33)

line_165_disabled = tk.Label(maincanvas)
line_165_disabled["bg"] = "#adafae"
line_165_disabled["fg"] = "red"
line_165_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_165_disabled["font"] = ftl
line_165_disabled["justify"] = "left"
line_165_disabled["anchor"] = "w"
line_165_disabled["relief"] = "flat"
line_165_disabled.place(x=650, y=6765, width=150, height=33)

line_166_frame = tk.Label(maincanvas)
line_166_frame["bg"] = "#adafae"
line_166_frame["text"] = ""
line_166_frame["relief"] = "sunken"
line_166_frame.place(x=10, y=6800, width=1060, height=40)

line_166_index = tk.Label(maincanvas)
line_166_index["bg"] = "#adafae"
line_166_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_166_index["font"] = ft
line_166_index["justify"] = "left"
line_166_index["anchor"] = "w"
line_166_index.place(x=20, y=6805, width=150, height=33)

line_166_name = tk.Label(maincanvas)
line_166_name["bg"] = "#adafae"
line_166_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_166_name["font"] = ft
line_166_name["justify"] = "left"
line_166_name["anchor"] = "w"
line_166_name.place(x=250, y=6805, width=500, height=33)

line_166_duration = tk.Label(maincanvas)
line_166_duration["bg"] = "#adafae"
line_166_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_166_duration["font"] = ft
line_166_duration["justify"] = "right"
line_166_duration["anchor"] = "e"
line_166_duration.place(x=910, y=6805, width=150, height=33)

line_166_live = tk.Label(maincanvas)
line_166_live["bg"] = "#adafae"
line_166_live["fg"] = "red"
line_166_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_166_live["font"] = ftl
line_166_live["justify"] = "left"
line_166_live["anchor"] = "w"
line_166_live["relief"] = "flat"
line_166_live.place(x=8000, y=6805, width=70, height=33)

line_166_disabled = tk.Label(maincanvas)
line_166_disabled["bg"] = "#adafae"
line_166_disabled["fg"] = "red"
line_166_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_166_disabled["font"] = ftl
line_166_disabled["justify"] = "left"
line_166_disabled["anchor"] = "w"
line_166_disabled["relief"] = "flat"
line_166_disabled.place(x=650, y=6805, width=150, height=33)

line_167_frame = tk.Label(maincanvas)
line_167_frame["bg"] = "#adafae"
line_167_frame["text"] = ""
line_167_frame["relief"] = "sunken"
line_167_frame.place(x=10, y=6840, width=1060, height=40)

line_167_index = tk.Label(maincanvas)
line_167_index["bg"] = "#adafae"
line_167_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_167_index["font"] = ft
line_167_index["justify"] = "left"
line_167_index["anchor"] = "w"
line_167_index.place(x=20, y=6845, width=150, height=33)

line_167_name = tk.Label(maincanvas)
line_167_name["bg"] = "#adafae"
line_167_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_167_name["font"] = ft
line_167_name["justify"] = "left"
line_167_name["anchor"] = "w"
line_167_name.place(x=250, y=6845, width=500, height=33)

line_167_duration = tk.Label(maincanvas)
line_167_duration["bg"] = "#adafae"
line_167_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_167_duration["font"] = ft
line_167_duration["justify"] = "right"
line_167_duration["anchor"] = "e"
line_167_duration.place(x=910, y=6845, width=150, height=33)

line_167_live = tk.Label(maincanvas)
line_167_live["bg"] = "#adafae"
line_167_live["fg"] = "red"
line_167_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_167_live["font"] = ftl
line_167_live["justify"] = "left"
line_167_live["anchor"] = "w"
line_167_live["relief"] = "flat"
line_167_live.place(x=8000, y=6845, width=70, height=33)

line_167_disabled = tk.Label(maincanvas)
line_167_disabled["bg"] = "#adafae"
line_167_disabled["fg"] = "red"
line_167_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_167_disabled["font"] = ftl
line_167_disabled["justify"] = "left"
line_167_disabled["anchor"] = "w"
line_167_disabled["relief"] = "flat"
line_167_disabled.place(x=650, y=6845, width=150, height=33)

line_168_frame = tk.Label(maincanvas)
line_168_frame["bg"] = "#adafae"
line_168_frame["text"] = ""
line_168_frame["relief"] = "sunken"
line_168_frame.place(x=10, y=6880, width=1060, height=40)

line_168_index = tk.Label(maincanvas)
line_168_index["bg"] = "#adafae"
line_168_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_168_index["font"] = ft
line_168_index["justify"] = "left"
line_168_index["anchor"] = "w"
line_168_index.place(x=20, y=6885, width=150, height=33)

line_168_name = tk.Label(maincanvas)
line_168_name["bg"] = "#adafae"
line_168_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_168_name["font"] = ft
line_168_name["justify"] = "left"
line_168_name["anchor"] = "w"
line_168_name.place(x=250, y=6885, width=500, height=33)

line_168_duration = tk.Label(maincanvas)
line_168_duration["bg"] = "#adafae"
line_168_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_168_duration["font"] = ft
line_168_duration["justify"] = "right"
line_168_duration["anchor"] = "e"
line_168_duration.place(x=910, y=6885, width=150, height=33)

line_168_live = tk.Label(maincanvas)
line_168_live["bg"] = "#adafae"
line_168_live["fg"] = "red"
line_168_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_168_live["font"] = ftl
line_168_live["justify"] = "left"
line_168_live["anchor"] = "w"
line_168_live["relief"] = "flat"
line_168_live.place(x=8000, y=6885, width=70, height=33)

line_168_disabled = tk.Label(maincanvas)
line_168_disabled["bg"] = "#adafae"
line_168_disabled["fg"] = "red"
line_168_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_168_disabled["font"] = ftl
line_168_disabled["justify"] = "left"
line_168_disabled["anchor"] = "w"
line_168_disabled["relief"] = "flat"
line_168_disabled.place(x=650, y=6885, width=150, height=33)

line_169_frame = tk.Label(maincanvas)
line_169_frame["bg"] = "#adafae"
line_169_frame["text"] = ""
line_169_frame["relief"] = "sunken"
line_169_frame.place(x=10, y=6920, width=1060, height=40)

line_169_index = tk.Label(maincanvas)
line_169_index["bg"] = "#adafae"
line_169_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_169_index["font"] = ft
line_169_index["justify"] = "left"
line_169_index["anchor"] = "w"
line_169_index.place(x=20, y=6925, width=150, height=33)

line_169_name = tk.Label(maincanvas)
line_169_name["bg"] = "#adafae"
line_169_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_169_name["font"] = ft
line_169_name["justify"] = "left"
line_169_name["anchor"] = "w"
line_169_name.place(x=250, y=6925, width=500, height=33)

line_169_duration = tk.Label(maincanvas)
line_169_duration["bg"] = "#adafae"
line_169_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_169_duration["font"] = ft
line_169_duration["justify"] = "right"
line_169_duration["anchor"] = "e"
line_169_duration.place(x=910, y=6925, width=150, height=33)

line_169_live = tk.Label(maincanvas)
line_169_live["bg"] = "#adafae"
line_169_live["fg"] = "red"
line_169_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_169_live["font"] = ftl
line_169_live["justify"] = "left"
line_169_live["anchor"] = "w"
line_169_live["relief"] = "flat"
line_169_live.place(x=8000, y=6925, width=70, height=33)

line_169_disabled = tk.Label(maincanvas)
line_169_disabled["bg"] = "#adafae"
line_169_disabled["fg"] = "red"
line_169_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_169_disabled["font"] = ftl
line_169_disabled["justify"] = "left"
line_169_disabled["anchor"] = "w"
line_169_disabled["relief"] = "flat"
line_169_disabled.place(x=650, y=6925, width=150, height=33)

line_170_frame = tk.Label(maincanvas)
line_170_frame["bg"] = "#adafae"
line_170_frame["text"] = ""
line_170_frame["relief"] = "sunken"
line_170_frame.place(x=10, y=6960, width=1060, height=40)

line_170_index = tk.Label(maincanvas)
line_170_index["bg"] = "#adafae"
line_170_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_170_index["font"] = ft
line_170_index["justify"] = "left"
line_170_index["anchor"] = "w"
line_170_index.place(x=20, y=6965, width=150, height=33)

line_170_name = tk.Label(maincanvas)
line_170_name["bg"] = "#adafae"
line_170_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_170_name["font"] = ft
line_170_name["justify"] = "left"
line_170_name["anchor"] = "w"
line_170_name.place(x=250, y=6965, width=500, height=33)

line_170_duration = tk.Label(maincanvas)
line_170_duration["bg"] = "#adafae"
line_170_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_170_duration["font"] = ft
line_170_duration["justify"] = "right"
line_170_duration["anchor"] = "e"
line_170_duration.place(x=910, y=6965, width=150, height=33)

line_170_live = tk.Label(maincanvas)
line_170_live["bg"] = "#adafae"
line_170_live["fg"] = "red"
line_170_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_170_live["font"] = ftl
line_170_live["justify"] = "left"
line_170_live["anchor"] = "w"
line_170_live["relief"] = "flat"
line_170_live.place(x=8000, y=6965, width=70, height=33)

line_170_disabled = tk.Label(maincanvas)
line_170_disabled["bg"] = "#adafae"
line_170_disabled["fg"] = "red"
line_170_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_170_disabled["font"] = ftl
line_170_disabled["justify"] = "left"
line_170_disabled["anchor"] = "w"
line_170_disabled["relief"] = "flat"
line_170_disabled.place(x=650, y=6965, width=150, height=33)

line_171_frame = tk.Label(maincanvas)
line_171_frame["bg"] = "#adafae"
line_171_frame["text"] = ""
line_171_frame["relief"] = "sunken"
line_171_frame.place(x=10, y=7000, width=1060, height=40)

line_171_index = tk.Label(maincanvas)
line_171_index["bg"] = "#adafae"
line_171_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_171_index["font"] = ft
line_171_index["justify"] = "left"
line_171_index["anchor"] = "w"
line_171_index.place(x=20, y=7005, width=150, height=33)

line_171_name = tk.Label(maincanvas)
line_171_name["bg"] = "#adafae"
line_171_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_171_name["font"] = ft
line_171_name["justify"] = "left"
line_171_name["anchor"] = "w"
line_171_name.place(x=250, y=7005, width=500, height=33)

line_171_duration = tk.Label(maincanvas)
line_171_duration["bg"] = "#adafae"
line_171_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_171_duration["font"] = ft
line_171_duration["justify"] = "right"
line_171_duration["anchor"] = "e"
line_171_duration.place(x=910, y=7005, width=150, height=33)

line_171_live = tk.Label(maincanvas)
line_171_live["bg"] = "#adafae"
line_171_live["fg"] = "red"
line_171_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_171_live["font"] = ftl
line_171_live["justify"] = "left"
line_171_live["anchor"] = "w"
line_171_live["relief"] = "flat"
line_171_live.place(x=8000, y=7005, width=70, height=33)

line_171_disabled = tk.Label(maincanvas)
line_171_disabled["bg"] = "#adafae"
line_171_disabled["fg"] = "red"
line_171_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_171_disabled["font"] = ftl
line_171_disabled["justify"] = "left"
line_171_disabled["anchor"] = "w"
line_171_disabled["relief"] = "flat"
line_171_disabled.place(x=650, y=7005, width=150, height=33)

line_172_frame = tk.Label(maincanvas)
line_172_frame["bg"] = "#adafae"
line_172_frame["text"] = ""
line_172_frame["relief"] = "sunken"
line_172_frame.place(x=10, y=7040, width=1060, height=40)

line_172_index = tk.Label(maincanvas)
line_172_index["bg"] = "#adafae"
line_172_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_172_index["font"] = ft
line_172_index["justify"] = "left"
line_172_index["anchor"] = "w"
line_172_index.place(x=20, y=7045, width=150, height=33)

line_172_name = tk.Label(maincanvas)
line_172_name["bg"] = "#adafae"
line_172_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_172_name["font"] = ft
line_172_name["justify"] = "left"
line_172_name["anchor"] = "w"
line_172_name.place(x=250, y=7045, width=500, height=33)

line_172_duration = tk.Label(maincanvas)
line_172_duration["bg"] = "#adafae"
line_172_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_172_duration["font"] = ft
line_172_duration["justify"] = "right"
line_172_duration["anchor"] = "e"
line_172_duration.place(x=910, y=7045, width=150, height=33)

line_172_live = tk.Label(maincanvas)
line_172_live["bg"] = "#adafae"
line_172_live["fg"] = "red"
line_172_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_172_live["font"] = ftl
line_172_live["justify"] = "left"
line_172_live["anchor"] = "w"
line_172_live["relief"] = "flat"
line_172_live.place(x=8000, y=7045, width=70, height=33)

line_172_disabled = tk.Label(maincanvas)
line_172_disabled["bg"] = "#adafae"
line_172_disabled["fg"] = "red"
line_172_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_172_disabled["font"] = ftl
line_172_disabled["justify"] = "left"
line_172_disabled["anchor"] = "w"
line_172_disabled["relief"] = "flat"
line_172_disabled.place(x=650, y=7045, width=150, height=33)

line_173_frame = tk.Label(maincanvas)
line_173_frame["bg"] = "#adafae"
line_173_frame["text"] = ""
line_173_frame["relief"] = "sunken"
line_173_frame.place(x=10, y=7080, width=1060, height=40)

line_173_index = tk.Label(maincanvas)
line_173_index["bg"] = "#adafae"
line_173_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_173_index["font"] = ft
line_173_index["justify"] = "left"
line_173_index["anchor"] = "w"
line_173_index.place(x=20, y=7085, width=150, height=33)

line_173_name = tk.Label(maincanvas)
line_173_name["bg"] = "#adafae"
line_173_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_173_name["font"] = ft
line_173_name["justify"] = "left"
line_173_name["anchor"] = "w"
line_173_name.place(x=250, y=7085, width=500, height=33)

line_173_duration = tk.Label(maincanvas)
line_173_duration["bg"] = "#adafae"
line_173_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_173_duration["font"] = ft
line_173_duration["justify"] = "right"
line_173_duration["anchor"] = "e"
line_173_duration.place(x=910, y=7085, width=150, height=33)

line_173_live = tk.Label(maincanvas)
line_173_live["bg"] = "#adafae"
line_173_live["fg"] = "red"
line_173_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_173_live["font"] = ftl
line_173_live["justify"] = "left"
line_173_live["anchor"] = "w"
line_173_live["relief"] = "flat"
line_173_live.place(x=8000, y=7085, width=70, height=33)

line_173_disabled = tk.Label(maincanvas)
line_173_disabled["bg"] = "#adafae"
line_173_disabled["fg"] = "red"
line_173_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_173_disabled["font"] = ftl
line_173_disabled["justify"] = "left"
line_173_disabled["anchor"] = "w"
line_173_disabled["relief"] = "flat"
line_173_disabled.place(x=650, y=7085, width=150, height=33)

line_174_frame = tk.Label(maincanvas)
line_174_frame["bg"] = "#adafae"
line_174_frame["text"] = ""
line_174_frame["relief"] = "sunken"
line_174_frame.place(x=10, y=7120, width=1060, height=40)

line_174_index = tk.Label(maincanvas)
line_174_index["bg"] = "#adafae"
line_174_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_174_index["font"] = ft
line_174_index["justify"] = "left"
line_174_index["anchor"] = "w"
line_174_index.place(x=20, y=7125, width=150, height=33)

line_174_name = tk.Label(maincanvas)
line_174_name["bg"] = "#adafae"
line_174_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_174_name["font"] = ft
line_174_name["justify"] = "left"
line_174_name["anchor"] = "w"
line_174_name.place(x=250, y=7125, width=500, height=33)

line_174_duration = tk.Label(maincanvas)
line_174_duration["bg"] = "#adafae"
line_174_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_174_duration["font"] = ft
line_174_duration["justify"] = "right"
line_174_duration["anchor"] = "e"
line_174_duration.place(x=910, y=7125, width=150, height=33)

line_174_live = tk.Label(maincanvas)
line_174_live["bg"] = "#adafae"
line_174_live["fg"] = "red"
line_174_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_174_live["font"] = ftl
line_174_live["justify"] = "left"
line_174_live["anchor"] = "w"
line_174_live["relief"] = "flat"
line_174_live.place(x=8000, y=7125, width=70, height=33)

line_174_disabled = tk.Label(maincanvas)
line_174_disabled["bg"] = "#adafae"
line_174_disabled["fg"] = "red"
line_174_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_174_disabled["font"] = ftl
line_174_disabled["justify"] = "left"
line_174_disabled["anchor"] = "w"
line_174_disabled["relief"] = "flat"
line_174_disabled.place(x=650, y=7125, width=150, height=33)

line_175_frame = tk.Label(maincanvas)
line_175_frame["bg"] = "#adafae"
line_175_frame["text"] = ""
line_175_frame["relief"] = "sunken"
line_175_frame.place(x=10, y=7160, width=1060, height=40)

line_175_index = tk.Label(maincanvas)
line_175_index["bg"] = "#adafae"
line_175_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_175_index["font"] = ft
line_175_index["justify"] = "left"
line_175_index["anchor"] = "w"
line_175_index.place(x=20, y=7165, width=150, height=33)

line_175_name = tk.Label(maincanvas)
line_175_name["bg"] = "#adafae"
line_175_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_175_name["font"] = ft
line_175_name["justify"] = "left"
line_175_name["anchor"] = "w"
line_175_name.place(x=250, y=7165, width=500, height=33)

line_175_duration = tk.Label(maincanvas)
line_175_duration["bg"] = "#adafae"
line_175_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_175_duration["font"] = ft
line_175_duration["justify"] = "right"
line_175_duration["anchor"] = "e"
line_175_duration.place(x=910, y=7165, width=150, height=33)

line_175_live = tk.Label(maincanvas)
line_175_live["bg"] = "#adafae"
line_175_live["fg"] = "red"
line_175_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_175_live["font"] = ftl
line_175_live["justify"] = "left"
line_175_live["anchor"] = "w"
line_175_live["relief"] = "flat"
line_175_live.place(x=8000, y=7165, width=70, height=33)

line_175_disabled = tk.Label(maincanvas)
line_175_disabled["bg"] = "#adafae"
line_175_disabled["fg"] = "red"
line_175_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_175_disabled["font"] = ftl
line_175_disabled["justify"] = "left"
line_175_disabled["anchor"] = "w"
line_175_disabled["relief"] = "flat"
line_175_disabled.place(x=650, y=7165, width=150, height=33)

line_176_frame = tk.Label(maincanvas)
line_176_frame["bg"] = "#adafae"
line_176_frame["text"] = ""
line_176_frame["relief"] = "sunken"
line_176_frame.place(x=10, y=7200, width=1060, height=40)

line_176_index = tk.Label(maincanvas)
line_176_index["bg"] = "#adafae"
line_176_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_176_index["font"] = ft
line_176_index["justify"] = "left"
line_176_index["anchor"] = "w"
line_176_index.place(x=20, y=7205, width=150, height=33)

line_176_name = tk.Label(maincanvas)
line_176_name["bg"] = "#adafae"
line_176_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_176_name["font"] = ft
line_176_name["justify"] = "left"
line_176_name["anchor"] = "w"
line_176_name.place(x=250, y=7205, width=500, height=33)

line_176_duration = tk.Label(maincanvas)
line_176_duration["bg"] = "#adafae"
line_176_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_176_duration["font"] = ft
line_176_duration["justify"] = "right"
line_176_duration["anchor"] = "e"
line_176_duration.place(x=910, y=7205, width=150, height=33)

line_176_live = tk.Label(maincanvas)
line_176_live["bg"] = "#adafae"
line_176_live["fg"] = "red"
line_176_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_176_live["font"] = ftl
line_176_live["justify"] = "left"
line_176_live["anchor"] = "w"
line_176_live["relief"] = "flat"
line_176_live.place(x=8000, y=7205, width=70, height=33)

line_176_disabled = tk.Label(maincanvas)
line_176_disabled["bg"] = "#adafae"
line_176_disabled["fg"] = "red"
line_176_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_176_disabled["font"] = ftl
line_176_disabled["justify"] = "left"
line_176_disabled["anchor"] = "w"
line_176_disabled["relief"] = "flat"
line_176_disabled.place(x=650, y=7205, width=150, height=33)

line_177_frame = tk.Label(maincanvas)
line_177_frame["bg"] = "#adafae"
line_177_frame["text"] = ""
line_177_frame["relief"] = "sunken"
line_177_frame.place(x=10, y=7240, width=1060, height=40)

line_177_index = tk.Label(maincanvas)
line_177_index["bg"] = "#adafae"
line_177_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_177_index["font"] = ft
line_177_index["justify"] = "left"
line_177_index["anchor"] = "w"
line_177_index.place(x=20, y=7245, width=150, height=33)

line_177_name = tk.Label(maincanvas)
line_177_name["bg"] = "#adafae"
line_177_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_177_name["font"] = ft
line_177_name["justify"] = "left"
line_177_name["anchor"] = "w"
line_177_name.place(x=250, y=7245, width=500, height=33)

line_177_duration = tk.Label(maincanvas)
line_177_duration["bg"] = "#adafae"
line_177_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_177_duration["font"] = ft
line_177_duration["justify"] = "right"
line_177_duration["anchor"] = "e"
line_177_duration.place(x=910, y=7245, width=150, height=33)

line_177_live = tk.Label(maincanvas)
line_177_live["bg"] = "#adafae"
line_177_live["fg"] = "red"
line_177_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_177_live["font"] = ftl
line_177_live["justify"] = "left"
line_177_live["anchor"] = "w"
line_177_live["relief"] = "flat"
line_177_live.place(x=8000, y=7245, width=70, height=33)

line_177_disabled = tk.Label(maincanvas)
line_177_disabled["bg"] = "#adafae"
line_177_disabled["fg"] = "red"
line_177_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_177_disabled["font"] = ftl
line_177_disabled["justify"] = "left"
line_177_disabled["anchor"] = "w"
line_177_disabled["relief"] = "flat"
line_177_disabled.place(x=650, y=7245, width=150, height=33)

line_178_frame = tk.Label(maincanvas)
line_178_frame["bg"] = "#adafae"
line_178_frame["text"] = ""
line_178_frame["relief"] = "sunken"
line_178_frame.place(x=10, y=7280, width=1060, height=40)

line_178_index = tk.Label(maincanvas)
line_178_index["bg"] = "#adafae"
line_178_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_178_index["font"] = ft
line_178_index["justify"] = "left"
line_178_index["anchor"] = "w"
line_178_index.place(x=20, y=7285, width=150, height=33)

line_178_name = tk.Label(maincanvas)
line_178_name["bg"] = "#adafae"
line_178_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_178_name["font"] = ft
line_178_name["justify"] = "left"
line_178_name["anchor"] = "w"
line_178_name.place(x=250, y=7285, width=500, height=33)

line_178_duration = tk.Label(maincanvas)
line_178_duration["bg"] = "#adafae"
line_178_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_178_duration["font"] = ft
line_178_duration["justify"] = "right"
line_178_duration["anchor"] = "e"
line_178_duration.place(x=910, y=7285, width=150, height=33)

line_178_live = tk.Label(maincanvas)
line_178_live["bg"] = "#adafae"
line_178_live["fg"] = "red"
line_178_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_178_live["font"] = ftl
line_178_live["justify"] = "left"
line_178_live["anchor"] = "w"
line_178_live["relief"] = "flat"
line_178_live.place(x=8000, y=7285, width=70, height=33)

line_178_disabled = tk.Label(maincanvas)
line_178_disabled["bg"] = "#adafae"
line_178_disabled["fg"] = "red"
line_178_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_178_disabled["font"] = ftl
line_178_disabled["justify"] = "left"
line_178_disabled["anchor"] = "w"
line_178_disabled["relief"] = "flat"
line_178_disabled.place(x=650, y=7285, width=150, height=33)

line_179_frame = tk.Label(maincanvas)
line_179_frame["bg"] = "#adafae"
line_179_frame["text"] = ""
line_179_frame["relief"] = "sunken"
line_179_frame.place(x=10, y=7320, width=1060, height=40)

line_179_index = tk.Label(maincanvas)
line_179_index["bg"] = "#adafae"
line_179_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_179_index["font"] = ft
line_179_index["justify"] = "left"
line_179_index["anchor"] = "w"
line_179_index.place(x=20, y=7325, width=150, height=33)

line_179_name = tk.Label(maincanvas)
line_179_name["bg"] = "#adafae"
line_179_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_179_name["font"] = ft
line_179_name["justify"] = "left"
line_179_name["anchor"] = "w"
line_179_name.place(x=250, y=7325, width=500, height=33)

line_179_duration = tk.Label(maincanvas)
line_179_duration["bg"] = "#adafae"
line_179_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_179_duration["font"] = ft
line_179_duration["justify"] = "right"
line_179_duration["anchor"] = "e"
line_179_duration.place(x=910, y=7325, width=150, height=33)

line_179_live = tk.Label(maincanvas)
line_179_live["bg"] = "#adafae"
line_179_live["fg"] = "red"
line_179_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_179_live["font"] = ftl
line_179_live["justify"] = "left"
line_179_live["anchor"] = "w"
line_179_live["relief"] = "flat"
line_179_live.place(x=8000, y=7325, width=70, height=33)

line_179_disabled = tk.Label(maincanvas)
line_179_disabled["bg"] = "#adafae"
line_179_disabled["fg"] = "red"
line_179_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_179_disabled["font"] = ftl
line_179_disabled["justify"] = "left"
line_179_disabled["anchor"] = "w"
line_179_disabled["relief"] = "flat"
line_179_disabled.place(x=650, y=7325, width=150, height=33)

line_180_frame = tk.Label(maincanvas)
line_180_frame["bg"] = "#adafae"
line_180_frame["text"] = ""
line_180_frame["relief"] = "sunken"
line_180_frame.place(x=10, y=7360, width=1060, height=40)

line_180_index = tk.Label(maincanvas)
line_180_index["bg"] = "#adafae"
line_180_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_180_index["font"] = ft
line_180_index["justify"] = "left"
line_180_index["anchor"] = "w"
line_180_index.place(x=20, y=7365, width=150, height=33)

line_180_name = tk.Label(maincanvas)
line_180_name["bg"] = "#adafae"
line_180_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_180_name["font"] = ft
line_180_name["justify"] = "left"
line_180_name["anchor"] = "w"
line_180_name.place(x=250, y=7365, width=500, height=33)

line_180_duration = tk.Label(maincanvas)
line_180_duration["bg"] = "#adafae"
line_180_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_180_duration["font"] = ft
line_180_duration["justify"] = "right"
line_180_duration["anchor"] = "e"
line_180_duration.place(x=910, y=7365, width=150, height=33)

line_180_live = tk.Label(maincanvas)
line_180_live["bg"] = "#adafae"
line_180_live["fg"] = "red"
line_180_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_180_live["font"] = ftl
line_180_live["justify"] = "left"
line_180_live["anchor"] = "w"
line_180_live["relief"] = "flat"
line_180_live.place(x=8000, y=7365, width=70, height=33)

line_180_disabled = tk.Label(maincanvas)
line_180_disabled["bg"] = "#adafae"
line_180_disabled["fg"] = "red"
line_180_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_180_disabled["font"] = ftl
line_180_disabled["justify"] = "left"
line_180_disabled["anchor"] = "w"
line_180_disabled["relief"] = "flat"
line_180_disabled.place(x=650, y=7365, width=150, height=33)

line_181_frame = tk.Label(maincanvas)
line_181_frame["bg"] = "#adafae"
line_181_frame["text"] = ""
line_181_frame["relief"] = "sunken"
line_181_frame.place(x=10, y=7400, width=1060, height=40)

line_181_index = tk.Label(maincanvas)
line_181_index["bg"] = "#adafae"
line_181_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_181_index["font"] = ft
line_181_index["justify"] = "left"
line_181_index["anchor"] = "w"
line_181_index.place(x=20, y=7405, width=150, height=33)

line_181_name = tk.Label(maincanvas)
line_181_name["bg"] = "#adafae"
line_181_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_181_name["font"] = ft
line_181_name["justify"] = "left"
line_181_name["anchor"] = "w"
line_181_name.place(x=250, y=7405, width=500, height=33)

line_181_duration = tk.Label(maincanvas)
line_181_duration["bg"] = "#adafae"
line_181_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_181_duration["font"] = ft
line_181_duration["justify"] = "right"
line_181_duration["anchor"] = "e"
line_181_duration.place(x=910, y=7405, width=150, height=33)

line_181_live = tk.Label(maincanvas)
line_181_live["bg"] = "#adafae"
line_181_live["fg"] = "red"
line_181_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_181_live["font"] = ftl
line_181_live["justify"] = "left"
line_181_live["anchor"] = "w"
line_181_live["relief"] = "flat"
line_181_live.place(x=8000, y=7405, width=70, height=33)

line_181_disabled = tk.Label(maincanvas)
line_181_disabled["bg"] = "#adafae"
line_181_disabled["fg"] = "red"
line_181_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_181_disabled["font"] = ftl
line_181_disabled["justify"] = "left"
line_181_disabled["anchor"] = "w"
line_181_disabled["relief"] = "flat"
line_181_disabled.place(x=650, y=7405, width=150, height=33)

line_182_frame = tk.Label(maincanvas)
line_182_frame["bg"] = "#adafae"
line_182_frame["text"] = ""
line_182_frame["relief"] = "sunken"
line_182_frame.place(x=10, y=7440, width=1060, height=40)

line_182_index = tk.Label(maincanvas)
line_182_index["bg"] = "#adafae"
line_182_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_182_index["font"] = ft
line_182_index["justify"] = "left"
line_182_index["anchor"] = "w"
line_182_index.place(x=20, y=7445, width=150, height=33)

line_182_name = tk.Label(maincanvas)
line_182_name["bg"] = "#adafae"
line_182_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_182_name["font"] = ft
line_182_name["justify"] = "left"
line_182_name["anchor"] = "w"
line_182_name.place(x=250, y=7445, width=500, height=33)

line_182_duration = tk.Label(maincanvas)
line_182_duration["bg"] = "#adafae"
line_182_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_182_duration["font"] = ft
line_182_duration["justify"] = "right"
line_182_duration["anchor"] = "e"
line_182_duration.place(x=910, y=7445, width=150, height=33)

line_182_live = tk.Label(maincanvas)
line_182_live["bg"] = "#adafae"
line_182_live["fg"] = "red"
line_182_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_182_live["font"] = ftl
line_182_live["justify"] = "left"
line_182_live["anchor"] = "w"
line_182_live["relief"] = "flat"
line_182_live.place(x=8000, y=7445, width=70, height=33)

line_182_disabled = tk.Label(maincanvas)
line_182_disabled["bg"] = "#adafae"
line_182_disabled["fg"] = "red"
line_182_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_182_disabled["font"] = ftl
line_182_disabled["justify"] = "left"
line_182_disabled["anchor"] = "w"
line_182_disabled["relief"] = "flat"
line_182_disabled.place(x=650, y=7445, width=150, height=33)

line_183_frame = tk.Label(maincanvas)
line_183_frame["bg"] = "#adafae"
line_183_frame["text"] = ""
line_183_frame["relief"] = "sunken"
line_183_frame.place(x=10, y=7480, width=1060, height=40)

line_183_index = tk.Label(maincanvas)
line_183_index["bg"] = "#adafae"
line_183_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_183_index["font"] = ft
line_183_index["justify"] = "left"
line_183_index["anchor"] = "w"
line_183_index.place(x=20, y=7485, width=150, height=33)

line_183_name = tk.Label(maincanvas)
line_183_name["bg"] = "#adafae"
line_183_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_183_name["font"] = ft
line_183_name["justify"] = "left"
line_183_name["anchor"] = "w"
line_183_name.place(x=250, y=7485, width=500, height=33)

line_183_duration = tk.Label(maincanvas)
line_183_duration["bg"] = "#adafae"
line_183_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_183_duration["font"] = ft
line_183_duration["justify"] = "right"
line_183_duration["anchor"] = "e"
line_183_duration.place(x=910, y=7485, width=150, height=33)

line_183_live = tk.Label(maincanvas)
line_183_live["bg"] = "#adafae"
line_183_live["fg"] = "red"
line_183_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_183_live["font"] = ftl
line_183_live["justify"] = "left"
line_183_live["anchor"] = "w"
line_183_live["relief"] = "flat"
line_183_live.place(x=8000, y=7485, width=70, height=33)

line_183_disabled = tk.Label(maincanvas)
line_183_disabled["bg"] = "#adafae"
line_183_disabled["fg"] = "red"
line_183_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_183_disabled["font"] = ftl
line_183_disabled["justify"] = "left"
line_183_disabled["anchor"] = "w"
line_183_disabled["relief"] = "flat"
line_183_disabled.place(x=650, y=7485, width=150, height=33)

line_184_frame = tk.Label(maincanvas)
line_184_frame["bg"] = "#adafae"
line_184_frame["text"] = ""
line_184_frame["relief"] = "sunken"
line_184_frame.place(x=10, y=7520, width=1060, height=40)

line_184_index = tk.Label(maincanvas)
line_184_index["bg"] = "#adafae"
line_184_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_184_index["font"] = ft
line_184_index["justify"] = "left"
line_184_index["anchor"] = "w"
line_184_index.place(x=20, y=7525, width=150, height=33)

line_184_name = tk.Label(maincanvas)
line_184_name["bg"] = "#adafae"
line_184_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_184_name["font"] = ft
line_184_name["justify"] = "left"
line_184_name["anchor"] = "w"
line_184_name.place(x=250, y=7525, width=500, height=33)

line_184_duration = tk.Label(maincanvas)
line_184_duration["bg"] = "#adafae"
line_184_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_184_duration["font"] = ft
line_184_duration["justify"] = "right"
line_184_duration["anchor"] = "e"
line_184_duration.place(x=910, y=7525, width=150, height=33)

line_184_live = tk.Label(maincanvas)
line_184_live["bg"] = "#adafae"
line_184_live["fg"] = "red"
line_184_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_184_live["font"] = ftl
line_184_live["justify"] = "left"
line_184_live["anchor"] = "w"
line_184_live["relief"] = "flat"
line_184_live.place(x=8000, y=7525, width=70, height=33)

line_184_disabled = tk.Label(maincanvas)
line_184_disabled["bg"] = "#adafae"
line_184_disabled["fg"] = "red"
line_184_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_184_disabled["font"] = ftl
line_184_disabled["justify"] = "left"
line_184_disabled["anchor"] = "w"
line_184_disabled["relief"] = "flat"
line_184_disabled.place(x=650, y=7525, width=150, height=33)

line_185_frame = tk.Label(maincanvas)
line_185_frame["bg"] = "#adafae"
line_185_frame["text"] = ""
line_185_frame["relief"] = "sunken"
line_185_frame.place(x=10, y=7560, width=1060, height=40)

line_185_index = tk.Label(maincanvas)
line_185_index["bg"] = "#adafae"
line_185_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_185_index["font"] = ft
line_185_index["justify"] = "left"
line_185_index["anchor"] = "w"
line_185_index.place(x=20, y=7565, width=150, height=33)

line_185_name = tk.Label(maincanvas)
line_185_name["bg"] = "#adafae"
line_185_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_185_name["font"] = ft
line_185_name["justify"] = "left"
line_185_name["anchor"] = "w"
line_185_name.place(x=250, y=7565, width=500, height=33)

line_185_duration = tk.Label(maincanvas)
line_185_duration["bg"] = "#adafae"
line_185_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_185_duration["font"] = ft
line_185_duration["justify"] = "right"
line_185_duration["anchor"] = "e"
line_185_duration.place(x=910, y=7565, width=150, height=33)

line_185_live = tk.Label(maincanvas)
line_185_live["bg"] = "#adafae"
line_185_live["fg"] = "red"
line_185_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_185_live["font"] = ftl
line_185_live["justify"] = "left"
line_185_live["anchor"] = "w"
line_185_live["relief"] = "flat"
line_185_live.place(x=8000, y=7565, width=70, height=33)

line_185_disabled = tk.Label(maincanvas)
line_185_disabled["bg"] = "#adafae"
line_185_disabled["fg"] = "red"
line_185_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_185_disabled["font"] = ftl
line_185_disabled["justify"] = "left"
line_185_disabled["anchor"] = "w"
line_185_disabled["relief"] = "flat"
line_185_disabled.place(x=650, y=7565, width=150, height=33)

line_186_frame = tk.Label(maincanvas)
line_186_frame["bg"] = "#adafae"
line_186_frame["text"] = ""
line_186_frame["relief"] = "sunken"
line_186_frame.place(x=10, y=7600, width=1060, height=40)

line_186_index = tk.Label(maincanvas)
line_186_index["bg"] = "#adafae"
line_186_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_186_index["font"] = ft
line_186_index["justify"] = "left"
line_186_index["anchor"] = "w"
line_186_index.place(x=20, y=7605, width=150, height=33)

line_186_name = tk.Label(maincanvas)
line_186_name["bg"] = "#adafae"
line_186_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_186_name["font"] = ft
line_186_name["justify"] = "left"
line_186_name["anchor"] = "w"
line_186_name.place(x=250, y=7605, width=500, height=33)

line_186_duration = tk.Label(maincanvas)
line_186_duration["bg"] = "#adafae"
line_186_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_186_duration["font"] = ft
line_186_duration["justify"] = "right"
line_186_duration["anchor"] = "e"
line_186_duration.place(x=910, y=7605, width=150, height=33)

line_186_live = tk.Label(maincanvas)
line_186_live["bg"] = "#adafae"
line_186_live["fg"] = "red"
line_186_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_186_live["font"] = ftl
line_186_live["justify"] = "left"
line_186_live["anchor"] = "w"
line_186_live["relief"] = "flat"
line_186_live.place(x=8000, y=7605, width=70, height=33)

line_186_disabled = tk.Label(maincanvas)
line_186_disabled["bg"] = "#adafae"
line_186_disabled["fg"] = "red"
line_186_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_186_disabled["font"] = ftl
line_186_disabled["justify"] = "left"
line_186_disabled["anchor"] = "w"
line_186_disabled["relief"] = "flat"
line_186_disabled.place(x=650, y=7605, width=150, height=33)

line_187_frame = tk.Label(maincanvas)
line_187_frame["bg"] = "#adafae"
line_187_frame["text"] = ""
line_187_frame["relief"] = "sunken"
line_187_frame.place(x=10, y=7640, width=1060, height=40)

line_187_index = tk.Label(maincanvas)
line_187_index["bg"] = "#adafae"
line_187_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_187_index["font"] = ft
line_187_index["justify"] = "left"
line_187_index["anchor"] = "w"
line_187_index.place(x=20, y=7645, width=150, height=33)

line_187_name = tk.Label(maincanvas)
line_187_name["bg"] = "#adafae"
line_187_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_187_name["font"] = ft
line_187_name["justify"] = "left"
line_187_name["anchor"] = "w"
line_187_name.place(x=250, y=7645, width=500, height=33)

line_187_duration = tk.Label(maincanvas)
line_187_duration["bg"] = "#adafae"
line_187_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_187_duration["font"] = ft
line_187_duration["justify"] = "right"
line_187_duration["anchor"] = "e"
line_187_duration.place(x=910, y=7645, width=150, height=33)

line_187_live = tk.Label(maincanvas)
line_187_live["bg"] = "#adafae"
line_187_live["fg"] = "red"
line_187_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_187_live["font"] = ftl
line_187_live["justify"] = "left"
line_187_live["anchor"] = "w"
line_187_live["relief"] = "flat"
line_187_live.place(x=8000, y=7645, width=70, height=33)

line_187_disabled = tk.Label(maincanvas)
line_187_disabled["bg"] = "#adafae"
line_187_disabled["fg"] = "red"
line_187_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_187_disabled["font"] = ftl
line_187_disabled["justify"] = "left"
line_187_disabled["anchor"] = "w"
line_187_disabled["relief"] = "flat"
line_187_disabled.place(x=650, y=7645, width=150, height=33)

line_188_frame = tk.Label(maincanvas)
line_188_frame["bg"] = "#adafae"
line_188_frame["text"] = ""
line_188_frame["relief"] = "sunken"
line_188_frame.place(x=10, y=7680, width=1060, height=40)

line_188_index = tk.Label(maincanvas)
line_188_index["bg"] = "#adafae"
line_188_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_188_index["font"] = ft
line_188_index["justify"] = "left"
line_188_index["anchor"] = "w"
line_188_index.place(x=20, y=7685, width=150, height=33)

line_188_name = tk.Label(maincanvas)
line_188_name["bg"] = "#adafae"
line_188_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_188_name["font"] = ft
line_188_name["justify"] = "left"
line_188_name["anchor"] = "w"
line_188_name.place(x=250, y=7685, width=500, height=33)

line_188_duration = tk.Label(maincanvas)
line_188_duration["bg"] = "#adafae"
line_188_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_188_duration["font"] = ft
line_188_duration["justify"] = "right"
line_188_duration["anchor"] = "e"
line_188_duration.place(x=910, y=7685, width=150, height=33)

line_188_live = tk.Label(maincanvas)
line_188_live["bg"] = "#adafae"
line_188_live["fg"] = "red"
line_188_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_188_live["font"] = ftl
line_188_live["justify"] = "left"
line_188_live["anchor"] = "w"
line_188_live["relief"] = "flat"
line_188_live.place(x=8000, y=7685, width=70, height=33)

line_188_disabled = tk.Label(maincanvas)
line_188_disabled["bg"] = "#adafae"
line_188_disabled["fg"] = "red"
line_188_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_188_disabled["font"] = ftl
line_188_disabled["justify"] = "left"
line_188_disabled["anchor"] = "w"
line_188_disabled["relief"] = "flat"
line_188_disabled.place(x=650, y=7685, width=150, height=33)

line_189_frame = tk.Label(maincanvas)
line_189_frame["bg"] = "#adafae"
line_189_frame["text"] = ""
line_189_frame["relief"] = "sunken"
line_189_frame.place(x=10, y=7720, width=1060, height=40)

line_189_index = tk.Label(maincanvas)
line_189_index["bg"] = "#adafae"
line_189_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_189_index["font"] = ft
line_189_index["justify"] = "left"
line_189_index["anchor"] = "w"
line_189_index.place(x=20, y=7725, width=150, height=33)

line_189_name = tk.Label(maincanvas)
line_189_name["bg"] = "#adafae"
line_189_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_189_name["font"] = ft
line_189_name["justify"] = "left"
line_189_name["anchor"] = "w"
line_189_name.place(x=250, y=7725, width=500, height=33)

line_189_duration = tk.Label(maincanvas)
line_189_duration["bg"] = "#adafae"
line_189_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_189_duration["font"] = ft
line_189_duration["justify"] = "right"
line_189_duration["anchor"] = "e"
line_189_duration.place(x=910, y=7725, width=150, height=33)

line_189_live = tk.Label(maincanvas)
line_189_live["bg"] = "#adafae"
line_189_live["fg"] = "red"
line_189_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_189_live["font"] = ftl
line_189_live["justify"] = "left"
line_189_live["anchor"] = "w"
line_189_live["relief"] = "flat"
line_189_live.place(x=8000, y=7725, width=70, height=33)

line_189_disabled = tk.Label(maincanvas)
line_189_disabled["bg"] = "#adafae"
line_189_disabled["fg"] = "red"
line_189_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_189_disabled["font"] = ftl
line_189_disabled["justify"] = "left"
line_189_disabled["anchor"] = "w"
line_189_disabled["relief"] = "flat"
line_189_disabled.place(x=650, y=7725, width=150, height=33)

line_190_frame = tk.Label(maincanvas)
line_190_frame["bg"] = "#adafae"
line_190_frame["text"] = ""
line_190_frame["relief"] = "sunken"
line_190_frame.place(x=10, y=7760, width=1060, height=40)

line_190_index = tk.Label(maincanvas)
line_190_index["bg"] = "#adafae"
line_190_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_190_index["font"] = ft
line_190_index["justify"] = "left"
line_190_index["anchor"] = "w"
line_190_index.place(x=20, y=7765, width=150, height=33)

line_190_name = tk.Label(maincanvas)
line_190_name["bg"] = "#adafae"
line_190_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_190_name["font"] = ft
line_190_name["justify"] = "left"
line_190_name["anchor"] = "w"
line_190_name.place(x=250, y=7765, width=500, height=33)

line_190_duration = tk.Label(maincanvas)
line_190_duration["bg"] = "#adafae"
line_190_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_190_duration["font"] = ft
line_190_duration["justify"] = "right"
line_190_duration["anchor"] = "e"
line_190_duration.place(x=910, y=7765, width=150, height=33)

line_190_live = tk.Label(maincanvas)
line_190_live["bg"] = "#adafae"
line_190_live["fg"] = "red"
line_190_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_190_live["font"] = ftl
line_190_live["justify"] = "left"
line_190_live["anchor"] = "w"
line_190_live["relief"] = "flat"
line_190_live.place(x=8000, y=7765, width=70, height=33)

line_190_disabled = tk.Label(maincanvas)
line_190_disabled["bg"] = "#adafae"
line_190_disabled["fg"] = "red"
line_190_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_190_disabled["font"] = ftl
line_190_disabled["justify"] = "left"
line_190_disabled["anchor"] = "w"
line_190_disabled["relief"] = "flat"
line_190_disabled.place(x=650, y=7765, width=150, height=33)

line_191_frame = tk.Label(maincanvas)
line_191_frame["bg"] = "#adafae"
line_191_frame["text"] = ""
line_191_frame["relief"] = "sunken"
line_191_frame.place(x=10, y=7800, width=1060, height=40)

line_191_index = tk.Label(maincanvas)
line_191_index["bg"] = "#adafae"
line_191_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_191_index["font"] = ft
line_191_index["justify"] = "left"
line_191_index["anchor"] = "w"
line_191_index.place(x=20, y=7805, width=150, height=33)

line_191_name = tk.Label(maincanvas)
line_191_name["bg"] = "#adafae"
line_191_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_191_name["font"] = ft
line_191_name["justify"] = "left"
line_191_name["anchor"] = "w"
line_191_name.place(x=250, y=7805, width=500, height=33)

line_191_duration = tk.Label(maincanvas)
line_191_duration["bg"] = "#adafae"
line_191_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_191_duration["font"] = ft
line_191_duration["justify"] = "right"
line_191_duration["anchor"] = "e"
line_191_duration.place(x=910, y=7805, width=150, height=33)

line_191_live = tk.Label(maincanvas)
line_191_live["bg"] = "#adafae"
line_191_live["fg"] = "red"
line_191_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_191_live["font"] = ftl
line_191_live["justify"] = "left"
line_191_live["anchor"] = "w"
line_191_live["relief"] = "flat"
line_191_live.place(x=8000, y=7805, width=70, height=33)

line_191_disabled = tk.Label(maincanvas)
line_191_disabled["bg"] = "#adafae"
line_191_disabled["fg"] = "red"
line_191_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_191_disabled["font"] = ftl
line_191_disabled["justify"] = "left"
line_191_disabled["anchor"] = "w"
line_191_disabled["relief"] = "flat"
line_191_disabled.place(x=650, y=7805, width=150, height=33)

line_192_frame = tk.Label(maincanvas)
line_192_frame["bg"] = "#adafae"
line_192_frame["text"] = ""
line_192_frame["relief"] = "sunken"
line_192_frame.place(x=10, y=7840, width=1060, height=40)

line_192_index = tk.Label(maincanvas)
line_192_index["bg"] = "#adafae"
line_192_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_192_index["font"] = ft
line_192_index["justify"] = "left"
line_192_index["anchor"] = "w"
line_192_index.place(x=20, y=7845, width=150, height=33)

line_192_name = tk.Label(maincanvas)
line_192_name["bg"] = "#adafae"
line_192_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_192_name["font"] = ft
line_192_name["justify"] = "left"
line_192_name["anchor"] = "w"
line_192_name.place(x=250, y=7845, width=500, height=33)

line_192_duration = tk.Label(maincanvas)
line_192_duration["bg"] = "#adafae"
line_192_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_192_duration["font"] = ft
line_192_duration["justify"] = "right"
line_192_duration["anchor"] = "e"
line_192_duration.place(x=910, y=7845, width=150, height=33)

line_192_live = tk.Label(maincanvas)
line_192_live["bg"] = "#adafae"
line_192_live["fg"] = "red"
line_192_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_192_live["font"] = ftl
line_192_live["justify"] = "left"
line_192_live["anchor"] = "w"
line_192_live["relief"] = "flat"
line_192_live.place(x=8000, y=7845, width=70, height=33)

line_192_disabled = tk.Label(maincanvas)
line_192_disabled["bg"] = "#adafae"
line_192_disabled["fg"] = "red"
line_192_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_192_disabled["font"] = ftl
line_192_disabled["justify"] = "left"
line_192_disabled["anchor"] = "w"
line_192_disabled["relief"] = "flat"
line_192_disabled.place(x=650, y=7845, width=150, height=33)

line_193_frame = tk.Label(maincanvas)
line_193_frame["bg"] = "#adafae"
line_193_frame["text"] = ""
line_193_frame["relief"] = "sunken"
line_193_frame.place(x=10, y=7880, width=1060, height=40)

line_193_index = tk.Label(maincanvas)
line_193_index["bg"] = "#adafae"
line_193_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_193_index["font"] = ft
line_193_index["justify"] = "left"
line_193_index["anchor"] = "w"
line_193_index.place(x=20, y=7885, width=150, height=33)

line_193_name = tk.Label(maincanvas)
line_193_name["bg"] = "#adafae"
line_193_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_193_name["font"] = ft
line_193_name["justify"] = "left"
line_193_name["anchor"] = "w"
line_193_name.place(x=250, y=7885, width=500, height=33)

line_193_duration = tk.Label(maincanvas)
line_193_duration["bg"] = "#adafae"
line_193_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_193_duration["font"] = ft
line_193_duration["justify"] = "right"
line_193_duration["anchor"] = "e"
line_193_duration.place(x=910, y=7885, width=150, height=33)

line_193_live = tk.Label(maincanvas)
line_193_live["bg"] = "#adafae"
line_193_live["fg"] = "red"
line_193_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_193_live["font"] = ftl
line_193_live["justify"] = "left"
line_193_live["anchor"] = "w"
line_193_live["relief"] = "flat"
line_193_live.place(x=8000, y=7885, width=70, height=33)

line_193_disabled = tk.Label(maincanvas)
line_193_disabled["bg"] = "#adafae"
line_193_disabled["fg"] = "red"
line_193_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_193_disabled["font"] = ftl
line_193_disabled["justify"] = "left"
line_193_disabled["anchor"] = "w"
line_193_disabled["relief"] = "flat"
line_193_disabled.place(x=650, y=7885, width=150, height=33)

line_194_frame = tk.Label(maincanvas)
line_194_frame["bg"] = "#adafae"
line_194_frame["text"] = ""
line_194_frame["relief"] = "sunken"
line_194_frame.place(x=10, y=7920, width=1060, height=40)

line_194_index = tk.Label(maincanvas)
line_194_index["bg"] = "#adafae"
line_194_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_194_index["font"] = ft
line_194_index["justify"] = "left"
line_194_index["anchor"] = "w"
line_194_index.place(x=20, y=7925, width=150, height=33)

line_194_name = tk.Label(maincanvas)
line_194_name["bg"] = "#adafae"
line_194_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_194_name["font"] = ft
line_194_name["justify"] = "left"
line_194_name["anchor"] = "w"
line_194_name.place(x=250, y=7925, width=500, height=33)

line_194_duration = tk.Label(maincanvas)
line_194_duration["bg"] = "#adafae"
line_194_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_194_duration["font"] = ft
line_194_duration["justify"] = "right"
line_194_duration["anchor"] = "e"
line_194_duration.place(x=910, y=7925, width=150, height=33)

line_194_live = tk.Label(maincanvas)
line_194_live["bg"] = "#adafae"
line_194_live["fg"] = "red"
line_194_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_194_live["font"] = ftl
line_194_live["justify"] = "left"
line_194_live["anchor"] = "w"
line_194_live["relief"] = "flat"
line_194_live.place(x=8000, y=7925, width=70, height=33)

line_194_disabled = tk.Label(maincanvas)
line_194_disabled["bg"] = "#adafae"
line_194_disabled["fg"] = "red"
line_194_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_194_disabled["font"] = ftl
line_194_disabled["justify"] = "left"
line_194_disabled["anchor"] = "w"
line_194_disabled["relief"] = "flat"
line_194_disabled.place(x=650, y=7925, width=150, height=33)

line_195_frame = tk.Label(maincanvas)
line_195_frame["bg"] = "#adafae"
line_195_frame["text"] = ""
line_195_frame["relief"] = "sunken"
line_195_frame.place(x=10, y=7960, width=1060, height=40)

line_195_index = tk.Label(maincanvas)
line_195_index["bg"] = "#adafae"
line_195_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_195_index["font"] = ft
line_195_index["justify"] = "left"
line_195_index["anchor"] = "w"
line_195_index.place(x=20, y=7965, width=150, height=33)

line_195_name = tk.Label(maincanvas)
line_195_name["bg"] = "#adafae"
line_195_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_195_name["font"] = ft
line_195_name["justify"] = "left"
line_195_name["anchor"] = "w"
line_195_name.place(x=250, y=7965, width=500, height=33)

line_195_duration = tk.Label(maincanvas)
line_195_duration["bg"] = "#adafae"
line_195_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_195_duration["font"] = ft
line_195_duration["justify"] = "right"
line_195_duration["anchor"] = "e"
line_195_duration.place(x=910, y=7965, width=150, height=33)

line_195_live = tk.Label(maincanvas)
line_195_live["bg"] = "#adafae"
line_195_live["fg"] = "red"
line_195_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_195_live["font"] = ftl
line_195_live["justify"] = "left"
line_195_live["anchor"] = "w"
line_195_live["relief"] = "flat"
line_195_live.place(x=8000, y=7965, width=70, height=33)

line_195_disabled = tk.Label(maincanvas)
line_195_disabled["bg"] = "#adafae"
line_195_disabled["fg"] = "red"
line_195_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_195_disabled["font"] = ftl
line_195_disabled["justify"] = "left"
line_195_disabled["anchor"] = "w"
line_195_disabled["relief"] = "flat"
line_195_disabled.place(x=650, y=7965, width=150, height=33)

line_196_frame = tk.Label(maincanvas)
line_196_frame["bg"] = "#adafae"
line_196_frame["text"] = ""
line_196_frame["relief"] = "sunken"
line_196_frame.place(x=10, y=8000, width=1060, height=40)

line_196_index = tk.Label(maincanvas)
line_196_index["bg"] = "#adafae"
line_196_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_196_index["font"] = ft
line_196_index["justify"] = "left"
line_196_index["anchor"] = "w"
line_196_index.place(x=20, y=8005, width=150, height=33)

line_196_name = tk.Label(maincanvas)
line_196_name["bg"] = "#adafae"
line_196_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_196_name["font"] = ft
line_196_name["justify"] = "left"
line_196_name["anchor"] = "w"
line_196_name.place(x=250, y=8005, width=500, height=33)

line_196_duration = tk.Label(maincanvas)
line_196_duration["bg"] = "#adafae"
line_196_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_196_duration["font"] = ft
line_196_duration["justify"] = "right"
line_196_duration["anchor"] = "e"
line_196_duration.place(x=910, y=8005, width=150, height=33)

line_196_live = tk.Label(maincanvas)
line_196_live["bg"] = "#adafae"
line_196_live["fg"] = "red"
line_196_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_196_live["font"] = ftl
line_196_live["justify"] = "left"
line_196_live["anchor"] = "w"
line_196_live["relief"] = "flat"
line_196_live.place(x=8000, y=8005, width=70, height=33)

line_196_disabled = tk.Label(maincanvas)
line_196_disabled["bg"] = "#adafae"
line_196_disabled["fg"] = "red"
line_196_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_196_disabled["font"] = ftl
line_196_disabled["justify"] = "left"
line_196_disabled["anchor"] = "w"
line_196_disabled["relief"] = "flat"
line_196_disabled.place(x=650, y=8005, width=150, height=33)

line_197_frame = tk.Label(maincanvas)
line_197_frame["bg"] = "#adafae"
line_197_frame["text"] = ""
line_197_frame["relief"] = "sunken"
line_197_frame.place(x=10, y=8040, width=1060, height=40)

line_197_index = tk.Label(maincanvas)
line_197_index["bg"] = "#adafae"
line_197_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_197_index["font"] = ft
line_197_index["justify"] = "left"
line_197_index["anchor"] = "w"
line_197_index.place(x=20, y=8045, width=150, height=33)

line_197_name = tk.Label(maincanvas)
line_197_name["bg"] = "#adafae"
line_197_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_197_name["font"] = ft
line_197_name["justify"] = "left"
line_197_name["anchor"] = "w"
line_197_name.place(x=250, y=8045, width=500, height=33)

line_197_duration = tk.Label(maincanvas)
line_197_duration["bg"] = "#adafae"
line_197_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_197_duration["font"] = ft
line_197_duration["justify"] = "right"
line_197_duration["anchor"] = "e"
line_197_duration.place(x=910, y=8045, width=150, height=33)

line_197_live = tk.Label(maincanvas)
line_197_live["bg"] = "#adafae"
line_197_live["fg"] = "red"
line_197_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_197_live["font"] = ftl
line_197_live["justify"] = "left"
line_197_live["anchor"] = "w"
line_197_live["relief"] = "flat"
line_197_live.place(x=8000, y=8045, width=70, height=33)

line_197_disabled = tk.Label(maincanvas)
line_197_disabled["bg"] = "#adafae"
line_197_disabled["fg"] = "red"
line_197_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_197_disabled["font"] = ftl
line_197_disabled["justify"] = "left"
line_197_disabled["anchor"] = "w"
line_197_disabled["relief"] = "flat"
line_197_disabled.place(x=650, y=8045, width=150, height=33)

line_198_frame = tk.Label(maincanvas)
line_198_frame["bg"] = "#adafae"
line_198_frame["text"] = ""
line_198_frame["relief"] = "sunken"
line_198_frame.place(x=10, y=8080, width=1060, height=40)

line_198_index = tk.Label(maincanvas)
line_198_index["bg"] = "#adafae"
line_198_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_198_index["font"] = ft
line_198_index["justify"] = "left"
line_198_index["anchor"] = "w"
line_198_index.place(x=20, y=8085, width=150, height=33)

line_198_name = tk.Label(maincanvas)
line_198_name["bg"] = "#adafae"
line_198_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_198_name["font"] = ft
line_198_name["justify"] = "left"
line_198_name["anchor"] = "w"
line_198_name.place(x=250, y=8085, width=500, height=33)

line_198_duration = tk.Label(maincanvas)
line_198_duration["bg"] = "#adafae"
line_198_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_198_duration["font"] = ft
line_198_duration["justify"] = "right"
line_198_duration["anchor"] = "e"
line_198_duration.place(x=910, y=8085, width=150, height=33)

line_198_live = tk.Label(maincanvas)
line_198_live["bg"] = "#adafae"
line_198_live["fg"] = "red"
line_198_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_198_live["font"] = ftl
line_198_live["justify"] = "left"
line_198_live["anchor"] = "w"
line_198_live["relief"] = "flat"
line_198_live.place(x=8000, y=8085, width=70, height=33)

line_198_disabled = tk.Label(maincanvas)
line_198_disabled["bg"] = "#adafae"
line_198_disabled["fg"] = "red"
line_198_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_198_disabled["font"] = ftl
line_198_disabled["justify"] = "left"
line_198_disabled["anchor"] = "w"
line_198_disabled["relief"] = "flat"
line_198_disabled.place(x=650, y=8085, width=150, height=33)

line_199_frame = tk.Label(maincanvas)
line_199_frame["bg"] = "#adafae"
line_199_frame["text"] = ""
line_199_frame["relief"] = "sunken"
line_199_frame.place(x=10, y=8120, width=1060, height=40)

line_199_index = tk.Label(maincanvas)
line_199_index["bg"] = "#adafae"
line_199_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_199_index["font"] = ft
line_199_index["justify"] = "left"
line_199_index["anchor"] = "w"
line_199_index.place(x=20, y=8125, width=150, height=33)

line_199_name = tk.Label(maincanvas)
line_199_name["bg"] = "#adafae"
line_199_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_199_name["font"] = ft
line_199_name["justify"] = "left"
line_199_name["anchor"] = "w"
line_199_name.place(x=250, y=8125, width=500, height=33)

line_199_duration = tk.Label(maincanvas)
line_199_duration["bg"] = "#adafae"
line_199_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_199_duration["font"] = ft
line_199_duration["justify"] = "right"
line_199_duration["anchor"] = "e"
line_199_duration.place(x=910, y=8125, width=150, height=33)

line_199_live = tk.Label(maincanvas)
line_199_live["bg"] = "#adafae"
line_199_live["fg"] = "red"
line_199_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_199_live["font"] = ftl
line_199_live["justify"] = "left"
line_199_live["anchor"] = "w"
line_199_live["relief"] = "flat"
line_199_live.place(x=8000, y=8125, width=70, height=33)

line_199_disabled = tk.Label(maincanvas)
line_199_disabled["bg"] = "#adafae"
line_199_disabled["fg"] = "red"
line_199_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_199_disabled["font"] = ftl
line_199_disabled["justify"] = "left"
line_199_disabled["anchor"] = "w"
line_199_disabled["relief"] = "flat"
line_199_disabled.place(x=650, y=8125, width=150, height=33)

line_200_frame = tk.Label(maincanvas)
line_200_frame["bg"] = "#adafae"
line_200_frame["text"] = ""
line_200_frame["relief"] = "sunken"
line_200_frame.place(x=10, y=8160, width=1060, height=40)

line_200_index = tk.Label(maincanvas)
line_200_index["bg"] = "#adafae"
line_200_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_200_index["font"] = ft
line_200_index["justify"] = "left"
line_200_index["anchor"] = "w"
line_200_index.place(x=20, y=8165, width=150, height=33)

line_200_name = tk.Label(maincanvas)
line_200_name["bg"] = "#adafae"
line_200_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_200_name["font"] = ft
line_200_name["justify"] = "left"
line_200_name["anchor"] = "w"
line_200_name.place(x=250, y=8165, width=500, height=33)

line_200_duration = tk.Label(maincanvas)
line_200_duration["bg"] = "#adafae"
line_200_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_200_duration["font"] = ft
line_200_duration["justify"] = "right"
line_200_duration["anchor"] = "e"
line_200_duration.place(x=910, y=8165, width=150, height=33)

line_200_live = tk.Label(maincanvas)
line_200_live["bg"] = "#adafae"
line_200_live["fg"] = "red"
line_200_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_200_live["font"] = ftl
line_200_live["justify"] = "left"
line_200_live["anchor"] = "w"
line_200_live["relief"] = "flat"
line_200_live.place(x=8000, y=8165, width=70, height=33)

line_200_disabled = tk.Label(maincanvas)
line_200_disabled["bg"] = "#adafae"
line_200_disabled["fg"] = "red"
line_200_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_200_disabled["font"] = ftl
line_200_disabled["justify"] = "left"
line_200_disabled["anchor"] = "w"
line_200_disabled["relief"] = "flat"
line_200_disabled.place(x=650, y=8165, width=150, height=33)

line_201_frame = tk.Label(maincanvas)
line_201_frame["bg"] = "#adafae"
line_201_frame["text"] = ""
line_201_frame["relief"] = "sunken"
line_201_frame.place(x=10, y=8200, width=1060, height=40)

line_201_index = tk.Label(maincanvas)
line_201_index["bg"] = "#adafae"
line_201_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_201_index["font"] = ft
line_201_index["justify"] = "left"
line_201_index["anchor"] = "w"
line_201_index.place(x=20, y=8205, width=150, height=33)

line_201_name = tk.Label(maincanvas)
line_201_name["bg"] = "#adafae"
line_201_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_201_name["font"] = ft
line_201_name["justify"] = "left"
line_201_name["anchor"] = "w"
line_201_name.place(x=250, y=8205, width=500, height=33)

line_201_duration = tk.Label(maincanvas)
line_201_duration["bg"] = "#adafae"
line_201_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_201_duration["font"] = ft
line_201_duration["justify"] = "right"
line_201_duration["anchor"] = "e"
line_201_duration.place(x=910, y=8205, width=150, height=33)

line_201_live = tk.Label(maincanvas)
line_201_live["bg"] = "#adafae"
line_201_live["fg"] = "red"
line_201_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_201_live["font"] = ftl
line_201_live["justify"] = "left"
line_201_live["anchor"] = "w"
line_201_live["relief"] = "flat"
line_201_live.place(x=8000, y=8205, width=70, height=33)

line_201_disabled = tk.Label(maincanvas)
line_201_disabled["bg"] = "#adafae"
line_201_disabled["fg"] = "red"
line_201_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_201_disabled["font"] = ftl
line_201_disabled["justify"] = "left"
line_201_disabled["anchor"] = "w"
line_201_disabled["relief"] = "flat"
line_201_disabled.place(x=650, y=8205, width=150, height=33)

line_202_frame = tk.Label(maincanvas)
line_202_frame["bg"] = "#adafae"
line_202_frame["text"] = ""
line_202_frame["relief"] = "sunken"
line_202_frame.place(x=10, y=8240, width=1060, height=40)

line_202_index = tk.Label(maincanvas)
line_202_index["bg"] = "#adafae"
line_202_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_202_index["font"] = ft
line_202_index["justify"] = "left"
line_202_index["anchor"] = "w"
line_202_index.place(x=20, y=8245, width=150, height=33)

line_202_name = tk.Label(maincanvas)
line_202_name["bg"] = "#adafae"
line_202_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_202_name["font"] = ft
line_202_name["justify"] = "left"
line_202_name["anchor"] = "w"
line_202_name.place(x=250, y=8245, width=500, height=33)

line_202_duration = tk.Label(maincanvas)
line_202_duration["bg"] = "#adafae"
line_202_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_202_duration["font"] = ft
line_202_duration["justify"] = "right"
line_202_duration["anchor"] = "e"
line_202_duration.place(x=910, y=8245, width=150, height=33)

line_202_live = tk.Label(maincanvas)
line_202_live["bg"] = "#adafae"
line_202_live["fg"] = "red"
line_202_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_202_live["font"] = ftl
line_202_live["justify"] = "left"
line_202_live["anchor"] = "w"
line_202_live["relief"] = "flat"
line_202_live.place(x=8000, y=8245, width=70, height=33)

line_202_disabled = tk.Label(maincanvas)
line_202_disabled["bg"] = "#adafae"
line_202_disabled["fg"] = "red"
line_202_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_202_disabled["font"] = ftl
line_202_disabled["justify"] = "left"
line_202_disabled["anchor"] = "w"
line_202_disabled["relief"] = "flat"
line_202_disabled.place(x=650, y=8245, width=150, height=33)

line_203_frame = tk.Label(maincanvas)
line_203_frame["bg"] = "#adafae"
line_203_frame["text"] = ""
line_203_frame["relief"] = "sunken"
line_203_frame.place(x=10, y=8280, width=1060, height=40)

line_203_index = tk.Label(maincanvas)
line_203_index["bg"] = "#adafae"
line_203_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_203_index["font"] = ft
line_203_index["justify"] = "left"
line_203_index["anchor"] = "w"
line_203_index.place(x=20, y=8285, width=150, height=33)

line_203_name = tk.Label(maincanvas)
line_203_name["bg"] = "#adafae"
line_203_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_203_name["font"] = ft
line_203_name["justify"] = "left"
line_203_name["anchor"] = "w"
line_203_name.place(x=250, y=8285, width=500, height=33)

line_203_duration = tk.Label(maincanvas)
line_203_duration["bg"] = "#adafae"
line_203_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_203_duration["font"] = ft
line_203_duration["justify"] = "right"
line_203_duration["anchor"] = "e"
line_203_duration.place(x=910, y=8285, width=150, height=33)

line_203_live = tk.Label(maincanvas)
line_203_live["bg"] = "#adafae"
line_203_live["fg"] = "red"
line_203_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_203_live["font"] = ftl
line_203_live["justify"] = "left"
line_203_live["anchor"] = "w"
line_203_live["relief"] = "flat"
line_203_live.place(x=8000, y=8285, width=70, height=33)

line_203_disabled = tk.Label(maincanvas)
line_203_disabled["bg"] = "#adafae"
line_203_disabled["fg"] = "red"
line_203_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_203_disabled["font"] = ftl
line_203_disabled["justify"] = "left"
line_203_disabled["anchor"] = "w"
line_203_disabled["relief"] = "flat"
line_203_disabled.place(x=650, y=8285, width=150, height=33)

line_204_frame = tk.Label(maincanvas)
line_204_frame["bg"] = "#adafae"
line_204_frame["text"] = ""
line_204_frame["relief"] = "sunken"
line_204_frame.place(x=10, y=8320, width=1060, height=40)

line_204_index = tk.Label(maincanvas)
line_204_index["bg"] = "#adafae"
line_204_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_204_index["font"] = ft
line_204_index["justify"] = "left"
line_204_index["anchor"] = "w"
line_204_index.place(x=20, y=8325, width=150, height=33)

line_204_name = tk.Label(maincanvas)
line_204_name["bg"] = "#adafae"
line_204_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_204_name["font"] = ft
line_204_name["justify"] = "left"
line_204_name["anchor"] = "w"
line_204_name.place(x=250, y=8325, width=500, height=33)

line_204_duration = tk.Label(maincanvas)
line_204_duration["bg"] = "#adafae"
line_204_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_204_duration["font"] = ft
line_204_duration["justify"] = "right"
line_204_duration["anchor"] = "e"
line_204_duration.place(x=910, y=8325, width=150, height=33)

line_204_live = tk.Label(maincanvas)
line_204_live["bg"] = "#adafae"
line_204_live["fg"] = "red"
line_204_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_204_live["font"] = ftl
line_204_live["justify"] = "left"
line_204_live["anchor"] = "w"
line_204_live["relief"] = "flat"
line_204_live.place(x=8000, y=8325, width=70, height=33)

line_204_disabled = tk.Label(maincanvas)
line_204_disabled["bg"] = "#adafae"
line_204_disabled["fg"] = "red"
line_204_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_204_disabled["font"] = ftl
line_204_disabled["justify"] = "left"
line_204_disabled["anchor"] = "w"
line_204_disabled["relief"] = "flat"
line_204_disabled.place(x=650, y=8325, width=150, height=33)

line_205_frame = tk.Label(maincanvas)
line_205_frame["bg"] = "#adafae"
line_205_frame["text"] = ""
line_205_frame["relief"] = "sunken"
line_205_frame.place(x=10, y=8360, width=1060, height=40)

line_205_index = tk.Label(maincanvas)
line_205_index["bg"] = "#adafae"
line_205_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_205_index["font"] = ft
line_205_index["justify"] = "left"
line_205_index["anchor"] = "w"
line_205_index.place(x=20, y=8365, width=150, height=33)

line_205_name = tk.Label(maincanvas)
line_205_name["bg"] = "#adafae"
line_205_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_205_name["font"] = ft
line_205_name["justify"] = "left"
line_205_name["anchor"] = "w"
line_205_name.place(x=250, y=8365, width=500, height=33)

line_205_duration = tk.Label(maincanvas)
line_205_duration["bg"] = "#adafae"
line_205_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_205_duration["font"] = ft
line_205_duration["justify"] = "right"
line_205_duration["anchor"] = "e"
line_205_duration.place(x=910, y=8365, width=150, height=33)

line_205_live = tk.Label(maincanvas)
line_205_live["bg"] = "#adafae"
line_205_live["fg"] = "red"
line_205_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_205_live["font"] = ftl
line_205_live["justify"] = "left"
line_205_live["anchor"] = "w"
line_205_live["relief"] = "flat"
line_205_live.place(x=8000, y=8365, width=70, height=33)

line_205_disabled = tk.Label(maincanvas)
line_205_disabled["bg"] = "#adafae"
line_205_disabled["fg"] = "red"
line_205_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_205_disabled["font"] = ftl
line_205_disabled["justify"] = "left"
line_205_disabled["anchor"] = "w"
line_205_disabled["relief"] = "flat"
line_205_disabled.place(x=650, y=8365, width=150, height=33)

line_206_frame = tk.Label(maincanvas)
line_206_frame["bg"] = "#adafae"
line_206_frame["text"] = ""
line_206_frame["relief"] = "sunken"
line_206_frame.place(x=10, y=8400, width=1060, height=40)

line_206_index = tk.Label(maincanvas)
line_206_index["bg"] = "#adafae"
line_206_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_206_index["font"] = ft
line_206_index["justify"] = "left"
line_206_index["anchor"] = "w"
line_206_index.place(x=20, y=8405, width=150, height=33)

line_206_name = tk.Label(maincanvas)
line_206_name["bg"] = "#adafae"
line_206_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_206_name["font"] = ft
line_206_name["justify"] = "left"
line_206_name["anchor"] = "w"
line_206_name.place(x=250, y=8405, width=500, height=33)

line_206_duration = tk.Label(maincanvas)
line_206_duration["bg"] = "#adafae"
line_206_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_206_duration["font"] = ft
line_206_duration["justify"] = "right"
line_206_duration["anchor"] = "e"
line_206_duration.place(x=910, y=8405, width=150, height=33)

line_206_live = tk.Label(maincanvas)
line_206_live["bg"] = "#adafae"
line_206_live["fg"] = "red"
line_206_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_206_live["font"] = ftl
line_206_live["justify"] = "left"
line_206_live["anchor"] = "w"
line_206_live["relief"] = "flat"
line_206_live.place(x=8000, y=8405, width=70, height=33)

line_206_disabled = tk.Label(maincanvas)
line_206_disabled["bg"] = "#adafae"
line_206_disabled["fg"] = "red"
line_206_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_206_disabled["font"] = ftl
line_206_disabled["justify"] = "left"
line_206_disabled["anchor"] = "w"
line_206_disabled["relief"] = "flat"
line_206_disabled.place(x=650, y=8405, width=150, height=33)

line_207_frame = tk.Label(maincanvas)
line_207_frame["bg"] = "#adafae"
line_207_frame["text"] = ""
line_207_frame["relief"] = "sunken"
line_207_frame.place(x=10, y=8440, width=1060, height=40)

line_207_index = tk.Label(maincanvas)
line_207_index["bg"] = "#adafae"
line_207_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_207_index["font"] = ft
line_207_index["justify"] = "left"
line_207_index["anchor"] = "w"
line_207_index.place(x=20, y=8445, width=150, height=33)

line_207_name = tk.Label(maincanvas)
line_207_name["bg"] = "#adafae"
line_207_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_207_name["font"] = ft
line_207_name["justify"] = "left"
line_207_name["anchor"] = "w"
line_207_name.place(x=250, y=8445, width=500, height=33)

line_207_duration = tk.Label(maincanvas)
line_207_duration["bg"] = "#adafae"
line_207_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_207_duration["font"] = ft
line_207_duration["justify"] = "right"
line_207_duration["anchor"] = "e"
line_207_duration.place(x=910, y=8445, width=150, height=33)

line_207_live = tk.Label(maincanvas)
line_207_live["bg"] = "#adafae"
line_207_live["fg"] = "red"
line_207_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_207_live["font"] = ftl
line_207_live["justify"] = "left"
line_207_live["anchor"] = "w"
line_207_live["relief"] = "flat"
line_207_live.place(x=8000, y=8445, width=70, height=33)

line_207_disabled = tk.Label(maincanvas)
line_207_disabled["bg"] = "#adafae"
line_207_disabled["fg"] = "red"
line_207_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_207_disabled["font"] = ftl
line_207_disabled["justify"] = "left"
line_207_disabled["anchor"] = "w"
line_207_disabled["relief"] = "flat"
line_207_disabled.place(x=650, y=8445, width=150, height=33)

line_208_frame = tk.Label(maincanvas)
line_208_frame["bg"] = "#adafae"
line_208_frame["text"] = ""
line_208_frame["relief"] = "sunken"
line_208_frame.place(x=10, y=8480, width=1060, height=40)

line_208_index = tk.Label(maincanvas)
line_208_index["bg"] = "#adafae"
line_208_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_208_index["font"] = ft
line_208_index["justify"] = "left"
line_208_index["anchor"] = "w"
line_208_index.place(x=20, y=8485, width=150, height=33)

line_208_name = tk.Label(maincanvas)
line_208_name["bg"] = "#adafae"
line_208_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_208_name["font"] = ft
line_208_name["justify"] = "left"
line_208_name["anchor"] = "w"
line_208_name.place(x=250, y=8485, width=500, height=33)

line_208_duration = tk.Label(maincanvas)
line_208_duration["bg"] = "#adafae"
line_208_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_208_duration["font"] = ft
line_208_duration["justify"] = "right"
line_208_duration["anchor"] = "e"
line_208_duration.place(x=910, y=8485, width=150, height=33)

line_208_live = tk.Label(maincanvas)
line_208_live["bg"] = "#adafae"
line_208_live["fg"] = "red"
line_208_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_208_live["font"] = ftl
line_208_live["justify"] = "left"
line_208_live["anchor"] = "w"
line_208_live["relief"] = "flat"
line_208_live.place(x=8000, y=8485, width=70, height=33)

line_208_disabled = tk.Label(maincanvas)
line_208_disabled["bg"] = "#adafae"
line_208_disabled["fg"] = "red"
line_208_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_208_disabled["font"] = ftl
line_208_disabled["justify"] = "left"
line_208_disabled["anchor"] = "w"
line_208_disabled["relief"] = "flat"
line_208_disabled.place(x=650, y=8485, width=150, height=33)

line_209_frame = tk.Label(maincanvas)
line_209_frame["bg"] = "#adafae"
line_209_frame["text"] = ""
line_209_frame["relief"] = "sunken"
line_209_frame.place(x=10, y=8520, width=1060, height=40)

line_209_index = tk.Label(maincanvas)
line_209_index["bg"] = "#adafae"
line_209_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_209_index["font"] = ft
line_209_index["justify"] = "left"
line_209_index["anchor"] = "w"
line_209_index.place(x=20, y=8525, width=150, height=33)

line_209_name = tk.Label(maincanvas)
line_209_name["bg"] = "#adafae"
line_209_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_209_name["font"] = ft
line_209_name["justify"] = "left"
line_209_name["anchor"] = "w"
line_209_name.place(x=250, y=8525, width=500, height=33)

line_209_duration = tk.Label(maincanvas)
line_209_duration["bg"] = "#adafae"
line_209_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_209_duration["font"] = ft
line_209_duration["justify"] = "right"
line_209_duration["anchor"] = "e"
line_209_duration.place(x=910, y=8525, width=150, height=33)

line_209_live = tk.Label(maincanvas)
line_209_live["bg"] = "#adafae"
line_209_live["fg"] = "red"
line_209_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_209_live["font"] = ftl
line_209_live["justify"] = "left"
line_209_live["anchor"] = "w"
line_209_live["relief"] = "flat"
line_209_live.place(x=8000, y=8525, width=70, height=33)

line_209_disabled = tk.Label(maincanvas)
line_209_disabled["bg"] = "#adafae"
line_209_disabled["fg"] = "red"
line_209_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_209_disabled["font"] = ftl
line_209_disabled["justify"] = "left"
line_209_disabled["anchor"] = "w"
line_209_disabled["relief"] = "flat"
line_209_disabled.place(x=650, y=8525, width=150, height=33)

line_210_frame = tk.Label(maincanvas)
line_210_frame["bg"] = "#adafae"
line_210_frame["text"] = ""
line_210_frame["relief"] = "sunken"
line_210_frame.place(x=10, y=8560, width=1060, height=40)

line_210_index = tk.Label(maincanvas)
line_210_index["bg"] = "#adafae"
line_210_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_210_index["font"] = ft
line_210_index["justify"] = "left"
line_210_index["anchor"] = "w"
line_210_index.place(x=20, y=8565, width=150, height=33)

line_210_name = tk.Label(maincanvas)
line_210_name["bg"] = "#adafae"
line_210_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_210_name["font"] = ft
line_210_name["justify"] = "left"
line_210_name["anchor"] = "w"
line_210_name.place(x=250, y=8565, width=500, height=33)

line_210_duration = tk.Label(maincanvas)
line_210_duration["bg"] = "#adafae"
line_210_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_210_duration["font"] = ft
line_210_duration["justify"] = "right"
line_210_duration["anchor"] = "e"
line_210_duration.place(x=910, y=8565, width=150, height=33)

line_210_live = tk.Label(maincanvas)
line_210_live["bg"] = "#adafae"
line_210_live["fg"] = "red"
line_210_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_210_live["font"] = ftl
line_210_live["justify"] = "left"
line_210_live["anchor"] = "w"
line_210_live["relief"] = "flat"
line_210_live.place(x=8000, y=8565, width=70, height=33)

line_210_disabled = tk.Label(maincanvas)
line_210_disabled["bg"] = "#adafae"
line_210_disabled["fg"] = "red"
line_210_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_210_disabled["font"] = ftl
line_210_disabled["justify"] = "left"
line_210_disabled["anchor"] = "w"
line_210_disabled["relief"] = "flat"
line_210_disabled.place(x=650, y=8565, width=150, height=33)

line_211_frame = tk.Label(maincanvas)
line_211_frame["bg"] = "#adafae"
line_211_frame["text"] = ""
line_211_frame["relief"] = "sunken"
line_211_frame.place(x=10, y=8600, width=1060, height=40)

line_211_index = tk.Label(maincanvas)
line_211_index["bg"] = "#adafae"
line_211_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_211_index["font"] = ft
line_211_index["justify"] = "left"
line_211_index["anchor"] = "w"
line_211_index.place(x=20, y=8605, width=150, height=33)

line_211_name = tk.Label(maincanvas)
line_211_name["bg"] = "#adafae"
line_211_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_211_name["font"] = ft
line_211_name["justify"] = "left"
line_211_name["anchor"] = "w"
line_211_name.place(x=250, y=8605, width=500, height=33)

line_211_duration = tk.Label(maincanvas)
line_211_duration["bg"] = "#adafae"
line_211_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_211_duration["font"] = ft
line_211_duration["justify"] = "right"
line_211_duration["anchor"] = "e"
line_211_duration.place(x=910, y=8605, width=150, height=33)

line_211_live = tk.Label(maincanvas)
line_211_live["bg"] = "#adafae"
line_211_live["fg"] = "red"
line_211_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_211_live["font"] = ftl
line_211_live["justify"] = "left"
line_211_live["anchor"] = "w"
line_211_live["relief"] = "flat"
line_211_live.place(x=8000, y=8605, width=70, height=33)

line_211_disabled = tk.Label(maincanvas)
line_211_disabled["bg"] = "#adafae"
line_211_disabled["fg"] = "red"
line_211_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_211_disabled["font"] = ftl
line_211_disabled["justify"] = "left"
line_211_disabled["anchor"] = "w"
line_211_disabled["relief"] = "flat"
line_211_disabled.place(x=650, y=8605, width=150, height=33)

line_212_frame = tk.Label(maincanvas)
line_212_frame["bg"] = "#adafae"
line_212_frame["text"] = ""
line_212_frame["relief"] = "sunken"
line_212_frame.place(x=10, y=8640, width=1060, height=40)

line_212_index = tk.Label(maincanvas)
line_212_index["bg"] = "#adafae"
line_212_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_212_index["font"] = ft
line_212_index["justify"] = "left"
line_212_index["anchor"] = "w"
line_212_index.place(x=20, y=8645, width=150, height=33)

line_212_name = tk.Label(maincanvas)
line_212_name["bg"] = "#adafae"
line_212_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_212_name["font"] = ft
line_212_name["justify"] = "left"
line_212_name["anchor"] = "w"
line_212_name.place(x=250, y=8645, width=500, height=33)

line_212_duration = tk.Label(maincanvas)
line_212_duration["bg"] = "#adafae"
line_212_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_212_duration["font"] = ft
line_212_duration["justify"] = "right"
line_212_duration["anchor"] = "e"
line_212_duration.place(x=910, y=8645, width=150, height=33)

line_212_live = tk.Label(maincanvas)
line_212_live["bg"] = "#adafae"
line_212_live["fg"] = "red"
line_212_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_212_live["font"] = ftl
line_212_live["justify"] = "left"
line_212_live["anchor"] = "w"
line_212_live["relief"] = "flat"
line_212_live.place(x=8000, y=8645, width=70, height=33)

line_212_disabled = tk.Label(maincanvas)
line_212_disabled["bg"] = "#adafae"
line_212_disabled["fg"] = "red"
line_212_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_212_disabled["font"] = ftl
line_212_disabled["justify"] = "left"
line_212_disabled["anchor"] = "w"
line_212_disabled["relief"] = "flat"
line_212_disabled.place(x=650, y=8645, width=150, height=33)

line_213_frame = tk.Label(maincanvas)
line_213_frame["bg"] = "#adafae"
line_213_frame["text"] = ""
line_213_frame["relief"] = "sunken"
line_213_frame.place(x=10, y=8680, width=1060, height=40)

line_213_index = tk.Label(maincanvas)
line_213_index["bg"] = "#adafae"
line_213_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_213_index["font"] = ft
line_213_index["justify"] = "left"
line_213_index["anchor"] = "w"
line_213_index.place(x=20, y=8685, width=150, height=33)

line_213_name = tk.Label(maincanvas)
line_213_name["bg"] = "#adafae"
line_213_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_213_name["font"] = ft
line_213_name["justify"] = "left"
line_213_name["anchor"] = "w"
line_213_name.place(x=250, y=8685, width=500, height=33)

line_213_duration = tk.Label(maincanvas)
line_213_duration["bg"] = "#adafae"
line_213_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_213_duration["font"] = ft
line_213_duration["justify"] = "right"
line_213_duration["anchor"] = "e"
line_213_duration.place(x=910, y=8685, width=150, height=33)

line_213_live = tk.Label(maincanvas)
line_213_live["bg"] = "#adafae"
line_213_live["fg"] = "red"
line_213_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_213_live["font"] = ftl
line_213_live["justify"] = "left"
line_213_live["anchor"] = "w"
line_213_live["relief"] = "flat"
line_213_live.place(x=8000, y=8685, width=70, height=33)

line_213_disabled = tk.Label(maincanvas)
line_213_disabled["bg"] = "#adafae"
line_213_disabled["fg"] = "red"
line_213_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_213_disabled["font"] = ftl
line_213_disabled["justify"] = "left"
line_213_disabled["anchor"] = "w"
line_213_disabled["relief"] = "flat"
line_213_disabled.place(x=650, y=8685, width=150, height=33)

line_214_frame = tk.Label(maincanvas)
line_214_frame["bg"] = "#adafae"
line_214_frame["text"] = ""
line_214_frame["relief"] = "sunken"
line_214_frame.place(x=10, y=8720, width=1060, height=40)

line_214_index = tk.Label(maincanvas)
line_214_index["bg"] = "#adafae"
line_214_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_214_index["font"] = ft
line_214_index["justify"] = "left"
line_214_index["anchor"] = "w"
line_214_index.place(x=20, y=8725, width=150, height=33)

line_214_name = tk.Label(maincanvas)
line_214_name["bg"] = "#adafae"
line_214_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_214_name["font"] = ft
line_214_name["justify"] = "left"
line_214_name["anchor"] = "w"
line_214_name.place(x=250, y=8725, width=500, height=33)

line_214_duration = tk.Label(maincanvas)
line_214_duration["bg"] = "#adafae"
line_214_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_214_duration["font"] = ft
line_214_duration["justify"] = "right"
line_214_duration["anchor"] = "e"
line_214_duration.place(x=910, y=8725, width=150, height=33)

line_214_live = tk.Label(maincanvas)
line_214_live["bg"] = "#adafae"
line_214_live["fg"] = "red"
line_214_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_214_live["font"] = ftl
line_214_live["justify"] = "left"
line_214_live["anchor"] = "w"
line_214_live["relief"] = "flat"
line_214_live.place(x=8000, y=8725, width=70, height=33)

line_214_disabled = tk.Label(maincanvas)
line_214_disabled["bg"] = "#adafae"
line_214_disabled["fg"] = "red"
line_214_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_214_disabled["font"] = ftl
line_214_disabled["justify"] = "left"
line_214_disabled["anchor"] = "w"
line_214_disabled["relief"] = "flat"
line_214_disabled.place(x=650, y=8725, width=150, height=33)

line_215_frame = tk.Label(maincanvas)
line_215_frame["bg"] = "#adafae"
line_215_frame["text"] = ""
line_215_frame["relief"] = "sunken"
line_215_frame.place(x=10, y=8760, width=1060, height=40)

line_215_index = tk.Label(maincanvas)
line_215_index["bg"] = "#adafae"
line_215_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_215_index["font"] = ft
line_215_index["justify"] = "left"
line_215_index["anchor"] = "w"
line_215_index.place(x=20, y=8765, width=150, height=33)

line_215_name = tk.Label(maincanvas)
line_215_name["bg"] = "#adafae"
line_215_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_215_name["font"] = ft
line_215_name["justify"] = "left"
line_215_name["anchor"] = "w"
line_215_name.place(x=250, y=8765, width=500, height=33)

line_215_duration = tk.Label(maincanvas)
line_215_duration["bg"] = "#adafae"
line_215_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_215_duration["font"] = ft
line_215_duration["justify"] = "right"
line_215_duration["anchor"] = "e"
line_215_duration.place(x=910, y=8765, width=150, height=33)

line_215_live = tk.Label(maincanvas)
line_215_live["bg"] = "#adafae"
line_215_live["fg"] = "red"
line_215_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_215_live["font"] = ftl
line_215_live["justify"] = "left"
line_215_live["anchor"] = "w"
line_215_live["relief"] = "flat"
line_215_live.place(x=8000, y=8765, width=70, height=33)

line_215_disabled = tk.Label(maincanvas)
line_215_disabled["bg"] = "#adafae"
line_215_disabled["fg"] = "red"
line_215_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_215_disabled["font"] = ftl
line_215_disabled["justify"] = "left"
line_215_disabled["anchor"] = "w"
line_215_disabled["relief"] = "flat"
line_215_disabled.place(x=650, y=8765, width=150, height=33)

line_216_frame = tk.Label(maincanvas)
line_216_frame["bg"] = "#adafae"
line_216_frame["text"] = ""
line_216_frame["relief"] = "sunken"
line_216_frame.place(x=10, y=8800, width=1060, height=40)

line_216_index = tk.Label(maincanvas)
line_216_index["bg"] = "#adafae"
line_216_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_216_index["font"] = ft
line_216_index["justify"] = "left"
line_216_index["anchor"] = "w"
line_216_index.place(x=20, y=8805, width=150, height=33)

line_216_name = tk.Label(maincanvas)
line_216_name["bg"] = "#adafae"
line_216_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_216_name["font"] = ft
line_216_name["justify"] = "left"
line_216_name["anchor"] = "w"
line_216_name.place(x=250, y=8805, width=500, height=33)

line_216_duration = tk.Label(maincanvas)
line_216_duration["bg"] = "#adafae"
line_216_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_216_duration["font"] = ft
line_216_duration["justify"] = "right"
line_216_duration["anchor"] = "e"
line_216_duration.place(x=910, y=8805, width=150, height=33)

line_216_live = tk.Label(maincanvas)
line_216_live["bg"] = "#adafae"
line_216_live["fg"] = "red"
line_216_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_216_live["font"] = ftl
line_216_live["justify"] = "left"
line_216_live["anchor"] = "w"
line_216_live["relief"] = "flat"
line_216_live.place(x=8000, y=8805, width=70, height=33)

line_216_disabled = tk.Label(maincanvas)
line_216_disabled["bg"] = "#adafae"
line_216_disabled["fg"] = "red"
line_216_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_216_disabled["font"] = ftl
line_216_disabled["justify"] = "left"
line_216_disabled["anchor"] = "w"
line_216_disabled["relief"] = "flat"
line_216_disabled.place(x=650, y=8805, width=150, height=33)

line_217_frame = tk.Label(maincanvas)
line_217_frame["bg"] = "#adafae"
line_217_frame["text"] = ""
line_217_frame["relief"] = "sunken"
line_217_frame.place(x=10, y=8840, width=1060, height=40)

line_217_index = tk.Label(maincanvas)
line_217_index["bg"] = "#adafae"
line_217_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_217_index["font"] = ft
line_217_index["justify"] = "left"
line_217_index["anchor"] = "w"
line_217_index.place(x=20, y=8845, width=150, height=33)

line_217_name = tk.Label(maincanvas)
line_217_name["bg"] = "#adafae"
line_217_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_217_name["font"] = ft
line_217_name["justify"] = "left"
line_217_name["anchor"] = "w"
line_217_name.place(x=250, y=8845, width=500, height=33)

line_217_duration = tk.Label(maincanvas)
line_217_duration["bg"] = "#adafae"
line_217_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_217_duration["font"] = ft
line_217_duration["justify"] = "right"
line_217_duration["anchor"] = "e"
line_217_duration.place(x=910, y=8845, width=150, height=33)

line_217_live = tk.Label(maincanvas)
line_217_live["bg"] = "#adafae"
line_217_live["fg"] = "red"
line_217_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_217_live["font"] = ftl
line_217_live["justify"] = "left"
line_217_live["anchor"] = "w"
line_217_live["relief"] = "flat"
line_217_live.place(x=8000, y=8845, width=70, height=33)

line_217_disabled = tk.Label(maincanvas)
line_217_disabled["bg"] = "#adafae"
line_217_disabled["fg"] = "red"
line_217_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_217_disabled["font"] = ftl
line_217_disabled["justify"] = "left"
line_217_disabled["anchor"] = "w"
line_217_disabled["relief"] = "flat"
line_217_disabled.place(x=650, y=8845, width=150, height=33)

line_218_frame = tk.Label(maincanvas)
line_218_frame["bg"] = "#adafae"
line_218_frame["text"] = ""
line_218_frame["relief"] = "sunken"
line_218_frame.place(x=10, y=8880, width=1060, height=40)

line_218_index = tk.Label(maincanvas)
line_218_index["bg"] = "#adafae"
line_218_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_218_index["font"] = ft
line_218_index["justify"] = "left"
line_218_index["anchor"] = "w"
line_218_index.place(x=20, y=8885, width=150, height=33)

line_218_name = tk.Label(maincanvas)
line_218_name["bg"] = "#adafae"
line_218_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_218_name["font"] = ft
line_218_name["justify"] = "left"
line_218_name["anchor"] = "w"
line_218_name.place(x=250, y=8885, width=500, height=33)

line_218_duration = tk.Label(maincanvas)
line_218_duration["bg"] = "#adafae"
line_218_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_218_duration["font"] = ft
line_218_duration["justify"] = "right"
line_218_duration["anchor"] = "e"
line_218_duration.place(x=910, y=8885, width=150, height=33)

line_218_live = tk.Label(maincanvas)
line_218_live["bg"] = "#adafae"
line_218_live["fg"] = "red"
line_218_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_218_live["font"] = ftl
line_218_live["justify"] = "left"
line_218_live["anchor"] = "w"
line_218_live["relief"] = "flat"
line_218_live.place(x=8000, y=8885, width=70, height=33)

line_218_disabled = tk.Label(maincanvas)
line_218_disabled["bg"] = "#adafae"
line_218_disabled["fg"] = "red"
line_218_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_218_disabled["font"] = ftl
line_218_disabled["justify"] = "left"
line_218_disabled["anchor"] = "w"
line_218_disabled["relief"] = "flat"
line_218_disabled.place(x=650, y=8885, width=150, height=33)

line_219_frame = tk.Label(maincanvas)
line_219_frame["bg"] = "#adafae"
line_219_frame["text"] = ""
line_219_frame["relief"] = "sunken"
line_219_frame.place(x=10, y=8920, width=1060, height=40)

line_219_index = tk.Label(maincanvas)
line_219_index["bg"] = "#adafae"
line_219_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_219_index["font"] = ft
line_219_index["justify"] = "left"
line_219_index["anchor"] = "w"
line_219_index.place(x=20, y=8925, width=150, height=33)

line_219_name = tk.Label(maincanvas)
line_219_name["bg"] = "#adafae"
line_219_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_219_name["font"] = ft
line_219_name["justify"] = "left"
line_219_name["anchor"] = "w"
line_219_name.place(x=250, y=8925, width=500, height=33)

line_219_duration = tk.Label(maincanvas)
line_219_duration["bg"] = "#adafae"
line_219_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_219_duration["font"] = ft
line_219_duration["justify"] = "right"
line_219_duration["anchor"] = "e"
line_219_duration.place(x=910, y=8925, width=150, height=33)

line_219_live = tk.Label(maincanvas)
line_219_live["bg"] = "#adafae"
line_219_live["fg"] = "red"
line_219_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_219_live["font"] = ftl
line_219_live["justify"] = "left"
line_219_live["anchor"] = "w"
line_219_live["relief"] = "flat"
line_219_live.place(x=8000, y=8925, width=70, height=33)

line_219_disabled = tk.Label(maincanvas)
line_219_disabled["bg"] = "#adafae"
line_219_disabled["fg"] = "red"
line_219_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_219_disabled["font"] = ftl
line_219_disabled["justify"] = "left"
line_219_disabled["anchor"] = "w"
line_219_disabled["relief"] = "flat"
line_219_disabled.place(x=650, y=8925, width=150, height=33)

line_220_frame = tk.Label(maincanvas)
line_220_frame["bg"] = "#adafae"
line_220_frame["text"] = ""
line_220_frame["relief"] = "sunken"
line_220_frame.place(x=10, y=8960, width=1060, height=40)

line_220_index = tk.Label(maincanvas)
line_220_index["bg"] = "#adafae"
line_220_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_220_index["font"] = ft
line_220_index["justify"] = "left"
line_220_index["anchor"] = "w"
line_220_index.place(x=20, y=8965, width=150, height=33)

line_220_name = tk.Label(maincanvas)
line_220_name["bg"] = "#adafae"
line_220_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_220_name["font"] = ft
line_220_name["justify"] = "left"
line_220_name["anchor"] = "w"
line_220_name.place(x=250, y=8965, width=500, height=33)

line_220_duration = tk.Label(maincanvas)
line_220_duration["bg"] = "#adafae"
line_220_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_220_duration["font"] = ft
line_220_duration["justify"] = "right"
line_220_duration["anchor"] = "e"
line_220_duration.place(x=910, y=8965, width=150, height=33)

line_220_live = tk.Label(maincanvas)
line_220_live["bg"] = "#adafae"
line_220_live["fg"] = "red"
line_220_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_220_live["font"] = ftl
line_220_live["justify"] = "left"
line_220_live["anchor"] = "w"
line_220_live["relief"] = "flat"
line_220_live.place(x=8000, y=8965, width=70, height=33)

line_220_disabled = tk.Label(maincanvas)
line_220_disabled["bg"] = "#adafae"
line_220_disabled["fg"] = "red"
line_220_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_220_disabled["font"] = ftl
line_220_disabled["justify"] = "left"
line_220_disabled["anchor"] = "w"
line_220_disabled["relief"] = "flat"
line_220_disabled.place(x=650, y=8965, width=150, height=33)

line_221_frame = tk.Label(maincanvas)
line_221_frame["bg"] = "#adafae"
line_221_frame["text"] = ""
line_221_frame["relief"] = "sunken"
line_221_frame.place(x=10, y=9000, width=1060, height=40)

line_221_index = tk.Label(maincanvas)
line_221_index["bg"] = "#adafae"
line_221_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_221_index["font"] = ft
line_221_index["justify"] = "left"
line_221_index["anchor"] = "w"
line_221_index.place(x=20, y=9005, width=150, height=33)

line_221_name = tk.Label(maincanvas)
line_221_name["bg"] = "#adafae"
line_221_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_221_name["font"] = ft
line_221_name["justify"] = "left"
line_221_name["anchor"] = "w"
line_221_name.place(x=250, y=9005, width=500, height=33)

line_221_duration = tk.Label(maincanvas)
line_221_duration["bg"] = "#adafae"
line_221_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_221_duration["font"] = ft
line_221_duration["justify"] = "right"
line_221_duration["anchor"] = "e"
line_221_duration.place(x=910, y=9005, width=150, height=33)

line_221_live = tk.Label(maincanvas)
line_221_live["bg"] = "#adafae"
line_221_live["fg"] = "red"
line_221_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_221_live["font"] = ftl
line_221_live["justify"] = "left"
line_221_live["anchor"] = "w"
line_221_live["relief"] = "flat"
line_221_live.place(x=8000, y=9005, width=70, height=33)

line_221_disabled = tk.Label(maincanvas)
line_221_disabled["bg"] = "#adafae"
line_221_disabled["fg"] = "red"
line_221_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_221_disabled["font"] = ftl
line_221_disabled["justify"] = "left"
line_221_disabled["anchor"] = "w"
line_221_disabled["relief"] = "flat"
line_221_disabled.place(x=650, y=9005, width=150, height=33)

line_222_frame = tk.Label(maincanvas)
line_222_frame["bg"] = "#adafae"
line_222_frame["text"] = ""
line_222_frame["relief"] = "sunken"
line_222_frame.place(x=10, y=9040, width=1060, height=40)

line_222_index = tk.Label(maincanvas)
line_222_index["bg"] = "#adafae"
line_222_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_222_index["font"] = ft
line_222_index["justify"] = "left"
line_222_index["anchor"] = "w"
line_222_index.place(x=20, y=9045, width=150, height=33)

line_222_name = tk.Label(maincanvas)
line_222_name["bg"] = "#adafae"
line_222_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_222_name["font"] = ft
line_222_name["justify"] = "left"
line_222_name["anchor"] = "w"
line_222_name.place(x=250, y=9045, width=500, height=33)

line_222_duration = tk.Label(maincanvas)
line_222_duration["bg"] = "#adafae"
line_222_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_222_duration["font"] = ft
line_222_duration["justify"] = "right"
line_222_duration["anchor"] = "e"
line_222_duration.place(x=910, y=9045, width=150, height=33)

line_222_live = tk.Label(maincanvas)
line_222_live["bg"] = "#adafae"
line_222_live["fg"] = "red"
line_222_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_222_live["font"] = ftl
line_222_live["justify"] = "left"
line_222_live["anchor"] = "w"
line_222_live["relief"] = "flat"
line_222_live.place(x=8000, y=9045, width=70, height=33)

line_222_disabled = tk.Label(maincanvas)
line_222_disabled["bg"] = "#adafae"
line_222_disabled["fg"] = "red"
line_222_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_222_disabled["font"] = ftl
line_222_disabled["justify"] = "left"
line_222_disabled["anchor"] = "w"
line_222_disabled["relief"] = "flat"
line_222_disabled.place(x=650, y=9045, width=150, height=33)

line_223_frame = tk.Label(maincanvas)
line_223_frame["bg"] = "#adafae"
line_223_frame["text"] = ""
line_223_frame["relief"] = "sunken"
line_223_frame.place(x=10, y=9080, width=1060, height=40)

line_223_index = tk.Label(maincanvas)
line_223_index["bg"] = "#adafae"
line_223_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_223_index["font"] = ft
line_223_index["justify"] = "left"
line_223_index["anchor"] = "w"
line_223_index.place(x=20, y=9085, width=150, height=33)

line_223_name = tk.Label(maincanvas)
line_223_name["bg"] = "#adafae"
line_223_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_223_name["font"] = ft
line_223_name["justify"] = "left"
line_223_name["anchor"] = "w"
line_223_name.place(x=250, y=9085, width=500, height=33)

line_223_duration = tk.Label(maincanvas)
line_223_duration["bg"] = "#adafae"
line_223_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_223_duration["font"] = ft
line_223_duration["justify"] = "right"
line_223_duration["anchor"] = "e"
line_223_duration.place(x=910, y=9085, width=150, height=33)

line_223_live = tk.Label(maincanvas)
line_223_live["bg"] = "#adafae"
line_223_live["fg"] = "red"
line_223_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_223_live["font"] = ftl
line_223_live["justify"] = "left"
line_223_live["anchor"] = "w"
line_223_live["relief"] = "flat"
line_223_live.place(x=8000, y=9085, width=70, height=33)

line_223_disabled = tk.Label(maincanvas)
line_223_disabled["bg"] = "#adafae"
line_223_disabled["fg"] = "red"
line_223_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_223_disabled["font"] = ftl
line_223_disabled["justify"] = "left"
line_223_disabled["anchor"] = "w"
line_223_disabled["relief"] = "flat"
line_223_disabled.place(x=650, y=9085, width=150, height=33)

line_224_frame = tk.Label(maincanvas)
line_224_frame["bg"] = "#adafae"
line_224_frame["text"] = ""
line_224_frame["relief"] = "sunken"
line_224_frame.place(x=10, y=9120, width=1060, height=40)

line_224_index = tk.Label(maincanvas)
line_224_index["bg"] = "#adafae"
line_224_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_224_index["font"] = ft
line_224_index["justify"] = "left"
line_224_index["anchor"] = "w"
line_224_index.place(x=20, y=9125, width=150, height=33)

line_224_name = tk.Label(maincanvas)
line_224_name["bg"] = "#adafae"
line_224_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_224_name["font"] = ft
line_224_name["justify"] = "left"
line_224_name["anchor"] = "w"
line_224_name.place(x=250, y=9125, width=500, height=33)

line_224_duration = tk.Label(maincanvas)
line_224_duration["bg"] = "#adafae"
line_224_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_224_duration["font"] = ft
line_224_duration["justify"] = "right"
line_224_duration["anchor"] = "e"
line_224_duration.place(x=910, y=9125, width=150, height=33)

line_224_live = tk.Label(maincanvas)
line_224_live["bg"] = "#adafae"
line_224_live["fg"] = "red"
line_224_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_224_live["font"] = ftl
line_224_live["justify"] = "left"
line_224_live["anchor"] = "w"
line_224_live["relief"] = "flat"
line_224_live.place(x=8000, y=9125, width=70, height=33)

line_224_disabled = tk.Label(maincanvas)
line_224_disabled["bg"] = "#adafae"
line_224_disabled["fg"] = "red"
line_224_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_224_disabled["font"] = ftl
line_224_disabled["justify"] = "left"
line_224_disabled["anchor"] = "w"
line_224_disabled["relief"] = "flat"
line_224_disabled.place(x=650, y=9125, width=150, height=33)

line_225_frame = tk.Label(maincanvas)
line_225_frame["bg"] = "#adafae"
line_225_frame["text"] = ""
line_225_frame["relief"] = "sunken"
line_225_frame.place(x=10, y=9160, width=1060, height=40)

line_225_index = tk.Label(maincanvas)
line_225_index["bg"] = "#adafae"
line_225_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_225_index["font"] = ft
line_225_index["justify"] = "left"
line_225_index["anchor"] = "w"
line_225_index.place(x=20, y=9165, width=150, height=33)

line_225_name = tk.Label(maincanvas)
line_225_name["bg"] = "#adafae"
line_225_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_225_name["font"] = ft
line_225_name["justify"] = "left"
line_225_name["anchor"] = "w"
line_225_name.place(x=250, y=9165, width=500, height=33)

line_225_duration = tk.Label(maincanvas)
line_225_duration["bg"] = "#adafae"
line_225_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_225_duration["font"] = ft
line_225_duration["justify"] = "right"
line_225_duration["anchor"] = "e"
line_225_duration.place(x=910, y=9165, width=150, height=33)

line_225_live = tk.Label(maincanvas)
line_225_live["bg"] = "#adafae"
line_225_live["fg"] = "red"
line_225_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_225_live["font"] = ftl
line_225_live["justify"] = "left"
line_225_live["anchor"] = "w"
line_225_live["relief"] = "flat"
line_225_live.place(x=8000, y=9165, width=70, height=33)

line_225_disabled = tk.Label(maincanvas)
line_225_disabled["bg"] = "#adafae"
line_225_disabled["fg"] = "red"
line_225_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_225_disabled["font"] = ftl
line_225_disabled["justify"] = "left"
line_225_disabled["anchor"] = "w"
line_225_disabled["relief"] = "flat"
line_225_disabled.place(x=650, y=9165, width=150, height=33)

line_226_frame = tk.Label(maincanvas)
line_226_frame["bg"] = "#adafae"
line_226_frame["text"] = ""
line_226_frame["relief"] = "sunken"
line_226_frame.place(x=10, y=9200, width=1060, height=40)

line_226_index = tk.Label(maincanvas)
line_226_index["bg"] = "#adafae"
line_226_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_226_index["font"] = ft
line_226_index["justify"] = "left"
line_226_index["anchor"] = "w"
line_226_index.place(x=20, y=9205, width=150, height=33)

line_226_name = tk.Label(maincanvas)
line_226_name["bg"] = "#adafae"
line_226_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_226_name["font"] = ft
line_226_name["justify"] = "left"
line_226_name["anchor"] = "w"
line_226_name.place(x=250, y=9205, width=500, height=33)

line_226_duration = tk.Label(maincanvas)
line_226_duration["bg"] = "#adafae"
line_226_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_226_duration["font"] = ft
line_226_duration["justify"] = "right"
line_226_duration["anchor"] = "e"
line_226_duration.place(x=910, y=9205, width=150, height=33)

line_226_live = tk.Label(maincanvas)
line_226_live["bg"] = "#adafae"
line_226_live["fg"] = "red"
line_226_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_226_live["font"] = ftl
line_226_live["justify"] = "left"
line_226_live["anchor"] = "w"
line_226_live["relief"] = "flat"
line_226_live.place(x=8000, y=9205, width=70, height=33)

line_226_disabled = tk.Label(maincanvas)
line_226_disabled["bg"] = "#adafae"
line_226_disabled["fg"] = "red"
line_226_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_226_disabled["font"] = ftl
line_226_disabled["justify"] = "left"
line_226_disabled["anchor"] = "w"
line_226_disabled["relief"] = "flat"
line_226_disabled.place(x=650, y=9205, width=150, height=33)

line_227_frame = tk.Label(maincanvas)
line_227_frame["bg"] = "#adafae"
line_227_frame["text"] = ""
line_227_frame["relief"] = "sunken"
line_227_frame.place(x=10, y=9240, width=1060, height=40)

line_227_index = tk.Label(maincanvas)
line_227_index["bg"] = "#adafae"
line_227_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_227_index["font"] = ft
line_227_index["justify"] = "left"
line_227_index["anchor"] = "w"
line_227_index.place(x=20, y=9245, width=150, height=33)

line_227_name = tk.Label(maincanvas)
line_227_name["bg"] = "#adafae"
line_227_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_227_name["font"] = ft
line_227_name["justify"] = "left"
line_227_name["anchor"] = "w"
line_227_name.place(x=250, y=9245, width=500, height=33)

line_227_duration = tk.Label(maincanvas)
line_227_duration["bg"] = "#adafae"
line_227_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_227_duration["font"] = ft
line_227_duration["justify"] = "right"
line_227_duration["anchor"] = "e"
line_227_duration.place(x=910, y=9245, width=150, height=33)

line_227_live = tk.Label(maincanvas)
line_227_live["bg"] = "#adafae"
line_227_live["fg"] = "red"
line_227_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_227_live["font"] = ftl
line_227_live["justify"] = "left"
line_227_live["anchor"] = "w"
line_227_live["relief"] = "flat"
line_227_live.place(x=8000, y=9245, width=70, height=33)

line_227_disabled = tk.Label(maincanvas)
line_227_disabled["bg"] = "#adafae"
line_227_disabled["fg"] = "red"
line_227_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_227_disabled["font"] = ftl
line_227_disabled["justify"] = "left"
line_227_disabled["anchor"] = "w"
line_227_disabled["relief"] = "flat"
line_227_disabled.place(x=650, y=9245, width=150, height=33)

line_228_frame = tk.Label(maincanvas)
line_228_frame["bg"] = "#adafae"
line_228_frame["text"] = ""
line_228_frame["relief"] = "sunken"
line_228_frame.place(x=10, y=9280, width=1060, height=40)

line_228_index = tk.Label(maincanvas)
line_228_index["bg"] = "#adafae"
line_228_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_228_index["font"] = ft
line_228_index["justify"] = "left"
line_228_index["anchor"] = "w"
line_228_index.place(x=20, y=9285, width=150, height=33)

line_228_name = tk.Label(maincanvas)
line_228_name["bg"] = "#adafae"
line_228_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_228_name["font"] = ft
line_228_name["justify"] = "left"
line_228_name["anchor"] = "w"
line_228_name.place(x=250, y=9285, width=500, height=33)

line_228_duration = tk.Label(maincanvas)
line_228_duration["bg"] = "#adafae"
line_228_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_228_duration["font"] = ft
line_228_duration["justify"] = "right"
line_228_duration["anchor"] = "e"
line_228_duration.place(x=910, y=9285, width=150, height=33)

line_228_live = tk.Label(maincanvas)
line_228_live["bg"] = "#adafae"
line_228_live["fg"] = "red"
line_228_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_228_live["font"] = ftl
line_228_live["justify"] = "left"
line_228_live["anchor"] = "w"
line_228_live["relief"] = "flat"
line_228_live.place(x=8000, y=9285, width=70, height=33)

line_228_disabled = tk.Label(maincanvas)
line_228_disabled["bg"] = "#adafae"
line_228_disabled["fg"] = "red"
line_228_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_228_disabled["font"] = ftl
line_228_disabled["justify"] = "left"
line_228_disabled["anchor"] = "w"
line_228_disabled["relief"] = "flat"
line_228_disabled.place(x=650, y=9285, width=150, height=33)

line_229_frame = tk.Label(maincanvas)
line_229_frame["bg"] = "#adafae"
line_229_frame["text"] = ""
line_229_frame["relief"] = "sunken"
line_229_frame.place(x=10, y=9320, width=1060, height=40)

line_229_index = tk.Label(maincanvas)
line_229_index["bg"] = "#adafae"
line_229_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_229_index["font"] = ft
line_229_index["justify"] = "left"
line_229_index["anchor"] = "w"
line_229_index.place(x=20, y=9325, width=150, height=33)

line_229_name = tk.Label(maincanvas)
line_229_name["bg"] = "#adafae"
line_229_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_229_name["font"] = ft
line_229_name["justify"] = "left"
line_229_name["anchor"] = "w"
line_229_name.place(x=250, y=9325, width=500, height=33)

line_229_duration = tk.Label(maincanvas)
line_229_duration["bg"] = "#adafae"
line_229_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_229_duration["font"] = ft
line_229_duration["justify"] = "right"
line_229_duration["anchor"] = "e"
line_229_duration.place(x=910, y=9325, width=150, height=33)

line_229_live = tk.Label(maincanvas)
line_229_live["bg"] = "#adafae"
line_229_live["fg"] = "red"
line_229_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_229_live["font"] = ftl
line_229_live["justify"] = "left"
line_229_live["anchor"] = "w"
line_229_live["relief"] = "flat"
line_229_live.place(x=8000, y=9325, width=70, height=33)

line_229_disabled = tk.Label(maincanvas)
line_229_disabled["bg"] = "#adafae"
line_229_disabled["fg"] = "red"
line_229_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_229_disabled["font"] = ftl
line_229_disabled["justify"] = "left"
line_229_disabled["anchor"] = "w"
line_229_disabled["relief"] = "flat"
line_229_disabled.place(x=650, y=9325, width=150, height=33)

line_230_frame = tk.Label(maincanvas)
line_230_frame["bg"] = "#adafae"
line_230_frame["text"] = ""
line_230_frame["relief"] = "sunken"
line_230_frame.place(x=10, y=9360, width=1060, height=40)

line_230_index = tk.Label(maincanvas)
line_230_index["bg"] = "#adafae"
line_230_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_230_index["font"] = ft
line_230_index["justify"] = "left"
line_230_index["anchor"] = "w"
line_230_index.place(x=20, y=9365, width=150, height=33)

line_230_name = tk.Label(maincanvas)
line_230_name["bg"] = "#adafae"
line_230_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_230_name["font"] = ft
line_230_name["justify"] = "left"
line_230_name["anchor"] = "w"
line_230_name.place(x=250, y=9365, width=500, height=33)

line_230_duration = tk.Label(maincanvas)
line_230_duration["bg"] = "#adafae"
line_230_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_230_duration["font"] = ft
line_230_duration["justify"] = "right"
line_230_duration["anchor"] = "e"
line_230_duration.place(x=910, y=9365, width=150, height=33)

line_230_live = tk.Label(maincanvas)
line_230_live["bg"] = "#adafae"
line_230_live["fg"] = "red"
line_230_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_230_live["font"] = ftl
line_230_live["justify"] = "left"
line_230_live["anchor"] = "w"
line_230_live["relief"] = "flat"
line_230_live.place(x=8000, y=9365, width=70, height=33)

line_230_disabled = tk.Label(maincanvas)
line_230_disabled["bg"] = "#adafae"
line_230_disabled["fg"] = "red"
line_230_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_230_disabled["font"] = ftl
line_230_disabled["justify"] = "left"
line_230_disabled["anchor"] = "w"
line_230_disabled["relief"] = "flat"
line_230_disabled.place(x=650, y=9365, width=150, height=33)

line_231_frame = tk.Label(maincanvas)
line_231_frame["bg"] = "#adafae"
line_231_frame["text"] = ""
line_231_frame["relief"] = "sunken"
line_231_frame.place(x=10, y=9400, width=1060, height=40)

line_231_index = tk.Label(maincanvas)
line_231_index["bg"] = "#adafae"
line_231_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_231_index["font"] = ft
line_231_index["justify"] = "left"
line_231_index["anchor"] = "w"
line_231_index.place(x=20, y=9405, width=150, height=33)

line_231_name = tk.Label(maincanvas)
line_231_name["bg"] = "#adafae"
line_231_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_231_name["font"] = ft
line_231_name["justify"] = "left"
line_231_name["anchor"] = "w"
line_231_name.place(x=250, y=9405, width=500, height=33)

line_231_duration = tk.Label(maincanvas)
line_231_duration["bg"] = "#adafae"
line_231_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_231_duration["font"] = ft
line_231_duration["justify"] = "right"
line_231_duration["anchor"] = "e"
line_231_duration.place(x=910, y=9405, width=150, height=33)

line_231_live = tk.Label(maincanvas)
line_231_live["bg"] = "#adafae"
line_231_live["fg"] = "red"
line_231_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_231_live["font"] = ftl
line_231_live["justify"] = "left"
line_231_live["anchor"] = "w"
line_231_live["relief"] = "flat"
line_231_live.place(x=8000, y=9405, width=70, height=33)

line_231_disabled = tk.Label(maincanvas)
line_231_disabled["bg"] = "#adafae"
line_231_disabled["fg"] = "red"
line_231_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_231_disabled["font"] = ftl
line_231_disabled["justify"] = "left"
line_231_disabled["anchor"] = "w"
line_231_disabled["relief"] = "flat"
line_231_disabled.place(x=650, y=9405, width=150, height=33)

line_232_frame = tk.Label(maincanvas)
line_232_frame["bg"] = "#adafae"
line_232_frame["text"] = ""
line_232_frame["relief"] = "sunken"
line_232_frame.place(x=10, y=9440, width=1060, height=40)

line_232_index = tk.Label(maincanvas)
line_232_index["bg"] = "#adafae"
line_232_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_232_index["font"] = ft
line_232_index["justify"] = "left"
line_232_index["anchor"] = "w"
line_232_index.place(x=20, y=9445, width=150, height=33)

line_232_name = tk.Label(maincanvas)
line_232_name["bg"] = "#adafae"
line_232_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_232_name["font"] = ft
line_232_name["justify"] = "left"
line_232_name["anchor"] = "w"
line_232_name.place(x=250, y=9445, width=500, height=33)

line_232_duration = tk.Label(maincanvas)
line_232_duration["bg"] = "#adafae"
line_232_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_232_duration["font"] = ft
line_232_duration["justify"] = "right"
line_232_duration["anchor"] = "e"
line_232_duration.place(x=910, y=9445, width=150, height=33)

line_232_live = tk.Label(maincanvas)
line_232_live["bg"] = "#adafae"
line_232_live["fg"] = "red"
line_232_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_232_live["font"] = ftl
line_232_live["justify"] = "left"
line_232_live["anchor"] = "w"
line_232_live["relief"] = "flat"
line_232_live.place(x=8000, y=9445, width=70, height=33)

line_232_disabled = tk.Label(maincanvas)
line_232_disabled["bg"] = "#adafae"
line_232_disabled["fg"] = "red"
line_232_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_232_disabled["font"] = ftl
line_232_disabled["justify"] = "left"
line_232_disabled["anchor"] = "w"
line_232_disabled["relief"] = "flat"
line_232_disabled.place(x=650, y=9445, width=150, height=33)

line_233_frame = tk.Label(maincanvas)
line_233_frame["bg"] = "#adafae"
line_233_frame["text"] = ""
line_233_frame["relief"] = "sunken"
line_233_frame.place(x=10, y=9480, width=1060, height=40)

line_233_index = tk.Label(maincanvas)
line_233_index["bg"] = "#adafae"
line_233_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_233_index["font"] = ft
line_233_index["justify"] = "left"
line_233_index["anchor"] = "w"
line_233_index.place(x=20, y=9485, width=150, height=33)

line_233_name = tk.Label(maincanvas)
line_233_name["bg"] = "#adafae"
line_233_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_233_name["font"] = ft
line_233_name["justify"] = "left"
line_233_name["anchor"] = "w"
line_233_name.place(x=250, y=9485, width=500, height=33)

line_233_duration = tk.Label(maincanvas)
line_233_duration["bg"] = "#adafae"
line_233_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_233_duration["font"] = ft
line_233_duration["justify"] = "right"
line_233_duration["anchor"] = "e"
line_233_duration.place(x=910, y=9485, width=150, height=33)

line_233_live = tk.Label(maincanvas)
line_233_live["bg"] = "#adafae"
line_233_live["fg"] = "red"
line_233_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_233_live["font"] = ftl
line_233_live["justify"] = "left"
line_233_live["anchor"] = "w"
line_233_live["relief"] = "flat"
line_233_live.place(x=8000, y=9485, width=70, height=33)

line_233_disabled = tk.Label(maincanvas)
line_233_disabled["bg"] = "#adafae"
line_233_disabled["fg"] = "red"
line_233_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_233_disabled["font"] = ftl
line_233_disabled["justify"] = "left"
line_233_disabled["anchor"] = "w"
line_233_disabled["relief"] = "flat"
line_233_disabled.place(x=650, y=9485, width=150, height=33)

line_234_frame = tk.Label(maincanvas)
line_234_frame["bg"] = "#adafae"
line_234_frame["text"] = ""
line_234_frame["relief"] = "sunken"
line_234_frame.place(x=10, y=9520, width=1060, height=40)

line_234_index = tk.Label(maincanvas)
line_234_index["bg"] = "#adafae"
line_234_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_234_index["font"] = ft
line_234_index["justify"] = "left"
line_234_index["anchor"] = "w"
line_234_index.place(x=20, y=9525, width=150, height=33)

line_234_name = tk.Label(maincanvas)
line_234_name["bg"] = "#adafae"
line_234_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_234_name["font"] = ft
line_234_name["justify"] = "left"
line_234_name["anchor"] = "w"
line_234_name.place(x=250, y=9525, width=500, height=33)

line_234_duration = tk.Label(maincanvas)
line_234_duration["bg"] = "#adafae"
line_234_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_234_duration["font"] = ft
line_234_duration["justify"] = "right"
line_234_duration["anchor"] = "e"
line_234_duration.place(x=910, y=9525, width=150, height=33)

line_234_live = tk.Label(maincanvas)
line_234_live["bg"] = "#adafae"
line_234_live["fg"] = "red"
line_234_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_234_live["font"] = ftl
line_234_live["justify"] = "left"
line_234_live["anchor"] = "w"
line_234_live["relief"] = "flat"
line_234_live.place(x=8000, y=9525, width=70, height=33)

line_234_disabled = tk.Label(maincanvas)
line_234_disabled["bg"] = "#adafae"
line_234_disabled["fg"] = "red"
line_234_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_234_disabled["font"] = ftl
line_234_disabled["justify"] = "left"
line_234_disabled["anchor"] = "w"
line_234_disabled["relief"] = "flat"
line_234_disabled.place(x=650, y=9525, width=150, height=33)

line_235_frame = tk.Label(maincanvas)
line_235_frame["bg"] = "#adafae"
line_235_frame["text"] = ""
line_235_frame["relief"] = "sunken"
line_235_frame.place(x=10, y=9560, width=1060, height=40)

line_235_index = tk.Label(maincanvas)
line_235_index["bg"] = "#adafae"
line_235_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_235_index["font"] = ft
line_235_index["justify"] = "left"
line_235_index["anchor"] = "w"
line_235_index.place(x=20, y=9565, width=150, height=33)

line_235_name = tk.Label(maincanvas)
line_235_name["bg"] = "#adafae"
line_235_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_235_name["font"] = ft
line_235_name["justify"] = "left"
line_235_name["anchor"] = "w"
line_235_name.place(x=250, y=9565, width=500, height=33)

line_235_duration = tk.Label(maincanvas)
line_235_duration["bg"] = "#adafae"
line_235_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_235_duration["font"] = ft
line_235_duration["justify"] = "right"
line_235_duration["anchor"] = "e"
line_235_duration.place(x=910, y=9565, width=150, height=33)

line_235_live = tk.Label(maincanvas)
line_235_live["bg"] = "#adafae"
line_235_live["fg"] = "red"
line_235_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_235_live["font"] = ftl
line_235_live["justify"] = "left"
line_235_live["anchor"] = "w"
line_235_live["relief"] = "flat"
line_235_live.place(x=8000, y=9565, width=70, height=33)

line_235_disabled = tk.Label(maincanvas)
line_235_disabled["bg"] = "#adafae"
line_235_disabled["fg"] = "red"
line_235_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_235_disabled["font"] = ftl
line_235_disabled["justify"] = "left"
line_235_disabled["anchor"] = "w"
line_235_disabled["relief"] = "flat"
line_235_disabled.place(x=650, y=9565, width=150, height=33)

line_236_frame = tk.Label(maincanvas)
line_236_frame["bg"] = "#adafae"
line_236_frame["text"] = ""
line_236_frame["relief"] = "sunken"
line_236_frame.place(x=10, y=9600, width=1060, height=40)

line_236_index = tk.Label(maincanvas)
line_236_index["bg"] = "#adafae"
line_236_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_236_index["font"] = ft
line_236_index["justify"] = "left"
line_236_index["anchor"] = "w"
line_236_index.place(x=20, y=9605, width=150, height=33)

line_236_name = tk.Label(maincanvas)
line_236_name["bg"] = "#adafae"
line_236_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_236_name["font"] = ft
line_236_name["justify"] = "left"
line_236_name["anchor"] = "w"
line_236_name.place(x=250, y=9605, width=500, height=33)

line_236_duration = tk.Label(maincanvas)
line_236_duration["bg"] = "#adafae"
line_236_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_236_duration["font"] = ft
line_236_duration["justify"] = "right"
line_236_duration["anchor"] = "e"
line_236_duration.place(x=910, y=9605, width=150, height=33)

line_236_live = tk.Label(maincanvas)
line_236_live["bg"] = "#adafae"
line_236_live["fg"] = "red"
line_236_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_236_live["font"] = ftl
line_236_live["justify"] = "left"
line_236_live["anchor"] = "w"
line_236_live["relief"] = "flat"
line_236_live.place(x=8000, y=9605, width=70, height=33)

line_236_disabled = tk.Label(maincanvas)
line_236_disabled["bg"] = "#adafae"
line_236_disabled["fg"] = "red"
line_236_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_236_disabled["font"] = ftl
line_236_disabled["justify"] = "left"
line_236_disabled["anchor"] = "w"
line_236_disabled["relief"] = "flat"
line_236_disabled.place(x=650, y=9605, width=150, height=33)

line_237_frame = tk.Label(maincanvas)
line_237_frame["bg"] = "#adafae"
line_237_frame["text"] = ""
line_237_frame["relief"] = "sunken"
line_237_frame.place(x=10, y=9640, width=1060, height=40)

line_237_index = tk.Label(maincanvas)
line_237_index["bg"] = "#adafae"
line_237_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_237_index["font"] = ft
line_237_index["justify"] = "left"
line_237_index["anchor"] = "w"
line_237_index.place(x=20, y=9645, width=150, height=33)

line_237_name = tk.Label(maincanvas)
line_237_name["bg"] = "#adafae"
line_237_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_237_name["font"] = ft
line_237_name["justify"] = "left"
line_237_name["anchor"] = "w"
line_237_name.place(x=250, y=9645, width=500, height=33)

line_237_duration = tk.Label(maincanvas)
line_237_duration["bg"] = "#adafae"
line_237_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_237_duration["font"] = ft
line_237_duration["justify"] = "right"
line_237_duration["anchor"] = "e"
line_237_duration.place(x=910, y=9645, width=150, height=33)

line_237_live = tk.Label(maincanvas)
line_237_live["bg"] = "#adafae"
line_237_live["fg"] = "red"
line_237_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_237_live["font"] = ftl
line_237_live["justify"] = "left"
line_237_live["anchor"] = "w"
line_237_live["relief"] = "flat"
line_237_live.place(x=8000, y=9645, width=70, height=33)

line_237_disabled = tk.Label(maincanvas)
line_237_disabled["bg"] = "#adafae"
line_237_disabled["fg"] = "red"
line_237_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_237_disabled["font"] = ftl
line_237_disabled["justify"] = "left"
line_237_disabled["anchor"] = "w"
line_237_disabled["relief"] = "flat"
line_237_disabled.place(x=650, y=9645, width=150, height=33)

line_238_frame = tk.Label(maincanvas)
line_238_frame["bg"] = "#adafae"
line_238_frame["text"] = ""
line_238_frame["relief"] = "sunken"
line_238_frame.place(x=10, y=9680, width=1060, height=40)

line_238_index = tk.Label(maincanvas)
line_238_index["bg"] = "#adafae"
line_238_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_238_index["font"] = ft
line_238_index["justify"] = "left"
line_238_index["anchor"] = "w"
line_238_index.place(x=20, y=9685, width=150, height=33)

line_238_name = tk.Label(maincanvas)
line_238_name["bg"] = "#adafae"
line_238_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_238_name["font"] = ft
line_238_name["justify"] = "left"
line_238_name["anchor"] = "w"
line_238_name.place(x=250, y=9685, width=500, height=33)

line_238_duration = tk.Label(maincanvas)
line_238_duration["bg"] = "#adafae"
line_238_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_238_duration["font"] = ft
line_238_duration["justify"] = "right"
line_238_duration["anchor"] = "e"
line_238_duration.place(x=910, y=9685, width=150, height=33)

line_238_live = tk.Label(maincanvas)
line_238_live["bg"] = "#adafae"
line_238_live["fg"] = "red"
line_238_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_238_live["font"] = ftl
line_238_live["justify"] = "left"
line_238_live["anchor"] = "w"
line_238_live["relief"] = "flat"
line_238_live.place(x=8000, y=9685, width=70, height=33)

line_238_disabled = tk.Label(maincanvas)
line_238_disabled["bg"] = "#adafae"
line_238_disabled["fg"] = "red"
line_238_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_238_disabled["font"] = ftl
line_238_disabled["justify"] = "left"
line_238_disabled["anchor"] = "w"
line_238_disabled["relief"] = "flat"
line_238_disabled.place(x=650, y=9685, width=150, height=33)

line_239_frame = tk.Label(maincanvas)
line_239_frame["bg"] = "#adafae"
line_239_frame["text"] = ""
line_239_frame["relief"] = "sunken"
line_239_frame.place(x=10, y=9720, width=1060, height=40)

line_239_index = tk.Label(maincanvas)
line_239_index["bg"] = "#adafae"
line_239_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_239_index["font"] = ft
line_239_index["justify"] = "left"
line_239_index["anchor"] = "w"
line_239_index.place(x=20, y=9725, width=150, height=33)

line_239_name = tk.Label(maincanvas)
line_239_name["bg"] = "#adafae"
line_239_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_239_name["font"] = ft
line_239_name["justify"] = "left"
line_239_name["anchor"] = "w"
line_239_name.place(x=250, y=9725, width=500, height=33)

line_239_duration = tk.Label(maincanvas)
line_239_duration["bg"] = "#adafae"
line_239_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_239_duration["font"] = ft
line_239_duration["justify"] = "right"
line_239_duration["anchor"] = "e"
line_239_duration.place(x=910, y=9725, width=150, height=33)

line_239_live = tk.Label(maincanvas)
line_239_live["bg"] = "#adafae"
line_239_live["fg"] = "red"
line_239_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_239_live["font"] = ftl
line_239_live["justify"] = "left"
line_239_live["anchor"] = "w"
line_239_live["relief"] = "flat"
line_239_live.place(x=8000, y=9725, width=70, height=33)

line_239_disabled = tk.Label(maincanvas)
line_239_disabled["bg"] = "#adafae"
line_239_disabled["fg"] = "red"
line_239_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_239_disabled["font"] = ftl
line_239_disabled["justify"] = "left"
line_239_disabled["anchor"] = "w"
line_239_disabled["relief"] = "flat"
line_239_disabled.place(x=650, y=9725, width=150, height=33)

line_240_frame = tk.Label(maincanvas)
line_240_frame["bg"] = "#adafae"
line_240_frame["text"] = ""
line_240_frame["relief"] = "sunken"
line_240_frame.place(x=10, y=9760, width=1060, height=40)

line_240_index = tk.Label(maincanvas)
line_240_index["bg"] = "#adafae"
line_240_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_240_index["font"] = ft
line_240_index["justify"] = "left"
line_240_index["anchor"] = "w"
line_240_index.place(x=20, y=9765, width=150, height=33)

line_240_name = tk.Label(maincanvas)
line_240_name["bg"] = "#adafae"
line_240_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_240_name["font"] = ft
line_240_name["justify"] = "left"
line_240_name["anchor"] = "w"
line_240_name.place(x=250, y=9765, width=500, height=33)

line_240_duration = tk.Label(maincanvas)
line_240_duration["bg"] = "#adafae"
line_240_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_240_duration["font"] = ft
line_240_duration["justify"] = "right"
line_240_duration["anchor"] = "e"
line_240_duration.place(x=910, y=9765, width=150, height=33)

line_240_live = tk.Label(maincanvas)
line_240_live["bg"] = "#adafae"
line_240_live["fg"] = "red"
line_240_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_240_live["font"] = ftl
line_240_live["justify"] = "left"
line_240_live["anchor"] = "w"
line_240_live["relief"] = "flat"
line_240_live.place(x=8000, y=9765, width=70, height=33)

line_240_disabled = tk.Label(maincanvas)
line_240_disabled["bg"] = "#adafae"
line_240_disabled["fg"] = "red"
line_240_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_240_disabled["font"] = ftl
line_240_disabled["justify"] = "left"
line_240_disabled["anchor"] = "w"
line_240_disabled["relief"] = "flat"
line_240_disabled.place(x=650, y=9765, width=150, height=33)

line_241_frame = tk.Label(maincanvas)
line_241_frame["bg"] = "#adafae"
line_241_frame["text"] = ""
line_241_frame["relief"] = "sunken"
line_241_frame.place(x=10, y=9800, width=1060, height=40)

line_241_index = tk.Label(maincanvas)
line_241_index["bg"] = "#adafae"
line_241_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_241_index["font"] = ft
line_241_index["justify"] = "left"
line_241_index["anchor"] = "w"
line_241_index.place(x=20, y=9805, width=150, height=33)

line_241_name = tk.Label(maincanvas)
line_241_name["bg"] = "#adafae"
line_241_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_241_name["font"] = ft
line_241_name["justify"] = "left"
line_241_name["anchor"] = "w"
line_241_name.place(x=250, y=9805, width=500, height=33)

line_241_duration = tk.Label(maincanvas)
line_241_duration["bg"] = "#adafae"
line_241_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_241_duration["font"] = ft
line_241_duration["justify"] = "right"
line_241_duration["anchor"] = "e"
line_241_duration.place(x=910, y=9805, width=150, height=33)

line_241_live = tk.Label(maincanvas)
line_241_live["bg"] = "#adafae"
line_241_live["fg"] = "red"
line_241_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_241_live["font"] = ftl
line_241_live["justify"] = "left"
line_241_live["anchor"] = "w"
line_241_live["relief"] = "flat"
line_241_live.place(x=8000, y=9805, width=70, height=33)

line_241_disabled = tk.Label(maincanvas)
line_241_disabled["bg"] = "#adafae"
line_241_disabled["fg"] = "red"
line_241_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_241_disabled["font"] = ftl
line_241_disabled["justify"] = "left"
line_241_disabled["anchor"] = "w"
line_241_disabled["relief"] = "flat"
line_241_disabled.place(x=650, y=9805, width=150, height=33)

line_242_frame = tk.Label(maincanvas)
line_242_frame["bg"] = "#adafae"
line_242_frame["text"] = ""
line_242_frame["relief"] = "sunken"
line_242_frame.place(x=10, y=9840, width=1060, height=40)

line_242_index = tk.Label(maincanvas)
line_242_index["bg"] = "#adafae"
line_242_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_242_index["font"] = ft
line_242_index["justify"] = "left"
line_242_index["anchor"] = "w"
line_242_index.place(x=20, y=9845, width=150, height=33)

line_242_name = tk.Label(maincanvas)
line_242_name["bg"] = "#adafae"
line_242_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_242_name["font"] = ft
line_242_name["justify"] = "left"
line_242_name["anchor"] = "w"
line_242_name.place(x=250, y=9845, width=500, height=33)

line_242_duration = tk.Label(maincanvas)
line_242_duration["bg"] = "#adafae"
line_242_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_242_duration["font"] = ft
line_242_duration["justify"] = "right"
line_242_duration["anchor"] = "e"
line_242_duration.place(x=910, y=9845, width=150, height=33)

line_242_live = tk.Label(maincanvas)
line_242_live["bg"] = "#adafae"
line_242_live["fg"] = "red"
line_242_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_242_live["font"] = ftl
line_242_live["justify"] = "left"
line_242_live["anchor"] = "w"
line_242_live["relief"] = "flat"
line_242_live.place(x=8000, y=9845, width=70, height=33)

line_242_disabled = tk.Label(maincanvas)
line_242_disabled["bg"] = "#adafae"
line_242_disabled["fg"] = "red"
line_242_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_242_disabled["font"] = ftl
line_242_disabled["justify"] = "left"
line_242_disabled["anchor"] = "w"
line_242_disabled["relief"] = "flat"
line_242_disabled.place(x=650, y=9845, width=150, height=33)

line_243_frame = tk.Label(maincanvas)
line_243_frame["bg"] = "#adafae"
line_243_frame["text"] = ""
line_243_frame["relief"] = "sunken"
line_243_frame.place(x=10, y=9880, width=1060, height=40)

line_243_index = tk.Label(maincanvas)
line_243_index["bg"] = "#adafae"
line_243_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_243_index["font"] = ft
line_243_index["justify"] = "left"
line_243_index["anchor"] = "w"
line_243_index.place(x=20, y=9885, width=150, height=33)

line_243_name = tk.Label(maincanvas)
line_243_name["bg"] = "#adafae"
line_243_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_243_name["font"] = ft
line_243_name["justify"] = "left"
line_243_name["anchor"] = "w"
line_243_name.place(x=250, y=9885, width=500, height=33)

line_243_duration = tk.Label(maincanvas)
line_243_duration["bg"] = "#adafae"
line_243_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_243_duration["font"] = ft
line_243_duration["justify"] = "right"
line_243_duration["anchor"] = "e"
line_243_duration.place(x=910, y=9885, width=150, height=33)

line_243_live = tk.Label(maincanvas)
line_243_live["bg"] = "#adafae"
line_243_live["fg"] = "red"
line_243_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_243_live["font"] = ftl
line_243_live["justify"] = "left"
line_243_live["anchor"] = "w"
line_243_live["relief"] = "flat"
line_243_live.place(x=8000, y=9885, width=70, height=33)

line_243_disabled = tk.Label(maincanvas)
line_243_disabled["bg"] = "#adafae"
line_243_disabled["fg"] = "red"
line_243_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_243_disabled["font"] = ftl
line_243_disabled["justify"] = "left"
line_243_disabled["anchor"] = "w"
line_243_disabled["relief"] = "flat"
line_243_disabled.place(x=650, y=9885, width=150, height=33)

line_244_frame = tk.Label(maincanvas)
line_244_frame["bg"] = "#adafae"
line_244_frame["text"] = ""
line_244_frame["relief"] = "sunken"
line_244_frame.place(x=10, y=9920, width=1060, height=40)

line_244_index = tk.Label(maincanvas)
line_244_index["bg"] = "#adafae"
line_244_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_244_index["font"] = ft
line_244_index["justify"] = "left"
line_244_index["anchor"] = "w"
line_244_index.place(x=20, y=9925, width=150, height=33)

line_244_name = tk.Label(maincanvas)
line_244_name["bg"] = "#adafae"
line_244_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_244_name["font"] = ft
line_244_name["justify"] = "left"
line_244_name["anchor"] = "w"
line_244_name.place(x=250, y=9925, width=500, height=33)

line_244_duration = tk.Label(maincanvas)
line_244_duration["bg"] = "#adafae"
line_244_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_244_duration["font"] = ft
line_244_duration["justify"] = "right"
line_244_duration["anchor"] = "e"
line_244_duration.place(x=910, y=9925, width=150, height=33)

line_244_live = tk.Label(maincanvas)
line_244_live["bg"] = "#adafae"
line_244_live["fg"] = "red"
line_244_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_244_live["font"] = ftl
line_244_live["justify"] = "left"
line_244_live["anchor"] = "w"
line_244_live["relief"] = "flat"
line_244_live.place(x=8000, y=9925, width=70, height=33)

line_244_disabled = tk.Label(maincanvas)
line_244_disabled["bg"] = "#adafae"
line_244_disabled["fg"] = "red"
line_244_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_244_disabled["font"] = ftl
line_244_disabled["justify"] = "left"
line_244_disabled["anchor"] = "w"
line_244_disabled["relief"] = "flat"
line_244_disabled.place(x=650, y=9925, width=150, height=33)

line_245_frame = tk.Label(maincanvas)
line_245_frame["bg"] = "#adafae"
line_245_frame["text"] = ""
line_245_frame["relief"] = "sunken"
line_245_frame.place(x=10, y=9960, width=1060, height=40)

line_245_index = tk.Label(maincanvas)
line_245_index["bg"] = "#adafae"
line_245_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_245_index["font"] = ft
line_245_index["justify"] = "left"
line_245_index["anchor"] = "w"
line_245_index.place(x=20, y=9965, width=150, height=33)

line_245_name = tk.Label(maincanvas)
line_245_name["bg"] = "#adafae"
line_245_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_245_name["font"] = ft
line_245_name["justify"] = "left"
line_245_name["anchor"] = "w"
line_245_name.place(x=250, y=9965, width=500, height=33)

line_245_duration = tk.Label(maincanvas)
line_245_duration["bg"] = "#adafae"
line_245_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_245_duration["font"] = ft
line_245_duration["justify"] = "right"
line_245_duration["anchor"] = "e"
line_245_duration.place(x=910, y=9965, width=150, height=33)

line_245_live = tk.Label(maincanvas)
line_245_live["bg"] = "#adafae"
line_245_live["fg"] = "red"
line_245_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_245_live["font"] = ftl
line_245_live["justify"] = "left"
line_245_live["anchor"] = "w"
line_245_live["relief"] = "flat"
line_245_live.place(x=8000, y=9965, width=70, height=33)

line_245_disabled = tk.Label(maincanvas)
line_245_disabled["bg"] = "#adafae"
line_245_disabled["fg"] = "red"
line_245_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_245_disabled["font"] = ftl
line_245_disabled["justify"] = "left"
line_245_disabled["anchor"] = "w"
line_245_disabled["relief"] = "flat"
line_245_disabled.place(x=650, y=9965, width=150, height=33)

line_246_frame = tk.Label(maincanvas)
line_246_frame["bg"] = "#adafae"
line_246_frame["text"] = ""
line_246_frame["relief"] = "sunken"
line_246_frame.place(x=10, y=10000, width=1060, height=40)

line_246_index = tk.Label(maincanvas)
line_246_index["bg"] = "#adafae"
line_246_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_246_index["font"] = ft
line_246_index["justify"] = "left"
line_246_index["anchor"] = "w"
line_246_index.place(x=20, y=10005, width=150, height=33)

line_246_name = tk.Label(maincanvas)
line_246_name["bg"] = "#adafae"
line_246_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_246_name["font"] = ft
line_246_name["justify"] = "left"
line_246_name["anchor"] = "w"
line_246_name.place(x=250, y=10005, width=500, height=33)

line_246_duration = tk.Label(maincanvas)
line_246_duration["bg"] = "#adafae"
line_246_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_246_duration["font"] = ft
line_246_duration["justify"] = "right"
line_246_duration["anchor"] = "e"
line_246_duration.place(x=910, y=10005, width=150, height=33)

line_246_live = tk.Label(maincanvas)
line_246_live["bg"] = "#adafae"
line_246_live["fg"] = "red"
line_246_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_246_live["font"] = ftl
line_246_live["justify"] = "left"
line_246_live["anchor"] = "w"
line_246_live["relief"] = "flat"
line_246_live.place(x=8000, y=10005, width=70, height=33)

line_246_disabled = tk.Label(maincanvas)
line_246_disabled["bg"] = "#adafae"
line_246_disabled["fg"] = "red"
line_246_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_246_disabled["font"] = ftl
line_246_disabled["justify"] = "left"
line_246_disabled["anchor"] = "w"
line_246_disabled["relief"] = "flat"
line_246_disabled.place(x=650, y=10005, width=150, height=33)

line_247_frame = tk.Label(maincanvas)
line_247_frame["bg"] = "#adafae"
line_247_frame["text"] = ""
line_247_frame["relief"] = "sunken"
line_247_frame.place(x=10, y=10040, width=1060, height=40)

line_247_index = tk.Label(maincanvas)
line_247_index["bg"] = "#adafae"
line_247_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_247_index["font"] = ft
line_247_index["justify"] = "left"
line_247_index["anchor"] = "w"
line_247_index.place(x=20, y=10045, width=150, height=33)

line_247_name = tk.Label(maincanvas)
line_247_name["bg"] = "#adafae"
line_247_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_247_name["font"] = ft
line_247_name["justify"] = "left"
line_247_name["anchor"] = "w"
line_247_name.place(x=250, y=10045, width=500, height=33)

line_247_duration = tk.Label(maincanvas)
line_247_duration["bg"] = "#adafae"
line_247_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_247_duration["font"] = ft
line_247_duration["justify"] = "right"
line_247_duration["anchor"] = "e"
line_247_duration.place(x=910, y=10045, width=150, height=33)

line_247_live = tk.Label(maincanvas)
line_247_live["bg"] = "#adafae"
line_247_live["fg"] = "red"
line_247_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_247_live["font"] = ftl
line_247_live["justify"] = "left"
line_247_live["anchor"] = "w"
line_247_live["relief"] = "flat"
line_247_live.place(x=8000, y=10045, width=70, height=33)

line_247_disabled = tk.Label(maincanvas)
line_247_disabled["bg"] = "#adafae"
line_247_disabled["fg"] = "red"
line_247_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_247_disabled["font"] = ftl
line_247_disabled["justify"] = "left"
line_247_disabled["anchor"] = "w"
line_247_disabled["relief"] = "flat"
line_247_disabled.place(x=650, y=10045, width=150, height=33)

line_248_frame = tk.Label(maincanvas)
line_248_frame["bg"] = "#adafae"
line_248_frame["text"] = ""
line_248_frame["relief"] = "sunken"
line_248_frame.place(x=10, y=10080, width=1060, height=40)

line_248_index = tk.Label(maincanvas)
line_248_index["bg"] = "#adafae"
line_248_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_248_index["font"] = ft
line_248_index["justify"] = "left"
line_248_index["anchor"] = "w"
line_248_index.place(x=20, y=10085, width=150, height=33)

line_248_name = tk.Label(maincanvas)
line_248_name["bg"] = "#adafae"
line_248_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_248_name["font"] = ft
line_248_name["justify"] = "left"
line_248_name["anchor"] = "w"
line_248_name.place(x=250, y=10085, width=500, height=33)

line_248_duration = tk.Label(maincanvas)
line_248_duration["bg"] = "#adafae"
line_248_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_248_duration["font"] = ft
line_248_duration["justify"] = "right"
line_248_duration["anchor"] = "e"
line_248_duration.place(x=910, y=10085, width=150, height=33)

line_248_live = tk.Label(maincanvas)
line_248_live["bg"] = "#adafae"
line_248_live["fg"] = "red"
line_248_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_248_live["font"] = ftl
line_248_live["justify"] = "left"
line_248_live["anchor"] = "w"
line_248_live["relief"] = "flat"
line_248_live.place(x=8000, y=10085, width=70, height=33)

line_248_disabled = tk.Label(maincanvas)
line_248_disabled["bg"] = "#adafae"
line_248_disabled["fg"] = "red"
line_248_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_248_disabled["font"] = ftl
line_248_disabled["justify"] = "left"
line_248_disabled["anchor"] = "w"
line_248_disabled["relief"] = "flat"
line_248_disabled.place(x=650, y=10085, width=150, height=33)

line_249_frame = tk.Label(maincanvas)
line_249_frame["bg"] = "#adafae"
line_249_frame["text"] = ""
line_249_frame["relief"] = "sunken"
line_249_frame.place(x=10, y=10120, width=1060, height=40)

line_249_index = tk.Label(maincanvas)
line_249_index["bg"] = "#adafae"
line_249_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_249_index["font"] = ft
line_249_index["justify"] = "left"
line_249_index["anchor"] = "w"
line_249_index.place(x=20, y=10125, width=150, height=33)

line_249_name = tk.Label(maincanvas)
line_249_name["bg"] = "#adafae"
line_249_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_249_name["font"] = ft
line_249_name["justify"] = "left"
line_249_name["anchor"] = "w"
line_249_name.place(x=250, y=10125, width=500, height=33)

line_249_duration = tk.Label(maincanvas)
line_249_duration["bg"] = "#adafae"
line_249_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_249_duration["font"] = ft
line_249_duration["justify"] = "right"
line_249_duration["anchor"] = "e"
line_249_duration.place(x=910, y=10125, width=150, height=33)

line_249_live = tk.Label(maincanvas)
line_249_live["bg"] = "#adafae"
line_249_live["fg"] = "red"
line_249_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_249_live["font"] = ftl
line_249_live["justify"] = "left"
line_249_live["anchor"] = "w"
line_249_live["relief"] = "flat"
line_249_live.place(x=8000, y=10125, width=70, height=33)

line_249_disabled = tk.Label(maincanvas)
line_249_disabled["bg"] = "#adafae"
line_249_disabled["fg"] = "red"
line_249_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_249_disabled["font"] = ftl
line_249_disabled["justify"] = "left"
line_249_disabled["anchor"] = "w"
line_249_disabled["relief"] = "flat"
line_249_disabled.place(x=650, y=10125, width=150, height=33)

line_250_frame = tk.Label(maincanvas)
line_250_frame["bg"] = "#adafae"
line_250_frame["text"] = ""
line_250_frame["relief"] = "sunken"
line_250_frame.place(x=10, y=10160, width=1060, height=40)

line_250_index = tk.Label(maincanvas)
line_250_index["bg"] = "#adafae"
line_250_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_250_index["font"] = ft
line_250_index["justify"] = "left"
line_250_index["anchor"] = "w"
line_250_index.place(x=20, y=10165, width=150, height=33)

line_250_name = tk.Label(maincanvas)
line_250_name["bg"] = "#adafae"
line_250_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_250_name["font"] = ft
line_250_name["justify"] = "left"
line_250_name["anchor"] = "w"
line_250_name.place(x=250, y=10165, width=500, height=33)

line_250_duration = tk.Label(maincanvas)
line_250_duration["bg"] = "#adafae"
line_250_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_250_duration["font"] = ft
line_250_duration["justify"] = "right"
line_250_duration["anchor"] = "e"
line_250_duration.place(x=910, y=10165, width=150, height=33)

line_250_live = tk.Label(maincanvas)
line_250_live["bg"] = "#adafae"
line_250_live["fg"] = "red"
line_250_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_250_live["font"] = ftl
line_250_live["justify"] = "left"
line_250_live["anchor"] = "w"
line_250_live["relief"] = "flat"
line_250_live.place(x=8000, y=10165, width=70, height=33)

line_250_disabled = tk.Label(maincanvas)
line_250_disabled["bg"] = "#adafae"
line_250_disabled["fg"] = "red"
line_250_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_250_disabled["font"] = ftl
line_250_disabled["justify"] = "left"
line_250_disabled["anchor"] = "w"
line_250_disabled["relief"] = "flat"
line_250_disabled.place(x=650, y=10165, width=150, height=33)

line_251_frame = tk.Label(maincanvas)
line_251_frame["bg"] = "#adafae"
line_251_frame["text"] = ""
line_251_frame["relief"] = "sunken"
line_251_frame.place(x=10, y=10200, width=1060, height=40)

line_251_index = tk.Label(maincanvas)
line_251_index["bg"] = "#adafae"
line_251_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_251_index["font"] = ft
line_251_index["justify"] = "left"
line_251_index["anchor"] = "w"
line_251_index.place(x=20, y=10205, width=150, height=33)

line_251_name = tk.Label(maincanvas)
line_251_name["bg"] = "#adafae"
line_251_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_251_name["font"] = ft
line_251_name["justify"] = "left"
line_251_name["anchor"] = "w"
line_251_name.place(x=250, y=10205, width=500, height=33)

line_251_duration = tk.Label(maincanvas)
line_251_duration["bg"] = "#adafae"
line_251_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_251_duration["font"] = ft
line_251_duration["justify"] = "right"
line_251_duration["anchor"] = "e"
line_251_duration.place(x=910, y=10205, width=150, height=33)

line_251_live = tk.Label(maincanvas)
line_251_live["bg"] = "#adafae"
line_251_live["fg"] = "red"
line_251_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_251_live["font"] = ftl
line_251_live["justify"] = "left"
line_251_live["anchor"] = "w"
line_251_live["relief"] = "flat"
line_251_live.place(x=8000, y=10205, width=70, height=33)

line_251_disabled = tk.Label(maincanvas)
line_251_disabled["bg"] = "#adafae"
line_251_disabled["fg"] = "red"
line_251_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_251_disabled["font"] = ftl
line_251_disabled["justify"] = "left"
line_251_disabled["anchor"] = "w"
line_251_disabled["relief"] = "flat"
line_251_disabled.place(x=650, y=10205, width=150, height=33)

line_252_frame = tk.Label(maincanvas)
line_252_frame["bg"] = "#adafae"
line_252_frame["text"] = ""
line_252_frame["relief"] = "sunken"
line_252_frame.place(x=10, y=10240, width=1060, height=40)

line_252_index = tk.Label(maincanvas)
line_252_index["bg"] = "#adafae"
line_252_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_252_index["font"] = ft
line_252_index["justify"] = "left"
line_252_index["anchor"] = "w"
line_252_index.place(x=20, y=10245, width=150, height=33)

line_252_name = tk.Label(maincanvas)
line_252_name["bg"] = "#adafae"
line_252_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_252_name["font"] = ft
line_252_name["justify"] = "left"
line_252_name["anchor"] = "w"
line_252_name.place(x=250, y=10245, width=500, height=33)

line_252_duration = tk.Label(maincanvas)
line_252_duration["bg"] = "#adafae"
line_252_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_252_duration["font"] = ft
line_252_duration["justify"] = "right"
line_252_duration["anchor"] = "e"
line_252_duration.place(x=910, y=10245, width=150, height=33)

line_252_live = tk.Label(maincanvas)
line_252_live["bg"] = "#adafae"
line_252_live["fg"] = "red"
line_252_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_252_live["font"] = ftl
line_252_live["justify"] = "left"
line_252_live["anchor"] = "w"
line_252_live["relief"] = "flat"
line_252_live.place(x=8000, y=10245, width=70, height=33)

line_252_disabled = tk.Label(maincanvas)
line_252_disabled["bg"] = "#adafae"
line_252_disabled["fg"] = "red"
line_252_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_252_disabled["font"] = ftl
line_252_disabled["justify"] = "left"
line_252_disabled["anchor"] = "w"
line_252_disabled["relief"] = "flat"
line_252_disabled.place(x=650, y=10245, width=150, height=33)

line_253_frame = tk.Label(maincanvas)
line_253_frame["bg"] = "#adafae"
line_253_frame["text"] = ""
line_253_frame["relief"] = "sunken"
line_253_frame.place(x=10, y=10280, width=1060, height=40)

line_253_index = tk.Label(maincanvas)
line_253_index["bg"] = "#adafae"
line_253_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_253_index["font"] = ft
line_253_index["justify"] = "left"
line_253_index["anchor"] = "w"
line_253_index.place(x=20, y=10285, width=150, height=33)

line_253_name = tk.Label(maincanvas)
line_253_name["bg"] = "#adafae"
line_253_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_253_name["font"] = ft
line_253_name["justify"] = "left"
line_253_name["anchor"] = "w"
line_253_name.place(x=250, y=10285, width=500, height=33)

line_253_duration = tk.Label(maincanvas)
line_253_duration["bg"] = "#adafae"
line_253_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_253_duration["font"] = ft
line_253_duration["justify"] = "right"
line_253_duration["anchor"] = "e"
line_253_duration.place(x=910, y=10285, width=150, height=33)

line_253_live = tk.Label(maincanvas)
line_253_live["bg"] = "#adafae"
line_253_live["fg"] = "red"
line_253_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_253_live["font"] = ftl
line_253_live["justify"] = "left"
line_253_live["anchor"] = "w"
line_253_live["relief"] = "flat"
line_253_live.place(x=8000, y=10285, width=70, height=33)

line_253_disabled = tk.Label(maincanvas)
line_253_disabled["bg"] = "#adafae"
line_253_disabled["fg"] = "red"
line_253_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_253_disabled["font"] = ftl
line_253_disabled["justify"] = "left"
line_253_disabled["anchor"] = "w"
line_253_disabled["relief"] = "flat"
line_253_disabled.place(x=650, y=10285, width=150, height=33)

line_254_frame = tk.Label(maincanvas)
line_254_frame["bg"] = "#adafae"
line_254_frame["text"] = ""
line_254_frame["relief"] = "sunken"
line_254_frame.place(x=10, y=10320, width=1060, height=40)

line_254_index = tk.Label(maincanvas)
line_254_index["bg"] = "#adafae"
line_254_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_254_index["font"] = ft
line_254_index["justify"] = "left"
line_254_index["anchor"] = "w"
line_254_index.place(x=20, y=10325, width=150, height=33)

line_254_name = tk.Label(maincanvas)
line_254_name["bg"] = "#adafae"
line_254_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_254_name["font"] = ft
line_254_name["justify"] = "left"
line_254_name["anchor"] = "w"
line_254_name.place(x=250, y=10325, width=500, height=33)

line_254_duration = tk.Label(maincanvas)
line_254_duration["bg"] = "#adafae"
line_254_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_254_duration["font"] = ft
line_254_duration["justify"] = "right"
line_254_duration["anchor"] = "e"
line_254_duration.place(x=910, y=10325, width=150, height=33)

line_254_live = tk.Label(maincanvas)
line_254_live["bg"] = "#adafae"
line_254_live["fg"] = "red"
line_254_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_254_live["font"] = ftl
line_254_live["justify"] = "left"
line_254_live["anchor"] = "w"
line_254_live["relief"] = "flat"
line_254_live.place(x=8000, y=10325, width=70, height=33)

line_254_disabled = tk.Label(maincanvas)
line_254_disabled["bg"] = "#adafae"
line_254_disabled["fg"] = "red"
line_254_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_254_disabled["font"] = ftl
line_254_disabled["justify"] = "left"
line_254_disabled["anchor"] = "w"
line_254_disabled["relief"] = "flat"
line_254_disabled.place(x=650, y=10325, width=150, height=33)

line_255_frame = tk.Label(maincanvas)
line_255_frame["bg"] = "#adafae"
line_255_frame["text"] = ""
line_255_frame["relief"] = "sunken"
line_255_frame.place(x=10, y=10360, width=1060, height=40)

line_255_index = tk.Label(maincanvas)
line_255_index["bg"] = "#adafae"
line_255_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_255_index["font"] = ft
line_255_index["justify"] = "left"
line_255_index["anchor"] = "w"
line_255_index.place(x=20, y=10365, width=150, height=33)

line_255_name = tk.Label(maincanvas)
line_255_name["bg"] = "#adafae"
line_255_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_255_name["font"] = ft
line_255_name["justify"] = "left"
line_255_name["anchor"] = "w"
line_255_name.place(x=250, y=10365, width=500, height=33)

line_255_duration = tk.Label(maincanvas)
line_255_duration["bg"] = "#adafae"
line_255_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_255_duration["font"] = ft
line_255_duration["justify"] = "right"
line_255_duration["anchor"] = "e"
line_255_duration.place(x=910, y=10365, width=150, height=33)

line_255_live = tk.Label(maincanvas)
line_255_live["bg"] = "#adafae"
line_255_live["fg"] = "red"
line_255_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_255_live["font"] = ftl
line_255_live["justify"] = "left"
line_255_live["anchor"] = "w"
line_255_live["relief"] = "flat"
line_255_live.place(x=8000, y=10365, width=70, height=33)

line_255_disabled = tk.Label(maincanvas)
line_255_disabled["bg"] = "#adafae"
line_255_disabled["fg"] = "red"
line_255_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_255_disabled["font"] = ftl
line_255_disabled["justify"] = "left"
line_255_disabled["anchor"] = "w"
line_255_disabled["relief"] = "flat"
line_255_disabled.place(x=650, y=10365, width=150, height=33)

line_256_frame = tk.Label(maincanvas)
line_256_frame["bg"] = "#adafae"
line_256_frame["text"] = ""
line_256_frame["relief"] = "sunken"
line_256_frame.place(x=10, y=10400, width=1060, height=40)

line_256_index = tk.Label(maincanvas)
line_256_index["bg"] = "#adafae"
line_256_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_256_index["font"] = ft
line_256_index["justify"] = "left"
line_256_index["anchor"] = "w"
line_256_index.place(x=20, y=10405, width=150, height=33)

line_256_name = tk.Label(maincanvas)
line_256_name["bg"] = "#adafae"
line_256_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_256_name["font"] = ft
line_256_name["justify"] = "left"
line_256_name["anchor"] = "w"
line_256_name.place(x=250, y=10405, width=500, height=33)

line_256_duration = tk.Label(maincanvas)
line_256_duration["bg"] = "#adafae"
line_256_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_256_duration["font"] = ft
line_256_duration["justify"] = "right"
line_256_duration["anchor"] = "e"
line_256_duration.place(x=910, y=10405, width=150, height=33)

line_256_live = tk.Label(maincanvas)
line_256_live["bg"] = "#adafae"
line_256_live["fg"] = "red"
line_256_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_256_live["font"] = ftl
line_256_live["justify"] = "left"
line_256_live["anchor"] = "w"
line_256_live["relief"] = "flat"
line_256_live.place(x=8000, y=10405, width=70, height=33)

line_256_disabled = tk.Label(maincanvas)
line_256_disabled["bg"] = "#adafae"
line_256_disabled["fg"] = "red"
line_256_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_256_disabled["font"] = ftl
line_256_disabled["justify"] = "left"
line_256_disabled["anchor"] = "w"
line_256_disabled["relief"] = "flat"
line_256_disabled.place(x=650, y=10405, width=150, height=33)

line_257_frame = tk.Label(maincanvas)
line_257_frame["bg"] = "#adafae"
line_257_frame["text"] = ""
line_257_frame["relief"] = "sunken"
line_257_frame.place(x=10, y=10440, width=1060, height=40)

line_257_index = tk.Label(maincanvas)
line_257_index["bg"] = "#adafae"
line_257_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_257_index["font"] = ft
line_257_index["justify"] = "left"
line_257_index["anchor"] = "w"
line_257_index.place(x=20, y=10445, width=150, height=33)

line_257_name = tk.Label(maincanvas)
line_257_name["bg"] = "#adafae"
line_257_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_257_name["font"] = ft
line_257_name["justify"] = "left"
line_257_name["anchor"] = "w"
line_257_name.place(x=250, y=10445, width=500, height=33)

line_257_duration = tk.Label(maincanvas)
line_257_duration["bg"] = "#adafae"
line_257_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_257_duration["font"] = ft
line_257_duration["justify"] = "right"
line_257_duration["anchor"] = "e"
line_257_duration.place(x=910, y=10445, width=150, height=33)

line_257_live = tk.Label(maincanvas)
line_257_live["bg"] = "#adafae"
line_257_live["fg"] = "red"
line_257_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_257_live["font"] = ftl
line_257_live["justify"] = "left"
line_257_live["anchor"] = "w"
line_257_live["relief"] = "flat"
line_257_live.place(x=8000, y=10445, width=70, height=33)

line_257_disabled = tk.Label(maincanvas)
line_257_disabled["bg"] = "#adafae"
line_257_disabled["fg"] = "red"
line_257_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_257_disabled["font"] = ftl
line_257_disabled["justify"] = "left"
line_257_disabled["anchor"] = "w"
line_257_disabled["relief"] = "flat"
line_257_disabled.place(x=650, y=10445, width=150, height=33)

line_258_frame = tk.Label(maincanvas)
line_258_frame["bg"] = "#adafae"
line_258_frame["text"] = ""
line_258_frame["relief"] = "sunken"
line_258_frame.place(x=10, y=10480, width=1060, height=40)

line_258_index = tk.Label(maincanvas)
line_258_index["bg"] = "#adafae"
line_258_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_258_index["font"] = ft
line_258_index["justify"] = "left"
line_258_index["anchor"] = "w"
line_258_index.place(x=20, y=10485, width=150, height=33)

line_258_name = tk.Label(maincanvas)
line_258_name["bg"] = "#adafae"
line_258_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_258_name["font"] = ft
line_258_name["justify"] = "left"
line_258_name["anchor"] = "w"
line_258_name.place(x=250, y=10485, width=500, height=33)

line_258_duration = tk.Label(maincanvas)
line_258_duration["bg"] = "#adafae"
line_258_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_258_duration["font"] = ft
line_258_duration["justify"] = "right"
line_258_duration["anchor"] = "e"
line_258_duration.place(x=910, y=10485, width=150, height=33)

line_258_live = tk.Label(maincanvas)
line_258_live["bg"] = "#adafae"
line_258_live["fg"] = "red"
line_258_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_258_live["font"] = ftl
line_258_live["justify"] = "left"
line_258_live["anchor"] = "w"
line_258_live["relief"] = "flat"
line_258_live.place(x=8000, y=10485, width=70, height=33)

line_258_disabled = tk.Label(maincanvas)
line_258_disabled["bg"] = "#adafae"
line_258_disabled["fg"] = "red"
line_258_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_258_disabled["font"] = ftl
line_258_disabled["justify"] = "left"
line_258_disabled["anchor"] = "w"
line_258_disabled["relief"] = "flat"
line_258_disabled.place(x=650, y=10485, width=150, height=33)

line_259_frame = tk.Label(maincanvas)
line_259_frame["bg"] = "#adafae"
line_259_frame["text"] = ""
line_259_frame["relief"] = "sunken"
line_259_frame.place(x=10, y=10520, width=1060, height=40)

line_259_index = tk.Label(maincanvas)
line_259_index["bg"] = "#adafae"
line_259_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_259_index["font"] = ft
line_259_index["justify"] = "left"
line_259_index["anchor"] = "w"
line_259_index.place(x=20, y=10525, width=150, height=33)

line_259_name = tk.Label(maincanvas)
line_259_name["bg"] = "#adafae"
line_259_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_259_name["font"] = ft
line_259_name["justify"] = "left"
line_259_name["anchor"] = "w"
line_259_name.place(x=250, y=10525, width=500, height=33)

line_259_duration = tk.Label(maincanvas)
line_259_duration["bg"] = "#adafae"
line_259_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_259_duration["font"] = ft
line_259_duration["justify"] = "right"
line_259_duration["anchor"] = "e"
line_259_duration.place(x=910, y=10525, width=150, height=33)

line_259_live = tk.Label(maincanvas)
line_259_live["bg"] = "#adafae"
line_259_live["fg"] = "red"
line_259_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_259_live["font"] = ftl
line_259_live["justify"] = "left"
line_259_live["anchor"] = "w"
line_259_live["relief"] = "flat"
line_259_live.place(x=8000, y=10525, width=70, height=33)

line_259_disabled = tk.Label(maincanvas)
line_259_disabled["bg"] = "#adafae"
line_259_disabled["fg"] = "red"
line_259_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_259_disabled["font"] = ftl
line_259_disabled["justify"] = "left"
line_259_disabled["anchor"] = "w"
line_259_disabled["relief"] = "flat"
line_259_disabled.place(x=650, y=10525, width=150, height=33)

line_260_frame = tk.Label(maincanvas)
line_260_frame["bg"] = "#adafae"
line_260_frame["text"] = ""
line_260_frame["relief"] = "sunken"
line_260_frame.place(x=10, y=10560, width=1060, height=40)

line_260_index = tk.Label(maincanvas)
line_260_index["bg"] = "#adafae"
line_260_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_260_index["font"] = ft
line_260_index["justify"] = "left"
line_260_index["anchor"] = "w"
line_260_index.place(x=20, y=10565, width=150, height=33)

line_260_name = tk.Label(maincanvas)
line_260_name["bg"] = "#adafae"
line_260_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_260_name["font"] = ft
line_260_name["justify"] = "left"
line_260_name["anchor"] = "w"
line_260_name.place(x=250, y=10565, width=500, height=33)

line_260_duration = tk.Label(maincanvas)
line_260_duration["bg"] = "#adafae"
line_260_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_260_duration["font"] = ft
line_260_duration["justify"] = "right"
line_260_duration["anchor"] = "e"
line_260_duration.place(x=910, y=10565, width=150, height=33)

line_260_live = tk.Label(maincanvas)
line_260_live["bg"] = "#adafae"
line_260_live["fg"] = "red"
line_260_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_260_live["font"] = ftl
line_260_live["justify"] = "left"
line_260_live["anchor"] = "w"
line_260_live["relief"] = "flat"
line_260_live.place(x=8000, y=10565, width=70, height=33)

line_260_disabled = tk.Label(maincanvas)
line_260_disabled["bg"] = "#adafae"
line_260_disabled["fg"] = "red"
line_260_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_260_disabled["font"] = ftl
line_260_disabled["justify"] = "left"
line_260_disabled["anchor"] = "w"
line_260_disabled["relief"] = "flat"
line_260_disabled.place(x=650, y=10565, width=150, height=33)

line_261_frame = tk.Label(maincanvas)
line_261_frame["bg"] = "#adafae"
line_261_frame["text"] = ""
line_261_frame["relief"] = "sunken"
line_261_frame.place(x=10, y=10600, width=1060, height=40)

line_261_index = tk.Label(maincanvas)
line_261_index["bg"] = "#adafae"
line_261_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_261_index["font"] = ft
line_261_index["justify"] = "left"
line_261_index["anchor"] = "w"
line_261_index.place(x=20, y=10605, width=150, height=33)

line_261_name = tk.Label(maincanvas)
line_261_name["bg"] = "#adafae"
line_261_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_261_name["font"] = ft
line_261_name["justify"] = "left"
line_261_name["anchor"] = "w"
line_261_name.place(x=250, y=10605, width=500, height=33)

line_261_duration = tk.Label(maincanvas)
line_261_duration["bg"] = "#adafae"
line_261_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_261_duration["font"] = ft
line_261_duration["justify"] = "right"
line_261_duration["anchor"] = "e"
line_261_duration.place(x=910, y=10605, width=150, height=33)

line_261_live = tk.Label(maincanvas)
line_261_live["bg"] = "#adafae"
line_261_live["fg"] = "red"
line_261_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_261_live["font"] = ftl
line_261_live["justify"] = "left"
line_261_live["anchor"] = "w"
line_261_live["relief"] = "flat"
line_261_live.place(x=8000, y=10605, width=70, height=33)

line_261_disabled = tk.Label(maincanvas)
line_261_disabled["bg"] = "#adafae"
line_261_disabled["fg"] = "red"
line_261_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_261_disabled["font"] = ftl
line_261_disabled["justify"] = "left"
line_261_disabled["anchor"] = "w"
line_261_disabled["relief"] = "flat"
line_261_disabled.place(x=650, y=10605, width=150, height=33)

line_262_frame = tk.Label(maincanvas)
line_262_frame["bg"] = "#adafae"
line_262_frame["text"] = ""
line_262_frame["relief"] = "sunken"
line_262_frame.place(x=10, y=10640, width=1060, height=40)

line_262_index = tk.Label(maincanvas)
line_262_index["bg"] = "#adafae"
line_262_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_262_index["font"] = ft
line_262_index["justify"] = "left"
line_262_index["anchor"] = "w"
line_262_index.place(x=20, y=10645, width=150, height=33)

line_262_name = tk.Label(maincanvas)
line_262_name["bg"] = "#adafae"
line_262_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_262_name["font"] = ft
line_262_name["justify"] = "left"
line_262_name["anchor"] = "w"
line_262_name.place(x=250, y=10645, width=500, height=33)

line_262_duration = tk.Label(maincanvas)
line_262_duration["bg"] = "#adafae"
line_262_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_262_duration["font"] = ft
line_262_duration["justify"] = "right"
line_262_duration["anchor"] = "e"
line_262_duration.place(x=910, y=10645, width=150, height=33)

line_262_live = tk.Label(maincanvas)
line_262_live["bg"] = "#adafae"
line_262_live["fg"] = "red"
line_262_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_262_live["font"] = ftl
line_262_live["justify"] = "left"
line_262_live["anchor"] = "w"
line_262_live["relief"] = "flat"
line_262_live.place(x=8000, y=10645, width=70, height=33)

line_262_disabled = tk.Label(maincanvas)
line_262_disabled["bg"] = "#adafae"
line_262_disabled["fg"] = "red"
line_262_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_262_disabled["font"] = ftl
line_262_disabled["justify"] = "left"
line_262_disabled["anchor"] = "w"
line_262_disabled["relief"] = "flat"
line_262_disabled.place(x=650, y=10645, width=150, height=33)

line_263_frame = tk.Label(maincanvas)
line_263_frame["bg"] = "#adafae"
line_263_frame["text"] = ""
line_263_frame["relief"] = "sunken"
line_263_frame.place(x=10, y=10680, width=1060, height=40)

line_263_index = tk.Label(maincanvas)
line_263_index["bg"] = "#adafae"
line_263_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_263_index["font"] = ft
line_263_index["justify"] = "left"
line_263_index["anchor"] = "w"
line_263_index.place(x=20, y=10685, width=150, height=33)

line_263_name = tk.Label(maincanvas)
line_263_name["bg"] = "#adafae"
line_263_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_263_name["font"] = ft
line_263_name["justify"] = "left"
line_263_name["anchor"] = "w"
line_263_name.place(x=250, y=10685, width=500, height=33)

line_263_duration = tk.Label(maincanvas)
line_263_duration["bg"] = "#adafae"
line_263_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_263_duration["font"] = ft
line_263_duration["justify"] = "right"
line_263_duration["anchor"] = "e"
line_263_duration.place(x=910, y=10685, width=150, height=33)

line_263_live = tk.Label(maincanvas)
line_263_live["bg"] = "#adafae"
line_263_live["fg"] = "red"
line_263_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_263_live["font"] = ftl
line_263_live["justify"] = "left"
line_263_live["anchor"] = "w"
line_263_live["relief"] = "flat"
line_263_live.place(x=8000, y=10685, width=70, height=33)

line_263_disabled = tk.Label(maincanvas)
line_263_disabled["bg"] = "#adafae"
line_263_disabled["fg"] = "red"
line_263_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_263_disabled["font"] = ftl
line_263_disabled["justify"] = "left"
line_263_disabled["anchor"] = "w"
line_263_disabled["relief"] = "flat"
line_263_disabled.place(x=650, y=10685, width=150, height=33)

line_264_frame = tk.Label(maincanvas)
line_264_frame["bg"] = "#adafae"
line_264_frame["text"] = ""
line_264_frame["relief"] = "sunken"
line_264_frame.place(x=10, y=10720, width=1060, height=40)

line_264_index = tk.Label(maincanvas)
line_264_index["bg"] = "#adafae"
line_264_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_264_index["font"] = ft
line_264_index["justify"] = "left"
line_264_index["anchor"] = "w"
line_264_index.place(x=20, y=10725, width=150, height=33)

line_264_name = tk.Label(maincanvas)
line_264_name["bg"] = "#adafae"
line_264_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_264_name["font"] = ft
line_264_name["justify"] = "left"
line_264_name["anchor"] = "w"
line_264_name.place(x=250, y=10725, width=500, height=33)

line_264_duration = tk.Label(maincanvas)
line_264_duration["bg"] = "#adafae"
line_264_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_264_duration["font"] = ft
line_264_duration["justify"] = "right"
line_264_duration["anchor"] = "e"
line_264_duration.place(x=910, y=10725, width=150, height=33)

line_264_live = tk.Label(maincanvas)
line_264_live["bg"] = "#adafae"
line_264_live["fg"] = "red"
line_264_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_264_live["font"] = ftl
line_264_live["justify"] = "left"
line_264_live["anchor"] = "w"
line_264_live["relief"] = "flat"
line_264_live.place(x=8000, y=10725, width=70, height=33)

line_264_disabled = tk.Label(maincanvas)
line_264_disabled["bg"] = "#adafae"
line_264_disabled["fg"] = "red"
line_264_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_264_disabled["font"] = ftl
line_264_disabled["justify"] = "left"
line_264_disabled["anchor"] = "w"
line_264_disabled["relief"] = "flat"
line_264_disabled.place(x=650, y=10725, width=150, height=33)

line_265_frame = tk.Label(maincanvas)
line_265_frame["bg"] = "#adafae"
line_265_frame["text"] = ""
line_265_frame["relief"] = "sunken"
line_265_frame.place(x=10, y=10760, width=1060, height=40)

line_265_index = tk.Label(maincanvas)
line_265_index["bg"] = "#adafae"
line_265_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_265_index["font"] = ft
line_265_index["justify"] = "left"
line_265_index["anchor"] = "w"
line_265_index.place(x=20, y=10765, width=150, height=33)

line_265_name = tk.Label(maincanvas)
line_265_name["bg"] = "#adafae"
line_265_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_265_name["font"] = ft
line_265_name["justify"] = "left"
line_265_name["anchor"] = "w"
line_265_name.place(x=250, y=10765, width=500, height=33)

line_265_duration = tk.Label(maincanvas)
line_265_duration["bg"] = "#adafae"
line_265_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_265_duration["font"] = ft
line_265_duration["justify"] = "right"
line_265_duration["anchor"] = "e"
line_265_duration.place(x=910, y=10765, width=150, height=33)

line_265_live = tk.Label(maincanvas)
line_265_live["bg"] = "#adafae"
line_265_live["fg"] = "red"
line_265_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_265_live["font"] = ftl
line_265_live["justify"] = "left"
line_265_live["anchor"] = "w"
line_265_live["relief"] = "flat"
line_265_live.place(x=8000, y=10765, width=70, height=33)

line_265_disabled = tk.Label(maincanvas)
line_265_disabled["bg"] = "#adafae"
line_265_disabled["fg"] = "red"
line_265_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_265_disabled["font"] = ftl
line_265_disabled["justify"] = "left"
line_265_disabled["anchor"] = "w"
line_265_disabled["relief"] = "flat"
line_265_disabled.place(x=650, y=10765, width=150, height=33)

line_266_frame = tk.Label(maincanvas)
line_266_frame["bg"] = "#adafae"
line_266_frame["text"] = ""
line_266_frame["relief"] = "sunken"
line_266_frame.place(x=10, y=10800, width=1060, height=40)

line_266_index = tk.Label(maincanvas)
line_266_index["bg"] = "#adafae"
line_266_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_266_index["font"] = ft
line_266_index["justify"] = "left"
line_266_index["anchor"] = "w"
line_266_index.place(x=20, y=10805, width=150, height=33)

line_266_name = tk.Label(maincanvas)
line_266_name["bg"] = "#adafae"
line_266_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_266_name["font"] = ft
line_266_name["justify"] = "left"
line_266_name["anchor"] = "w"
line_266_name.place(x=250, y=10805, width=500, height=33)

line_266_duration = tk.Label(maincanvas)
line_266_duration["bg"] = "#adafae"
line_266_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_266_duration["font"] = ft
line_266_duration["justify"] = "right"
line_266_duration["anchor"] = "e"
line_266_duration.place(x=910, y=10805, width=150, height=33)

line_266_live = tk.Label(maincanvas)
line_266_live["bg"] = "#adafae"
line_266_live["fg"] = "red"
line_266_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_266_live["font"] = ftl
line_266_live["justify"] = "left"
line_266_live["anchor"] = "w"
line_266_live["relief"] = "flat"
line_266_live.place(x=8000, y=10805, width=70, height=33)

line_266_disabled = tk.Label(maincanvas)
line_266_disabled["bg"] = "#adafae"
line_266_disabled["fg"] = "red"
line_266_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_266_disabled["font"] = ftl
line_266_disabled["justify"] = "left"
line_266_disabled["anchor"] = "w"
line_266_disabled["relief"] = "flat"
line_266_disabled.place(x=650, y=10805, width=150, height=33)

line_267_frame = tk.Label(maincanvas)
line_267_frame["bg"] = "#adafae"
line_267_frame["text"] = ""
line_267_frame["relief"] = "sunken"
line_267_frame.place(x=10, y=10840, width=1060, height=40)

line_267_index = tk.Label(maincanvas)
line_267_index["bg"] = "#adafae"
line_267_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_267_index["font"] = ft
line_267_index["justify"] = "left"
line_267_index["anchor"] = "w"
line_267_index.place(x=20, y=10845, width=150, height=33)

line_267_name = tk.Label(maincanvas)
line_267_name["bg"] = "#adafae"
line_267_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_267_name["font"] = ft
line_267_name["justify"] = "left"
line_267_name["anchor"] = "w"
line_267_name.place(x=250, y=10845, width=500, height=33)

line_267_duration = tk.Label(maincanvas)
line_267_duration["bg"] = "#adafae"
line_267_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_267_duration["font"] = ft
line_267_duration["justify"] = "right"
line_267_duration["anchor"] = "e"
line_267_duration.place(x=910, y=10845, width=150, height=33)

line_267_live = tk.Label(maincanvas)
line_267_live["bg"] = "#adafae"
line_267_live["fg"] = "red"
line_267_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_267_live["font"] = ftl
line_267_live["justify"] = "left"
line_267_live["anchor"] = "w"
line_267_live["relief"] = "flat"
line_267_live.place(x=8000, y=10845, width=70, height=33)

line_267_disabled = tk.Label(maincanvas)
line_267_disabled["bg"] = "#adafae"
line_267_disabled["fg"] = "red"
line_267_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_267_disabled["font"] = ftl
line_267_disabled["justify"] = "left"
line_267_disabled["anchor"] = "w"
line_267_disabled["relief"] = "flat"
line_267_disabled.place(x=650, y=10845, width=150, height=33)

line_268_frame = tk.Label(maincanvas)
line_268_frame["bg"] = "#adafae"
line_268_frame["text"] = ""
line_268_frame["relief"] = "sunken"
line_268_frame.place(x=10, y=10880, width=1060, height=40)

line_268_index = tk.Label(maincanvas)
line_268_index["bg"] = "#adafae"
line_268_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_268_index["font"] = ft
line_268_index["justify"] = "left"
line_268_index["anchor"] = "w"
line_268_index.place(x=20, y=10885, width=150, height=33)

line_268_name = tk.Label(maincanvas)
line_268_name["bg"] = "#adafae"
line_268_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_268_name["font"] = ft
line_268_name["justify"] = "left"
line_268_name["anchor"] = "w"
line_268_name.place(x=250, y=10885, width=500, height=33)

line_268_duration = tk.Label(maincanvas)
line_268_duration["bg"] = "#adafae"
line_268_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_268_duration["font"] = ft
line_268_duration["justify"] = "right"
line_268_duration["anchor"] = "e"
line_268_duration.place(x=910, y=10885, width=150, height=33)

line_268_live = tk.Label(maincanvas)
line_268_live["bg"] = "#adafae"
line_268_live["fg"] = "red"
line_268_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_268_live["font"] = ftl
line_268_live["justify"] = "left"
line_268_live["anchor"] = "w"
line_268_live["relief"] = "flat"
line_268_live.place(x=8000, y=10885, width=70, height=33)

line_268_disabled = tk.Label(maincanvas)
line_268_disabled["bg"] = "#adafae"
line_268_disabled["fg"] = "red"
line_268_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_268_disabled["font"] = ftl
line_268_disabled["justify"] = "left"
line_268_disabled["anchor"] = "w"
line_268_disabled["relief"] = "flat"
line_268_disabled.place(x=650, y=10885, width=150, height=33)

line_269_frame = tk.Label(maincanvas)
line_269_frame["bg"] = "#adafae"
line_269_frame["text"] = ""
line_269_frame["relief"] = "sunken"
line_269_frame.place(x=10, y=10920, width=1060, height=40)

line_269_index = tk.Label(maincanvas)
line_269_index["bg"] = "#adafae"
line_269_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_269_index["font"] = ft
line_269_index["justify"] = "left"
line_269_index["anchor"] = "w"
line_269_index.place(x=20, y=10925, width=150, height=33)

line_269_name = tk.Label(maincanvas)
line_269_name["bg"] = "#adafae"
line_269_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_269_name["font"] = ft
line_269_name["justify"] = "left"
line_269_name["anchor"] = "w"
line_269_name.place(x=250, y=10925, width=500, height=33)

line_269_duration = tk.Label(maincanvas)
line_269_duration["bg"] = "#adafae"
line_269_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_269_duration["font"] = ft
line_269_duration["justify"] = "right"
line_269_duration["anchor"] = "e"
line_269_duration.place(x=910, y=10925, width=150, height=33)

line_269_live = tk.Label(maincanvas)
line_269_live["bg"] = "#adafae"
line_269_live["fg"] = "red"
line_269_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_269_live["font"] = ftl
line_269_live["justify"] = "left"
line_269_live["anchor"] = "w"
line_269_live["relief"] = "flat"
line_269_live.place(x=8000, y=10925, width=70, height=33)

line_269_disabled = tk.Label(maincanvas)
line_269_disabled["bg"] = "#adafae"
line_269_disabled["fg"] = "red"
line_269_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_269_disabled["font"] = ftl
line_269_disabled["justify"] = "left"
line_269_disabled["anchor"] = "w"
line_269_disabled["relief"] = "flat"
line_269_disabled.place(x=650, y=10925, width=150, height=33)

line_270_frame = tk.Label(maincanvas)
line_270_frame["bg"] = "#adafae"
line_270_frame["text"] = ""
line_270_frame["relief"] = "sunken"
line_270_frame.place(x=10, y=10960, width=1060, height=40)

line_270_index = tk.Label(maincanvas)
line_270_index["bg"] = "#adafae"
line_270_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_270_index["font"] = ft
line_270_index["justify"] = "left"
line_270_index["anchor"] = "w"
line_270_index.place(x=20, y=10965, width=150, height=33)

line_270_name = tk.Label(maincanvas)
line_270_name["bg"] = "#adafae"
line_270_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_270_name["font"] = ft
line_270_name["justify"] = "left"
line_270_name["anchor"] = "w"
line_270_name.place(x=250, y=10965, width=500, height=33)

line_270_duration = tk.Label(maincanvas)
line_270_duration["bg"] = "#adafae"
line_270_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_270_duration["font"] = ft
line_270_duration["justify"] = "right"
line_270_duration["anchor"] = "e"
line_270_duration.place(x=910, y=10965, width=150, height=33)

line_270_live = tk.Label(maincanvas)
line_270_live["bg"] = "#adafae"
line_270_live["fg"] = "red"
line_270_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_270_live["font"] = ftl
line_270_live["justify"] = "left"
line_270_live["anchor"] = "w"
line_270_live["relief"] = "flat"
line_270_live.place(x=8000, y=10965, width=70, height=33)

line_270_disabled = tk.Label(maincanvas)
line_270_disabled["bg"] = "#adafae"
line_270_disabled["fg"] = "red"
line_270_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_270_disabled["font"] = ftl
line_270_disabled["justify"] = "left"
line_270_disabled["anchor"] = "w"
line_270_disabled["relief"] = "flat"
line_270_disabled.place(x=650, y=10965, width=150, height=33)

line_271_frame = tk.Label(maincanvas)
line_271_frame["bg"] = "#adafae"
line_271_frame["text"] = ""
line_271_frame["relief"] = "sunken"
line_271_frame.place(x=10, y=11000, width=1060, height=40)

line_271_index = tk.Label(maincanvas)
line_271_index["bg"] = "#adafae"
line_271_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_271_index["font"] = ft
line_271_index["justify"] = "left"
line_271_index["anchor"] = "w"
line_271_index.place(x=20, y=11005, width=150, height=33)

line_271_name = tk.Label(maincanvas)
line_271_name["bg"] = "#adafae"
line_271_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_271_name["font"] = ft
line_271_name["justify"] = "left"
line_271_name["anchor"] = "w"
line_271_name.place(x=250, y=11005, width=500, height=33)

line_271_duration = tk.Label(maincanvas)
line_271_duration["bg"] = "#adafae"
line_271_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_271_duration["font"] = ft
line_271_duration["justify"] = "right"
line_271_duration["anchor"] = "e"
line_271_duration.place(x=910, y=11005, width=150, height=33)

line_271_live = tk.Label(maincanvas)
line_271_live["bg"] = "#adafae"
line_271_live["fg"] = "red"
line_271_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_271_live["font"] = ftl
line_271_live["justify"] = "left"
line_271_live["anchor"] = "w"
line_271_live["relief"] = "flat"
line_271_live.place(x=8000, y=11005, width=70, height=33)

line_271_disabled = tk.Label(maincanvas)
line_271_disabled["bg"] = "#adafae"
line_271_disabled["fg"] = "red"
line_271_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_271_disabled["font"] = ftl
line_271_disabled["justify"] = "left"
line_271_disabled["anchor"] = "w"
line_271_disabled["relief"] = "flat"
line_271_disabled.place(x=650, y=11005, width=150, height=33)

line_272_frame = tk.Label(maincanvas)
line_272_frame["bg"] = "#adafae"
line_272_frame["text"] = ""
line_272_frame["relief"] = "sunken"
line_272_frame.place(x=10, y=11040, width=1060, height=40)

line_272_index = tk.Label(maincanvas)
line_272_index["bg"] = "#adafae"
line_272_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_272_index["font"] = ft
line_272_index["justify"] = "left"
line_272_index["anchor"] = "w"
line_272_index.place(x=20, y=11045, width=150, height=33)

line_272_name = tk.Label(maincanvas)
line_272_name["bg"] = "#adafae"
line_272_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_272_name["font"] = ft
line_272_name["justify"] = "left"
line_272_name["anchor"] = "w"
line_272_name.place(x=250, y=11045, width=500, height=33)

line_272_duration = tk.Label(maincanvas)
line_272_duration["bg"] = "#adafae"
line_272_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_272_duration["font"] = ft
line_272_duration["justify"] = "right"
line_272_duration["anchor"] = "e"
line_272_duration.place(x=910, y=11045, width=150, height=33)

line_272_live = tk.Label(maincanvas)
line_272_live["bg"] = "#adafae"
line_272_live["fg"] = "red"
line_272_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_272_live["font"] = ftl
line_272_live["justify"] = "left"
line_272_live["anchor"] = "w"
line_272_live["relief"] = "flat"
line_272_live.place(x=8000, y=11045, width=70, height=33)

line_272_disabled = tk.Label(maincanvas)
line_272_disabled["bg"] = "#adafae"
line_272_disabled["fg"] = "red"
line_272_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_272_disabled["font"] = ftl
line_272_disabled["justify"] = "left"
line_272_disabled["anchor"] = "w"
line_272_disabled["relief"] = "flat"
line_272_disabled.place(x=650, y=11045, width=150, height=33)

line_273_frame = tk.Label(maincanvas)
line_273_frame["bg"] = "#adafae"
line_273_frame["text"] = ""
line_273_frame["relief"] = "sunken"
line_273_frame.place(x=10, y=11080, width=1060, height=40)

line_273_index = tk.Label(maincanvas)
line_273_index["bg"] = "#adafae"
line_273_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_273_index["font"] = ft
line_273_index["justify"] = "left"
line_273_index["anchor"] = "w"
line_273_index.place(x=20, y=11085, width=150, height=33)

line_273_name = tk.Label(maincanvas)
line_273_name["bg"] = "#adafae"
line_273_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_273_name["font"] = ft
line_273_name["justify"] = "left"
line_273_name["anchor"] = "w"
line_273_name.place(x=250, y=11085, width=500, height=33)

line_273_duration = tk.Label(maincanvas)
line_273_duration["bg"] = "#adafae"
line_273_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_273_duration["font"] = ft
line_273_duration["justify"] = "right"
line_273_duration["anchor"] = "e"
line_273_duration.place(x=910, y=11085, width=150, height=33)

line_273_live = tk.Label(maincanvas)
line_273_live["bg"] = "#adafae"
line_273_live["fg"] = "red"
line_273_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_273_live["font"] = ftl
line_273_live["justify"] = "left"
line_273_live["anchor"] = "w"
line_273_live["relief"] = "flat"
line_273_live.place(x=8000, y=11085, width=70, height=33)

line_273_disabled = tk.Label(maincanvas)
line_273_disabled["bg"] = "#adafae"
line_273_disabled["fg"] = "red"
line_273_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_273_disabled["font"] = ftl
line_273_disabled["justify"] = "left"
line_273_disabled["anchor"] = "w"
line_273_disabled["relief"] = "flat"
line_273_disabled.place(x=650, y=11085, width=150, height=33)

line_274_frame = tk.Label(maincanvas)
line_274_frame["bg"] = "#adafae"
line_274_frame["text"] = ""
line_274_frame["relief"] = "sunken"
line_274_frame.place(x=10, y=11120, width=1060, height=40)

line_274_index = tk.Label(maincanvas)
line_274_index["bg"] = "#adafae"
line_274_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_274_index["font"] = ft
line_274_index["justify"] = "left"
line_274_index["anchor"] = "w"
line_274_index.place(x=20, y=11125, width=150, height=33)

line_274_name = tk.Label(maincanvas)
line_274_name["bg"] = "#adafae"
line_274_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_274_name["font"] = ft
line_274_name["justify"] = "left"
line_274_name["anchor"] = "w"
line_274_name.place(x=250, y=11125, width=500, height=33)

line_274_duration = tk.Label(maincanvas)
line_274_duration["bg"] = "#adafae"
line_274_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_274_duration["font"] = ft
line_274_duration["justify"] = "right"
line_274_duration["anchor"] = "e"
line_274_duration.place(x=910, y=11125, width=150, height=33)

line_274_live = tk.Label(maincanvas)
line_274_live["bg"] = "#adafae"
line_274_live["fg"] = "red"
line_274_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_274_live["font"] = ftl
line_274_live["justify"] = "left"
line_274_live["anchor"] = "w"
line_274_live["relief"] = "flat"
line_274_live.place(x=8000, y=11125, width=70, height=33)

line_274_disabled = tk.Label(maincanvas)
line_274_disabled["bg"] = "#adafae"
line_274_disabled["fg"] = "red"
line_274_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_274_disabled["font"] = ftl
line_274_disabled["justify"] = "left"
line_274_disabled["anchor"] = "w"
line_274_disabled["relief"] = "flat"
line_274_disabled.place(x=650, y=11125, width=150, height=33)

line_275_frame = tk.Label(maincanvas)
line_275_frame["bg"] = "#adafae"
line_275_frame["text"] = ""
line_275_frame["relief"] = "sunken"
line_275_frame.place(x=10, y=11160, width=1060, height=40)

line_275_index = tk.Label(maincanvas)
line_275_index["bg"] = "#adafae"
line_275_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_275_index["font"] = ft
line_275_index["justify"] = "left"
line_275_index["anchor"] = "w"
line_275_index.place(x=20, y=11165, width=150, height=33)

line_275_name = tk.Label(maincanvas)
line_275_name["bg"] = "#adafae"
line_275_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_275_name["font"] = ft
line_275_name["justify"] = "left"
line_275_name["anchor"] = "w"
line_275_name.place(x=250, y=11165, width=500, height=33)

line_275_duration = tk.Label(maincanvas)
line_275_duration["bg"] = "#adafae"
line_275_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_275_duration["font"] = ft
line_275_duration["justify"] = "right"
line_275_duration["anchor"] = "e"
line_275_duration.place(x=910, y=11165, width=150, height=33)

line_275_live = tk.Label(maincanvas)
line_275_live["bg"] = "#adafae"
line_275_live["fg"] = "red"
line_275_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_275_live["font"] = ftl
line_275_live["justify"] = "left"
line_275_live["anchor"] = "w"
line_275_live["relief"] = "flat"
line_275_live.place(x=8000, y=11165, width=70, height=33)

line_275_disabled = tk.Label(maincanvas)
line_275_disabled["bg"] = "#adafae"
line_275_disabled["fg"] = "red"
line_275_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_275_disabled["font"] = ftl
line_275_disabled["justify"] = "left"
line_275_disabled["anchor"] = "w"
line_275_disabled["relief"] = "flat"
line_275_disabled.place(x=650, y=11165, width=150, height=33)

line_276_frame = tk.Label(maincanvas)
line_276_frame["bg"] = "#adafae"
line_276_frame["text"] = ""
line_276_frame["relief"] = "sunken"
line_276_frame.place(x=10, y=11200, width=1060, height=40)

line_276_index = tk.Label(maincanvas)
line_276_index["bg"] = "#adafae"
line_276_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_276_index["font"] = ft
line_276_index["justify"] = "left"
line_276_index["anchor"] = "w"
line_276_index.place(x=20, y=11205, width=150, height=33)

line_276_name = tk.Label(maincanvas)
line_276_name["bg"] = "#adafae"
line_276_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_276_name["font"] = ft
line_276_name["justify"] = "left"
line_276_name["anchor"] = "w"
line_276_name.place(x=250, y=11205, width=500, height=33)

line_276_duration = tk.Label(maincanvas)
line_276_duration["bg"] = "#adafae"
line_276_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_276_duration["font"] = ft
line_276_duration["justify"] = "right"
line_276_duration["anchor"] = "e"
line_276_duration.place(x=910, y=11205, width=150, height=33)

line_276_live = tk.Label(maincanvas)
line_276_live["bg"] = "#adafae"
line_276_live["fg"] = "red"
line_276_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_276_live["font"] = ftl
line_276_live["justify"] = "left"
line_276_live["anchor"] = "w"
line_276_live["relief"] = "flat"
line_276_live.place(x=8000, y=11205, width=70, height=33)

line_276_disabled = tk.Label(maincanvas)
line_276_disabled["bg"] = "#adafae"
line_276_disabled["fg"] = "red"
line_276_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_276_disabled["font"] = ftl
line_276_disabled["justify"] = "left"
line_276_disabled["anchor"] = "w"
line_276_disabled["relief"] = "flat"
line_276_disabled.place(x=650, y=11205, width=150, height=33)

line_277_frame = tk.Label(maincanvas)
line_277_frame["bg"] = "#adafae"
line_277_frame["text"] = ""
line_277_frame["relief"] = "sunken"
line_277_frame.place(x=10, y=11240, width=1060, height=40)

line_277_index = tk.Label(maincanvas)
line_277_index["bg"] = "#adafae"
line_277_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_277_index["font"] = ft
line_277_index["justify"] = "left"
line_277_index["anchor"] = "w"
line_277_index.place(x=20, y=11245, width=150, height=33)

line_277_name = tk.Label(maincanvas)
line_277_name["bg"] = "#adafae"
line_277_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_277_name["font"] = ft
line_277_name["justify"] = "left"
line_277_name["anchor"] = "w"
line_277_name.place(x=250, y=11245, width=500, height=33)

line_277_duration = tk.Label(maincanvas)
line_277_duration["bg"] = "#adafae"
line_277_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_277_duration["font"] = ft
line_277_duration["justify"] = "right"
line_277_duration["anchor"] = "e"
line_277_duration.place(x=910, y=11245, width=150, height=33)

line_277_live = tk.Label(maincanvas)
line_277_live["bg"] = "#adafae"
line_277_live["fg"] = "red"
line_277_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_277_live["font"] = ftl
line_277_live["justify"] = "left"
line_277_live["anchor"] = "w"
line_277_live["relief"] = "flat"
line_277_live.place(x=8000, y=11245, width=70, height=33)

line_277_disabled = tk.Label(maincanvas)
line_277_disabled["bg"] = "#adafae"
line_277_disabled["fg"] = "red"
line_277_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_277_disabled["font"] = ftl
line_277_disabled["justify"] = "left"
line_277_disabled["anchor"] = "w"
line_277_disabled["relief"] = "flat"
line_277_disabled.place(x=650, y=11245, width=150, height=33)

line_278_frame = tk.Label(maincanvas)
line_278_frame["bg"] = "#adafae"
line_278_frame["text"] = ""
line_278_frame["relief"] = "sunken"
line_278_frame.place(x=10, y=11280, width=1060, height=40)

line_278_index = tk.Label(maincanvas)
line_278_index["bg"] = "#adafae"
line_278_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_278_index["font"] = ft
line_278_index["justify"] = "left"
line_278_index["anchor"] = "w"
line_278_index.place(x=20, y=11285, width=150, height=33)

line_278_name = tk.Label(maincanvas)
line_278_name["bg"] = "#adafae"
line_278_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_278_name["font"] = ft
line_278_name["justify"] = "left"
line_278_name["anchor"] = "w"
line_278_name.place(x=250, y=11285, width=500, height=33)

line_278_duration = tk.Label(maincanvas)
line_278_duration["bg"] = "#adafae"
line_278_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_278_duration["font"] = ft
line_278_duration["justify"] = "right"
line_278_duration["anchor"] = "e"
line_278_duration.place(x=910, y=11285, width=150, height=33)

line_278_live = tk.Label(maincanvas)
line_278_live["bg"] = "#adafae"
line_278_live["fg"] = "red"
line_278_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_278_live["font"] = ftl
line_278_live["justify"] = "left"
line_278_live["anchor"] = "w"
line_278_live["relief"] = "flat"
line_278_live.place(x=8000, y=11285, width=70, height=33)

line_278_disabled = tk.Label(maincanvas)
line_278_disabled["bg"] = "#adafae"
line_278_disabled["fg"] = "red"
line_278_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_278_disabled["font"] = ftl
line_278_disabled["justify"] = "left"
line_278_disabled["anchor"] = "w"
line_278_disabled["relief"] = "flat"
line_278_disabled.place(x=650, y=11285, width=150, height=33)

line_279_frame = tk.Label(maincanvas)
line_279_frame["bg"] = "#adafae"
line_279_frame["text"] = ""
line_279_frame["relief"] = "sunken"
line_279_frame.place(x=10, y=11320, width=1060, height=40)

line_279_index = tk.Label(maincanvas)
line_279_index["bg"] = "#adafae"
line_279_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_279_index["font"] = ft
line_279_index["justify"] = "left"
line_279_index["anchor"] = "w"
line_279_index.place(x=20, y=11325, width=150, height=33)

line_279_name = tk.Label(maincanvas)
line_279_name["bg"] = "#adafae"
line_279_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_279_name["font"] = ft
line_279_name["justify"] = "left"
line_279_name["anchor"] = "w"
line_279_name.place(x=250, y=11325, width=500, height=33)

line_279_duration = tk.Label(maincanvas)
line_279_duration["bg"] = "#adafae"
line_279_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_279_duration["font"] = ft
line_279_duration["justify"] = "right"
line_279_duration["anchor"] = "e"
line_279_duration.place(x=910, y=11325, width=150, height=33)

line_279_live = tk.Label(maincanvas)
line_279_live["bg"] = "#adafae"
line_279_live["fg"] = "red"
line_279_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_279_live["font"] = ftl
line_279_live["justify"] = "left"
line_279_live["anchor"] = "w"
line_279_live["relief"] = "flat"
line_279_live.place(x=8000, y=11325, width=70, height=33)

line_279_disabled = tk.Label(maincanvas)
line_279_disabled["bg"] = "#adafae"
line_279_disabled["fg"] = "red"
line_279_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_279_disabled["font"] = ftl
line_279_disabled["justify"] = "left"
line_279_disabled["anchor"] = "w"
line_279_disabled["relief"] = "flat"
line_279_disabled.place(x=650, y=11325, width=150, height=33)

line_280_frame = tk.Label(maincanvas)
line_280_frame["bg"] = "#adafae"
line_280_frame["text"] = ""
line_280_frame["relief"] = "sunken"
line_280_frame.place(x=10, y=11360, width=1060, height=40)

line_280_index = tk.Label(maincanvas)
line_280_index["bg"] = "#adafae"
line_280_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_280_index["font"] = ft
line_280_index["justify"] = "left"
line_280_index["anchor"] = "w"
line_280_index.place(x=20, y=11365, width=150, height=33)

line_280_name = tk.Label(maincanvas)
line_280_name["bg"] = "#adafae"
line_280_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_280_name["font"] = ft
line_280_name["justify"] = "left"
line_280_name["anchor"] = "w"
line_280_name.place(x=250, y=11365, width=500, height=33)

line_280_duration = tk.Label(maincanvas)
line_280_duration["bg"] = "#adafae"
line_280_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_280_duration["font"] = ft
line_280_duration["justify"] = "right"
line_280_duration["anchor"] = "e"
line_280_duration.place(x=910, y=11365, width=150, height=33)

line_280_live = tk.Label(maincanvas)
line_280_live["bg"] = "#adafae"
line_280_live["fg"] = "red"
line_280_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_280_live["font"] = ftl
line_280_live["justify"] = "left"
line_280_live["anchor"] = "w"
line_280_live["relief"] = "flat"
line_280_live.place(x=8000, y=11365, width=70, height=33)

line_280_disabled = tk.Label(maincanvas)
line_280_disabled["bg"] = "#adafae"
line_280_disabled["fg"] = "red"
line_280_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_280_disabled["font"] = ftl
line_280_disabled["justify"] = "left"
line_280_disabled["anchor"] = "w"
line_280_disabled["relief"] = "flat"
line_280_disabled.place(x=650, y=11365, width=150, height=33)

line_281_frame = tk.Label(maincanvas)
line_281_frame["bg"] = "#adafae"
line_281_frame["text"] = ""
line_281_frame["relief"] = "sunken"
line_281_frame.place(x=10, y=11400, width=1060, height=40)

line_281_index = tk.Label(maincanvas)
line_281_index["bg"] = "#adafae"
line_281_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_281_index["font"] = ft
line_281_index["justify"] = "left"
line_281_index["anchor"] = "w"
line_281_index.place(x=20, y=11405, width=150, height=33)

line_281_name = tk.Label(maincanvas)
line_281_name["bg"] = "#adafae"
line_281_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_281_name["font"] = ft
line_281_name["justify"] = "left"
line_281_name["anchor"] = "w"
line_281_name.place(x=250, y=11405, width=500, height=33)

line_281_duration = tk.Label(maincanvas)
line_281_duration["bg"] = "#adafae"
line_281_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_281_duration["font"] = ft
line_281_duration["justify"] = "right"
line_281_duration["anchor"] = "e"
line_281_duration.place(x=910, y=11405, width=150, height=33)

line_281_live = tk.Label(maincanvas)
line_281_live["bg"] = "#adafae"
line_281_live["fg"] = "red"
line_281_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_281_live["font"] = ftl
line_281_live["justify"] = "left"
line_281_live["anchor"] = "w"
line_281_live["relief"] = "flat"
line_281_live.place(x=8000, y=11405, width=70, height=33)

line_281_disabled = tk.Label(maincanvas)
line_281_disabled["bg"] = "#adafae"
line_281_disabled["fg"] = "red"
line_281_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_281_disabled["font"] = ftl
line_281_disabled["justify"] = "left"
line_281_disabled["anchor"] = "w"
line_281_disabled["relief"] = "flat"
line_281_disabled.place(x=650, y=11405, width=150, height=33)

line_282_frame = tk.Label(maincanvas)
line_282_frame["bg"] = "#adafae"
line_282_frame["text"] = ""
line_282_frame["relief"] = "sunken"
line_282_frame.place(x=10, y=11440, width=1060, height=40)

line_282_index = tk.Label(maincanvas)
line_282_index["bg"] = "#adafae"
line_282_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_282_index["font"] = ft
line_282_index["justify"] = "left"
line_282_index["anchor"] = "w"
line_282_index.place(x=20, y=11445, width=150, height=33)

line_282_name = tk.Label(maincanvas)
line_282_name["bg"] = "#adafae"
line_282_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_282_name["font"] = ft
line_282_name["justify"] = "left"
line_282_name["anchor"] = "w"
line_282_name.place(x=250, y=11445, width=500, height=33)

line_282_duration = tk.Label(maincanvas)
line_282_duration["bg"] = "#adafae"
line_282_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_282_duration["font"] = ft
line_282_duration["justify"] = "right"
line_282_duration["anchor"] = "e"
line_282_duration.place(x=910, y=11445, width=150, height=33)

line_282_live = tk.Label(maincanvas)
line_282_live["bg"] = "#adafae"
line_282_live["fg"] = "red"
line_282_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_282_live["font"] = ftl
line_282_live["justify"] = "left"
line_282_live["anchor"] = "w"
line_282_live["relief"] = "flat"
line_282_live.place(x=8000, y=11445, width=70, height=33)

line_282_disabled = tk.Label(maincanvas)
line_282_disabled["bg"] = "#adafae"
line_282_disabled["fg"] = "red"
line_282_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_282_disabled["font"] = ftl
line_282_disabled["justify"] = "left"
line_282_disabled["anchor"] = "w"
line_282_disabled["relief"] = "flat"
line_282_disabled.place(x=650, y=11445, width=150, height=33)

line_283_frame = tk.Label(maincanvas)
line_283_frame["bg"] = "#adafae"
line_283_frame["text"] = ""
line_283_frame["relief"] = "sunken"
line_283_frame.place(x=10, y=11480, width=1060, height=40)

line_283_index = tk.Label(maincanvas)
line_283_index["bg"] = "#adafae"
line_283_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_283_index["font"] = ft
line_283_index["justify"] = "left"
line_283_index["anchor"] = "w"
line_283_index.place(x=20, y=11485, width=150, height=33)

line_283_name = tk.Label(maincanvas)
line_283_name["bg"] = "#adafae"
line_283_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_283_name["font"] = ft
line_283_name["justify"] = "left"
line_283_name["anchor"] = "w"
line_283_name.place(x=250, y=11485, width=500, height=33)

line_283_duration = tk.Label(maincanvas)
line_283_duration["bg"] = "#adafae"
line_283_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_283_duration["font"] = ft
line_283_duration["justify"] = "right"
line_283_duration["anchor"] = "e"
line_283_duration.place(x=910, y=11485, width=150, height=33)

line_283_live = tk.Label(maincanvas)
line_283_live["bg"] = "#adafae"
line_283_live["fg"] = "red"
line_283_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_283_live["font"] = ftl
line_283_live["justify"] = "left"
line_283_live["anchor"] = "w"
line_283_live["relief"] = "flat"
line_283_live.place(x=8000, y=11485, width=70, height=33)

line_283_disabled = tk.Label(maincanvas)
line_283_disabled["bg"] = "#adafae"
line_283_disabled["fg"] = "red"
line_283_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_283_disabled["font"] = ftl
line_283_disabled["justify"] = "left"
line_283_disabled["anchor"] = "w"
line_283_disabled["relief"] = "flat"
line_283_disabled.place(x=650, y=11485, width=150, height=33)

line_284_frame = tk.Label(maincanvas)
line_284_frame["bg"] = "#adafae"
line_284_frame["text"] = ""
line_284_frame["relief"] = "sunken"
line_284_frame.place(x=10, y=11520, width=1060, height=40)

line_284_index = tk.Label(maincanvas)
line_284_index["bg"] = "#adafae"
line_284_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_284_index["font"] = ft
line_284_index["justify"] = "left"
line_284_index["anchor"] = "w"
line_284_index.place(x=20, y=11525, width=150, height=33)

line_284_name = tk.Label(maincanvas)
line_284_name["bg"] = "#adafae"
line_284_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_284_name["font"] = ft
line_284_name["justify"] = "left"
line_284_name["anchor"] = "w"
line_284_name.place(x=250, y=11525, width=500, height=33)

line_284_duration = tk.Label(maincanvas)
line_284_duration["bg"] = "#adafae"
line_284_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_284_duration["font"] = ft
line_284_duration["justify"] = "right"
line_284_duration["anchor"] = "e"
line_284_duration.place(x=910, y=11525, width=150, height=33)

line_284_live = tk.Label(maincanvas)
line_284_live["bg"] = "#adafae"
line_284_live["fg"] = "red"
line_284_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_284_live["font"] = ftl
line_284_live["justify"] = "left"
line_284_live["anchor"] = "w"
line_284_live["relief"] = "flat"
line_284_live.place(x=8000, y=11525, width=70, height=33)

line_284_disabled = tk.Label(maincanvas)
line_284_disabled["bg"] = "#adafae"
line_284_disabled["fg"] = "red"
line_284_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_284_disabled["font"] = ftl
line_284_disabled["justify"] = "left"
line_284_disabled["anchor"] = "w"
line_284_disabled["relief"] = "flat"
line_284_disabled.place(x=650, y=11525, width=150, height=33)

line_285_frame = tk.Label(maincanvas)
line_285_frame["bg"] = "#adafae"
line_285_frame["text"] = ""
line_285_frame["relief"] = "sunken"
line_285_frame.place(x=10, y=11560, width=1060, height=40)

line_285_index = tk.Label(maincanvas)
line_285_index["bg"] = "#adafae"
line_285_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_285_index["font"] = ft
line_285_index["justify"] = "left"
line_285_index["anchor"] = "w"
line_285_index.place(x=20, y=11565, width=150, height=33)

line_285_name = tk.Label(maincanvas)
line_285_name["bg"] = "#adafae"
line_285_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_285_name["font"] = ft
line_285_name["justify"] = "left"
line_285_name["anchor"] = "w"
line_285_name.place(x=250, y=11565, width=500, height=33)

line_285_duration = tk.Label(maincanvas)
line_285_duration["bg"] = "#adafae"
line_285_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_285_duration["font"] = ft
line_285_duration["justify"] = "right"
line_285_duration["anchor"] = "e"
line_285_duration.place(x=910, y=11565, width=150, height=33)

line_285_live = tk.Label(maincanvas)
line_285_live["bg"] = "#adafae"
line_285_live["fg"] = "red"
line_285_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_285_live["font"] = ftl
line_285_live["justify"] = "left"
line_285_live["anchor"] = "w"
line_285_live["relief"] = "flat"
line_285_live.place(x=8000, y=11565, width=70, height=33)

line_285_disabled = tk.Label(maincanvas)
line_285_disabled["bg"] = "#adafae"
line_285_disabled["fg"] = "red"
line_285_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_285_disabled["font"] = ftl
line_285_disabled["justify"] = "left"
line_285_disabled["anchor"] = "w"
line_285_disabled["relief"] = "flat"
line_285_disabled.place(x=650, y=11565, width=150, height=33)

line_286_frame = tk.Label(maincanvas)
line_286_frame["bg"] = "#adafae"
line_286_frame["text"] = ""
line_286_frame["relief"] = "sunken"
line_286_frame.place(x=10, y=11600, width=1060, height=40)

line_286_index = tk.Label(maincanvas)
line_286_index["bg"] = "#adafae"
line_286_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_286_index["font"] = ft
line_286_index["justify"] = "left"
line_286_index["anchor"] = "w"
line_286_index.place(x=20, y=11605, width=150, height=33)

line_286_name = tk.Label(maincanvas)
line_286_name["bg"] = "#adafae"
line_286_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_286_name["font"] = ft
line_286_name["justify"] = "left"
line_286_name["anchor"] = "w"
line_286_name.place(x=250, y=11605, width=500, height=33)

line_286_duration = tk.Label(maincanvas)
line_286_duration["bg"] = "#adafae"
line_286_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_286_duration["font"] = ft
line_286_duration["justify"] = "right"
line_286_duration["anchor"] = "e"
line_286_duration.place(x=910, y=11605, width=150, height=33)

line_286_live = tk.Label(maincanvas)
line_286_live["bg"] = "#adafae"
line_286_live["fg"] = "red"
line_286_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_286_live["font"] = ftl
line_286_live["justify"] = "left"
line_286_live["anchor"] = "w"
line_286_live["relief"] = "flat"
line_286_live.place(x=8000, y=11605, width=70, height=33)

line_286_disabled = tk.Label(maincanvas)
line_286_disabled["bg"] = "#adafae"
line_286_disabled["fg"] = "red"
line_286_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_286_disabled["font"] = ftl
line_286_disabled["justify"] = "left"
line_286_disabled["anchor"] = "w"
line_286_disabled["relief"] = "flat"
line_286_disabled.place(x=650, y=11605, width=150, height=33)

line_287_frame = tk.Label(maincanvas)
line_287_frame["bg"] = "#adafae"
line_287_frame["text"] = ""
line_287_frame["relief"] = "sunken"
line_287_frame.place(x=10, y=11640, width=1060, height=40)

line_287_index = tk.Label(maincanvas)
line_287_index["bg"] = "#adafae"
line_287_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_287_index["font"] = ft
line_287_index["justify"] = "left"
line_287_index["anchor"] = "w"
line_287_index.place(x=20, y=11645, width=150, height=33)

line_287_name = tk.Label(maincanvas)
line_287_name["bg"] = "#adafae"
line_287_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_287_name["font"] = ft
line_287_name["justify"] = "left"
line_287_name["anchor"] = "w"
line_287_name.place(x=250, y=11645, width=500, height=33)

line_287_duration = tk.Label(maincanvas)
line_287_duration["bg"] = "#adafae"
line_287_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_287_duration["font"] = ft
line_287_duration["justify"] = "right"
line_287_duration["anchor"] = "e"
line_287_duration.place(x=910, y=11645, width=150, height=33)

line_287_live = tk.Label(maincanvas)
line_287_live["bg"] = "#adafae"
line_287_live["fg"] = "red"
line_287_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_287_live["font"] = ftl
line_287_live["justify"] = "left"
line_287_live["anchor"] = "w"
line_287_live["relief"] = "flat"
line_287_live.place(x=8000, y=11645, width=70, height=33)

line_287_disabled = tk.Label(maincanvas)
line_287_disabled["bg"] = "#adafae"
line_287_disabled["fg"] = "red"
line_287_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_287_disabled["font"] = ftl
line_287_disabled["justify"] = "left"
line_287_disabled["anchor"] = "w"
line_287_disabled["relief"] = "flat"
line_287_disabled.place(x=650, y=11645, width=150, height=33)

line_288_frame = tk.Label(maincanvas)
line_288_frame["bg"] = "#adafae"
line_288_frame["text"] = ""
line_288_frame["relief"] = "sunken"
line_288_frame.place(x=10, y=11680, width=1060, height=40)

line_288_index = tk.Label(maincanvas)
line_288_index["bg"] = "#adafae"
line_288_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_288_index["font"] = ft
line_288_index["justify"] = "left"
line_288_index["anchor"] = "w"
line_288_index.place(x=20, y=11685, width=150, height=33)

line_288_name = tk.Label(maincanvas)
line_288_name["bg"] = "#adafae"
line_288_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_288_name["font"] = ft
line_288_name["justify"] = "left"
line_288_name["anchor"] = "w"
line_288_name.place(x=250, y=11685, width=500, height=33)

line_288_duration = tk.Label(maincanvas)
line_288_duration["bg"] = "#adafae"
line_288_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_288_duration["font"] = ft
line_288_duration["justify"] = "right"
line_288_duration["anchor"] = "e"
line_288_duration.place(x=910, y=11685, width=150, height=33)

line_288_live = tk.Label(maincanvas)
line_288_live["bg"] = "#adafae"
line_288_live["fg"] = "red"
line_288_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_288_live["font"] = ftl
line_288_live["justify"] = "left"
line_288_live["anchor"] = "w"
line_288_live["relief"] = "flat"
line_288_live.place(x=8000, y=11685, width=70, height=33)

line_288_disabled = tk.Label(maincanvas)
line_288_disabled["bg"] = "#adafae"
line_288_disabled["fg"] = "red"
line_288_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_288_disabled["font"] = ftl
line_288_disabled["justify"] = "left"
line_288_disabled["anchor"] = "w"
line_288_disabled["relief"] = "flat"
line_288_disabled.place(x=650, y=11685, width=150, height=33)

line_289_frame = tk.Label(maincanvas)
line_289_frame["bg"] = "#adafae"
line_289_frame["text"] = ""
line_289_frame["relief"] = "sunken"
line_289_frame.place(x=10, y=11720, width=1060, height=40)

line_289_index = tk.Label(maincanvas)
line_289_index["bg"] = "#adafae"
line_289_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_289_index["font"] = ft
line_289_index["justify"] = "left"
line_289_index["anchor"] = "w"
line_289_index.place(x=20, y=11725, width=150, height=33)

line_289_name = tk.Label(maincanvas)
line_289_name["bg"] = "#adafae"
line_289_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_289_name["font"] = ft
line_289_name["justify"] = "left"
line_289_name["anchor"] = "w"
line_289_name.place(x=250, y=11725, width=500, height=33)

line_289_duration = tk.Label(maincanvas)
line_289_duration["bg"] = "#adafae"
line_289_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_289_duration["font"] = ft
line_289_duration["justify"] = "right"
line_289_duration["anchor"] = "e"
line_289_duration.place(x=910, y=11725, width=150, height=33)

line_289_live = tk.Label(maincanvas)
line_289_live["bg"] = "#adafae"
line_289_live["fg"] = "red"
line_289_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_289_live["font"] = ftl
line_289_live["justify"] = "left"
line_289_live["anchor"] = "w"
line_289_live["relief"] = "flat"
line_289_live.place(x=8000, y=11725, width=70, height=33)

line_289_disabled = tk.Label(maincanvas)
line_289_disabled["bg"] = "#adafae"
line_289_disabled["fg"] = "red"
line_289_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_289_disabled["font"] = ftl
line_289_disabled["justify"] = "left"
line_289_disabled["anchor"] = "w"
line_289_disabled["relief"] = "flat"
line_289_disabled.place(x=650, y=11725, width=150, height=33)

line_290_frame = tk.Label(maincanvas)
line_290_frame["bg"] = "#adafae"
line_290_frame["text"] = ""
line_290_frame["relief"] = "sunken"
line_290_frame.place(x=10, y=11760, width=1060, height=40)

line_290_index = tk.Label(maincanvas)
line_290_index["bg"] = "#adafae"
line_290_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_290_index["font"] = ft
line_290_index["justify"] = "left"
line_290_index["anchor"] = "w"
line_290_index.place(x=20, y=11765, width=150, height=33)

line_290_name = tk.Label(maincanvas)
line_290_name["bg"] = "#adafae"
line_290_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_290_name["font"] = ft
line_290_name["justify"] = "left"
line_290_name["anchor"] = "w"
line_290_name.place(x=250, y=11765, width=500, height=33)

line_290_duration = tk.Label(maincanvas)
line_290_duration["bg"] = "#adafae"
line_290_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_290_duration["font"] = ft
line_290_duration["justify"] = "right"
line_290_duration["anchor"] = "e"
line_290_duration.place(x=910, y=11765, width=150, height=33)

line_290_live = tk.Label(maincanvas)
line_290_live["bg"] = "#adafae"
line_290_live["fg"] = "red"
line_290_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_290_live["font"] = ftl
line_290_live["justify"] = "left"
line_290_live["anchor"] = "w"
line_290_live["relief"] = "flat"
line_290_live.place(x=8000, y=11765, width=70, height=33)

line_290_disabled = tk.Label(maincanvas)
line_290_disabled["bg"] = "#adafae"
line_290_disabled["fg"] = "red"
line_290_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_290_disabled["font"] = ftl
line_290_disabled["justify"] = "left"
line_290_disabled["anchor"] = "w"
line_290_disabled["relief"] = "flat"
line_290_disabled.place(x=650, y=11765, width=150, height=33)

line_291_frame = tk.Label(maincanvas)
line_291_frame["bg"] = "#adafae"
line_291_frame["text"] = ""
line_291_frame["relief"] = "sunken"
line_291_frame.place(x=10, y=11800, width=1060, height=40)

line_291_index = tk.Label(maincanvas)
line_291_index["bg"] = "#adafae"
line_291_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_291_index["font"] = ft
line_291_index["justify"] = "left"
line_291_index["anchor"] = "w"
line_291_index.place(x=20, y=11805, width=150, height=33)

line_291_name = tk.Label(maincanvas)
line_291_name["bg"] = "#adafae"
line_291_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_291_name["font"] = ft
line_291_name["justify"] = "left"
line_291_name["anchor"] = "w"
line_291_name.place(x=250, y=11805, width=500, height=33)

line_291_duration = tk.Label(maincanvas)
line_291_duration["bg"] = "#adafae"
line_291_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_291_duration["font"] = ft
line_291_duration["justify"] = "right"
line_291_duration["anchor"] = "e"
line_291_duration.place(x=910, y=11805, width=150, height=33)

line_291_live = tk.Label(maincanvas)
line_291_live["bg"] = "#adafae"
line_291_live["fg"] = "red"
line_291_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_291_live["font"] = ftl
line_291_live["justify"] = "left"
line_291_live["anchor"] = "w"
line_291_live["relief"] = "flat"
line_291_live.place(x=8000, y=11805, width=70, height=33)

line_291_disabled = tk.Label(maincanvas)
line_291_disabled["bg"] = "#adafae"
line_291_disabled["fg"] = "red"
line_291_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_291_disabled["font"] = ftl
line_291_disabled["justify"] = "left"
line_291_disabled["anchor"] = "w"
line_291_disabled["relief"] = "flat"
line_291_disabled.place(x=650, y=11805, width=150, height=33)

line_292_frame = tk.Label(maincanvas)
line_292_frame["bg"] = "#adafae"
line_292_frame["text"] = ""
line_292_frame["relief"] = "sunken"
line_292_frame.place(x=10, y=11840, width=1060, height=40)

line_292_index = tk.Label(maincanvas)
line_292_index["bg"] = "#adafae"
line_292_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_292_index["font"] = ft
line_292_index["justify"] = "left"
line_292_index["anchor"] = "w"
line_292_index.place(x=20, y=11845, width=150, height=33)

line_292_name = tk.Label(maincanvas)
line_292_name["bg"] = "#adafae"
line_292_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_292_name["font"] = ft
line_292_name["justify"] = "left"
line_292_name["anchor"] = "w"
line_292_name.place(x=250, y=11845, width=500, height=33)

line_292_duration = tk.Label(maincanvas)
line_292_duration["bg"] = "#adafae"
line_292_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_292_duration["font"] = ft
line_292_duration["justify"] = "right"
line_292_duration["anchor"] = "e"
line_292_duration.place(x=910, y=11845, width=150, height=33)

line_292_live = tk.Label(maincanvas)
line_292_live["bg"] = "#adafae"
line_292_live["fg"] = "red"
line_292_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_292_live["font"] = ftl
line_292_live["justify"] = "left"
line_292_live["anchor"] = "w"
line_292_live["relief"] = "flat"
line_292_live.place(x=8000, y=11845, width=70, height=33)

line_292_disabled = tk.Label(maincanvas)
line_292_disabled["bg"] = "#adafae"
line_292_disabled["fg"] = "red"
line_292_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_292_disabled["font"] = ftl
line_292_disabled["justify"] = "left"
line_292_disabled["anchor"] = "w"
line_292_disabled["relief"] = "flat"
line_292_disabled.place(x=650, y=11845, width=150, height=33)

line_293_frame = tk.Label(maincanvas)
line_293_frame["bg"] = "#adafae"
line_293_frame["text"] = ""
line_293_frame["relief"] = "sunken"
line_293_frame.place(x=10, y=11880, width=1060, height=40)

line_293_index = tk.Label(maincanvas)
line_293_index["bg"] = "#adafae"
line_293_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_293_index["font"] = ft
line_293_index["justify"] = "left"
line_293_index["anchor"] = "w"
line_293_index.place(x=20, y=11885, width=150, height=33)

line_293_name = tk.Label(maincanvas)
line_293_name["bg"] = "#adafae"
line_293_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_293_name["font"] = ft
line_293_name["justify"] = "left"
line_293_name["anchor"] = "w"
line_293_name.place(x=250, y=11885, width=500, height=33)

line_293_duration = tk.Label(maincanvas)
line_293_duration["bg"] = "#adafae"
line_293_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_293_duration["font"] = ft
line_293_duration["justify"] = "right"
line_293_duration["anchor"] = "e"
line_293_duration.place(x=910, y=11885, width=150, height=33)

line_293_live = tk.Label(maincanvas)
line_293_live["bg"] = "#adafae"
line_293_live["fg"] = "red"
line_293_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_293_live["font"] = ftl
line_293_live["justify"] = "left"
line_293_live["anchor"] = "w"
line_293_live["relief"] = "flat"
line_293_live.place(x=8000, y=11885, width=70, height=33)

line_293_disabled = tk.Label(maincanvas)
line_293_disabled["bg"] = "#adafae"
line_293_disabled["fg"] = "red"
line_293_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_293_disabled["font"] = ftl
line_293_disabled["justify"] = "left"
line_293_disabled["anchor"] = "w"
line_293_disabled["relief"] = "flat"
line_293_disabled.place(x=650, y=11885, width=150, height=33)

line_294_frame = tk.Label(maincanvas)
line_294_frame["bg"] = "#adafae"
line_294_frame["text"] = ""
line_294_frame["relief"] = "sunken"
line_294_frame.place(x=10, y=11920, width=1060, height=40)

line_294_index = tk.Label(maincanvas)
line_294_index["bg"] = "#adafae"
line_294_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_294_index["font"] = ft
line_294_index["justify"] = "left"
line_294_index["anchor"] = "w"
line_294_index.place(x=20, y=11925, width=150, height=33)

line_294_name = tk.Label(maincanvas)
line_294_name["bg"] = "#adafae"
line_294_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_294_name["font"] = ft
line_294_name["justify"] = "left"
line_294_name["anchor"] = "w"
line_294_name.place(x=250, y=11925, width=500, height=33)

line_294_duration = tk.Label(maincanvas)
line_294_duration["bg"] = "#adafae"
line_294_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_294_duration["font"] = ft
line_294_duration["justify"] = "right"
line_294_duration["anchor"] = "e"
line_294_duration.place(x=910, y=11925, width=150, height=33)

line_294_live = tk.Label(maincanvas)
line_294_live["bg"] = "#adafae"
line_294_live["fg"] = "red"
line_294_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_294_live["font"] = ftl
line_294_live["justify"] = "left"
line_294_live["anchor"] = "w"
line_294_live["relief"] = "flat"
line_294_live.place(x=8000, y=11925, width=70, height=33)

line_294_disabled = tk.Label(maincanvas)
line_294_disabled["bg"] = "#adafae"
line_294_disabled["fg"] = "red"
line_294_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_294_disabled["font"] = ftl
line_294_disabled["justify"] = "left"
line_294_disabled["anchor"] = "w"
line_294_disabled["relief"] = "flat"
line_294_disabled.place(x=650, y=11925, width=150, height=33)

line_295_frame = tk.Label(maincanvas)
line_295_frame["bg"] = "#adafae"
line_295_frame["text"] = ""
line_295_frame["relief"] = "sunken"
line_295_frame.place(x=10, y=11960, width=1060, height=40)

line_295_index = tk.Label(maincanvas)
line_295_index["bg"] = "#adafae"
line_295_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_295_index["font"] = ft
line_295_index["justify"] = "left"
line_295_index["anchor"] = "w"
line_295_index.place(x=20, y=11965, width=150, height=33)

line_295_name = tk.Label(maincanvas)
line_295_name["bg"] = "#adafae"
line_295_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_295_name["font"] = ft
line_295_name["justify"] = "left"
line_295_name["anchor"] = "w"
line_295_name.place(x=250, y=11965, width=500, height=33)

line_295_duration = tk.Label(maincanvas)
line_295_duration["bg"] = "#adafae"
line_295_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_295_duration["font"] = ft
line_295_duration["justify"] = "right"
line_295_duration["anchor"] = "e"
line_295_duration.place(x=910, y=11965, width=150, height=33)

line_295_live = tk.Label(maincanvas)
line_295_live["bg"] = "#adafae"
line_295_live["fg"] = "red"
line_295_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_295_live["font"] = ftl
line_295_live["justify"] = "left"
line_295_live["anchor"] = "w"
line_295_live["relief"] = "flat"
line_295_live.place(x=8000, y=11965, width=70, height=33)

line_295_disabled = tk.Label(maincanvas)
line_295_disabled["bg"] = "#adafae"
line_295_disabled["fg"] = "red"
line_295_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_295_disabled["font"] = ftl
line_295_disabled["justify"] = "left"
line_295_disabled["anchor"] = "w"
line_295_disabled["relief"] = "flat"
line_295_disabled.place(x=650, y=11965, width=150, height=33)

line_296_frame = tk.Label(maincanvas)
line_296_frame["bg"] = "#adafae"
line_296_frame["text"] = ""
line_296_frame["relief"] = "sunken"
line_296_frame.place(x=10, y=12000, width=1060, height=40)

line_296_index = tk.Label(maincanvas)
line_296_index["bg"] = "#adafae"
line_296_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_296_index["font"] = ft
line_296_index["justify"] = "left"
line_296_index["anchor"] = "w"
line_296_index.place(x=20, y=12005, width=150, height=33)

line_296_name = tk.Label(maincanvas)
line_296_name["bg"] = "#adafae"
line_296_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_296_name["font"] = ft
line_296_name["justify"] = "left"
line_296_name["anchor"] = "w"
line_296_name.place(x=250, y=12005, width=500, height=33)

line_296_duration = tk.Label(maincanvas)
line_296_duration["bg"] = "#adafae"
line_296_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_296_duration["font"] = ft
line_296_duration["justify"] = "right"
line_296_duration["anchor"] = "e"
line_296_duration.place(x=910, y=12005, width=150, height=33)

line_296_live = tk.Label(maincanvas)
line_296_live["bg"] = "#adafae"
line_296_live["fg"] = "red"
line_296_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_296_live["font"] = ftl
line_296_live["justify"] = "left"
line_296_live["anchor"] = "w"
line_296_live["relief"] = "flat"
line_296_live.place(x=8000, y=12005, width=70, height=33)

line_296_disabled = tk.Label(maincanvas)
line_296_disabled["bg"] = "#adafae"
line_296_disabled["fg"] = "red"
line_296_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_296_disabled["font"] = ftl
line_296_disabled["justify"] = "left"
line_296_disabled["anchor"] = "w"
line_296_disabled["relief"] = "flat"
line_296_disabled.place(x=650, y=12005, width=150, height=33)

line_297_frame = tk.Label(maincanvas)
line_297_frame["bg"] = "#adafae"
line_297_frame["text"] = ""
line_297_frame["relief"] = "sunken"
line_297_frame.place(x=10, y=12040, width=1060, height=40)

line_297_index = tk.Label(maincanvas)
line_297_index["bg"] = "#adafae"
line_297_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_297_index["font"] = ft
line_297_index["justify"] = "left"
line_297_index["anchor"] = "w"
line_297_index.place(x=20, y=12045, width=150, height=33)

line_297_name = tk.Label(maincanvas)
line_297_name["bg"] = "#adafae"
line_297_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_297_name["font"] = ft
line_297_name["justify"] = "left"
line_297_name["anchor"] = "w"
line_297_name.place(x=250, y=12045, width=500, height=33)

line_297_duration = tk.Label(maincanvas)
line_297_duration["bg"] = "#adafae"
line_297_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_297_duration["font"] = ft
line_297_duration["justify"] = "right"
line_297_duration["anchor"] = "e"
line_297_duration.place(x=910, y=12045, width=150, height=33)

line_297_live = tk.Label(maincanvas)
line_297_live["bg"] = "#adafae"
line_297_live["fg"] = "red"
line_297_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_297_live["font"] = ftl
line_297_live["justify"] = "left"
line_297_live["anchor"] = "w"
line_297_live["relief"] = "flat"
line_297_live.place(x=8000, y=12045, width=70, height=33)

line_297_disabled = tk.Label(maincanvas)
line_297_disabled["bg"] = "#adafae"
line_297_disabled["fg"] = "red"
line_297_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_297_disabled["font"] = ftl
line_297_disabled["justify"] = "left"
line_297_disabled["anchor"] = "w"
line_297_disabled["relief"] = "flat"
line_297_disabled.place(x=650, y=12045, width=150, height=33)

line_298_frame = tk.Label(maincanvas)
line_298_frame["bg"] = "#adafae"
line_298_frame["text"] = ""
line_298_frame["relief"] = "sunken"
line_298_frame.place(x=10, y=12080, width=1060, height=40)

line_298_index = tk.Label(maincanvas)
line_298_index["bg"] = "#adafae"
line_298_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_298_index["font"] = ft
line_298_index["justify"] = "left"
line_298_index["anchor"] = "w"
line_298_index.place(x=20, y=12085, width=150, height=33)

line_298_name = tk.Label(maincanvas)
line_298_name["bg"] = "#adafae"
line_298_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_298_name["font"] = ft
line_298_name["justify"] = "left"
line_298_name["anchor"] = "w"
line_298_name.place(x=250, y=12085, width=500, height=33)

line_298_duration = tk.Label(maincanvas)
line_298_duration["bg"] = "#adafae"
line_298_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_298_duration["font"] = ft
line_298_duration["justify"] = "right"
line_298_duration["anchor"] = "e"
line_298_duration.place(x=910, y=12085, width=150, height=33)

line_298_live = tk.Label(maincanvas)
line_298_live["bg"] = "#adafae"
line_298_live["fg"] = "red"
line_298_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_298_live["font"] = ftl
line_298_live["justify"] = "left"
line_298_live["anchor"] = "w"
line_298_live["relief"] = "flat"
line_298_live.place(x=8000, y=12085, width=70, height=33)

line_298_disabled = tk.Label(maincanvas)
line_298_disabled["bg"] = "#adafae"
line_298_disabled["fg"] = "red"
line_298_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_298_disabled["font"] = ftl
line_298_disabled["justify"] = "left"
line_298_disabled["anchor"] = "w"
line_298_disabled["relief"] = "flat"
line_298_disabled.place(x=650, y=12085, width=150, height=33)

line_299_frame = tk.Label(maincanvas)
line_299_frame["bg"] = "#adafae"
line_299_frame["text"] = ""
line_299_frame["relief"] = "sunken"
line_299_frame.place(x=10, y=12120, width=1060, height=40)

line_299_index = tk.Label(maincanvas)
line_299_index["bg"] = "#adafae"
line_299_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_299_index["font"] = ft
line_299_index["justify"] = "left"
line_299_index["anchor"] = "w"
line_299_index.place(x=20, y=12125, width=150, height=33)

line_299_name = tk.Label(maincanvas)
line_299_name["bg"] = "#adafae"
line_299_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_299_name["font"] = ft
line_299_name["justify"] = "left"
line_299_name["anchor"] = "w"
line_299_name.place(x=250, y=12125, width=500, height=33)

line_299_duration = tk.Label(maincanvas)
line_299_duration["bg"] = "#adafae"
line_299_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_299_duration["font"] = ft
line_299_duration["justify"] = "right"
line_299_duration["anchor"] = "e"
line_299_duration.place(x=910, y=12125, width=150, height=33)

line_299_live = tk.Label(maincanvas)
line_299_live["bg"] = "#adafae"
line_299_live["fg"] = "red"
line_299_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_299_live["font"] = ftl
line_299_live["justify"] = "left"
line_299_live["anchor"] = "w"
line_299_live["relief"] = "flat"
line_299_live.place(x=8000, y=12125, width=70, height=33)

line_299_disabled = tk.Label(maincanvas)
line_299_disabled["bg"] = "#adafae"
line_299_disabled["fg"] = "red"
line_299_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_299_disabled["font"] = ftl
line_299_disabled["justify"] = "left"
line_299_disabled["anchor"] = "w"
line_299_disabled["relief"] = "flat"
line_299_disabled.place(x=650, y=12125, width=150, height=33)

line_300_frame = tk.Label(maincanvas)
line_300_frame["bg"] = "#adafae"
line_300_frame["text"] = ""
line_300_frame["relief"] = "sunken"
line_300_frame.place(x=10, y=12160, width=1060, height=40)

line_300_index = tk.Label(maincanvas)
line_300_index["bg"] = "#adafae"
line_300_index["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_300_index["font"] = ft
line_300_index["justify"] = "left"
line_300_index["anchor"] = "w"
line_300_index.place(x=20, y=12165, width=150, height=33)

line_300_name = tk.Label(maincanvas)
line_300_name["bg"] = "#adafae"
line_300_name["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_300_name["font"] = ft
line_300_name["justify"] = "left"
line_300_name["anchor"] = "w"
line_300_name.place(x=250, y=12165, width=500, height=33)

line_300_duration = tk.Label(maincanvas)
line_300_duration["bg"] = "#adafae"
line_300_duration["text"] = ""
ft = tkFont.Font(family='Proxima', size=22)
line_300_duration["font"] = ft
line_300_duration["justify"] = "right"
line_300_duration["anchor"] = "e"
line_300_duration.place(x=910, y=12165, width=150, height=33)

line_300_live = tk.Label(maincanvas)
line_300_live["bg"] = "#adafae"
line_300_live["fg"] = "red"
line_300_live["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_300_live["font"] = ftl
line_300_live["justify"] = "left"
line_300_live["anchor"] = "w"
line_300_live["relief"] = "flat"
line_300_live.place(x=8000, y=12165, width=70, height=33)

line_300_disabled = tk.Label(maincanvas)
line_300_disabled["bg"] = "#adafae"
line_300_disabled["fg"] = "red"
line_300_disabled["text"] = ""
ftl = tkFont.Font(family='Proxima', size=22, weight='bold')
line_300_disabled["font"] = ftl
line_300_disabled["justify"] = "left"
line_300_disabled["anchor"] = "w"
line_300_disabled["relief"] = "flat"
line_300_disabled.place(x=650, y=12165, width=150, height=33)







name_list= [line_1_name, line_2_name, line_3_name, line_4_name, line_5_name, line_6_name, line_7_name,
    line_8_name, line_9_name, line_10_name, line_11_name, line_12_name, line_13_name, line_14_name,
    line_15_name, line_16_name, line_17_name, line_18_name, line_19_name, line_20_name, line_21_name,
    line_22_name, line_23_name, line_24_name, line_25_name, line_26_name, line_27_name, line_28_name,
    line_29_name, line_30_name, line_31_name, line_32_name, line_33_name, line_34_name, line_35_name,
    line_36_name, line_37_name, line_38_name, line_39_name, line_40_name, line_41_name, line_42_name,
    line_43_name, line_44_name, line_45_name, line_46_name, line_47_name, line_48_name, line_49_name,
    line_50_name, line_51_name, line_52_name, line_53_name, line_54_name, line_55_name, line_56_name,
    line_57_name, line_58_name, line_59_name, line_60_name, line_61_name, line_62_name, line_63_name,
    line_64_name, line_65_name, line_66_name, line_67_name, line_68_name, line_69_name, line_70_name,
    line_71_name, line_72_name, line_73_name, line_74_name, line_75_name, line_76_name, line_77_name,
    line_78_name, line_79_name, line_80_name, line_81_name, line_82_name, line_83_name, line_84_name,
    line_85_name, line_86_name, line_87_name, line_88_name, line_89_name, line_90_name, line_91_name,
    line_92_name, line_93_name, line_94_name, line_95_name, line_96_name, line_97_name, line_98_name,
    line_99_name, line_100_name, line_101_name, line_102_name, line_103_name, line_104_name,
    line_105_name, line_106_name, line_107_name, line_108_name, line_109_name, line_110_name,
    line_111_name, line_112_name, line_113_name, line_114_name, line_115_name, line_116_name,
    line_117_name, line_118_name, line_119_name, line_120_name, line_121_name, line_122_name,
    line_123_name, line_124_name, line_125_name, line_126_name, line_127_name, line_128_name,
    line_129_name, line_130_name, line_131_name, line_132_name, line_133_name, line_134_name,
    line_135_name, line_136_name, line_137_name, line_138_name, line_139_name, line_140_name,
    line_141_name, line_142_name, line_143_name, line_144_name, line_145_name, line_146_name,
    line_147_name, line_148_name, line_149_name, line_150_name, line_151_name, line_152_name,
    line_153_name, line_154_name, line_155_name, line_156_name, line_157_name, line_158_name,
    line_159_name, line_160_name, line_161_name, line_162_name, line_163_name, line_164_name,
    line_165_name, line_166_name, line_167_name, line_168_name, line_169_name, line_170_name,
    line_171_name, line_172_name, line_173_name, line_174_name, line_175_name, line_176_name,
    line_177_name, line_178_name, line_179_name, line_180_name, line_181_name, line_182_name,
    line_183_name, line_184_name, line_185_name, line_186_name, line_187_name, line_188_name,
    line_189_name, line_190_name, line_191_name, line_192_name, line_193_name, line_194_name,
    line_195_name, line_196_name, line_197_name, line_198_name, line_199_name, line_200_name,
    line_201_name, line_202_name, line_203_name, line_204_name, line_205_name, line_206_name,
    line_207_name, line_208_name, line_209_name, line_210_name, line_211_name, line_212_name,
    line_213_name, line_214_name, line_215_name, line_216_name, line_217_name, line_218_name,
    line_219_name, line_220_name, line_221_name, line_222_name, line_223_name, line_224_name,
    line_225_name, line_226_name, line_227_name, line_228_name, line_229_name, line_230_name,
    line_231_name, line_232_name, line_233_name, line_234_name, line_235_name, line_236_name,
    line_237_name, line_238_name, line_239_name, line_240_name, line_241_name, line_242_name,
    line_243_name, line_244_name, line_245_name, line_246_name, line_247_name, line_248_name,
    line_249_name, line_250_name, line_251_name, line_252_name, line_253_name, line_254_name,
    line_255_name, line_256_name, line_257_name, line_258_name, line_259_name, line_260_name,
    line_261_name, line_262_name, line_263_name, line_264_name, line_265_name, line_266_name,
    line_267_name, line_268_name, line_269_name, line_270_name, line_271_name, line_272_name,
    line_273_name, line_274_name, line_275_name, line_276_name, line_277_name, line_278_name,
    line_279_name, line_280_name, line_281_name, line_282_name, line_283_name, line_284_name,
    line_285_name, line_286_name, line_287_name, line_288_name, line_289_name, line_290_name,
    line_291_name, line_292_name, line_293_name, line_294_name, line_295_name, line_296_name,
    line_297_name, line_298_name, line_299_name, line_300_name]

duration_list= [line_1_duration, line_2_duration, line_3_duration, line_4_duration, line_5_duration, line_6_duration, line_7_duration,
    line_8_duration, line_9_duration, line_10_duration, line_11_duration, line_12_duration, line_13_duration, line_14_duration,
    line_15_duration, line_16_duration, line_17_duration, line_18_duration, line_19_duration, line_20_duration, line_21_duration,
    line_22_duration, line_23_duration, line_24_duration, line_25_duration, line_26_duration, line_27_duration, line_28_duration,
    line_29_duration, line_30_duration, line_31_duration, line_32_duration, line_33_duration, line_34_duration, line_35_duration,
    line_36_duration, line_37_duration, line_38_duration, line_39_duration, line_40_duration, line_41_duration, line_42_duration,
    line_43_duration, line_44_duration, line_45_duration, line_46_duration, line_47_duration, line_48_duration, line_49_duration,
    line_50_duration, line_51_duration, line_52_duration, line_53_duration, line_54_duration, line_55_duration, line_56_duration,
    line_57_duration, line_58_duration, line_59_duration, line_60_duration, line_61_duration, line_62_duration, line_63_duration,
    line_64_duration, line_65_duration, line_66_duration, line_67_duration, line_68_duration, line_69_duration, line_70_duration,
    line_71_duration, line_72_duration, line_73_duration, line_74_duration, line_75_duration, line_76_duration, line_77_duration,
    line_78_duration, line_79_duration, line_80_duration, line_81_duration, line_82_duration, line_83_duration, line_84_duration,
    line_85_duration, line_86_duration, line_87_duration, line_88_duration, line_89_duration, line_90_duration, line_91_duration,
    line_92_duration, line_93_duration, line_94_duration, line_95_duration, line_96_duration, line_97_duration, line_98_duration,
    line_99_duration, line_100_duration, line_101_duration, line_102_duration, line_103_duration, line_104_duration,
    line_105_duration, line_106_duration, line_107_duration, line_108_duration, line_109_duration, line_110_duration,
    line_111_duration, line_112_duration, line_113_duration, line_114_duration, line_115_duration, line_116_duration,
    line_117_duration, line_118_duration, line_119_duration, line_120_duration, line_121_duration, line_122_duration,
    line_123_duration, line_124_duration, line_125_duration, line_126_duration, line_127_duration, line_128_duration,
    line_129_duration, line_130_duration, line_131_duration, line_132_duration, line_133_duration, line_134_duration,
    line_135_duration, line_136_duration, line_137_duration, line_138_duration, line_139_duration, line_140_duration,
    line_141_duration, line_142_duration, line_143_duration, line_144_duration, line_145_duration, line_146_duration,
    line_147_duration, line_148_duration, line_149_duration, line_150_duration, line_151_duration, line_152_duration,
    line_153_duration, line_154_duration, line_155_duration, line_156_duration, line_157_duration, line_158_duration,
    line_159_duration, line_160_duration, line_161_duration, line_162_duration, line_163_duration, line_164_duration,
    line_165_duration, line_166_duration, line_167_duration, line_168_duration, line_169_duration, line_170_duration,
    line_171_duration, line_172_duration, line_173_duration, line_174_duration, line_175_duration, line_176_duration,
    line_177_duration, line_178_duration, line_179_duration, line_180_duration, line_181_duration, line_182_duration,
    line_183_duration, line_184_duration, line_185_duration, line_186_duration, line_187_duration, line_188_duration,
    line_189_duration, line_190_duration, line_191_duration, line_192_duration, line_193_duration, line_194_duration,
    line_195_duration, line_196_duration, line_197_duration, line_198_duration, line_199_duration, line_200_duration,
    line_201_duration, line_202_duration, line_203_duration, line_204_duration, line_205_duration, line_206_duration,
    line_207_duration, line_208_duration, line_209_duration, line_210_duration, line_211_duration, line_212_duration,
    line_213_duration, line_214_duration, line_215_duration, line_216_duration, line_217_duration, line_218_duration,
    line_219_duration, line_220_duration, line_221_duration, line_222_duration, line_223_duration, line_224_duration,
    line_225_duration, line_226_duration, line_227_duration, line_228_duration, line_229_duration, line_230_duration,
    line_231_duration, line_232_duration, line_233_duration, line_234_duration, line_235_duration, line_236_duration,
    line_237_duration, line_238_duration, line_239_duration, line_240_duration, line_241_duration, line_242_duration,
    line_243_duration, line_244_duration, line_245_duration, line_246_duration, line_247_duration, line_248_duration,
    line_249_duration, line_250_duration, line_251_duration, line_252_duration, line_253_duration, line_254_duration,
    line_255_duration, line_256_duration, line_257_duration, line_258_duration, line_259_duration, line_260_duration,
    line_261_duration, line_262_duration, line_263_duration, line_264_duration, line_265_duration, line_266_duration,
    line_267_duration, line_268_duration, line_269_duration, line_270_duration, line_271_duration, line_272_duration,
    line_273_duration, line_274_duration, line_275_duration, line_276_duration, line_277_duration, line_278_duration,
    line_279_duration, line_280_duration, line_281_duration, line_282_duration, line_283_duration, line_284_duration,
    line_285_duration, line_286_duration, line_287_duration, line_288_duration, line_289_duration, line_290_duration,
    line_291_duration, line_292_duration, line_293_duration, line_294_duration, line_295_duration, line_296_duration,
    line_297_duration, line_298_duration, line_299_duration, line_300_duration]

index_list= [line_1_index, line_2_index, line_3_index, line_4_index, line_5_index, line_6_index, line_7_index,
    line_8_index, line_9_index, line_10_index, line_11_index, line_12_index, line_13_index, line_14_index,
    line_15_index, line_16_index, line_17_index, line_18_index, line_19_index, line_20_index, line_21_index,
    line_22_index, line_23_index, line_24_index, line_25_index, line_26_index, line_27_index, line_28_index,
    line_29_index, line_30_index, line_31_index, line_32_index, line_33_index, line_34_index, line_35_index,
    line_36_index, line_37_index, line_38_index, line_39_index, line_40_index, line_41_index, line_42_index,
    line_43_index, line_44_index, line_45_index, line_46_index, line_47_index, line_48_index, line_49_index,
    line_50_index, line_51_index, line_52_index, line_53_index, line_54_index, line_55_index, line_56_index,
    line_57_index, line_58_index, line_59_index, line_60_index, line_61_index, line_62_index, line_63_index,
    line_64_index, line_65_index, line_66_index, line_67_index, line_68_index, line_69_index, line_70_index,
    line_71_index, line_72_index, line_73_index, line_74_index, line_75_index, line_76_index, line_77_index,
    line_78_index, line_79_index, line_80_index, line_81_index, line_82_index, line_83_index, line_84_index,
    line_85_index, line_86_index, line_87_index, line_88_index, line_89_index, line_90_index, line_91_index,
    line_92_index, line_93_index, line_94_index, line_95_index, line_96_index, line_97_index, line_98_index,
    line_99_index, line_100_index, line_101_index, line_102_index, line_103_index, line_104_index,
    line_105_index, line_106_index, line_107_index, line_108_index, line_109_index, line_110_index,
    line_111_index, line_112_index, line_113_index, line_114_index, line_115_index, line_116_index,
    line_117_index, line_118_index, line_119_index, line_120_index, line_121_index, line_122_index,
    line_123_index, line_124_index, line_125_index, line_126_index, line_127_index, line_128_index,
    line_129_index, line_130_index, line_131_index, line_132_index, line_133_index, line_134_index,
    line_135_index, line_136_index, line_137_index, line_138_index, line_139_index, line_140_index,
    line_141_index, line_142_index, line_143_index, line_144_index, line_145_index, line_146_index,
    line_147_index, line_148_index, line_149_index, line_150_index, line_151_index, line_152_index,
    line_153_index, line_154_index, line_155_index, line_156_index, line_157_index, line_158_index,
    line_159_index, line_160_index, line_161_index, line_162_index, line_163_index, line_164_index,
    line_165_index, line_166_index, line_167_index, line_168_index, line_169_index, line_170_index,
    line_171_index, line_172_index, line_173_index, line_174_index, line_175_index, line_176_index,
    line_177_index, line_178_index, line_179_index, line_180_index, line_181_index, line_182_index,
    line_183_index, line_184_index, line_185_index, line_186_index, line_187_index, line_188_index,
    line_189_index, line_190_index, line_191_index, line_192_index, line_193_index, line_194_index,
    line_195_index, line_196_index, line_197_index, line_198_index, line_199_index, line_200_index,
    line_201_index, line_202_index, line_203_index, line_204_index, line_205_index, line_206_index,
    line_207_index, line_208_index, line_209_index, line_210_index, line_211_index, line_212_index,
    line_213_index, line_214_index, line_215_index, line_216_index, line_217_index, line_218_index,
    line_219_index, line_220_index, line_221_index, line_222_index, line_223_index, line_224_index,
    line_225_index, line_226_index, line_227_index, line_228_index, line_229_index, line_230_index,
    line_231_index, line_232_index, line_233_index, line_234_index, line_235_index, line_236_index,
    line_237_index, line_238_index, line_239_index, line_240_index, line_241_index, line_242_index,
    line_243_index, line_244_index, line_245_index, line_246_index, line_247_index, line_248_index,
    line_249_index, line_250_index, line_251_index, line_252_index, line_253_index, line_254_index,
    line_255_index, line_256_index, line_257_index, line_258_index, line_259_index, line_260_index,
    line_261_index, line_262_index, line_263_index, line_264_index, line_265_index, line_266_index,
    line_267_index, line_268_index, line_269_index, line_270_index, line_271_index, line_272_index,
    line_273_index, line_274_index, line_275_index, line_276_index, line_277_index, line_278_index,
    line_279_index, line_280_index, line_281_index, line_282_index, line_283_index, line_284_index,
    line_285_index, line_286_index, line_287_index, line_288_index, line_289_index, line_290_index,
    line_291_index, line_292_index, line_293_index, line_294_index, line_295_index, line_296_index,
    line_297_index, line_298_index, line_299_index, line_300_index]

frame_list= [line_1_frame, line_2_frame, line_3_frame, line_4_frame, line_5_frame, line_6_frame, line_7_frame,
    line_8_frame, line_9_frame, line_10_frame, line_11_frame, line_12_frame, line_13_frame, line_14_frame,
    line_15_frame, line_16_frame, line_17_frame, line_18_frame, line_19_frame, line_20_frame, line_21_frame,
    line_22_frame, line_23_frame, line_24_frame, line_25_frame, line_26_frame, line_27_frame, line_28_frame,
    line_29_frame, line_30_frame, line_31_frame, line_32_frame, line_33_frame, line_34_frame, line_35_frame,
    line_36_frame, line_37_frame, line_38_frame, line_39_frame, line_40_frame, line_41_frame, line_42_frame,
    line_43_frame, line_44_frame, line_45_frame, line_46_frame, line_47_frame, line_48_frame, line_49_frame,
    line_50_frame, line_51_frame, line_52_frame, line_53_frame, line_54_frame, line_55_frame, line_56_frame,
    line_57_frame, line_58_frame, line_59_frame, line_60_frame, line_61_frame, line_62_frame, line_63_frame,
    line_64_frame, line_65_frame, line_66_frame, line_67_frame, line_68_frame, line_69_frame, line_70_frame,
    line_71_frame, line_72_frame, line_73_frame, line_74_frame, line_75_frame, line_76_frame, line_77_frame,
    line_78_frame, line_79_frame, line_80_frame, line_81_frame, line_82_frame, line_83_frame, line_84_frame,
    line_85_frame, line_86_frame, line_87_frame, line_88_frame, line_89_frame, line_90_frame, line_91_frame,
    line_92_frame, line_93_frame, line_94_frame, line_95_frame, line_96_frame, line_97_frame, line_98_frame,
    line_99_frame, line_100_frame, line_101_frame, line_102_frame, line_103_frame, line_104_frame,
    line_105_frame, line_106_frame, line_107_frame, line_108_frame, line_109_frame, line_110_frame,
    line_111_frame, line_112_frame, line_113_frame, line_114_frame, line_115_frame, line_116_frame,
    line_117_frame, line_118_frame, line_119_frame, line_120_frame, line_121_frame, line_122_frame,
    line_123_frame, line_124_frame, line_125_frame, line_126_frame, line_127_frame, line_128_frame,
    line_129_frame, line_130_frame, line_131_frame, line_132_frame, line_133_frame, line_134_frame,
    line_135_frame, line_136_frame, line_137_frame, line_138_frame, line_139_frame, line_140_frame,
    line_141_frame, line_142_frame, line_143_frame, line_144_frame, line_145_frame, line_146_frame,
    line_147_frame, line_148_frame, line_149_frame, line_150_frame, line_151_frame, line_152_frame,
    line_153_frame, line_154_frame, line_155_frame, line_156_frame, line_157_frame, line_158_frame,
    line_159_frame, line_160_frame, line_161_frame, line_162_frame, line_163_frame, line_164_frame,
    line_165_frame, line_166_frame, line_167_frame, line_168_frame, line_169_frame, line_170_frame,
    line_171_frame, line_172_frame, line_173_frame, line_174_frame, line_175_frame, line_176_frame,
    line_177_frame, line_178_frame, line_179_frame, line_180_frame, line_181_frame, line_182_frame,
    line_183_frame, line_184_frame, line_185_frame, line_186_frame, line_187_frame, line_188_frame,
    line_189_frame, line_190_frame, line_191_frame, line_192_frame, line_193_frame, line_194_frame,
    line_195_frame, line_196_frame, line_197_frame, line_198_frame, line_199_frame, line_200_frame,
    line_201_frame, line_202_frame, line_203_frame, line_204_frame, line_205_frame, line_206_frame,
    line_207_frame, line_208_frame, line_209_frame, line_210_frame, line_211_frame, line_212_frame,
    line_213_frame, line_214_frame, line_215_frame, line_216_frame, line_217_frame, line_218_frame,
    line_219_frame, line_220_frame, line_221_frame, line_222_frame, line_223_frame, line_224_frame,
    line_225_frame, line_226_frame, line_227_frame, line_228_frame, line_229_frame, line_230_frame,
    line_231_frame, line_232_frame, line_233_frame, line_234_frame, line_235_frame, line_236_frame,
    line_237_frame, line_238_frame, line_239_frame, line_240_frame, line_241_frame, line_242_frame,
    line_243_frame, line_244_frame, line_245_frame, line_246_frame, line_247_frame, line_248_frame,
    line_249_frame, line_250_frame, line_251_frame, line_252_frame, line_253_frame, line_254_frame,
    line_255_frame, line_256_frame, line_257_frame, line_258_frame, line_259_frame, line_260_frame,
    line_261_frame, line_262_frame, line_263_frame, line_264_frame, line_265_frame, line_266_frame,
    line_267_frame, line_268_frame, line_269_frame, line_270_frame, line_271_frame, line_272_frame,
    line_273_frame, line_274_frame, line_275_frame, line_276_frame, line_277_frame, line_278_frame,
    line_279_frame, line_280_frame, line_281_frame, line_282_frame, line_283_frame, line_284_frame,
    line_285_frame, line_286_frame, line_287_frame, line_288_frame, line_289_frame, line_290_frame,
    line_291_frame, line_292_frame, line_293_frame, line_294_frame, line_295_frame, line_296_frame,
    line_297_frame, line_298_frame, line_299_frame, line_300_frame]

live_list= [line_1_live, line_2_live, line_3_live, line_4_live, line_5_live, line_6_live, line_7_live,
    line_8_live, line_9_live, line_10_live, line_11_live, line_12_live, line_13_live, line_14_live,
    line_15_live, line_16_live, line_17_live, line_18_live, line_19_live, line_20_live, line_21_live,
    line_22_live, line_23_live, line_24_live, line_25_live, line_26_live, line_27_live, line_28_live,
    line_29_live, line_30_live, line_31_live, line_32_live, line_33_live, line_34_live, line_35_live,
    line_36_live, line_37_live, line_38_live, line_39_live, line_40_live, line_41_live, line_42_live,
    line_43_live, line_44_live, line_45_live, line_46_live, line_47_live, line_48_live, line_49_live,
    line_50_live, line_51_live, line_52_live, line_53_live, line_54_live, line_55_live, line_56_live,
    line_57_live, line_58_live, line_59_live, line_60_live, line_61_live, line_62_live, line_63_live,
    line_64_live, line_65_live, line_66_live, line_67_live, line_68_live, line_69_live, line_70_live,
    line_71_live, line_72_live, line_73_live, line_74_live, line_75_live, line_76_live, line_77_live,
    line_78_live, line_79_live, line_80_live, line_81_live, line_82_live, line_83_live, line_84_live,
    line_85_live, line_86_live, line_87_live, line_88_live, line_89_live, line_90_live, line_91_live,
    line_92_live, line_93_live, line_94_live, line_95_live, line_96_live, line_97_live, line_98_live,
    line_99_live, line_100_live, line_101_live, line_102_live, line_103_live, line_104_live,
    line_105_live, line_106_live, line_107_live, line_108_live, line_109_live, line_110_live,
    line_111_live, line_112_live, line_113_live, line_114_live, line_115_live, line_116_live,
    line_117_live, line_118_live, line_119_live, line_120_live, line_121_live, line_122_live,
    line_123_live, line_124_live, line_125_live, line_126_live, line_127_live, line_128_live,
    line_129_live, line_130_live, line_131_live, line_132_live, line_133_live, line_134_live,
    line_135_live, line_136_live, line_137_live, line_138_live, line_139_live, line_140_live,
    line_141_live, line_142_live, line_143_live, line_144_live, line_145_live, line_146_live,
    line_147_live, line_148_live, line_149_live, line_150_live, line_151_live, line_152_live,
    line_153_live, line_154_live, line_155_live, line_156_live, line_157_live, line_158_live,
    line_159_live, line_160_live, line_161_live, line_162_live, line_163_live, line_164_live,
    line_165_live, line_166_live, line_167_live, line_168_live, line_169_live, line_170_live,
    line_171_live, line_172_live, line_173_live, line_174_live, line_175_live, line_176_live,
    line_177_live, line_178_live, line_179_live, line_180_live, line_181_live, line_182_live,
    line_183_live, line_184_live, line_185_live, line_186_live, line_187_live, line_188_live,
    line_189_live, line_190_live, line_191_live, line_192_live, line_193_live, line_194_live,
    line_195_live, line_196_live, line_197_live, line_198_live, line_199_live, line_200_live,
    line_201_live, line_202_live, line_203_live, line_204_live, line_205_live, line_206_live,
    line_207_live, line_208_live, line_209_live, line_210_live, line_211_live, line_212_live,
    line_213_live, line_214_live, line_215_live, line_216_live, line_217_live, line_218_live,
    line_219_live, line_220_live, line_221_live, line_222_live, line_223_live, line_224_live,
    line_225_live, line_226_live, line_227_live, line_228_live, line_229_live, line_230_live,
    line_231_live, line_232_live, line_233_live, line_234_live, line_235_live, line_236_live,
    line_237_live, line_238_live, line_239_live, line_240_live, line_241_live, line_242_live,
    line_243_live, line_244_live, line_245_live, line_246_live, line_247_live, line_248_live,
    line_249_live, line_250_live, line_251_live, line_252_live, line_253_live, line_254_live,
    line_255_live, line_256_live, line_257_live, line_258_live, line_259_live, line_260_live,
    line_261_live, line_262_live, line_263_live, line_264_live, line_265_live, line_266_live,
    line_267_live, line_268_live, line_269_live, line_270_live, line_271_live, line_272_live,
    line_273_live, line_274_live, line_275_live, line_276_live, line_277_live, line_278_live,
    line_279_live, line_280_live, line_281_live, line_282_live, line_283_live, line_284_live,
    line_285_live, line_286_live, line_287_live, line_288_live, line_289_live, line_290_live,
    line_291_live, line_292_live, line_293_live, line_294_live, line_295_live, line_296_live,
    line_297_live, line_298_live, line_299_live, line_300_live]

disabled_list= [line_1_disabled, line_2_disabled, line_3_disabled, line_4_disabled, line_5_disabled, line_6_disabled, line_7_disabled,
    line_8_disabled, line_9_disabled, line_10_disabled, line_11_disabled, line_12_disabled, line_13_disabled, line_14_disabled,
    line_15_disabled, line_16_disabled, line_17_disabled, line_18_disabled, line_19_disabled, line_20_disabled, line_21_disabled,
    line_22_disabled, line_23_disabled, line_24_disabled, line_25_disabled, line_26_disabled, line_27_disabled, line_28_disabled,
    line_29_disabled, line_30_disabled, line_31_disabled, line_32_disabled, line_33_disabled, line_34_disabled, line_35_disabled,
    line_36_disabled, line_37_disabled, line_38_disabled, line_39_disabled, line_40_disabled, line_41_disabled, line_42_disabled,
    line_43_disabled, line_44_disabled, line_45_disabled, line_46_disabled, line_47_disabled, line_48_disabled, line_49_disabled,
    line_50_disabled, line_51_disabled, line_52_disabled, line_53_disabled, line_54_disabled, line_55_disabled, line_56_disabled,
    line_57_disabled, line_58_disabled, line_59_disabled, line_60_disabled, line_61_disabled, line_62_disabled, line_63_disabled,
    line_64_disabled, line_65_disabled, line_66_disabled, line_67_disabled, line_68_disabled, line_69_disabled, line_70_disabled,
    line_71_disabled, line_72_disabled, line_73_disabled, line_74_disabled, line_75_disabled, line_76_disabled, line_77_disabled,
    line_78_disabled, line_79_disabled, line_80_disabled, line_81_disabled, line_82_disabled, line_83_disabled, line_84_disabled,
    line_85_disabled, line_86_disabled, line_87_disabled, line_88_disabled, line_89_disabled, line_90_disabled, line_91_disabled,
    line_92_disabled, line_93_disabled, line_94_disabled, line_95_disabled, line_96_disabled, line_97_disabled, line_98_disabled,
    line_99_disabled, line_100_disabled, line_101_disabled, line_102_disabled, line_103_disabled, line_104_disabled,
    line_105_disabled, line_106_disabled, line_107_disabled, line_108_disabled, line_109_disabled, line_110_disabled,
    line_111_disabled, line_112_disabled, line_113_disabled, line_114_disabled, line_115_disabled, line_116_disabled,
    line_117_disabled, line_118_disabled, line_119_disabled, line_120_disabled, line_121_disabled, line_122_disabled,
    line_123_disabled, line_124_disabled, line_125_disabled, line_126_disabled, line_127_disabled, line_128_disabled,
    line_129_disabled, line_130_disabled, line_131_disabled, line_132_disabled, line_133_disabled, line_134_disabled,
    line_135_disabled, line_136_disabled, line_137_disabled, line_138_disabled, line_139_disabled, line_140_disabled,
    line_141_disabled, line_142_disabled, line_143_disabled, line_144_disabled, line_145_disabled, line_146_disabled,
    line_147_disabled, line_148_disabled, line_149_disabled, line_150_disabled, line_151_disabled, line_152_disabled,
    line_153_disabled, line_154_disabled, line_155_disabled, line_156_disabled, line_157_disabled, line_158_disabled,
    line_159_disabled, line_160_disabled, line_161_disabled, line_162_disabled, line_163_disabled, line_164_disabled,
    line_165_disabled, line_166_disabled, line_167_disabled, line_168_disabled, line_169_disabled, line_170_disabled,
    line_171_disabled, line_172_disabled, line_173_disabled, line_174_disabled, line_175_disabled, line_176_disabled,
    line_177_disabled, line_178_disabled, line_179_disabled, line_180_disabled, line_181_disabled, line_182_disabled,
    line_183_disabled, line_184_disabled, line_185_disabled, line_186_disabled, line_187_disabled, line_188_disabled,
    line_189_disabled, line_190_disabled, line_191_disabled, line_192_disabled, line_193_disabled, line_194_disabled,
    line_195_disabled, line_196_disabled, line_197_disabled, line_198_disabled, line_199_disabled, line_200_disabled,
    line_201_disabled, line_202_disabled, line_203_disabled, line_204_disabled, line_205_disabled, line_206_disabled,
    line_207_disabled, line_208_disabled, line_209_disabled, line_210_disabled, line_211_disabled, line_212_disabled,
    line_213_disabled, line_214_disabled, line_215_disabled, line_216_disabled, line_217_disabled, line_218_disabled,
    line_219_disabled, line_220_disabled, line_221_disabled, line_222_disabled, line_223_disabled, line_224_disabled,
    line_225_disabled, line_226_disabled, line_227_disabled, line_228_disabled, line_229_disabled, line_230_disabled,
    line_231_disabled, line_232_disabled, line_233_disabled, line_234_disabled, line_235_disabled, line_236_disabled,
    line_237_disabled, line_238_disabled, line_239_disabled, line_240_disabled, line_241_disabled, line_242_disabled,
    line_243_disabled, line_244_disabled, line_245_disabled, line_246_disabled, line_247_disabled, line_248_disabled,
    line_249_disabled, line_250_disabled, line_251_disabled, line_252_disabled, line_253_disabled, line_254_disabled,
    line_255_disabled, line_256_disabled, line_257_disabled, line_258_disabled, line_259_disabled, line_260_disabled,
    line_261_disabled, line_262_disabled, line_263_disabled, line_264_disabled, line_265_disabled, line_266_disabled,
    line_267_disabled, line_268_disabled, line_269_disabled, line_270_disabled, line_271_disabled, line_272_disabled,
    line_273_disabled, line_274_disabled, line_275_disabled, line_276_disabled, line_277_disabled, line_278_disabled,
    line_279_disabled, line_280_disabled, line_281_disabled, line_282_disabled, line_283_disabled, line_284_disabled,
    line_285_disabled, line_286_disabled, line_287_disabled, line_288_disabled, line_289_disabled, line_290_disabled,
    line_291_disabled, line_292_disabled, line_293_disabled, line_294_disabled, line_295_disabled, line_296_disabled,
    line_297_disabled, line_298_disabled, line_299_disabled, line_300_disabled]

maincanvas.create_window((0,0), height=13000, width=1080, window=scrollframe, anchor='nw')

update_list()
root.mainloop()




