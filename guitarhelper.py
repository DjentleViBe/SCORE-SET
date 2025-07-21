"""Helper functions for guitar operations"""
import math

def findnewstring(note, string, tuning):
    """Find new string given note and string"""
    # notepos = tuning[string - 1] + note
    notepos = note
    if string > 4:
        notepos += 12
    else:
        notepos -= 12
    closest_index = min(range(len(tuning)), key=lambda i: abs(tuning[i] - notepos))
    fret = note - tuning[closest_index]
    if fret == 12:
        fret = 0
    return fret, closest_index + 1

def find_string_and_fret(note_number, string_tuning, max_fret=24):
    """Find string and fret number"""
    if note_number <= string_tuning[5]:
        note_number += 12 * math.ceil(((string_tuning[5] - note_number) / 12))
    elif note_number >= string_tuning[0] + 24:
        note_number -= 12 * math.ceil(((note_number - string_tuning[0]) / 12))
    for string_index, tuning_note in enumerate(string_tuning):
        fret = note_number - tuning_note
        if 0 <= fret <= max_fret:
            if fret >= 12:
                fret -= 12
            # Return string number (1-based: 1 = high E)
            return (string_index + 1, fret)
    return None  # Note can't be played on any string

def find_closest_string_and_fret(note, used_strings, tuning, max_fret=24):
    """Find closest string and fret to given note"""
    candidates = []
    for i, tuning_note in enumerate(tuning):
        string_num = i + 1  # 1-based
        if string_num in used_strings:
            continue
        fret = note - tuning_note
        if 0 <= fret <= max_fret:
            if fret >= 12:
                fret -= 12
                candidates.append((fret, string_num))
    return min(candidates, default=(None, None), key=lambda x: x[0])
