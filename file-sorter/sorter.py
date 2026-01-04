from pathlib import Path
import shutil, utils


# sorts the files into corresponding folders
def sort(folder_path: str, backup_enabler: bool) -> bool:
    if backup_enabler:
        if not backup(folder_path, True):
            return False

    if not folder_setup(folder_path):
        return False

    source = Path(folder_path)
    items = list(source.iterdir())

    for item in items:
        if item.is_file():
            label = utils.get_extension(item.name)
            dest = source / label
            target = utils.unique_destination(dest, item.name)
            shutil.move(item, target)

    return True
    
# stores copies of the files in case of issues
def backup(folder_path: str, allow_overwrite: bool) -> bool:
    if not utils.check_folder(folder_path, "backup"):
        utils.create_folder(folder_path, "backup")
    
    source = Path(folder_path)
    dest = source / "backup"
    
    # do not backup under these conditions
    if any(dest.iterdir()) and not allow_overwrite:
        return False
    
    # else, backup files in a folder
    items = list(source.iterdir()) # safer than messing with files directly

    for item in items:
        if item.is_file():
            shutil.copy(item, dest)

    return True

# makes a folder per extension in selected directory
def folder_setup(folder_path: str) -> bool:
    extensions = utils.extension_list(folder_path)

    if not extensions:
        return False # no files were found, abort process
    
    for extension in extensions:
        if not utils.check_folder(folder_path, extension):
            utils.create_folder(folder_path, extension)

    return True