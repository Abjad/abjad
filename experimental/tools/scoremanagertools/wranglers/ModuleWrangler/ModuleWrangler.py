from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.ModuleProxy import ModuleProxy
from experimental.tools.scoremanagertools.wranglers.ImportableFilesystemAssetWrangler import ImportableFilesystemAssetWrangler
import os


class ModuleWrangler(ImportableFilesystemAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        return ModuleProxy
