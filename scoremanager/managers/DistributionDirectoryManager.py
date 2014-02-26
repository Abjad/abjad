# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.DirectoryManager import DirectoryManager


class DistributionDirectoryManager(DirectoryManager):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        if filesystem_path is not None:
            assert filesystem_path.endswith('distribution')
        DirectoryManager.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )
