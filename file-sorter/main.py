import sorter, utils

def main():
    
    folder_path = utils.file_selector("Choose a folder to sort...")

    if not folder_path:
        return # no valid folder detected
    
    sorter.sort(folder_path, True) # else, sort the folder

# “Only run main() if this file is being executed directly, not imported.”
if __name__ == "__main__":
    main()