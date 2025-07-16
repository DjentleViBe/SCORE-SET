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
