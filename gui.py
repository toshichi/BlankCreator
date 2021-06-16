import ctypes
import sys
from gooey import Gooey, GooeyParser, local_resource_path

from process import *


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


@Gooey(program_name='Blank Creator', image_dir=local_resource_path('.'))
def gui_main():
    parser = GooeyParser(
        description="Creating blanks for C language source code files")
    parser.add_argument('source_dir', widget='DirChooser',
                        help="The directory containing source code files to be processed.")
    args = parser.parse_args()
    main(args.source_dir)


if __name__ == "__main__":
    # deal with windows high dpi
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass
    sys.stdout = Unbuffered(sys.stdout)
    gui_main()
