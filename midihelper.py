import mido
from guitarprohelper import clip_to_nearest_duration

def midi_to_note_label(midi_note: int) -> str:
    """
    Convert a MIDI note number to a note label (e.g., 60 -> "C4").
    """
    if not (0 <= midi_note <= 127):
        raise ValueError("MIDI note must be between 0 and 127.")

    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note_names[midi_note % 12]
    octave = (midi_note // 12) - 1
    return f"{note_name}{octave}"


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

def midi_extract(midi_path, total_measure):
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
                    dur_value = max(16, clip_to_nearest_duration(duration, mid.ticks_per_beat))
                    tot_measure += 1 / dur_value
                    notevalue.append(msg.note)
                    start_tick.append(start)
                    duration_note.append(dur_value)
                        # break
            if tot_measure >= total_measure:
                break
            #if len(notevalue) >= 8 and len(notevalue) == len(duration_note):
            #    break
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
    # print("start",start_tick)
    print("note",notevalue)
    notevaluenanme = []
    for nv in notevalue:
        notevaluenanme.append(midi_to_note_label(nv))
    print("note",notevaluenanme)
    return duration_note, start_tick, notevalue