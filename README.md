# SCORE-SET
SCORE-SET [1] is a dataset composed of .gp5 [2] transcribed files, derived from the GiantMIDI [3] and MAESTRO [4] datasets. Guitar-specific expressions have been added based on the statistical patterns illustrated in [Accents](./_paper/accent_probability.pdf)

# Download
The files can either be downloaded directly or prepared with the scripts provided in the repository.
## Direct method
The dataset can be obtained from the latest [release](https://github.com/DjentleViBe/SCORE-SET/releases).

## Preparation method
It is recommended to run the following in an environment: 
1. Clone the repository:

```bash
git clone https://github.com/DjentleViBe/SCORE-SET.git
```

2. Install the requirements
```bash
pip install -r requirements.txt
```

3. Download ```gp5_templates.zip``` from the latest [release](https://github.com/DjentleViBe/SCORE-SET/releases). Extract the contents into ```./gprofiles/gp5_templates``` folder.

4. Run

```bash
python main.py
```

Dataset ```SCORE-SET_v*.*.*.zip``` containing ```.gp5``` files are output to the project root directory.

# References
[1]

[2] https://www.guitar-pro.com/

[3]  Qiuqiang Kong, Bochen Li, Jitong Chen, and Yuxuan Wang. "GiantMIDI-Piano: A large-scale MIDI dataset for classical piano music." arXiv preprint arXiv:2010.07061 (2020). [https://arxiv.org/pdf/2010.07061](https://arxiv.org/pdf/2010.07061)

[4] Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang,
  Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling
  Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."
  In International Conference on Learning Representations, 2019.
  [https://openreview.net/forum?id=r1lYRjC9F7]()

