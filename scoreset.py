"""Dataset creation"""
import re
import os
from midihelper import midi_extract
from guitarprohelper import makegpro, writegpro
from expressions import insertexpressions
from fileutils import get_all_files_recursive, create_or_clear_directory, create_directory
import config as cfg

def scoreset(gpro_dir, midi_dir, excluded_filenames):
    """loop through all .midi files and process them"""
    create_or_clear_directory(gpro_dir)
    files = get_all_files_recursive(midi_dir)
    filtered_files = [
    f for f in files
        if not os.path.basename(f) in excluded_filenames]
    for f in filtered_files:
        parts = re.split(r'[\\/]+', f)
        if ".mid" in parts[-1]:
            create_directory(gpro_dir + "/" + parts[-3] + "/" + parts[-2])
            print("Processing : ", parts[-1])
            duration_note, start_tick, notevalue = midi_extract(f, 0)
            song = makegpro(duration_note, start_tick, notevalue, cfg.TUNING, 55)
            song = insertexpressions(song)

            gprofilename = re.split(r'\.', parts[-1])
            writegpro(gpro_dir + "/" + parts[-3] + "/" + parts[-2] + "/" + gprofilename[0], song)
