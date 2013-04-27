from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy


class ImportableAssetProxy(AssetProxy):

    def __init__(self, asset_full_name=None, session=None):
        path = self.asset_full_name_to_path(asset_full_name)
        AssetProxy.__init__(self, path=path, session=session)

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.package_path is not None:
            return '{}({!r})'.format(self._class_name, self.package_path)
        else:
            return '{}()'.format(self._class_name)

    ### READ-ONLY PROPERTIES ###

    @property
    def package_path(self):
        return self.path_to_package_path(self.path)
