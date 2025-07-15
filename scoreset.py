import requests
from tqdm import tqdm
import zipfile
import io
import os

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


def midi_to_gp5(midi_path, gp5_path, string_tuning=[64, 59, 55, 50, 45, 40]):
    mid = mido.MidiFile(midi_path)
    song = gp.models.Song()
    song.tracks[0].name = "Guitar"
    song.tracks[0].channel.instrument = 30
    song.tracks[0].strings[0].value = string_tuning[0]
    song.tracks[0].strings[1].value = string_tuning[1]
    song.tracks[0].strings[2].value = string_tuning[2]
    song.tracks[0].strings[3].value = string_tuning[3]
    song.tracks[0].strings[4].value = string_tuning[4]
    song.tracks[0].strings[5].value = string_tuning[5]

    song.tracks[0].measures[0].hasTimeSignature  =True
    song.tracks[0].measures[0].timeSignature.denominator.value = 4
    voice = song.tracks[0].measures[0].voices[0]
    note_collect = []
    l_val = 0

    note_starts = {}  # note -> start_tick
    current_tick = 0

    for track in mid.tracks:
        for msg in track:
            current_tick += msg.time
            #print(msg.time)

            if msg.type == 'note_on' and msg.velocity > 0:
                note_starts[msg.note] = current_tick
            
            elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in note_starts:
                        midi_note = msg.note
                        start = note_starts.pop(msg.note)
                        duration = current_tick - start
                        dur_value = ticks_to_duration(duration, mid.ticks_per_beat)

                        # Basic fret/string assignment (e.g., all on 1st string)
                        string_number = 1
                        fret = 3
                        if fret < 0 or fret > 24:
                            continue  # skip unplayable notes

                        current_beat = gp.Beat(voice=voice)
                        current_beat.status = gp.models.BeatStatus.normal
                        voice.beats.append(current_beat)
                        note_collect.append(gp.Note(beat=current_beat))
                        note_collect[l_val].type = gp.models.NoteType.normal
                        note_collect[l_val].value = fret
                        note_collect[l_val].string = string_number
                        note_collect[l_val].beat.duration.value = dur_value
                        current_beat.notes.append(note_collect[l_val])
                        
                        l_val += 1
                        break

    gp.write(song, gp5_path)
    print(f"Guitar Pro file saved to {gp5_path}")

# Usage
midi_to_gp5("./MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi", "output.gp5")



# datasetdownload()

