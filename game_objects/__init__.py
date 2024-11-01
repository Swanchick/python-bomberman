from os import listdir
from os.path import dirname, isdir

from importlib import import_module

from .network_objects import *

package_name = __name__
package_dir = dirname(__file__)
ignored_units = ["__pycache__", "__init__.py"]

def initialize_all(dir, import_dirs: list[str]=[]):
    for unit in listdir(dir):
        if unit in ignored_units:
            continue

        full_path = f"{dir}\\{unit}"
        
        if isdir(full_path):
            import_dirs.append(unit)

            initialize_all(full_path, import_dirs)
            
            import_dirs.pop(-1)

            continue

        if not unit.endswith(".py"):
            continue

        print(".".join(import_dirs))


initialize_all(package_dir)
