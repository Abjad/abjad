import os
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy


class ExergueDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_name=None, session=None):
        score_directory_path = packagepathtools.package_path_to_directory_path(score_package_name)
        filesystem_path = os.path.join(score_directory_path, 'exergue')
        DirectoryProxy.__init__(self, filesystem_path=filesystem_path, session=session)
