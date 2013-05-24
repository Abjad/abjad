import os
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler


class PackagesystemAssetWrangler(FilesystemAssetWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        built_in_external_storehouse_filesystem_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
                self.built_in_external_storehouse_packagesystem_path)
        user_external_storehouse_filesystem_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            self.user_external_storehouse_packagesystem_path)
        self.built_in_external_storehouse_filesystem_path = built_in_external_storehouse_filesystem_path
        self.user_external_storehouse_filesystem_path = user_external_storehouse_filesystem_path
        FilesystemAssetWrangler.__init__(self, session=session)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when types are the same. Otherwise false.

        Return boolean.
        '''
        return type(self) is type(expr)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_packagesystem_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_package_path)
            parts.extend(self.storehouse_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.built_in_external_storehouse_packagesystem_path

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
            pacakgesystem_path = self.configuration.filesystem_path_to_packagesystem_path(packagesystem_path)
        return self.asset_proxy_class(packagesystem_path=packagesystem_path, session=self._session)

    def _list_built_in_external_storehouse_packagesystem_path(self, head=None):
        result = []
        for filesystem_path in self.list_storehouse_filesystem_paths(
            built_in_score=False, user_external=False, user_score=False, head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def _list_score_storehouse_package_paths(self, head=None):
        result = []
        for filesystem_path in self.list_storehouse_filesystem_paths(
            built_in_external=False, user_external=False, head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def _list_storehouse_package_paths(self, head=None):
        result = []
        result.extend(self._list_built_in_external_storehouse_packagesystem_path(head=head))
        result.extend(self._list_score_storehouse_package_paths(head=head))
        return result

    def _make_menu_tokens(self, head=None):
        keys = self.list_visible_asset_packagesystem_paths(head=head)
        bodies = self.list_asset_names(head=head)
        assert len(keys) == len(bodies), repr((keys, bodies))
        return zip(keys, bodies)

    ### PUBLIC METHODS ###

    def list_asset_packagesystem_paths(self, 
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_asset_proxies(self, built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        result = []
        for package_path in self.list_asset_packagesystem_paths(head=head):
            asset_proxy = self._initialize_asset_proxy(package_path)
            result.append(asset_proxy)
        return result

    def list_visible_asset_packagesystem_paths(self, head=None):
        result = []
        if hasattr(self, 'list_visible_asset_proxies'):
            for asset_proxy in self.list_visible_asset_proxies(head=head):
                result.append(asset_proxy.package_path)
        else:
            for asset_proxy in self.list_asset_proxies(
                built_in_external=True, user_external=True,
                built_in_score=True, user_score=True, head=head):
                result.append(asset_proxy.package_path)
        return result

    def make_empty_package(self, package_path):
        if package_path is None:
            return
        directory_path = self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            initializer_file_name = os.path.join(directory_path, '__init__.py')
            file_reference = file(initializer_file_name, 'w')
            file_reference.write('')
            file_reference.close()

    def make_external_storehouse_package(self):
        for package_path in self._list_built_in_external_storehouse_packagesystem_path():
            self.make_empty_package(package_path)

    def make_score_storehouse_packages(self, head=None):
        for score_storehouse_package_path in \
            self._list_score_storehouse_package_paths(head=head):
            self.make_empty_package(score_storehouse_package_path)

    def make_storehouse_packages(self, is_interactive=False):
        self.make_external_storehouse_package()
        self.make_score_storehouse_packages()
        self._io.proceed('missing packages created.', is_interactive=is_interactive)

    def rename_asset_interactively(self, head=None):
        self._session.push_backtrack()
        asset_package_path = self.select_asset_packagesystem_path_interactively(
            head=head, infinitival_phrase='to rename')
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        asset_proxy = self._initialize_asset_proxy(asset_package_path)
        asset_proxy.rename_interactively()

    def select_asset_packagesystem_path_interactively(
        self, clear=True, cache=False, head=None, infinitival_phrase=None, user_input=None):
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            self._session.push_breadcrumb(self._make_asset_selection_breadcrumb(
                infinitival_phrase=infinitival_phrase))
            menu = self._make_asset_selection_menu(head=head)
            result = menu._run(clear=clear)
            if self._session.backtrack():
                break
            elif not result:
                self._session.pop_breadcrumb()
                continue
            else:
                break
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        return result
