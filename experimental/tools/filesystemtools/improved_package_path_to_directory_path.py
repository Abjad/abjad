import imp
import os


def improved_package_path_to_directory_path(package_path):
    '''Change `package_path` to directory path.

    Implemented with built-in ``imp`` module.

    Return string.
    '''
    
    if package_path is None:
        return

    package_path_parts = package_path.split('.')
    root_package_name = package_path_parts[0]
    file_pointer, directory_path, description = imp.find_module(root_package_name)

    for subpackage_name in package_path_parts[1:]:
        file_pointer, directory_path, description = imp.find_module(subpackage_name, [directory_path])

    return directory_path
