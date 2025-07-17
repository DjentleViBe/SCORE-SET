from techniques import VALUES
import random
import guitarpro as gp

def find_insert_index(arr, value):
    """
    Returns the index `i` such that arr[i] <= value < arr[i+1] (if sorted ascending)
    If value is smaller than the first element, returns -1.
    If value is larger than the last element, returns len(arr) - 1.
    """
    for i in range(len(arr) - 1):
        if value < arr[i]:
            prev = arr[i - 1] if i > 0 else 0
            return i, int(value - prev)
    return -1  # Not in between any two values

def bend_note_1(song, total_beats, ratios, expr_count, beat_in_measure):
    song_bend_1 = gp.parse('./gprofiles/gp5_templates/bend_1.gp5')
    bend1_beat = song_bend_1.tracks[0].measures[0].voices[0].beats[0]
    indices_to_increment = random.sample(range(total_beats), int(expr_count * ratios[0]))
    # print(indices_to_increment)
    # print(beat_in_measure)
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        print(measure)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].effect.isBend = True
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].effect.bend = bend1_beat.notes[0].effect.bend
    return song

def insertexpressions(song):
    # calculate the total number of beats in the song
    total_beats = 0
    beat_in_measure = []
    measure_count = 0
    for measure in song.tracks[0].measures:
        for voice in measure.voices:
            total_beats += len(voice.beats)
        beat_in_measure.append(total_beats)
        measure_count += 1
    print("Total measures", measure_count)
    total = sum(VALUES)
    ratios = [round(v / total, 4) for v in VALUES]

    EXPR_PERCENTAGE = 0.2
    EXPR_COUNT = int(EXPR_PERCENTAGE * total_beats)
    # print(EXPR_COUNT)
    # print(ratios)

    song = bend_note_1(song, total_beats, ratios, EXPR_COUNT, beat_in_measure)

    return song