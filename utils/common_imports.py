import sys
import os

# Add the parent directory to the Python path 
def add_parent_dir():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))