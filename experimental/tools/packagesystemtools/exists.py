import os


def exists(packagesystem_path):
    '''True when `packagesystem_path` exists. Otherwise false.

    Return boolean.
    '''
    from experimental.tools import packagesystemtools

    # check input
    assert os.path.sep not in packagesystem_path, repr(packagesystem_path)

    # find directory path
    filesystem_path = packagesystemtools.packagesystem_path_to_filesystem_path(packagesystem_path)

    # return result
    return os.path.exists(filesystem_path)
