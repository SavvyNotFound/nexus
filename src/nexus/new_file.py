import os
import datetime
import subprocess

from . import file_structure as FileStructure
from . import log as Log

def NewNote(fileName: str):
    if os.path.exists(FileStructure.GetInboxDirectory()):
        if os.path.isdir(FileStructure.GetInboxDirectory()):
            make_file_in_inbox_and_open(fileName)
        else:
            # Exists but isn't a dir
            Log.LogCore(f"{FileStructure.GetInboxDirectory()} exists but isn't a directory, move it and re-run the command")
    else:
        # Doesn't exist
        Log.LogCore(f"{FileStructure.GetInboxDirectory()} is missing, initialize one? [(Y)es, (n)o]")
        userInput = input()
        init = True
        match userInput.lower():
            case "y":
                pass
            case "":
                pass
            case "n":
                init = False
            case _:
                init = False

        if init:
            FileStructure.nexus_create_directory(FileStructure.GetInboxDirectory())
            make_file_in_inbox_and_open(fileName)
        

def make_file_in_inbox_and_open(fileName):
    filePath = f"{FileStructure.GetInboxDirectory()}/{fileName}"

    if os.path.exists(f"{filePath}.md"):
        append = 1
        while os.path.exists(f"{filePath}-{append}.md"):
            append += 1
        filePath = f"{filePath}-{append}"

    filePath = f"{filePath}.md"

    with open(filePath, "w") as file:
        date = str(datetime.date.today())
        newFileData = f"---\ncreated: {date}\ntype: nexus-note\n---"
        file.write(newFileData)

    if "EDITOR" in os.environ:
        editor = str(os.getenv('EDITOR'))
        if editor != "":
            subprocess.run([editor, filePath])
    else:
        Log.LogCore("Failed to find an editor")
