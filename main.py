from scoreset import scoreset, midi_extract
from fileutils import zip_directory, datasetdownload, datasetdownload_gdown
from techniques import create_accents
import config as cfg

if __name__ == "__main__":
    create_accents()

    if cfg.DOWNLOAD:
        if cfg.DATASET == 0 or cfg.DATASET == 2:
            print("Maestro dataset : Downloading")
            datasetdownload("https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip", "maestro-v3.0.0")
            print("Maestro dataset : Download complete!")
        if cfg.DATASET == 1 or cfg.DATASET == 2:
            print("GiantMIDI dataset : Downloading")
            datasetdownload_gdown("https://drive.google.com/drive/folders/1Stz3CAvMoplo79LR5I3onMWRelCugBYS?usp=sharing", "./midis_dataset")
            print("GiantMIDI dataset : Download complete")

    if cfg.PROCESS:
        if cfg.DATASET == 0 or cfg.DATASET == 2:
            print("Maestro dataset : Processing started")
            scoreset("./maestro_dataset_gpro", "./maestro-v3.0.0", [])
            print("Maestro dataset : Processing completed!")
        if cfg.DATASET == 1 or cfg.DATASET == 2:
            print("GiantMIDI dataset : Processing started!")
            exclude_files = ["Gumpelzhaimer, Adam, Was mein Gott will, das g'scheh allzeit, BTQegBbW13A.mid",
                            "Stahl, William C., Golden Bell Waltz, gmrKI53VUVQ.mid"]
            scoreset("./midis_dataset_gpro", "./midis_dataset", exclude_files)
            print("GiantMIDI dataset : Processing completed!")

    if cfg.CREATE_ZIP:
        if cfg.DATASET == 0 or cfg.DATASET == 2:
            print("Creating .zip file")
            zip_directory("./maestro_dataset_gpro", "maestro_gpro-v1.0.0.zip")
            print(".zip file created!")
        if cfg.DATASET == 1 or cfg.DATASET == 2:
            print("Creating .zip file")
            zip_directory("./midis_dataset_gpro", "midis_gpro-v1.0.0.zip")
            print(".zip file created!")
