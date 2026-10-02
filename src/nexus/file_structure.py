import os
import datetime
import tomllib
from textwrap import dedent
from . import log as Log

nexus_main_file_dir = ".nexus"
nexus_main_config_file = "config.toml"

nexus_valid_user_index_min = 1
nexus_valid_user_index_max = 899

nexus_inbox_file_dir = "000-inbox"
nexus_unmanaged_file_dir = "900-unmanaged"
nexus_unknown_file_dir = "901-unknown"
nexus_image_attachments_file_dir = "997-images"
nexus_archive_file_dir = "998-archive"
nexus_template_file_dir = "999-template"

nexus_file_structure = [
        nexus_inbox_file_dir,
        nexus_unmanaged_file_dir,
        nexus_unknown_file_dir,
        nexus_image_attachments_file_dir,
        nexus_archive_file_dir,
        nexus_template_file_dir
    ]


def nexus_init_new_space(path: str):

    nexus_make_nexus_dir_and_cd(path)
    nexus_init_nexus_space()
    nexus_init_nexus_directories()


def nexus_init_nexus_directories():
    for directory in nexus_file_structure:
        nexus_create_directory(directory)


def nexus_init_nexus_space():
    if os.path.exists(nexus_main_file_dir):
        Log.AssertTrue(f"{nexus_main_file_dir} already exists in current folder\nCancelling...")
    nexus_create_directory(nexus_main_file_dir)

    with open(f"{nexus_main_file_dir}/{nexus_main_config_file}", "a") as configFile:
        date = datetime.date.today()

        defaultConfig = dedent(f"""
            # nexus-space-config

            [nexus-space]
            dateOfCreation = "{date}"

            [nexus-directories]
            nexus_inbox_file_dir = "000-inbox"
            nexus_unmanaged_file_dir = "900-unmanaged"
            nexus_unknown_file_dir = "901-unknown"
            nexus_image_attachments_file_dir = "997-images"
            nexus_archive_file_dir = "998-archive"
            nexus_template_file_dir = "999-template"

            #EOF
        """)

        configFile.write(defaultConfig)


def nexus_make_nexus_dir_and_cd(path):
    nexus_create_directory(path)
    nexus_change_dir(path)


def GetConfigFileData():
    # Check if on nexus space
    isExists = os.path.exists(nexus_main_file_dir)

    if not isExists:
        Log.AssertTrue(f"Didn't find '{nexus_main_file_dir}' in current directory")
        return

    try:
        with open(f"{nexus_main_file_dir}/{nexus_main_config_file}", "r") as file:
            configFile = file.read()
            return configFile
    except FileNotFoundError:
        Log.AssertTrue(f"Didn't find '{nexus_main_config_file}' in '{nexus_main_file_dir}'")
    except Exception as e:
        Log.AssertTrue(f"Error: {e}")


def GetInboxDirectory():
    try:
        configFile = GetConfigFileData()
        config = tomllib.loads(configFile)
        inbox_dir = config["nexus-directories"]["nexus_inbox_file_dir"]
        return inbox_dir
    except Exception as e:
        Log.AssertTrue(f"ErrorL {e}")       


def nexus_change_dir(path):

    exists = os.path.exists(path)
    isDir = os.path.isdir(path)

    if exists and isDir:
        if path != ".":
            Log.LogCore(f"Changing directory to {path}")
        os.chdir(path)
    else:
        Log.AssertTrue("Unknown directory")


def nexus_create_directory(path):

    exists = os.path.exists(path)
    isDir = os.path.isdir(path)

    if exists and not isDir:
        # prompt to remove / mv that to file to file.bak
        Log.LogCore(f"File exists with name {path}, move / delete the file before proceding")

    elif exists and isDir:
        if path != ".":
            Log.LogCore(f"Directory already exists , skipping creating '{path}'")
            Log.LogCore(f"Failed to create file, removing nexus space")

    elif not exists:
        # do full initialize
        try:
            os.mkdir(path)
            Log.LogCore(f"Initialized a directory: {path}")
        except PermissionError:
            Log.AssertTrue(f"Permission denied: Unable to create {path}")
        except Exception as e:
            Log.AssertTrue(f"An error occured: {e}")
