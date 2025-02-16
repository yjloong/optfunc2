from optfunc2 import cmdline, cmdline_default, cmdline_start
import os

@cmdline_default
def list_files(directory: str = ".", show_size: bool = False):
    """List files in a directory.

    Args:
        directory (str, optional): Target directory. Defaults to ".".
        show_size (bool, optional): Whether to show size of file. Defaults to False.
    """
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if show_size and os.path.isfile(path):
            print(f"{f} ({os.path.getsize(path)} bytes)")
        else:
            print(f)

if __name__ == "__main__":
    cmdline_start(header_doc="📁 file manager", has_abbrev=True)