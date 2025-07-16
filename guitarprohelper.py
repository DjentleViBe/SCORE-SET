import guitarpro as gp

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

def insert_rest_beat(start_tick, ticks_per_beat, voice):
    """
    Inserts a rest at the beginning if the first note is delayed.

    Args:
        start_tick (int): Time before first note in ticks.
        ticks_per_beat (int): MIDI resolution.
        voice (gp.Voice): Voice to insert the rest into.
    """
    if start_tick <= 0:
        return  # No rest needed

    duration_ticks = start_tick
    duration_val = clip_to_nearest_duration(duration_ticks, ticks_per_beat)

    rest_beat = gp.Beat(voice=voice)
    rest_beat.status = gp.models.BeatStatus.rest
    rest_beat.duration.value = duration_val

    voice.beats.append(rest_beat)

    return voice, 1 / duration_val