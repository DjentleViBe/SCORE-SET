from techniques import VALUES
import random
import guitarpro as gp

def find_insert_index(arr, value):
    """
    Returns the index `i` such that arr[i] <= value < arr[i+1] (if sorted ascending)
    If value is smaller than the first element, returns -1.
    If value is larger than the last element, returns len(arr) - 1.
    """
    for i in range(len(arr)):
        if value < arr[i]:
            prev = arr[i - 1] if i > 0 else 0
            return i, int(value - prev)
    return -1  # Not in between any two values

def bend_note(song, beat_in_measure, indices_to_increment, filename):
    song_bend = gp.parse(filename)
    bend_beat = song_bend.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].effect.isBend = True
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].effect.bend = bend_beat.notes[0].effect.bend
    return song

def trem_note(song, beat_in_measure, indices_to_increment, filename):
    song_trem = gp.parse(filename)
    trem_beat = song_trem.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].effect.isTremoloBar = True
        song.tracks[0].measures[measure].voices[0].beats[beat_index].effect.tremoloBar = trem_beat.notes[0].beat.effect.tremoloBar
    return song

def slide_note(song, beat_in_measure, indices_to_increment, filename):
    song_slide = gp.parse(filename)
    slide_beat = song_slide.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].effect.slides = slide_beat.notes[0].effect.slides
    return song

def harmonic(song, beat_in_measure, indices_to_increment):
    song_harmonic_1 = gp.parse('./gprofiles/gp5_templates/harmonic_1.gp5')
    harmonic_1_beat = song_harmonic_1.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        note = song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0]
        note.effect.harmonic = harmonic_1_beat.notes[0].effect.harmonic
    return song

def vibrato(song, beat_in_measure, indices_to_increment):
    song_vibrato = gp.parse('./gprofiles/gp5_templates/vibrato.gp5')
    vibrato_beat = song_vibrato.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        note = song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0]
        note.effect.vibrato = vibrato_beat.notes[0].effect.vibrato
    return song

def hammer(song, beat_in_measure, indices_to_increment):
    song_hammer = gp.parse('./gprofiles/gp5_templates/hammer.gp5')
    hammer_beat = song_hammer.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        note = song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0]
        note.effect.hammer = hammer_beat.notes[0].effect.hammer
    return song

def dead(song, beat_in_measure, indices_to_increment):
    song_dead = gp.parse('./gprofiles/gp5_templates/dead.gp5')
    dead_beat = song_dead.tracks[0].measures[0].voices[0].beats[0]
    for iti in indices_to_increment:
        measure, beat_index = find_insert_index(beat_in_measure, iti)
        song.tracks[0].measures[measure].voices[0].beats[beat_index].notes[0].type = dead_beat.notes[0].type
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

    indices_to_increment = random.sample(range(total_beats), int(EXPR_COUNT))

    # Step 2: Split these indices into groups based on the percentages
    split_counts = [int(EXPR_COUNT * p) for p in ratios ]

    # Step 3: Assign indices to groups
    grouped_indices = []
    start = 0
    for count in split_counts:
        grouped_indices.append(indices_to_increment[start : start + count])
        start += count

    print("total beats : ", total_beats)
    print("insert beats : ", EXPR_COUNT)
    for i in range(1, 8):
        # print("bend_note_" + str(i) + " :", len(grouped_indices[i - 1]))
        song = bend_note(song, beat_in_measure, grouped_indices[i - 1],"./gprofiles/gp5_templates/bend_" + str(i) + ".gp5")

    for j in range(1, 6):
        # print("trem_bar_" + str(j) + " :", len(grouped_indices[j + i - 1]))
        song = trem_note(song, beat_in_measure, grouped_indices[j + i - 1],"./gprofiles/gp5_templates/trem_" + str(j) + ".gp5")

    for k in range(1, 7):
        # print("slide_note_" + str(k) + " :", len(grouped_indices[i - 1 + j + k]))
        song = slide_note(song, beat_in_measure, grouped_indices[i - 1 + j + k],"./gprofiles/gp5_templates/slide_" + str(k) + ".gp5")

    # print("harmonic :", len(grouped_indices[21]))
    song = harmonic(song, beat_in_measure, grouped_indices[21])

    # print("vibrato :", len(grouped_indices[20]))
    song = vibrato(song, beat_in_measure, grouped_indices[20])

    #  print("hammer :", len(grouped_indices[19]))
    song = hammer(song, beat_in_measure, grouped_indices[19])

    # print("dead :", len(grouped_indices[18]))
    song = dead(song, beat_in_measure, grouped_indices[18])

    return song