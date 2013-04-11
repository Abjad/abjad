from abjad.tools import iotools
from experimental.tools.scftools.proxies.FileProxy import FileProxy
from experimental.tools.scftools.wranglers.AssetWrangler import AssetWrangler
import os


class FileWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return FileProxy
