import sys
from . import log as Log
from . import file_structure as FileStructure
from . import new_file as New


def main():

    number_of_args = len(sys.argv)
    if number_of_args < 2:
        Log.PrintNexusUsage()
        return

    function_to_call = sys.argv[1]

    match function_to_call:
        case "init":
            path = "."
            if number_of_args >= 3:
                path = sys.argv[2]

            FileStructure.nexus_init_new_space(path)
        case "new":
            fileName = ""
            if number_of_args >= 3:
                fileName = sys.argv[2]
            else:
                Log.AssertTrue("No file name specified")
                Log.PrintNexusUsage()

            New.NewNote(fileName)
        case _:
            Log.PrintNexusUsage()


if __name__ == "__main__":
    main()
