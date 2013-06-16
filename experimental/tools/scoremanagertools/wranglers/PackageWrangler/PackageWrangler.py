import abc
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.PackagesystemAssetWrangler import \
    PackagesystemAssetWrangler


class PackageWrangler(PackagesystemAssetWrangler):

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    ### PRIVATE PROPERTIES ###

    @property
    def _temporary_asset_name(self):
        return '__temporary_package'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        self._io.print_not_yet_implemented()

    def _make_main_menu(self, head=None):
        self._io.print_not_yet_implemented()

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def asset_proxy_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    ### PUBLIC METHODS ###

    def interactively_make_asset(self):
        self._io.print_not_yet_implemented()

    def make_asset(self, asset_name):
        assert stringtools.is_underscore_delimited_lowercase_package_name(asset_name)
        asset_filesystem_path = os.path.join(self._current_storehouse_filesystem_path, asset_name)
        os.mkdir(asset_filesystem_path)
        package_proxy = self._initialize_asset_proxy(asset_name)
        package_proxy.fix(is_interactive=False)

    ### UI MANIFEST ###

    user_input_to_action = PackagesystemAssetWrangler.user_input_to_action.copy()
    user_input_to_action.update({

        })
