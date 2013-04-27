from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy
import os


class DistDirectoryProxy(DirectoryProxy):

    def __init__(self, score_package_name=None, session=None):
        path = os.path.join(self.configuration.SCORES_DIRECTORY_PATH, score_package_name, 'dist')
        DirectoryProxy.__init__(self, path=path, session=session)
