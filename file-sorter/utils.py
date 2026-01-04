import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os

# returns the path to a folder directory
def file_selector(info: str):
    root = tk.Tk()
    root.withdraw() # hides window as nothing there yet
    folder_path = filedialog.askdirectory(title=info)
    return folder_path

# returns a list of extensions that exist in a folder directory
def extension_list(folder_path: str):
    extensions = set()
    folder = Path(folder_path)
    items = list(folder.iterdir())

    for item in items:
        if item.is_file():
            extensions.add(get_extension(item.name))

    return extensions

# return the extension type (without a dot)
def get_extension(filename: str):
    extension = os.path.splitext(filename)[1].lstrip(".")

    if extension == "":
        extension = "unknown"

    return extension

# creates a folder in a directory
def create_folder(folder_path: str, folder_name: str):
    path = Path(folder_path) / folder_name
    
    try:
        path.mkdir(parents=True, exist_ok=True)
        print(f"Directory '{folder_path}/{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{folder_path}/{folder_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{folder_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

# makes sure that a folder doesn't exist already
def check_folder(folder_path: str, folder_name: str = ""):
    path = Path(folder_path) / folder_name
    return path.is_dir()

# checks if a file is unique, if not, assigns a number to avoid overwriting
def unique_destination(dest_path: Path, filename: str) -> Path:
    target = dest_path / filename
    counter = 1

    while target.exists():
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        target = dest_path / f"{stem} ({counter}){suffix}"
        counter += 1

    return target