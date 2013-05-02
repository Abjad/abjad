import os


def package_exists(package_path, configuration=None):
    '''True when `package_path` exists. Otherwise false.

    Return boolean.
    '''
    from experimental.tools import packagepathtools
    from experimental.tools.scoremanagertools import core

    # check input
    assert isinstance(package_path, str), repr(package_path)
    configuration = configuration or core.ScoreManagerConfiguration()

    # find directory path
    directory_path = packagepathtools.package_path_to_directory_path(package_path, configuration)

    # return result
    return os.path.exists(directory_path)
