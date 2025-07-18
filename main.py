from scoreset import scoreset
from fileutils import zip_directory, datasetdownload
from techniques import create_accents

if __name__ == "__main__":
    # datasetdownload()
    # create_accents()
    print("Processing started!")
    scoreset("./maestro_dataset_gpro", "./maestro_dataset")
    print("Processing completed!")

    print("Creating .zip file")
    zip_directory("./maestro_dataset_gpro", "maestro_gpro-v1.0.0.zip")
    print(".zip file created!")