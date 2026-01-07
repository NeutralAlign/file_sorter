import tkinter as tk
from ui import FileSorterUI

def main():

    root = tk.Tk() # create main window
    ui = FileSorterUI(root) # builds ui to the window, can be used to inspect objects of the class
    root.mainloop() # tk event loop

# “Only run main() if this file is being executed directly, not imported.”
if __name__ == "__main__":
    main()