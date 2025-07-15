import matplotlib.pyplot as plt
import os
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
'DEAD_NOTE',
'SLIDE_NOTE_1',
'SLIDE_NOTE_2',
'SLIDE_NOTE_3',
'SLIDE_NOTE_4',
'SLIDE_NOTE_5',
'SLIDE_NOTE_6',
'HAMMER',
'VIBRATO',
'HARMONIC']

VALUES = [2477, 
804,
1256,
2025,
1765,
0,
0,
321,
1056,
0,
0,
0,
2253,
6165,
2304,
62,
30,
669,
680,
2140,
250,
3013]

total = sum(VALUES)
print(total)

ratios = [v / total for v in VALUES]

plt.figure(figsize=(6,4))
plt.title('Accent occurences')
plt.bar(LABELS, ratios, color = 'k')
plt.ylabel('Count ratio')
#plt.tight_layout()
plt.xticks(rotation = 90, ha = 'right', fontsize = 7)
plt.subplots_adjust(bottom=0.25)
plt.savefig(current_dir + '/accent_probability.pdf', dpi = 200)