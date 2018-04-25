from cx_Freeze import setup, Executable
import sys
base = 'WIN32GUI' if sys.platform == "win32" else None


executables = [Executable("upload.py", base=base, icon='myapp.ico')]

packages = []
include_files=['myapp.ico']
options = {
    'build_exe': {
        'packages':packages,
        'include_files': include_files
    },

}

setup(
    name = "upload",
    options = options,
    version = "1.0",
    description = 'upload tool',
    executables = executables
)