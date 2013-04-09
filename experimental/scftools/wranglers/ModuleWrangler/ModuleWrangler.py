from abjad.tools import iotools
from scftools.proxies.ModuleProxy import ModuleProxy
from scftools.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class ModuleWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return ModuleProxy
