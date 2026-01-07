import tkinter as tk
from tkinter import ttk, filedialog
import sorter, threading
from pathlib import Path

class FileSorterUI():

    def __init__(self, root):

        self.root = root
        root.title("File Sorter")
        
        # folder to sort path text box
        self.folder_path = tk.StringVar()
        self.backup_enabler = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Choose a valid folder to continue")
        
        # frame is child to main window, parent to widgets placed inside it
        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky="nwes")

        folder_entry = ttk.Entry(mainframe, state='readonly', width=40, textvariable=self.folder_path)
        folder_entry.grid(column=2, row=1, sticky="we")

        self.backup_checkbox = ttk.Checkbutton(mainframe, text='Backup files', 
            variable=self.backup_enabler)
        self.backup_checkbox.grid(column=3, row=3, sticky="we")

        ttk.Button(mainframe, text="Browse...", command=self.on_browse_clicked).grid(column=3, row=1, sticky="e")

        # chaining resulted in sort_button becoming 'None', we seperate it here
        self.sort_button = ttk.Button(mainframe, text="Sort", state='disabled', command=self.on_sort_clicked)
        self.sort_button.grid(column=2, row=5, sticky="s")

        ttk.Label(mainframe, text="Folder to sort:").grid(column=1, row=1, sticky="w")
        ttk.Label(mainframe, textvariable=self.status).grid(column=2, row=3, sticky="s")
        ttk.Label(mainframe, text="Progress:").grid(column=1, row=4, sticky="w")

        self.progress = ttk.Progressbar(mainframe, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(column=2, row=4, columnspan=1, sticky="s")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        root.bind("<Return>", self.trigger_sort)


    def update_progress(self, current, total):
        percent = round((current / total) * 100)
        self.progress["value"] = percent
        self.progress.update_idletasks()

    def trigger_sort(self, event=None):
        if str(self.sort_button['state']) == 'normal':
            self.sort_button.invoke()

    def on_sort_clicked(self):
        if not self.folder_path.get():
            self.status.set("Please choose an appropriate folder")
            return
        
        path = Path(self.folder_path.get())

        if not path.exists() or not path.is_dir():
            self.status.set("Invalid folder chosen")

        self.sort_button.config(state="disabled")
        self.backup_checkbox.config(state="disabled")
        
        self.progress["value"] = 0

        success = sorter.sort(
            self.folder_path.get(),
            self.backup_enabler.get(),
            on_progress=self.update_progress
        )

        if success:
            self.status.set("Sorting was successful")
        else:
            self.status.set("Sorting aborted")

        self.sort_button.config(state="normal")
        self.backup_checkbox.config(state="normal")
        

    def on_browse_clicked(self):
        folder = (filedialog.askdirectory(title="Choose folder to sort..."))
        if folder:
            self.folder_path.set(folder)
            self.sort_button.config(state="normal")
            self.status.set("Ready to sort")
        pass
            

