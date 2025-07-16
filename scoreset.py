import requests
from tqdm import tqdm
import zipfile
import io
import os
from midihelper import midi_to_note_label
from guitarhelper import findnewstring, find_string_and_fret

def datasetdownload():
    # URL of the dataset
    url = "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip"
    local_filename = "maestro-v3.0.0.zip"

    # Stream download with progress bar
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(local_filename, 'wb') as file, tqdm(
        desc="Downloading MAESTRO Dataset",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            file.write(data)
            bar.update(len(data))

    # Unzip after download
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        print("\nExtracting...")
        zip_ref.extractall("maestro_dataset")

    print("Done! Dataset is in the 'maestro_dataset' folder.")

import mido
import guitarpro as gp
from guitarpro import Song, Track, Measure, Voice, Beat, Note, Duration

def clip_to_nearest_duration(ticks, ticks_per_beat):
    # Precompute standard durations in ticks
    duration_map = {
        int(ticks_per_beat * 4): 1,       # whole
        int(ticks_per_beat * 2): 2,       # half
        int(ticks_per_beat * 1): 4,       # quarter
        int(ticks_per_beat * 0.5): 8,     # eighth
        int(ticks_per_beat * 0.25): 16,   # 16th
        int(ticks_per_beat * 0.125): 32,  # 32nd
        int(ticks_per_beat * 0.0625): 64  # 64th
    }
    # Find closest
    closest_ticks = min(duration_map.keys(), key=lambda x: abs(x - ticks))
    return duration_map[closest_ticks]

def ticks_to_duration(ticks, tpq):
    ratio = ticks / tpq  # ratio to quarter note
    
    if ratio < 0.375:       # less than dotted 16th (approx)
        return 32          # 32nd note
    elif ratio < 0.75:      # less than dotted 8th
        return 16          # 16th note
    elif ratio < 1.5:       # less than dotted quarter
        return 8           # 8th note
    elif ratio < 3:
        return 4           # quarter note
    elif ratio < 6:
        return 2           # half note
    else:
        return 1           # whole note


def midi_to_gp5(midi_path):
    mid = mido.MidiFile(midi_path)
    duration_note = []
    start_tick = []
    notevalue = []

    note_starts = {}  # note -> start_tick
    current_tick = 0
    tot_measure = 0
    for track in mid.tracks:
        for msg in track:
            current_tick += msg.time
            #print(msg.time)

            if msg.type == 'note_on' and msg.velocity > 0:
                note_starts[msg.note] = current_tick

            elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in note_starts:
                    start = note_starts.pop(msg.note)
                    duration = current_tick - start
                    dur_value = clip_to_nearest_duration(duration, mid.ticks_per_beat)
                    
                    notevalue.append(msg.note)
                    start_tick.append(start)
                    duration_note.append(dur_value)
                        # break
            if len(notevalue) >= 8 and len(notevalue) == len(duration_note):
                break
    # Combine all into tuples
    combined = list(zip(start_tick, notevalue, duration_note))

    # Sort by start_tick (the first element of each tuple)
    combined.sort(key=lambda x: x[0])

    # Unzip back to separate lists
    start_tick, notevalue, duration_note = zip(*combined)

    # Convert back to lists (zip returns tuples)
    start_tick = list(start_tick)
    notevalue = list(notevalue)
    duration_note = list(duration_note)

    print("Duration", duration_note)
    print("start",start_tick)
    print("note",notevalue)
    notevaluenanme = []
    for nv in notevalue:
        notevaluenanme.append(midi_to_note_label(nv))
    print("note",notevaluenanme)
    return duration_note, start_tick, notevalue

# Usage
duration_note, start_tick, notevalue = midi_to_gp5("./MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi")

def makegpro(duration, start, noteval, tolerence):
    song = gp.models.Song()
    song.artist = "DjentleViBe"
    song.tempo = 120  # Set the tempo
    song.tracks[0].name = "Guitar"
    song.tracks[0].channel.instrument = 30

    song.tracks[0].measures[0].hasTimeSignature  = True 
    song.tracks[0].measures[0].timeSignature.denominator.value = 4
    voice = song.tracks[0].measures[0].voices[0]
    note_collect = []
    beat_collect = []
    string_collect = []
    fret_collect = []
    kval_collect = []
    l_val = 0
    k_val =0
    string_tuning=[64, 59, 55, 50, 45, 40]
    reuse_last_beat = False
    for n_val, note in enumerate(noteval):
        if n_val != 0:
            if start[n_val] - start [n_val - 1] <= tolerence:
                # print("barred",start[n_val],start[n_val-1])
                reuse_last_beat = True
        
        if reuse_last_beat:
            current_beat = beat_collect[k_val - 1]
            if duration[n_val] < beat_collect[k_val - 1].duration.value:
                beat_collect[k_val - 1].duration.value = duration[n_val]
            current_beat.status = gp.models.BeatStatus.normal
            reuse_last_beat = False
            string_number, fret = find_string_and_fret(note, string_tuning, 23)
            if string_number == string_collect[l_val -1]:
                fret, string_number = findnewstring(note, string_number, string_tuning)
            kval_collect.append(k_val - 1)
        else:
            string_number, fret = find_string_and_fret(note, string_tuning, 23)
            current_beat = gp.Beat(voice=voice)
            current_beat.status = gp.models.BeatStatus.normal
            beat_collect.append(current_beat)
            voice.beats.append(current_beat)
            kval_collect.append(k_val)
            k_val += 1
    
        string_collect.append(string_number)
        fret_collect.append(fret)
        note_collect.append(gp.Note(beat=current_beat))
        note_collect[l_val].type = gp.models.NoteType.normal
        note_collect[l_val].value = fret
        note_collect[l_val].string = string_number
        note_collect[l_val].beat.duration.value = duration[n_val]
        current_beat.notes.append(note_collect[l_val])
                        
        l_val += 1
    print(string_collect)
    print(fret_collect)
    print(kval_collect)
    return song

def writegpro(filename, song):
    """write gpro file to disk"""
    # Save the song to a Guitar Pro file
    with open(filename + ".gp5", 'wb') as file:
        gp.write(song, file)

song = makegpro(duration_note, start_tick, notevalue, 55)
writegpro('output', song)
# datasetdownload()

