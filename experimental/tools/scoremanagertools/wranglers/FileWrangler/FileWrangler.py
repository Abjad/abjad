from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy
from experimental.tools.scoremanagertools.wranglers.AssetWrangler import AssetWrangler
import os


class FileWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return FileProxy
