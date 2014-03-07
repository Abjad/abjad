# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.DirectoryManager import DirectoryManager


class DistributionDirectoryManager(DirectoryManager):
    r'''Distribution directory manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        if path is not None:
            assert path.endswith('distribution')
        DirectoryManager.__init__(
            self,
            path=path,
            session=session,
            )
