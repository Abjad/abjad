from experimental.tools.scoremanagementtools.proxies.AssetProxy import AssetProxy


class ImportableAssetProxy(AssetProxy):

    def __init__(self, asset_full_name=None, session=None):
        path_name = self.asset_full_name_to_path_name(asset_full_name)
        AssetProxy.__init__(self, path_name=path_name, session=session)

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.importable_name is not None:
            return '{}({!r})'.format(self.class_name, self.importable_name)
        else:
            return '{}()'.format(self.class_name)

    ### READ-ONLY PROPERTIES ###

    @property
    def importable_name(self):
        return self.path_name_to_package_importable_name(self.path_name)
