import os
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler


class ImportableFilesystemAssetWrangler(FilesystemAssetWrangler):

    def __init__(self,
        built_in_asset_container_directory_paths=None,
        built_in_asset_container_package_paths=None,
        user_asset_container_directory_paths=None,
        user_asset_container_package_paths=None,
        session=None,
        ):
        built_in_asset_container_directory_paths = built_in_asset_container_directory_paths or \
            [packagepathtools.package_path_to_directory_path(x) for x in built_in_asset_container_package_paths]
        if user_asset_container_directory_paths is None and \
            user_asset_container_package_paths is not None:
            user_asset_container_directory_paths = [
                packagepathtools.package_path_to_directory_path(x) 
                for x in user_asset_container_package_paths]
        FilesystemAssetWrangler.__init__(self,
            built_in_asset_container_directory_paths=built_in_asset_container_directory_paths,
            user_asset_container_directory_paths=user_asset_container_directory_paths,
            session=session,
            )
        self._built_in_asset_container_package_paths = \
            built_in_asset_container_package_paths or []
        self._user_asset_container_package_paths = \
            user_asset_container_package_paths or []

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when system asset container package paths and score-internal
        asset container package path infixes are both equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.list_built_in_asset_container_package_paths() == \
                expr.list_built_in_asset_container_package_paths():
                if self.asset_container_path_infix_parts == \
                    expr.asset_container_path_infix_parts:
                    return True
        return False

    def __repr__(self):
        '''Importable filesystem asset wrangler repr.
        
        Return string.
        '''
        parts = []
        parts.extend(self.list_built_in_asset_container_package_paths())
        if self.asset_container_path_infix_parts:
            parts.append('.'.join(self.asset_container_path_infix_parts))
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self._class_name, parts)

    ### PRIVATE METHODS ###

    def _make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_package_paths(head=head)
        bodies = self.list_space_delimited_lowercase_visible_asset_names(head=head)
        return zip(keys, bodies)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _temporary_asset_package_path(self):
        if self.current_asset_container_package_path:
            return '.'.join([
                self.current_asset_container_package_path,
                self._temporary_asset_name])
        else:
            return self._temporary_asset_name

    @property
    def _temporary_asset_proxy(self):
        return self.get_asset_proxy(self._temporary_asset_package_path)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_container_proxy_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    @property
    def built_in_asset_container_package_paths(self):
        return self._built_in_asset_container_package_paths

    @property
    def current_asset_container_package_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.underscore_delimited_current_score_name)
            parts.extend(self.asset_container_path_infix_parts)
            return '.'.join(parts)
        if self.list_built_in_asset_container_package_paths():
            return self.list_built_in_asset_container_package_paths()[0]

    @property
    def user_asset_container_package_paths(self):
        return self._user_asset_container_package_paths

    ### PUBLIC METHODS ###

    def get_asset_proxies(self, head=None):
        result = []
        for package_path in self.list_asset_package_paths(head=head):
            asset_proxy = self.get_asset_proxy(package_path)
            result.append(asset_proxy)
        return result

    def list_asset_container_package_paths(self, head=None):
        result = []
        result.extend(self.list_built_in_asset_container_package_paths(head=head))
        result.extend(self.list_score_internal_asset_container_package_paths(head=head))
        return result

    def list_asset_package_paths(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_package_paths(head=head))
        result.extend(self.list_score_internal_asset_package_paths(head=head))
        result.extend(self.list_user_asset_package_paths(head=head))
        return result

    def list_built_in_asset_container_package_paths(self, head=None):
        result = []
        for package_path in self.built_in_asset_container_package_paths:
            if head is None or package_path.startswith(head):
                result.append(package_path)
        return result

    # TODO: eventually remove altogether
    def list_score_external_asset_container_directory_paths(self, head=None):
        result = []
        for package_path in self.list_built_in_asset_container_package_paths(head=head):
            result.append(packagepathtools.package_path_to_directory_path(package_path))
        return result

    def list_score_external_asset_package_paths(self, head=None):
        result = []
        for directory_path in self.list_score_external_asset_container_directory_paths(head=head):
            for directory_entry in os.listdir(directory_path):
                package_path = packagepathtools.filesystem_path_to_package_path(directory_path)
                if directory_entry[0].isalpha():
                    result.append('.'.join([package_path, directory_entry]))
        return result

    def list_score_internal_asset_container_package_paths(self, head=None):
        result = []
        for score_package_name in self.list_score_directory_basenames(head=head):
            parts = [score_package_name]
            if self.asset_container_path_infix_parts:
                parts.extend(self.asset_container_path_infix_parts)
            score_internal_score_package_path = '.'.join(parts)
            result.append(score_internal_score_package_path)
        return result

    def list_score_internal_asset_package_paths(self, head=None):
        result = []
        for asset_container_package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            if self.asset_container_path_infix_parts:
                asset_filesystem_path = packagepathtools.package_path_to_directory_path(
                    asset_container_package_path)
                for directory_entry in os.listdir(asset_filesystem_path):
                    if directory_entry[0].isalpha():
                        package_name = self._strip_file_extension_from_file_name(directory_entry)
                        result.append('{}.{}'.format(
                            asset_container_package_path, package_name))
            else:
                result.append(asset_container_package_path)
        return result

    def list_user_asset_container_package_paths(self, head=None):
        result = []
        for package_path in self.user_asset_container_package_paths:
            if head is None or package_path.startswith(head):
                result.append(package_path)
        return result

    def list_user_asset_package_paths(self, head=None):
        result = []
        for asset_filesystem_path in self.list_user_asset_container_directory_paths(head=head):
            for directory_entry in os.listdir(asset_filesystem_path):
                if directory_entry[0].isalpha():
                    result.append('.'.join([
                        self.configuration.user_material_package_makers_package_path, 
                        directory_entry]))
        return result

    # TODO: try to reimplement without proxy instantiation
    def list_visible_asset_package_paths(self, head=None):
        result = []
        for asset_proxy in self.get_visible_asset_proxies(head=head):
            result.append(asset_proxy.package_path)
        return result

    def make_asset_container_packages(self, is_interactive=False):
        self.make_score_external_asset_container_package()
        self.make_score_internal_asset_container_packages()
        self._io.proceed('missing packages created.', is_interactive=is_interactive)

    # TODO: write test
    def make_empty_package(self, package_path):
        if package_path is None:
            return
        directory_path = packagepathtools.package_path_to_directory_path(package_path)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            initializer_file_name = os.path.join(directory_path, '__init__.py')
            file_reference = file(initializer_file_name, 'w')
            file_reference.write('')
            file_reference.close()

    def make_score_external_asset_container_package(self):
        for package_path in self.list_built_in_asset_container_package_paths():
            self.make_empty_package(package_path)

    def make_score_internal_asset_container_packages(self, head=None):
        for score_internal_asset_container_package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            self.make_empty_package(score_internal_asset_container_package_path)

    # TODO: write test
    def rename_asset_interactively(self, head=None):
        self._session.push_backtrack()
        asset_package_path = self.select_asset_package_path_interactively(
            head=head, infinitival_phrase='to rename')
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        asset_proxy = self.get_asset_proxy(asset_package_path)
        asset_proxy.rename_interactively()

    def select_asset_package_path_interactively(
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
