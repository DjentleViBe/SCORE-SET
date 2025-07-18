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

def bend_note_1(song, beat_in_measure, indices_to_increment):
    song_bend_1 = gp.parse('./gprofiles/gp5_templates/bend_1.gp5')
    bend1_beat = song_bend_1.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].effect.isBend = True
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].effect.bend = bend1_beat.notes[0].effect.bend
    return song

def harmonic(song, beat_in_measure, indices_to_increment):
    song_harmonic_1 = gp.parse('./gprofiles/gp5_templates/harmonic.gp5')
    harmonic_1_beat = song_harmonic_1.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].harmonic = harmonic_1_beat.notes[0].effect.harmonic
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
    # int(EXPR_COUNT * ratios[0])
    indices_to_increment = random.sample(range(total_beats), int(EXPR_COUNT))

    # Step 2: Split these indices into groups based on the percentages
    split_counts = [int(EXPR_COUNT * p) for p in ratios ]

    # Fix rounding errors to ensure total adds up to EXPR_COUNT
    while sum(split_counts) < EXPR_COUNT:
        for i in range(len(split_counts)):
            split_counts[i] += 1
            if sum(split_counts) == EXPR_COUNT:
                break

    # Step 3: Assign indices to groups
    random.shuffle(indices_to_increment)
    grouped_indices = []
    start = 0
    for count in split_counts:
        grouped_indices.append(indices_to_increment[start:start + count])
        start += count

    print("total beats : ", total_beats)
    print("insert beats : ", EXPR_COUNT)

    print("bend_note_1 :", len(grouped_indices[0]))
    song = bend_note_1(song, beat_in_measure, grouped_indices[0])

    print("harmonic :", len(grouped_indices[21]))
    song = harmonic(song, beat_in_measure, grouped_indices[21])

    return song