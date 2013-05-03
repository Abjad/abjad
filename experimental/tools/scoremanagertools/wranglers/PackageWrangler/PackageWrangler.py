import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.proxies.PackageProxy import PackageProxy
from experimental.tools.scoremanagertools.wranglers.ImportableAssetWrangler import ImportableAssetWrangler


class PackageWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return PackageProxy

    @property
    def score_external_asset_proxies(self):
        result = []
        for asset_filesystem_path in self.score_external_asset_filesystem_paths:
            asset_package_path = packagepathtools.directory_path_to_package_path(asset_filesystem_path)
            asset_proxy = self.get_asset_proxy(asset_package_path)
            result.append(asset_proxy)
        return result

    @property
    def temporary_asset_name(self):
        return '__temporary_package'

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        self.print_not_yet_implemented()

    def make_asset(self, asset_name):
        assert stringtools.is_underscore_delimited_lowercase_package_name(asset_name)
        asset_filesystem_path = os.path.join(self.current_asset_container_path, asset_name)
        os.mkdir(asset_filesystem_path)
        package_proxy = self.get_asset_proxy(asset_name)
        package_proxy.fix(is_interactive=False)

    def make_asset_interactively(self):
        self.print_not_yet_implemented()

    def make_main_menu(self):
        self.print_not_yet_implemented()
