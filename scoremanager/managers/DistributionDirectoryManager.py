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
        if not os.path.exists(path):
            self._make_empty_asset()

    ### PRIVATE METHODS ###

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        self._make_directory_menu_section(menu, is_permanent=True)
        return menu
