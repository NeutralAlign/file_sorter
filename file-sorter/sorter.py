from pathlib import Path
import sys, shutil, utils
import os

# sorts the files into corresponding folders
def sort(folder_path: str, extensions: set):

    source = backup(folder_path)
    folder_setup(folder_path, extensions)

    for extension in extensions:
        dest = Path(folder_path) / f"{extension}"
        for item in source.iterdir():
            if item.is_file():
                if os.path.splitext(item.name)[1].lstrip(".") == extension:
                    target = utils.unique_destination(dest, item.name)
                    shutil.move(item, target)

                elif os.path.splitext(item.name)[1].lstrip(".") == "":
                    unknown = Path(folder_path) / "unknown"
                    target = utils.unique_destination(unknown, item.name)
                    shutil.move(item, target)
    
    print("Process completed.")
    


# stores copies of the files in case of issues
def backup(folder_path: str):
    if utils.check_folder(folder_path, "backup") == False: 
        utils.create_folder(folder_path, "backup")
    
    source = Path(folder_path)
    dest = Path(folder_path) / "backup"
    
    # if any files exists in the directory...
    if any(dest.iterdir()):
        print("Backup folder is not empty. Proceeding will overwrite conflicting files.")
        if input("Proceed? (y/n) ").lower() != "y":
            print("Process aborted!")
            sys.exit()
    for item in source.iterdir():
        if item.is_file():
            shutil.copy(item, dest)
    return source

# makes a folder per extension in selected directory
def folder_setup(folder_path: str, extensions: set):
    for extension in extensions:
        if utils.check_folder(folder_path, extension) == False:
            utils.create_folder(folder_path, extension)
    return