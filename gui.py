import ctypes
from gooey import Gooey, GooeyParser, local_resource_path

from process import *

@Gooey(program_name='Blank Creator', image_dir=local_resource_path('.'))
def gui_main():
    parser = GooeyParser(description="Creating blanks for C language source code files")
    parser.add_argument('source_dir', widget='DirChooser', help="The directory containing source code files to be processed.")
    args = parser.parse_args()
    main(args.source_dir)

if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass
    gui_main()