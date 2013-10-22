# -*- encoding: utf-8 -*-
import abc
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.PackagesystemAssetWrangler \
    import PackagesystemAssetWrangler


class PackageWrangler(PackagesystemAssetWrangler):
    r'''Package wrangler.
    '''

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        superclass = super(PackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = scoremanagertools.managers.PackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _temporary_asset_name(self):
        return '__temporary_package'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        self.session.io_manager.print_not_yet_implemented()

    def _is_valid_directory_entry(self, expr):
        superclass = super(PackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_main_menu(self, head=None):
        self.session.io_manager.print_not_yet_implemented()

    ### PUBLIC METHODS ###

    def interactively_get_available_packagesystem_path(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively gets available packagesystem path.

        Returns string.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        while True:
            getter = self.session.io_manager.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string('name')
            with self.backtracking:
                package_name = getter._run()
            if self.session.backtrack():
                return
            package_name = \
                stringtools.string_to_accent_free_snake_case(package_name)
            package_path = '.'.join([
                self._current_storehouse_packagesystem_path, 
                package_name,
                ])
            if self.configuration.packagesystem_path_exists(package_path):
                line = 'Package {!r} already exists.'
                line = line.format(package_path)
                self.session.io_manager.display([line, ''])
            else:
                return package_path

    def interactively_make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively makes asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        with self.backtracking:
            package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_asset(package_path)

    def make_asset(self, asset_name):
        r'''Makes asset.

        Returns none.
        '''
        assert stringtools.is_snake_case_package_name(asset_name)
        asset_filesystem_path = os.path.join(
            self._current_storehouse_filesystem_path, asset_name)
        os.mkdir(asset_filesystem_path)
        package_manager = self._initialize_asset_manager(asset_name)
        package_manager.fix(is_interactive=False)

    ### UI MANIFEST ###

    user_input_to_action = \
        PackagesystemAssetWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'new': interactively_make_asset,
        })
