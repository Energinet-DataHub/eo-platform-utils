import os
import sys

# Adds the src folder to the local path
test_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(test_dir, '..', 'src')
sys.path.append(root_dir)
