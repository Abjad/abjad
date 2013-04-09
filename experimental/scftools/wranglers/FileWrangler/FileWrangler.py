from abjad.tools import iotools
from scftools.proxies.FileProxy import FileProxy
from scftools.wranglers.AssetWrangler import AssetWrangler
import os


class FileWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return FileProxy
