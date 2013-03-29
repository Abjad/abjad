from scf.proxies.DirectoryProxy import DirectoryProxy
import os


class ExgDirectoryProxy(DirectoryProxy):

    def __init__(self, score_package_short_name=None, session=None):
        path_name = os.path.join(self.scores_directory_name, score_package_short_name, 'exg')
        DirectoryProxy.__init__(self, path_name=path_name, session=session)
