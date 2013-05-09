import os
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.wranglers.FilesystemAssetWrangler import FilesystemAssetWrangler


class ImportableFilesystemAssetWrangler(FilesystemAssetWrangler):

    def __init__(self,
        system_asset_container_directory_paths=None,
        system_asset_container_package_paths=None,
        user_asset_container_directory_paths=None,
        user_asset_container_package_paths=None,
        score_internal_asset_container_package_path_infix=None,
        session=None,
        ):
        FilesystemAssetWrangler.__init__(self,
            system_asset_container_directory_paths=system_asset_container_directory_paths,
            system_asset_container_package_paths=system_asset_container_package_paths,
            user_asset_container_directory_paths=user_asset_container_directory_paths,
            session=session,
            )
        self._user_asset_container_package_paths = \
            user_asset_container_package_paths or []
        self._score_internal_asset_container_package_path_infix = \
            score_internal_asset_container_package_path_infix

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when system asset container package paths and score-internal
        asset container package path infixes are both equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.list_system_asset_container_package_paths() == \
                expr.list_system_asset_container_package_paths():
                if self.score_internal_asset_container_package_path_infix == \
                    expr.score_internal_asset_container_package_path_infix:
                    return True
        return False

    def __repr__(self):
        '''Importable filesystem asset wrangler repr.
        
        Return string.
        '''
        parts = []
        parts.extend(self.list_system_asset_container_package_paths())
        if self.score_internal_asset_container_package_path_infix:
            parts.append(self.score_internal_asset_container_package_path_infix)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self._class_name, parts)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_container_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.PackageProxy

    @property
    def current_asset_container_directory_path(self):
        return packagepathtools.package_path_to_directory_path(
            self.current_asset_container_package_path)

    @property
    def current_asset_container_package_path(self):
        if self.session.is_in_score:
            return '.'.join([
                self.session.current_score_package_name,
                self.score_internal_asset_container_package_path_infix])
        elif self.list_system_asset_container_package_paths():
            return self.list_system_asset_container_package_paths()[0]

    @property
    def current_asset_container_proxy(self):
        return self.asset_container_class(self.current_asset_container_package_path)

    @property
    def score_internal_asset_container_package_path_infix(self):
        return self._score_internal_asset_container_package_path_infix

    @property
    def temporary_asset_package_path(self):
        if self.current_asset_container_package_path:
            return '.'.join([
                self.current_asset_container_package_path,
                self._temporary_asset_name])
        else:
            return self._temporary_asset_name

    @property
    def temporary_asset_proxy(self):
        return self.get_asset_proxy(self.temporary_asset_package_path)

    @property
    def user_asset_container_package_paths(self):
        return self._user_asset_container_package_paths

    ### PUBLIC METHODS ###

    def list_asset_container_package_paths(self, head=None):
        result = []
        result.extend(self.list_system_asset_container_package_paths(head=head))
        result.extend(self.list_score_internal_asset_container_package_paths(head=head))
        return result

    def list_asset_package_paths(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_package_paths(head=head))
        result.extend(self.list_score_internal_asset_package_paths(head=head))
        result.extend(self.list_user_asset_package_paths(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for package_path in self.list_asset_package_paths(head=head):
            asset_proxy = self.get_asset_proxy(package_path)
            result.append(asset_proxy)
        return result

    def list_score_external_asset_package_paths(self, head=None):
        result = []
        for directory_path in self.list_score_external_asset_container_directory_paths(head=head):
            for directory_entry in os.listdir(directory_path):
                package_path = packagepathtools.filesystem_path_to_package_path(directory_path)
                if directory_entry[0].isalpha():
                    result.append('.'.join([package_path, directory_entry]))
        return result

    def list_score_internal_asset_package_paths(self, head=None):
        result = []
        for asset_container_package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            if self.score_internal_asset_container_package_path_infix:
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
        for asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(asset_proxy.package_path)
        return result

    def make_asset_container_packages(self, is_interactive=False):
        self.make_score_external_asset_container_package()
        self.make_score_internal_asset_container_packages()
        self.io.proceed('missing packages created.', is_interactive=is_interactive)

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
        for package_path in self.list_system_asset_container_package_paths():
            self.make_empty_package(package_path)

    def make_score_internal_asset_container_packages(self, head=None):
        for score_internal_asset_container_package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            self.make_empty_package(score_internal_asset_container_package_path)

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_package_paths(head=head)
        bodies = self.list_space_delimited_lowercase_visible_asset_names(head=head)
        return zip(keys, bodies)
