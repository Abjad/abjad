import os
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler


class PackagesystemAssetWrangler(FilesystemAssetWrangler):

    def __init__(self,
        built_in_external_storehouse_filesystem_path=None,
        built_in_external_storehouse_packagesystem_path=None,
        user_external_storehouse_filesystem_path=None,
        user_external_storehouse_packagesystem_path=None,
        session=None,
        ):
        built_in_external_storehouse_filesystem_path = \
            built_in_external_storehouse_filesystem_path or \
            self.configuration.packagesystem_path_to_filesystem_path(
                built_in_external_storehouse_packagesystem_path)
        if user_external_storehouse_filesystem_path is None and \
            user_external_storehouse_packagesystem_path is not None:
            user_external_storehouse_filesystem_path = \
                self.configuration.packagesystem_path_to_filesystem_path(
                user_external_storehouse_packagesystem_path)
        FilesystemAssetWrangler.__init__(self,
            built_in_external_storehouse_filesystem_path=\
                built_in_external_storehouse_filesystem_path,
            user_external_storehouse_filesystem_path=\
                user_external_storehouse_filesystem_path,
            session=session,
            )
        self._built_in_external_storehouse_packagesystem_path = \
            built_in_external_storehouse_packagesystem_path or ''
        self._user_external_storehouse_packagesystem_path = \
            user_external_storehouse_packagesystem_path or ''

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when system storehouse package paths and score
        storehouse package path infixes are both equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self._list_built_in_external_storehouse_packagesystem_path() == \
                expr._list_built_in_external_storehouse_packagesystem_path():
                if self.storehouse_path_infix_parts == \
                    expr.storehouse_path_infix_parts:
                    return True
        return False

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_packagesystem_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_package_path)
            parts.extend(self.storehouse_path_infix_parts)
            return '.'.join(parts)
        if self._list_built_in_external_storehouse_packagesystem_path():
            return self._list_built_in_external_storehouse_packagesystem_path()[0]

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
        return self._get_asset_proxy(self._temporary_asset_package_path)

    ### PRIVATE METHODS ###

    def _get_asset_proxy(self, packagesystem_path):
        if os.path.sep in packagesystem_path:
            pacakgesystem_path = self.configuration.filesystem_path_to_packagesystem_path(packagesystem_path)
        return self.asset_proxy_class(packagesystem_path=packagesystem_path, session=self._session)

    def _list_built_in_external_storehouse_packagesystem_path(self, head=None):
        result = []
        for package_path in [self.built_in_external_storehouse_packagesystem_path]:
            if head is None or package_path.startswith(head):
                result.append(package_path)
        return result

    def _list_built_in_score_package_paths(self, head=None):
        result = []
        for directory_path in self.configuration.list_score_directory_paths(
            built_in=True, head=head):
            package_path = self.configuration.filesystem_path_to_packagesystem_path(directory_path)
            reuslt.append(package_path)
        return result

    def _list_score_directory_package_paths(self, head=None):
        result = []
        for directory_path in self.configuration.list_score_directory_paths(
            built_in=True, user=True, head=head):
            package_path = self.configuration.filesystem_path_to_packagesystem_path(directory_path)
            result.append(package_path)
        return result

    def _list_score_storehouse_package_paths(self, head=None):
        result = []
        for score_package_name in self._list_score_directory_package_paths(head=head):
            parts = [score_package_name]
            if self.storehouse_path_infix_parts:
                parts.extend(self.storehouse_path_infix_parts)
            score_score_package_path = '.'.join(parts)
            result.append(score_score_package_path)
        return result

    def _list_storehouse_package_paths(self, head=None):
        result = []
        result.extend(self._list_built_in_external_storehouse_packagesystem_path(head=head))
        result.extend(self._list_score_storehouse_package_paths(head=head))
        return result

    def _list_user_storehouse_package_paths(self, head=None):
        result = []
        for package_path in [self.user_external_storehouse_packagesystem_path]:
            if head is None or package_path.startswith(head):
                result.append(package_path)
        return result

    def _make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_packagesystem_paths(head=head)
        bodies = self.list_space_delimited_lowercase_visible_asset_names(head=head)
        assert len(keys) == len(bodies), repr((keys, bodies))
        return zip(keys, bodies)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def built_in_external_storehouse_packagesystem_path(self):
        return self._built_in_external_storehouse_packagesystem_path

    @property
    def user_external_storehouse_packagesystem_path(self):
        return self._user_external_storehouse_packagesystem_path

    ### PUBLIC METHODS ###

    def get_asset_proxies(self, head=None):
        result = []
        for package_path in self.list_asset_packagesystem_paths(head=head):
            asset_proxy = self._get_asset_proxy(package_path)
            result.append(asset_proxy)
        return result

    def list_asset_packagesystem_paths(self, head=None):
        result = []
        result.extend(self.list_external_asset_packagesystem_paths(head=head))
        result.extend(self.list_score_asset_packagesystem_paths(head=head))
        return result
        #result = []
        #for filesystem_path in self.list_asset_filesystem_paths(
        #    built_in_external=True, user_external=True,
        #    built_in_score=True, user_score=True, head=head):
        #    packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
        #    result.append(packagesystem_path)
        #return result

    def list_built_in_score_asset_packagesystem_paths(self, head=None):
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_score=True, head=head):
            package_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(package_path)
        return result

    def list_external_asset_packagesystem_paths(self, head=None):
        result = []
        for directory_path in self.list_storehouse_filesystem_paths(
            built_in_external=True, user_external=True, head=head):
            if 'recursif' not in directory_path:
                package_path = self.configuration.filesystem_path_to_packagesystem_path(directory_path)
                if head is None or package_path.startswith(head):
                    for directory_entry in os.listdir(directory_path):
                        if directory_entry[0].isalpha():
                            result.append('.'.join([package_path, directory_entry]))
        return result

    def list_score_asset_packagesystem_paths(self, head=None):
        result = []
        for storehouse_package_path in \
            self._list_score_storehouse_package_paths(head=head):
            if self.storehouse_path_infix_parts:
                asset_filesystem_path = self.configuration.packagesystem_path_to_filesystem_path(
                    storehouse_package_path)
                for directory_entry in os.listdir(asset_filesystem_path):
                    if directory_entry[0].isalpha():
                        package_name = directory_entry
                        if '.' in package_name:
                            package_name = package_name[:package_name.rindex('.')]
                        result.append('{}.{}'.format(
                            storehouse_package_path, package_name))
            else:
                result.append(storehouse_package_path)
        return result

    def list_user_asset_packagesystem_paths(self, head=None):
        result = []
        for asset_filesystem_path in self.list_storehouse_filesystem_paths(
            user_external=True, user_score=True, head=head):
            for directory_entry in os.listdir(asset_filesystem_path):
                if directory_entry[0].isalpha():
                    result.append('.'.join([
                        self.configuration.user_material_package_makers_package_path, 
                        directory_entry]))
        return result

    # TODO: try to reimplement without proxy instantiation
    def list_visible_asset_packagesystem_paths(self, head=None):
        result = []
        for asset_proxy in self.get_visible_asset_proxies(head=head):
            result.append(asset_proxy.package_path)
        return result

    # TODO: write test
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

    # TODO: write test
    def rename_asset_interactively(self, head=None):
        self._session.push_backtrack()
        asset_package_path = self.select_asset_packagesystem_path_interactively(
            head=head, infinitival_phrase='to rename')
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        asset_proxy = self._get_asset_proxy(asset_package_path)
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
