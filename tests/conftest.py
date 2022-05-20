import sys
from os.path import abspath, dirname, join

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)
infra_dir_path = join(root_dir, 'infra')

pytest_plugins = [
]
