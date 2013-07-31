# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler \
    import FilesystemAssetWrangler


class FileWrangler(FilesystemAssetWrangler):

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.FileProxy
