import os
import subprocess
version_py = os.path.join(os.path.dirname(__file__), 'version.py')

try:
    version_git = subprocess.check_output(["git", "describe"]).rstrip()
except:
    version_git = "0.0.0-error"


__version__ = version_git