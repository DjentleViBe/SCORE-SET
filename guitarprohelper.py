import guitarpro as gp
from guitarhelper import find_string_and_fret, find_closest_string_and_fret

def clip_to_nearest_duration(ticks, ticks_per_beat):
    # Precompute standard durations in ticks
    duration_map = {
        int(ticks_per_beat * 4): 1,       # whole
        int(ticks_per_beat * 2): 2,       # half
        int(ticks_per_beat * 1): 4,       # quarter
        int(ticks_per_beat * 0.5): 8,     # eighth
        int(ticks_per_beat * 0.25): 16,   # 16th
        int(ticks_per_beat * 0.125): 32,  # 32nd
        int(ticks_per_beat * 0.0625): 64  # 64th
    }
    # Find closest
    closest_ticks = min(duration_map.keys(), key=lambda x: abs(x - ticks))
    return duration_map[closest_ticks]


def decompose_duration(duration_beats):
    """
    Decomposes a float duration in beats into standard note values.
    Returns a list of durations that sum to the original value.
    Example: 2.25 -> [2, 0.25]
    """
    note_values = [4, 2, 1, 0.5, 0.25, 0.125, 0.0625]
    result = []
    remaining = duration_beats

    for val in note_values:
        while remaining >= val - 1e-4:  # Small epsilon for floating point tolerance
            result.append(val)
            remaining -= val
            if abs(remaining) < 1e-4:
                return result

    if remaining > 0:
        print(f"Warning: Unmatched remaining duration: {remaining}")
    return result

def insert_rest_beat(start_tick, ticks_per_beat, voice):
    """
    Inserts a rest at the beginning if the first note is delayed.

    Args:
        start_tick (int): Time before first note in ticks.
        ticks_per_beat (int): MIDI resolution.
        voice (gp.Voice): Voice to insert the rest into.
    """
    mapping = {
        4.0: gp.models.Duration.whole,
        2.0: gp.models.Duration.half,
        1.0: gp.models.Duration.quarter,
        0.5: gp.models.Duration.eighth,
        0.25: gp.models.Duration.sixteenth,
        0.125: gp.models.Duration.thirtySecond,
        0.0625: gp.models.Duration.sixtyFourth,
    }
    if start_tick <= 0:
        return  # No rest needed

    duration_val =0
    rest_beat = gp.Beat(voice=voice)
    rest_beat.status = gp.models.BeatStatus.rest
    # duration_val = clip_to_nearest_duration(duration_ticks, ticks_per_beat)
    rest_durations = decompose_duration(start_tick / ticks_per_beat)
    for rt in rest_durations:
        rest_beat = gp.Beat(voice=voice)
        rest_beat.status = gp.models.BeatStatus.rest
        rest_beat.duration.value = mapping.get(rt, None)
        voice.beats.append(rest_beat)
        duration_val+= rt

    return voice, 1 / duration_val


def makegpro(duration, start, noteval, string_tuning, tolerence):
    song = gp.models.Song()
    song.artist = "DjentleViBe"
    song.tempo = 120  # Set the tempo
    song.tracks[0].name = "Guitar"
    song.tracks[0].channel.instrument = 30

    song.tracks[0].measures[0].hasTimeSignature  = True 
    song.tracks[0].measures[0].timeSignature.denominator.value = 4
    tot_duration = 0
    current_measure = song.tracks[0].measures[0]  # start with the first
    voice = current_measure.voices[0]
    note_collect = []
    beat_collect = []
    string_collect = []
    fret_collect = []
    kval_collect = []
    l_val = 0
    k_val = 0
    reuse_last_beat = False

    # voice, tot_duration = insert_rest_beat(start[0], 480, voice)
    for n_val, note in enumerate(noteval):
        if k_val != 0:
            if start[n_val] - start [n_val - 1] <= tolerence:
                # print("barred",start[n_val],start[n_val-1])
                reuse_last_beat = True

        if reuse_last_beat:
            current_beat = beat_collect[k_val - 1]
            duration[n_val] = max(beat_collect[k_val - 1].duration.value, duration[n_val])
            beat_collect[k_val - 1].duration.value = duration[n_val]
            current_beat.status = gp.models.BeatStatus.normal
            reuse_last_beat = False
            string_number, fret = find_string_and_fret(note, string_tuning, 23)
            used_strings = {n.string for n in current_beat.notes}
            if string_number in used_strings:
                for shift in [-12, -24, 12]:  # Try down 1 octave, 2 octaves, then up 1 octave
                    shifted_note = note + shift
                    fret, alt_string = find_closest_string_and_fret(shifted_note, used_strings, string_tuning)
                    if fret is not None:
                        note = shifted_note
                        string_number = alt_string
                        break
                else:
                    print(f"Warning: Skipping note {note} at tick {start[n_val]} due to string conflict.")
                    continue
            kval_collect.append(k_val - 1)
        else:
            string_number, fret = find_string_and_fret(note, string_tuning, 23)
            current_beat = gp.Beat(voice=voice)
            current_beat.status = gp.models.BeatStatus.normal
            beat_collect.append(current_beat)
            voice.beats.append(current_beat)
            kval_collect.append(k_val)
            k_val += 1
    
        string_collect.append(string_number)
        fret_collect.append(fret)
        note_collect.append(gp.Note(beat=current_beat))
        note_collect[l_val].type = gp.models.NoteType.normal
        note_collect[l_val].value = fret
        note_collect[l_val].string = string_number
        note_collect[l_val].beat.duration.value = duration[n_val]
        current_beat.notes.append(note_collect[l_val])
        tot_duration = sum(1 / beat.duration.value for beat in beat_collect)
        l_val += 1

        if tot_duration >= 1:
            track = song.tracks[0]
            header = gp.models.MeasureHeader(number=len(track.measures))
            # Append the header to the song
            song.measureHeaders.append(header)
            # Now create the measure with the header
            new_measure = gp.models.Measure(track=track, header=header)
            song.tracks[0].measures.append(new_measure)
            voice = new_measure.voices[0]  # reset to new measure's voice
            tot_duration = 0
            k_val = 0
            l_val = 0
            beat_collect = []
            note_collect = []
        

    #print(string_collect)
    #print(fret_collect)
    #print(kval_collect)
    return song

def writegpro(filename, song):
    """write gpro file to disk"""
    # Save the song to a Guitar Pro file
    with open(filename + ".gp5", 'wb') as file:
        gp.write(song, file)