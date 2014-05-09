from IPython import embed
from pydub import AudioSegment
from pydub.playback import play
from pydub import utils
from track import Track
import bpm

tracks = [
    Track("./long_way_home.mp3",     30.5,  3 * 60 + 16,    10, 128, "Bmaj"),
    Track("./revolution.mp3",        14.5,  4 * 60 + 27,    10, 128, "Gmin"),
    Track("./get_lucky.mp3",         0,     3 * 60 + 55,    10, 116, "F#min"),
    Track("./animals.mp3",           30,    3 * 60 + 15,    10, 128, "Fmaj"),
    Track("./light_and_thunder.mp3", 55.5,  4 * 60 + 50,    10, 132, "Fmin")
]


def processSingleTrack(track):
    sound = AudioSegment.from_mp3(track.path)
    offset = track.start_offset*1000
    sound = sound[offset:offset + track.length*1000]
    return sound


def combineTracks(processed, track):
    sound = processSingleTrack(track)
    p = processed.append(sound, crossfade=track.crossfade_time*1000)
    return p

def mixTracks(tracks):
    init = processSingleTrack(tracks[0])
    return reduce(combineTracks, tracks[1:], init)

reorderedTracks = bpm.trackWrapper(tracks)

sound = mixTracks(reorderedTracks)
sound.export("mix.mp3", format="mp3")
print "done"

def slowDown(seg, playbackRate):
    assert(playbackRate <= 1.0)
    origFrameRate = seg.frame_rate
    out1 = seg * 1
    out1.frame_rate = int(origFrameRate * playbackRate)
    return out1.set_frame_rate(origFrameRate)

def changeSpeed(seg, playbackSpeedMultiplier,
        chunksize=150, crossfade=25):
    if playbackSpeedMultiplier < 1.0:
        return slowDown(seg, playbackSpeedMultiplier)
    else:
        return seg.speedup(playbackSpeedMultiplier,
                chunk_size=chunksize, crossfade=crossfade)

def changeBPM(seg, origBPM, newBPM,
        chunksize=150, crossfade=0):
    playbackSpeedMultiplier = float(newBPM)/float(origBPM)
    return changeSpeed(seg, playbackSpeedMultiplier,
            chunksize, crossfade)

def fasterToOriginalSlowerBPM(seg, startingBPM, origBPM, timeSpan):
    part = seg[0:timeSpan*1000]
    orig = seg[timeSpan*1000:]

    newPart = changeBPM(part, origBPM, startingBPM)

    return newPart.append(orig, crossfade=500)



#get_lucky = processSingleTrack(tracks[2])
#animals = processSingleTrack(tracks[1])
#faster_get_lucky = fasterToOriginalSlowerBPM(get_lucky, 128, 116, 10)
#
#animals.append(faster_get_lucky, crossfade=10*1000)
#p = processSingleTrack(tracks[1]).append(processSingleTrack(tracks[0]),
#    crossfade=2*10*1000)
#play(p)


#play(slowDown(sound, 0.75))

# play(mixTracks(tracks))
    
embed()
