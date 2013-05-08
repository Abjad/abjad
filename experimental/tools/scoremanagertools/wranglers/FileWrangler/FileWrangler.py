from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler


class FileWrangler(FilesystemAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.FileProxy
