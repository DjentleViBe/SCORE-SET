"""This script generates .zip datasets containing .gp5 files
"""
from scoreset import scoreset
from fileutils import zip_directory, datasetdownload, datasetdownload_gdown, create_or_clear_directory
from techniques import create_accents
import config as cfg
import shutil
import os

if __name__ == "__main__":
    create_accents()

    if cfg.DOWNLOAD:
        if cfg.DATASET in (0, 2):
            print("Maestro dataset : Downloading")
            datasetdownload("https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip", "maestro-v3.0.0")
            print("Maestro dataset : Download complete!")
        if cfg.DATASET in (1, 2):
            print("GiantMIDI dataset : Downloading")
            datasetdownload_gdown("https://drive.google.com/drive/folders/1Stz3CAvMoplo79LR5I3onMWRelCugBYS?usp=sharing", "./midis_dataset")
            print("GiantMIDI dataset : Download complete")

    if cfg.PROCESS:
        if cfg.DATASET in (0, 2):
            print("Maestro dataset : Processing started")
            scoreset("./maestro_dataset_gpro", "./maestro-v3.0.0", [])
            print("Maestro dataset : Processing completed!")
        if cfg.DATASET in (1, 2):
            print("GiantMIDI dataset : Processing started!")
            exclude_files = ["Gumpelzhaimer, Adam, Was mein Gott will, das g'scheh allzeit, BTQegBbW13A.mid",
                            "Stahl, William C., Golden Bell Waltz, gmrKI53VUVQ.mid"]
            scoreset("./midis_dataset_gpro", "./midis_dataset", exclude_files)
            print("GiantMIDI dataset : Processing completed!")

    if cfg.CREATE_ZIP:
        create_or_clear_directory("./SCORE-SET_v" + cfg.VERSION)
        if os.path.exists("./SCORE-SET_v" + cfg.VERSION + ".zip"):
            os.remove("./SCORE-SET_v" + cfg.VERSION + ".zip")
        shutil.copytree("./gprofiles/gp5_templates", os.path.join("./SCORE-SET_v" + cfg.VERSION, os.path.basename("./gprofiles/gp5_templates")))
        if cfg.DATASET in (0, 2):
            shutil.copytree("./maestro_dataset_gpro/maestro-v3.0.0", os.path.join("./SCORE-SET_v" + cfg.VERSION, os.path.basename("./maestro_dataset_gpro/maestro-v3.0.0")))
        if cfg.DATASET in (1, 2):
            shutil.copytree("./midis_dataset_gpro/midis_dataset", os.path.join("./SCORE-SET_v" + cfg.VERSION, os.path.basename("./midis_dataset_gpro/midis_dataset")))
        print("Creating .zip file")
        zip_directory("./SCORE-SET_v" + cfg.VERSION, "SCORE-SET_v" + cfg.VERSION + ".zip")
        print(".zip file created!")
