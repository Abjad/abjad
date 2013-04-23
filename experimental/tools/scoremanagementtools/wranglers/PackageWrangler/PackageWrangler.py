import os
from abjad.tools import stringtools
from experimental.tools.scoremanagementtools.proxies.PackageProxy import PackageProxy
from experimental.tools.scoremanagementtools.wranglers.ImportableAssetWrangler import ImportableAssetWrangler


class PackageWrangler(ImportableAssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return PackageProxy

    @property
    def score_external_asset_proxies(self):
        result = []
        for asset_path_name in self.score_external_asset_path_names:
            asset_package_importable_name = self.path_name_to_package_importable_name(asset_path_name)
            asset_proxy = self.get_asset_proxy(asset_package_importable_name)
            result.append(asset_proxy)
        return result

    @property
    def temporary_asset_short_name(self):
        return '__temporary_package'

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        self.print_not_yet_implemented()

    def make_asset(self, asset_short_name):
        assert stringtools.is_underscore_delimited_lowercase_package_name(asset_short_name)
        asset_path_name = os.path.join(self.current_asset_container_path_name, asset_short_name)
        os.mkdir(asset_path_name)
        package_proxy = self.get_asset_proxy(asset_short_name)
        package_proxy.fix(is_interactive=False)

    def make_asset_interactively(self):
        self.print_not_yet_implemented()

    def make_main_menu(self):
        self.print_not_yet_implemented()
