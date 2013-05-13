import os
from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy


class DistributionDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_name=None, session=None):
        filesystem_path = os.path.join(
            self.configuration.user_scores_directory_path, score_package_name, 'distribution')
        DirectoryProxy.__init__(self, filesystem_path=filesystem_path, session=session)
