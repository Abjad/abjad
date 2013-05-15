from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.ModuleProxy import ModuleProxy
from experimental.tools.scoremanagertools.wranglers.PackagesystemAssetWrangler import PackagesystemAssetWrangler
import os


class ModuleWrangler(PackagesystemAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        return ModuleProxy
