import requests
from tqdm import tqdm
import zipfile
import io
import os
from midihelper import midi_extract
from guitarhelper import findnewstring, find_string_and_fret
from guitarprohelper import makegpro, writegpro
import guitarpro as gp

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

# Usage
duration_note, start_tick, notevalue = midi_extract("./MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi")

song = makegpro(duration_note, start_tick, notevalue, 55)
writegpro('output', song)
# datasetdownload()

