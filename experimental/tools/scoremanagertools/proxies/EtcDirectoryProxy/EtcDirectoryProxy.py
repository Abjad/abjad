from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy
import os


class EtcDirectoryProxy(DirectoryProxy):

    def __init__(self, score_package_name=None, session=None):
        path = os.path.join(self.configuration.SCORES_DIRECTORY_PATH, score_package_name, 'etc')
        DirectoryProxy.__init__(self, path=path, session=session)
