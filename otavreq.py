import requests
import time
import os
import datetime
def clear():
    os.system('cls')

def otavplaystatus(endpoint):
    playbackpoint = "playback/playing"
    try:
        status = requests.get(endpoint + playbackpoint)
        statusjson = status.json()
    except:
        return['STOPPED','']
    else:
        if statusjson['playback_status'] != 'Stopped' and statusjson['playback_status'] != 'Closed':
            if 'item_display_name' in statusjson:
                return [statusjson['item_display_name'],statusjson['item_remaining'], statusjson['playlist_elapsed']]
            else:
                try:
                    return[statusjson['item_filename'],statusjson['item_remaining'], statusjson['playlist_elapsed']]
                except:
                    return ['STOPPED', '']
        else:
            return['STOPPED', '']

def otavgetplaylist(endpoint):
    playbackpoint = "playback/playing"
    playuniqueid = ''
    clipindex = 1
    clipnumber = []
    cliptype = []
    clipname = []
    clipduration = []
    clipstart = []
    clipid = []
    isdisabled = []
    clipstartcode = []
    next_live = ""

    try:
        currentplayback = requests.get(endpoint + playbackpoint)
        currentplaybackjson = currentplayback.json()
        uniqueid = currentplaybackjson['playlist_unique_id']
        playuniqueid = currentplaybackjson['item_unique_id']
        playlistitems = endpoint + "playlists/" + uniqueid + "/items"
        status = requests.get(playlistitems)
        statusjson = status.json()
    except:
        return [clipnumber, cliptype, clipname, clipduration, clipstart, clipid, playuniqueid, isdisabled, next_live,
                clipstartcode]
    else:
        for x in statusjson:
            if x['clip_type'] != 3:
                clipnumber.append(str(clipindex))
                clipduration.append(x['duration_timecode'])
                clipstart.append(x['displayed_start_timecode'])
                try:
                    clipid.append(x['unique_id'])
                except:
                    clipid.append('')
                clipstartcode.append(x['relative_start_time'])
            else:
                #clipnumber.append("")
                clipnumber.append(str(clipindex))
                clipduration.append("")
                clipstart.append("")
                clipid.append("")
                clipstartcode.append([""])
            cliptype.append(x['clip_type'])
            if x['name'] != "":
                clipname.append(x['name'])
            else:
                clipname.append(x["filename"])
            clipindex += 1
            if 'is_disabled' in x and x['is_disabled']:
                isdisabled.append('disabled')
            else:
                isdisabled.append('enabled')

            if "remaining_time_until_next_live" in currentplaybackjson:
                updatetime = currentplaybackjson["remaining_time_until_next_live"]
                next_live = "0" + str(datetime.timedelta(seconds=int(updatetime)))
            else:
                next_live = "NONE"
        return [clipnumber, cliptype, clipname, clipduration, clipstart, clipid, playuniqueid, isdisabled, next_live,
                clipstartcode]


#playcontrols for testing
def playnext():
    #proceed = requests.get("http://172.17.186.48:8081/playback/skip_next")
    proceed = requests.get("http://172.17.250.10:8081/playback/skip_next")

def stopplay():
    #proceed = requests.get("http://172.17.186.48:8081/playback/stop")
    proceed = requests.get("http://172.17.250.10:8081/playback/stop")

def startplay():
    #proceed = requests.get("http://172.17.186.48:8081/playback/play")
    proceed = requests.get("http://172.17.250.10:8081/playback/play")
