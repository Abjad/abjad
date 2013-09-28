# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.wranglers.PackagesystemAssetWrangler \
    import PackagesystemAssetWrangler


class ModuleWrangler(PackagesystemAssetWrangler):
    r'''Module wrangler.
    '''

    ### PRIVATE METHODS ###

    def _is_valid_directory_entry(self, directory_entry):
        if super(ModuleWrangler, self)._is_valid_directory_entry(
            directory_entry):
            if directory_entry.endswith('.py'):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def asset_manager_class(self):
        r'''Asset manager class of module wrangler.

        Returns class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.managers.ModuleManager
