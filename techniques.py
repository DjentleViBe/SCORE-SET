"""Techniques list"""
import os
import matplotlib.pyplot as plt
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

LABELS = ['BEND_NOTE_1',
'BEND_NOTE_2',
'BEND_NOTE_3',
'BEND_NOTE_4',
'BEND_NOTE_5',
'BEND_NOTE_6',
'BEND_NOTE_7',
'TREM_BAR_1',
'TREM_BAR_2',
'TREM_BAR_3',
'TREM_BAR_4',
'TREM_BAR_5',
'SLIDE_NOTE_1',
'SLIDE_NOTE_2',
'SLIDE_NOTE_3',
'SLIDE_NOTE_4',
'SLIDE_NOTE_5',
'SLIDE_NOTE_6',
'DEAD_NOTE',
'HAMMER',
'VIBRATO',
'HARMONIC',
'PALM_MUTE']

VALUES = [758,
0,
45,
0,
880,
212,
1230,
104,
0,
355,
837,
72,
6000,
1831,
29,
0,
635,
666,
918,
933,
11,
3001,
31930]

def create_accents():
    """Create statistics of various accents"""
    total = sum(VALUES)
    total = 6290 * 32
    ratios = [v / total for v in VALUES]

    plt.figure(figsize=(6,4))
    plt.title('Accent occurences')
    plt.bar(LABELS, ratios, color = 'k')
    plt.ylabel('Count ratio')
    plt.yscale('log')
    #plt.tight_layout()
    plt.xticks(rotation = 90, ha = 'right', fontsize = 7)
    plt.subplots_adjust(bottom=0.25)
    plt.savefig(current_dir + '/_paper/accent_probability.pdf', dpi = 200)
