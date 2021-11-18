import sys
from os.path import dirname as d
from os.path import abspath, join
# Adds the src folder to the local path
root_dir = join(d(d(abspath(__file__))), 'src')
sys.path.append(root_dir)
