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
        self.cancel_event = threading.Event()
        
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

        # cancel button
        self.cancel_button = ttk.Button(mainframe, text="Cancel", state="disabled", command=self.on_cancel_clicked)
        self.cancel_button.grid(column=3, row=5, sticky="s")

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

    # browse button functionality, and conditions for sort button
    def on_browse_clicked(self):
        folder = (filedialog.askdirectory(title="Choose folder to sort..."))
        if folder:
            self.folder_path.set(folder)
            self.sort_button.config(state="normal")
            self.status.set("Ready to sort")
        pass

    # cancel the sorting process
    def on_cancel_clicked(self):
        self.cancel_event.set()
        self.cancel_button.config(state="disabled")
        self.status.set("Cancelling at safe point...")
        return
    
    # when sort button is pressed, run a secondary thread to sort to not interupt UI
    def on_sort_clicked(self):
        self.cancel_event.clear()
        if not self.folder_path.get():
            self.status.set("Please choose an appropriate folder")
            return
        
        path = Path(self.folder_path.get())

        if not path.exists() or not path.is_dir():
            self.status.set("Invalid folder chosen")
            return
        
        self.progress["value"] = 0
        
        if self.backup_enabler.get() == True:
            self.status.set("Backing up and sorting files...")
        else:
            self.status.set("Sorting files...")

        self.sort_button.config(state="disabled")
        self.backup_checkbox.config(state="disabled")
        self.cancel_button.config(state="normal")
        
        # run this function in the background
        threading.Thread(target=self.run_sort, daemon=True).start() # daemon makes thread 'die' when the app closes
        return

    # runs the sort function, using the thread_progress function to get updated values for UI
    def run_sort(self):
        success = sorter.sort(
            self.folder_path.get(),
            self.backup_enabler.get(),
            cancel=self.cancel_event,
            on_progress=self.thread_progress
        )

        # tell the UI thread we're done 
        # tells tkinter when it has the chance to run this function using the sucess as its arg
        self.root.after(0, self.on_sort_finished, success)
        return
    
    # background thread gets the needed values to update progress and sends them
    def thread_progress(self, current, total):
        self.root.after(
            0,
            self.update_progress,
            current,
            total
        )
        return
    
    # takes the calculated values from background thread and updates UI
    def update_progress(self, current, total):
        percent = round((current / total) * 100)
        self.progress["value"] = percent

        # forces Tkinter to process pending redraw events immediately
        self.progress.update_idletasks()
        return
    
    # informs user if sorting was sucessful or not, resets buttons
    def on_sort_finished(self, success):
        if success:
            self.status.set("Sorting was successful")
        else:
            self.status.set("Sorting aborted")

        self.sort_button.config(state="normal")
        self.backup_checkbox.config(state="normal")
        self.cancel_button.config(state="disabled")
        return

    # allows triggering of the sort button with enter key if available   
    def trigger_sort(self, event=None):
        if str(self.sort_button['state']) == 'normal':
            self.sort_button.invoke()
