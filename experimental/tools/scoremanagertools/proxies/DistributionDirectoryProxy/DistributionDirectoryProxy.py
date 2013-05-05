import os
from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy


class DistributionDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_name=None, session=None):
        directory_path = os.path.join(
            self.configuration.scores_directory_path, score_package_name, 'distribution')
        DirectoryProxy.__init__(self, directory_path=directory_path, session=session)
