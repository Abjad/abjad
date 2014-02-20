# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.DirectoryManager import DirectoryManager


class DistributionDirectoryManager(DirectoryManager):

    ### INITIALIZER ###

    def __init__(self, score_package_path=None, _session=None):
        score_directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            score_package_path)
        filesystem_path = os.path.join(score_directory_path, 'distribution')
        DirectoryManager.__init__(
            self,
            filesystem_path=filesystem_path,
            _session=_session)
