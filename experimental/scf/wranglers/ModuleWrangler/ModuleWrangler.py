from abjad.tools import iotools
from scf.proxies.ModuleProxy import ModuleProxy
from scf.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class ModuleWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return ModuleProxy
