from abjad.tools import iotools
from experimental.tools.scoremanagementtools.proxies.ModuleProxy import ModuleProxy
from experimental.tools.scoremanagementtools.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class ModuleWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return ModuleProxy
