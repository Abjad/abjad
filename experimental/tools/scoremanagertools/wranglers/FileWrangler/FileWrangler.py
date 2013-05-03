from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler
import os


class FileWrangler(FilesystemAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return FileProxy
