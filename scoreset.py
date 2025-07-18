from midihelper import midi_extract
from guitarprohelper import makegpro, writegpro
from expressions import insertexpressions
from fileutils import get_all_files_recursive, create_or_clear_directory, create_directory
import re

def scoreset():
    gpro_dir = "./maestro_dataset_gpro"
    create_or_clear_directory(gpro_dir)
    files = get_all_files_recursive('./maestro_dataset')
    for f in files: 
        parts = re.split(r'[\\/]+', f)
        if len(parts) == 5:
            if ".midi" in parts[4]:
                create_directory(gpro_dir + "/" + parts[2] + "/" + parts[3])
                print("Processing : ", parts[4])
                duration_note, start_tick, notevalue = midi_extract(f, 0)
                song = makegpro(duration_note, start_tick, notevalue, [64, 59, 55, 50, 45, 40], 55)
                song = insertexpressions(song)

                gprofilename = re.split(r'\.', parts[4])
                writegpro(gpro_dir + "/" + parts[2] + "/" + parts[3] + "/" + gprofilename[0], song)

