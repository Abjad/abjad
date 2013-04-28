from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy


class ImportableAssetProxy(AssetProxy):

    ### INITIALIZER ###

    def __init__(self, asset_path=None, session=None):
        directory_path = self.asset_path_to_directory_path(asset_path)
        AssetProxy.__init__(self, asset_path=directory_path, session=session)

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.package_path is not None:
            return '{}({!r})'.format(self._class_name, self.package_path)
        else:
            return '{}()'.format(self._class_name)

    ### READ-ONLY PROPERTIES ###

    @property
    def package_path(self):
        return self.directory_path_to_package_path(self.path)
