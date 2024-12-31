import sys
import os

# Add the parent directory to the Python path biar bisa import file py di folder lain
def add_parent_dir():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))