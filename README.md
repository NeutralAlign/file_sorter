# File Sorter

#### Program Outline
Allows the user to choose a folder and sort files into specific folders based on their extension via a UI.

#### Running the project via source

Run 'python project.py' to run the program from the source code when cloned.

#### Usage

Opening the program opens a user interface where you can:

+ Pick a folder to sort files by their extensions.
+ Check a box to create backup copies of your files.
+ Pressing 'Sort' will start the sorting process.
+ Pressing 'Cancel' will terminate the sorting process.

#### What it does

+ Upon selecting a folder, creates a backup of files within (if checked).
+ Creates multiple folders within the user selected directory, with the names being the extensions of every file.
+ Files are moved into their respective folders depending on their extension.
+ Progress is tracked with dynamic progress bar.

#### Safety notes
+ Backing up will backup files in a new folder in the chosen directory (../folder/backup/FILES_HERE).
+ Note that any files in the backup folder that have the same file name will be overwritten if backup is selected (ensure to move them after a sort is completed).
+ Messages are present which indicate success or failure.
+ Files must exist in the folder for sorting to be activated.

#### Future Ideas

+ More details regarding the sorting in the UI.
+ Update UI design to be more attractive.
+ Add another button to accept / refuse overwriting of backup or automatically handle these situations with renaming.
+ More to be added.



