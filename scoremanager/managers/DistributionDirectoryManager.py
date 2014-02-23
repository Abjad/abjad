# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.DirectoryManager import DirectoryManager


class DistributionDirectoryManager(DirectoryManager):

    ### INITIALIZER ###

    def __init__(self, score_directory_path=None, session=None):
        filesystem_path = os.path.join(score_directory_path, 'distribution')
        DirectoryManager.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )
