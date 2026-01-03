from pathlib import Path
import sys, shutil, utils
import os

# sorts the files into corresponding folders
def sort(folder_path: str):

    backup_enabler = input("Automatically backup files before sorting? (y/n): ").lower()
    if backup_enabler == "y":
        if backup(folder_path) == False:
            return

    if folder_setup(folder_path) == False:
        return

    source = Path(folder_path)

    for item in source.iterdir():
        if item.is_file():
            label = utils.get_extension(item.name)
            dest = Path(folder_path) / label
            target = utils.unique_destination(dest, item.name)
            shutil.move(item, target)
    
    print("Process completed.")
    
# stores copies of the files in case of issues
def backup(folder_path: str) -> bool:
    if utils.check_folder(folder_path, "backup") == False: 
        utils.create_folder(folder_path, "backup")
    
    source = Path(folder_path)
    dest = Path(folder_path) / "backup"
    
    # if any files exists in the directory...
    if any(dest.iterdir()):
        print("'backup' folder is not empty. Proceeding will overwrite any conflicting files.")
        if input("Proceed? (y/n) ").lower() != "y":
            if input("Continue to sort without backup? (y/n): ").lower() != "y":
                return False

    items = list(source.iterdir())
    for item in items:
        if item.is_file():
            shutil.copy(item, dest)
    return True

# makes a folder per extension in selected directory
def folder_setup(folder_path: str) -> bool:
    extensions = utils.extension_list(folder_path)
    if not extensions:
        print("No sortable files found, aborting process.")
        return False
    for extension in extensions:
        if utils.check_folder(folder_path, extension) == False:
            utils.create_folder(folder_path, extension)
    return True