from abjad.tools import iotools
from scf.proxies.FileProxy import FileProxy
from scf.wranglers.AssetWrangler import AssetWrangler
import os


class FileWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return FileProxy
