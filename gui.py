from gooey import Gooey, GooeyParser

from process import *

@Gooey(program_name='Blank Creator', image_dir='.')
def gui_main():
    parser = GooeyParser(description="Creating blanks for C language source code files")
    parser.add_argument('source_dir', widget='DirChooser', help="The directory containing source code files to be processed.")
    args = parser.parse_args()
    main(args.source_dir)

if __name__ == "__main__":
    gui_main()