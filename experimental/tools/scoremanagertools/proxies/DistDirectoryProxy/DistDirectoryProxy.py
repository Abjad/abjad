import os
from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy


class DistDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_name=None, session=None):
        directory_path = os.path.join(self.configuration.scores_directory_path, score_package_name, 'dist')
        DirectoryProxy.__init__(self, directory_path=directory_path, session=session)
