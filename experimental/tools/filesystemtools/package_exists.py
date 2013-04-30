import os


def package_exists(package_path, configuration):
    '''True when `package_path` exists. Otherwise false.

    Return boolean.
    '''
    from experimental.tools import filesystemtools

    assert isinstance(package_path, str)
    directory_path = filesystemtools.package_path_to_directory_path(package_path, configuration)
    return os.path.exists(directory_path)
