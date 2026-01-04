import sorter, utils

def main():
    
    folder_path = utils.file_selector("Choose a folder to sort...")

    if not folder_path:
        print("No valid folder selected.")
        return
    
    print(f"Selected folder: {folder_path}")

    sorter.sort(folder_path)


# “Only run main() if this file is being executed directly, not imported.”
if __name__ == "__main__":
    main()