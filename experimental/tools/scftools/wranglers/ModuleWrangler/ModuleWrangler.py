from abjad.tools import iotools
from experimental.tools.scftools.proxies.ModuleProxy import ModuleProxy
from experimental.tools.scftools.wranglers.ImportableAssetWrangler import ImportableAssetWrangler
import os


class ModuleWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return ModuleProxy
