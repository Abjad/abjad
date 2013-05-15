import os


def package_exists(package_path):
    '''True when `package_path` exists. Otherwise false.

    Return boolean.
    '''
    from experimental.tools import packagesystemtools

    # check input
    assert os.path.sep not in package_path, repr(package_path)

    # find directory path
    directory_path = packagesystemtools.packagesystem_path_to_filesystem_path(package_path)

    # return result
    return os.path.exists(directory_path)
