from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy
import os


class ExgDirectoryProxy(DirectoryProxy):

    def __init__(self, score_package_short_name=None, session=None):
        path_name = os.path.join(self.configuration.SCORES_DIRECTORY_PATH, score_package_short_name, 'exg')
        DirectoryProxy.__init__(self, path_name=path_name, session=session)
