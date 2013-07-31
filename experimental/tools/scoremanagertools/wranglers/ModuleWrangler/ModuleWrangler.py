# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.wranglers.PackagesystemAssetWrangler \
    import PackagesystemAssetWrangler


class ModuleWrangler(PackagesystemAssetWrangler):

    ### PRIVATE METHODS ###

    def _is_valid_directory_entry(self, directory_entry):
        if super(ModuleWrangler, self)._is_valid_directory_entry(
            directory_entry):
            if directory_entry.endswith('.py'):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.ModuleProxy
