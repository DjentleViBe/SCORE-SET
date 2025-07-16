def findnewstring(note, string, TUNING):
    # notepos = TUNING[string - 1] + note
    notepos = note
    if string > 4:
        notepos += 12
    else:
        notepos -= 12
    closest_index = min(range(len(TUNING)), key=lambda i: abs(TUNING[i] - notepos))
    fret = note - TUNING[closest_index]
    if fret == 12:
        fret = 0
    return fret, closest_index + 1

def find_string_and_fret(note_number, string_tuning, max_fret=24):
    for string_index, tuning_note in enumerate(string_tuning):
        fret = note_number - tuning_note
        if 0 <= fret <= max_fret:
            # Return string number (1-based: 1 = high E)
            return (string_index + 1, fret)
    return None  # Note can't be played on any string