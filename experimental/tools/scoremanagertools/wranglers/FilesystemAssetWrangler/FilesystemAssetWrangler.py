import abc
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject \
    import ScoreManagerObject


class FilesystemAssetWrangler(ScoreManagerObject):
    '''Filesystem asset wrangler.

    Return filesystem asset wrangler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    forbidden_directory_entries = ()

    score_package_asset_storehouse_path_infix_parts = ()

    ### INITIALIZER ###

    def __init__(self, session=None):
        ScoreManagerObject.__init__(self, session=session)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when types are the same. Otherwise false.

        Return boolean.
        '''
        return type(self) is type(expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_filesystem_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory_path)
            parts.extend(self.score_package_asset_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.asset_storehouse_filesystem_path_in_built_in_asset_library

    @property
    def _temporary_asset_filesystem_path(self):
        return os.path.join(
            self._current_storehouse_filesystem_path, 
            self._temporary_asset_name)

    @abc.abstractproperty
    def _temporary_asset_name(self):
        pass

    @property
    def _temporary_asset_proxy(self):
        return self._initialize_asset_proxy(
            self._temporary_asset_filesystem_path)

    ### PRIVATE METHODS ###

    def _filesystem_path_to_space_delimited_lowercase_name(
        self, filesystem_path):
        filesystem_path = os.path.normpath(filesystem_path)
        asset_name = os.path.basename(filesystem_path)
        if '.' in asset_name:
            asset_name = asset_name[:asset_name.rindex('.')]
        return stringtools.string_to_space_delimited_lowercase(asset_name)

    @abc.abstractmethod
    def _handle_main_menu_result(self, result):
        pass

    def _initialize_asset_proxy(self, filesystem_path):
        assert os.path.sep in filesystem_path, repr(filesystem_path)
        return self.asset_proxy_class(
            filesystem_path=filesystem_path, session=self._session)

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry not in self.forbidden_directory_entries:
            if directory_entry[0].isalpha():
                return True
        return False

    def _make_asset_selection_breadcrumb(
        self, infinitival_phrase=None, is_storehouse=False):
        if infinitival_phrase:
            return 'select {} {}:'.format(
                self.asset_proxy_class._generic_class_name, 
                infinitival_phrase)
        elif is_storehouse:
            return 'select {} storehouse:'.format(
                self.asset_proxy_class._generic_class_name)
        else:
            return 'select {}:'.format(
                self.asset_proxy_class._generic_class_name)

    def _make_asset_selection_menu(self, head=None):
        menu_entries = self._make_asset_menu_entries(head=head)
        menu, menu_section = self._io.make_menu(
            where=self._where,
            return_value_attribute='key',
            menu_entries=menu_entries,
            is_numbered=True,
            )
        return menu

    def _make_asset_storehouse_menu_entries(self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True):
        from experimental.tools import scoremanagertools
        keys, display_strings = [], []
        keys.append(
            self.asset_storehouse_filesystem_path_in_user_asset_library)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = scoremanagertools.wranglers.ScorePackageWrangler(
            session=self._session)
        for proxy in wrangler.list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages):
            display_strings.append(proxy.title)
            path_parts = (proxy.filesystem_path,) + \
                self.score_package_asset_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        return zip(display_strings, keys)

    @abc.abstractmethod
    def _make_main_menu(self, head=None):
        pass

    def _make_asset_menu_entries(self, head=None, include_extension=False):
        raise Exception('FOO')
        keys = self.list_asset_filesystem_paths(head=head)
        display_strings = self.list_asset_names(
            head=head, include_extension=include_extension)
        return zip(display_strings, keys)

    def _run(self, 
        cache=False, 
        clear=True, 
        head=None, 
        rollback=None, 
        pending_user_input=None,
        ):
        self._io.assign_user_input(pending_user_input=pending_user_input)
        breadcrumb = self._session.pop_breadcrumb(rollback=rollback)
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            self._session.push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu(head=head)
            result = menu._run(clear=clear)
            if self._session.backtrack():
                break
            elif not result:
                self._session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self._session.backtrack():
                break
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)
        self._session.restore_breadcrumbs(cache=cache)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def asset_proxy_class(self):
        pass

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def interactively_make_asset(self):
        pass

    # TODO: write test
    def interactively_remove_assets(self, head=None):
        getter = self._io.make_getter(where=self._where)
        asset_menu_section = self._main_menu._asset_menu_section
        getter.append_menu_section_range(
            'number(s) to remove', asset_menu_section)
        result = getter._run()
        if self._session.backtrack():
            return
        asset_indices = [asset_number - 1 for asset_number in result]
        total_assets_removed = 0
        for asset_number in result:
            asset_index = asset_number - 1
            menu_entry = asset_menu_section.menu_entries[asset_index]
            asset_filesystem_path = menu_entry.return_value
            asset_proxy = self._initialize_asset_proxy(asset_filesystem_path)
            asset_proxy.remove()
            total_assets_removed += 1
        if total_assets_removed == 1:
            asset_string = 'asset'
        else:
            asset_string = 'assets'
        self._io.proceed('{} {} removed.'.format(
            total_assets_removed, asset_string))

    # TODO: write test
    def interactively_rename_asset(self):
        with self.backtracking:
            asset_filesystem_path = \
                self.interactively_select_asset_filesystem_path()
        if self._session.backtrack():
            return
        asset_proxy = self._initialize_asset_proxy(asset_filesystem_path)
        asset_proxy.interactively_rename()

    def interactively_select_asset_filesystem_path(self, 
        clear=True, cache=False):
        self._session.cache_breadcrumbs(cache=cache)
        menu, menu_section = self._io.make_menu(
            where=self._where,
            return_value_attribute='explicit',
            is_numbered=True,
            )
        menu_section.menu_entries = self._make_asset_menu_entries()
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb()
            self._session.push_breadcrumb(breadcrumb)
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

    def interactively_select_asset_storehouse_filesystem_path(self,
        clear=True, cache=False,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True):
        self._session.cache_breadcrumbs(cache=cache)
        menu, menu_section = self._io.make_menu(
            where=self._where,
            is_numbered=True,
            return_value_attribute='key',
            )
        menu_section.menu_entries = self._make_asset_storehouse_menu_entries(
            in_built_in_asset_library=False,
            in_user_asset_library=True,
            in_built_in_score_packages=False,
            in_user_score_packages=False)
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb(
                is_storehouse=True)
            self._session.push_breadcrumb(breadcrumb)
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

    def list_asset_filesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        result = []
        for directory_path in self.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages):
            if directory_path:
                storehouse_package_path = \
                    self.configuration.filesystem_path_to_packagesystem_path(
                    directory_path)
                for directory_entry in os.listdir(directory_path):
                    if self._is_valid_directory_entry(directory_entry):
                        filesystem_path = os.path.join(
                            directory_path, directory_entry)
                        if head is None:
                            result.append(filesystem_path)
                        else:
                            package_path = '.'.join([
                                storehouse_package_path, directory_entry])
                            if package_path.startswith(head):
                                result.append(filesystem_path)
        return result

    def list_asset_names(self,
        in_built_in_asset_library=True, in_user_asset_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True,
        head=None, include_extension=False):
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head):
            if include_extension:
                result.append(os.path.basename(filesystem_path))
            else:
                result.append(
                    self._filesystem_path_to_space_delimited_lowercase_name(
                        filesystem_path))
        return result

    def list_asset_proxies(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        if hasattr(self, 'list_visible_asset_proxies'):
            return self.list_visible_asset_proxies(head=head)
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head):
            asset_proxy = self._initialize_asset_proxy(filesystem_path)
            result.append(asset_proxy)
        return result

    def list_asset_storehouse_filesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        result = []
        if in_built_in_asset_library and \
            self.asset_storehouse_filesystem_path_in_built_in_asset_library is not None:
            result.append(self.asset_storehouse_filesystem_path_in_built_in_asset_library)
        if in_user_asset_library and \
            self.asset_storehouse_filesystem_path_in_user_asset_library is not None:
            result.append(self.asset_storehouse_filesystem_path_in_user_asset_library)
        if in_built_in_score_packages and \
            self.score_package_asset_storehouse_path_infix_parts is not None:
            for score_directory_path in \
                self.configuration.list_score_directory_paths(built_in=True):
                parts = [score_directory_path]
                if self.score_package_asset_storehouse_path_infix_parts:
                    parts.extend(
                        self.score_package_asset_storehouse_path_infix_parts)
                storehouse_filesystem_path = os.path.join(*parts)
                result.append(storehouse_filesystem_path)
        if in_user_score_packages and \
            self.score_package_asset_storehouse_path_infix_parts is not None:
            for directory_path in self.configuration.list_score_directory_paths(user=True):
                parts = [directory_path]
                if self.score_package_asset_storehouse_path_infix_parts:
                    parts.extend(
                        self.score_package_asset_storehouse_path_infix_parts)
                filesystem_path = os.path.join(*parts)
                result.append(filesystem_path)
        return result

    def make_asset(self, asset_name):
        assert stringtools.is_snake_case_string(asset_name)
        asset_filesystem_path = os.path.join(
            self._current_storehouse_filesystem_path, asset_name)
        asset_proxy = self._initialize_asset_proxy(asset_filesystem_path)
        asset_proxy.write_stub_to_disk()

    ### UI MANIFEST ###

    user_input_to_action = {
        'ren': interactively_rename_asset,
        'rm': interactively_remove_assets,
        }
