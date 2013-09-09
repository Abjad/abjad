# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler \
    import FilesystemAssetWrangler


class PackagesystemAssetWrangler(FilesystemAssetWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        asset_storehouse_filesystem_path_in_built_in_asset_library = \
            self.configuration.packagesystem_path_to_filesystem_path(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library)
        asset_storehouse_filesystem_path_in_user_asset_library = \
            self.configuration.packagesystem_path_to_filesystem_path(
            self.asset_storehouse_packagesystem_path_in_user_asset_library)
        self.asset_storehouse_filesystem_path_in_built_in_asset_library = \
            asset_storehouse_filesystem_path_in_built_in_asset_library
        self.asset_storehouse_filesystem_path_in_user_asset_library = \
            asset_storehouse_filesystem_path_in_user_asset_library
        FilesystemAssetWrangler.__init__(self, session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_packagesystem_path(self):
        if self.session.is_in_score:
            parts = []
            parts.append(self.session.current_score_package_path)
            parts.extend(self.score_package_asset_storehouse_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.asset_storehouse_packagesystem_path_in_built_in_asset_library

    @property
    def _temporary_asset_package_path(self):
        if self._current_storehouse_packagesystem_path:
            return '.'.join([
                self._current_storehouse_packagesystem_path,
                self._temporary_asset_name])
        else:
            return self._temporary_asset_name

    @property
    def _temporary_asset_proxy(self):
        return self._initialize_asset_proxy(self._temporary_asset_package_path)

    ### PRIVATE METHODS ###

    def _initialize_asset_proxy(self, packagesystem_path):
        if os.path.sep in packagesystem_path:
            pacakgesystem_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
            packagesystem_path)
        return self.asset_proxy_class(
            packagesystem_path=packagesystem_path, session=self.session)

    def _make_asset_menu_entries(self, head=None):
        names = self.list_asset_names(head=head)
        keys = len(names) * [None]
        prepopulated_return_values = len(names) * [None]
        paths = self.list_visible_asset_packagesystem_paths(head=head)
        assert len(names) == len(keys) == len(paths)
        if names:
            return sequencetools.zip_sequences_cyclically(
                names, [None], [None], paths)

    ### PUBLIC METHODS ###

    def interactively_rename_asset(
        self, 
        head=None,
        pending_user_input=None,
        ):
        r'''Interactively renames asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        with self.backtracking:
            asset_package_path = \
                self.interactively_select_asset_packagesystem_path(
                head=head, infinitival_phrase='to rename')
        if self.session.backtrack():
            return
        asset_proxy = self._initialize_asset_proxy(asset_package_path)
        asset_proxy.interactively_rename()

    def interactively_select_asset_packagesystem_path(
        self,
        clear=True,
        cache=False,
        head=None,
        infinitival_phrase=None,
        pending_user_input=None,
        ):
        '''Interactively selects asset packagesystem path.

        Returns string.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(
                self._make_asset_selection_breadcrumb(
                infinitival_phrase=infinitival_phrase))
            menu = self._make_asset_selection_menu(head=head)
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            else:
                break
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        return result

    def list_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Returns list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head):
            packagesystem_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                    filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_asset_proxies(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        head=None,
        ):
        r'''Lists asset proxies.

        Returns list.
        '''
        result = []
        for package_path in self.list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            asset_proxy = self._initialize_asset_proxy(package_path)
            result.append(asset_proxy)
        return result

    def list_asset_storehouse_packagesystem_paths(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse packagesystem paths.

        Returns list.
        '''
        result = []
        superclass = super(PackagesystemAssetWrangler, self)
        for filesystem_path in \
            superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=True,
            in_user_asset_library=True,
            in_built_in_score_packages=True,
            in_user_score_packages=True,
            ):
            packagesystem_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_visible_asset_packagesystem_paths(self, head=None):
        r'''Lists visible asset packagesystem paths.

        Returns list.
        '''
        result = []
        if hasattr(self, 'list_visible_asset_proxies'):
            for asset_proxy in self.list_visible_asset_proxies(head=head):
                result.append(asset_proxy.package_path)
        else:
            for asset_proxy in self.list_asset_proxies(
                in_built_in_asset_library=True,
                in_user_asset_library=True,
                in_built_in_score_packages=True,
                in_user_score_packages=True,
                head=head,
                ):
                result.append(asset_proxy.package_path)
        return result

    def make_asset_storehouse_packages(self, is_interactive=False):
        r'''Makes asset storehouse packages.

        Returns none.
        '''
        for package_path in self.list_asset_storehouse_packagesystem_paths(
            in_built_in_asset_library=True,
            in_user_asset_library=True,
            in_built_in_score_packages=True,
            in_user_score_packages=True,
            ):
            self.make_empty_package(package_path)
        self.session.io_manager.proceed(
            'missing packages created.', 
            is_interactive=is_interactive,
            )

    def make_empty_package(self, package_path):
        r'''Makes empty package.

        Returns none.
        '''
        if package_path is None:
            return
        directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            initializer_file_name = os.path.join(
                directory_path, '__init__.py')
            file_reference = file(initializer_file_name, 'w')
            file_reference.write('')
            file_reference.close()

    ### UI MANIFEST ###

    user_input_to_action = FilesystemAssetWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'missing': make_asset_storehouse_packages,
        'ren': interactively_rename_asset,
        })
