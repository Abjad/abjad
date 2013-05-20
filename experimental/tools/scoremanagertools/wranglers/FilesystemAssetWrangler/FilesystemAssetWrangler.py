import abc
import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject


class FilesystemAssetWrangler(ScoreManagerObject):
    '''Filesystem asset wrangler.

    Return filesystem asset wrangler.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    storehouse_path_infix_parts = ()

    ### INITIALIZER ###

    def __init__(self,
        built_in_external_storehouse_filesystem_path=None,
        user_external_storehouse_filesystem_path=None,
        session=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self._built_in_external_storehouse_filesystem_path = \
            built_in_external_storehouse_filesystem_path or ''
        self._user_external_storehouse_filesystem_path = \
            user_external_storehouse_filesystem_path or ''

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when built-in and user storehouse paths are both equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.built_in_external_storehouse_filesystem_path == \
                expr.built_in_external_storehouse_filesystem_path:
                if self.user_external_storehouse_filesystem_path == \
                    expr.user_external_storehouse_filesystem_path:
                        return True
        return False

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_filesystem_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory_path)
            parts.extend(self.storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.built_in_external_storehouse_filesystem_path

    @property
    def _temporary_asset_filesystem_path(self):
        return os.path.join(self._current_storehouse_filesystem_path, self._temporary_asset_name)

    @abc.abstractproperty
    def _temporary_asset_name(self):
        pass

    @property
    def _temporary_asset_proxy(self):
        return self._get_asset_proxy(self._temporary_asset_filesystem_path)

    ### PRIVATE METHODS ###

    def _filesystem_path_to_space_delimited_lowercase_name(self, filesystem_path):
        filesystem_path = os.path.normpath(filesystem_path)
        asset_name = os.path.basename(filesystem_path)
        if '.' in asset_name:
            asset_name = asset_name[:asset_name.rindex('.')]
        return stringtools.string_to_space_delimited_lowercase(asset_name)

    def _get_asset_proxy(self, filesystem_path):
        assert os.path.sep in filesystem_path, repr(filesystem_path)
        return self.asset_proxy_class(filesystem_path=filesystem_path, session=self._session)

    @abc.abstractmethod
    def _handle_main_menu_result(self, result):
        pass

    def _make_asset_selection_breadcrumb(self, infinitival_phrase=None):
        if infinitival_phrase:
            return 'select {} {}:'.format(self.asset_proxy_class._generic_class_name, infinitival_phrase)
        else:
            return 'select {}:'.format(self.asset_proxy_class._generic_class_name)

    def _make_asset_selection_menu(self, head=None):
        menu, section = self._io.make_menu(
            where=self._where, is_keyed=False, is_parenthetically_numbered=True)
        section.tokens = self._make_visible_asset_menu_tokens(head=head)
        section.return_value_attribute = 'key'
        return menu

    @abc.abstractmethod
    def _make_main_menu(self):
        pass

    def _make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_filesystem_paths(head=head)
        bodies = self.list_space_delimited_lowercase_visible_asset_names(head=head)
        return zip(keys, bodies)

    def _run(self, cache=False, clear=True, head=None, rollback=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def asset_proxy_class(self):
        pass

    @property
    def built_in_external_storehouse_filesystem_path(self):
        '''Filesystem asset wrangler user score storehouse filesystem path.

        Return string.
        '''
        return self._built_in_external_storehouse_filesystem_path

    @property
    def user_external_storehouse_filesystem_path(self):
        '''Filesystem asset wrangler user external storehouse filesystem path.

        Return string.
        '''
        return self._user_external_storehouse_filesystem_path
    
    ### PUBLIC METHODS ###

    def get_asset_proxies(self, built_in_external=False, user_external=False,
        built_in_score=False, user_score=False, head=None):
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_external=built_in_external, user_external=user_external,
            built_in_score=built_in_score, user_score=user_score, head=head):
            asset_proxy = self._get_asset_proxy(filesystem_path)
            result.append(asset_proxy)
        return result

    def list_asset_filesystem_paths(self, 
        built_in_external=False, user_external=False,
        built_in_score=False, user_score=False, head=None):
        result = []
        if built_in_external:
            for directory_path in self.list_storehouse_filesystem_paths(
                built_in_external=True, head=head):
                for directory_entry in os.listdir(directory_path):
                    if directory_entry[0].isalpha():
                        filesystem_path = os.path.join(directory_path, directory_entry)
                        result.append(filesystem_path)
        if user_external:
            for directory_path in self.list_storehouse_filesystem_paths(
                user_external=True, head=head):
                for directory_entry in os.listdir(directory_path):
                    if directory_entry[0].isalpha():
                        filesystem_path = os.path.join(directory_path, directory_entry)
                        result.append(filesystem_path)
        if built_in_score:
            for directory_path in self.list_storehouse_filesystem_paths(
                built_in_score=True, head=head):
                for directory_entry in os.listdir(directory_path):
                    if directory_entry[0].isalpha():
                        filesystem_path = os.path.join(directory_path, directory_entry)
                        result.append(filesystem_path)
        if user_score:
            for directory_path in self.list_storehouse_filesystem_paths(
                user_score=True, head=head):
                for directory_entry in os.listdir(directory_path):
                    if directory_entry[0].isalpha():
                        filesystem_path = os.path.join(directory_path, directory_entry)
                        result.append(filesystem_path)
        return result

    def list_space_delimited_lowercase_visible_asset_names(self, head=None):
        result = []
        for filesystem_path in self.list_visible_asset_filesystem_paths(head=head):
            result.append(self._filesystem_path_to_space_delimited_lowercase_name(filesystem_path))
        return result

    def list_storehouse_filesystem_paths(self, 
        built_in_external=False, user_external=False,
        built_in_score=False, user_score=False, head=None):
        result = []
        if built_in_external:
            if head is None:
                result.append(self.built_in_external_storehouse_filesystem_path)
            else:
                filesystem_path = self.configuration.packagesystem_path_to_filesystem_path(head)
                if self.built_in_external_storehouse_filesystem_path.startswith(
                    filesystem_path):
                    result.append(self.built_in_external_storehouse_filesystem_path)
        if user_external:
            if head is None:
                result.append(self.user_external_storehouse_filesystem_path)
            else:
                filesystem_path = self.configuration.packagesystem_path_to_filesystem_path(head)
                if self.user_external_storehouse_filesystem_path.startswith(
                    filesystem_path):
                    result.append(self.user_external_storehouse_filesystem_path)
        if built_in_score:
            for score_directory_path in self.configuration.list_score_directory_paths(
                built_in=True, head=head):
                parts = [score_directory_path]
                parts.extend(self.storehouse_path_infix_parts)
                storehouse_filesystem_path = os.path.join(*parts)
                result.append(storehouse_filesystem_path)
        if user_score:
            for directory_path in self.configuration.list_score_directory_paths(
                user=True, head=head):
                parts = [directory_path]
                if self.storehouse_path_infix_parts:
                    parts.extend(self.storehouse_path_infix_parts)
                filesystem_path = os.path.join(*parts)
                result.append(filesystem_path)
        return result

    def list_visible_asset_filesystem_paths(self, head=None):
        return self.list_asset_filesystem_paths(
            built_in_external=True, user_external=True,
            built_in_score=True, user_score=True, head=head)

    def make_asset(self, asset_name):
        assert stringtools.is_underscore_delimited_lowercase_string(asset_name)
        asset_filesystem_path = os.path.join(self._current_storehouse_filesystem_path, asset_name)
        asset_proxy = self._get_asset_proxy(asset_filesystem_path)
        asset_proxy.write_stub_to_disk()

    @abc.abstractmethod
    def make_asset_interactively(self):
        pass

    # TODO: write test
    def remove_assets_interactively(self, head=None):
        getter = self._io.make_getter(where=self._where)
        argument_list = self.list_visible_asset_filesystem_paths(head=head)
        space_delimited_lowercase_asset_class_name = stringtools.string_to_space_delimited_lowercase(
            self.asset_proxy_class.__name__)
        plural_space_delimited_lowercase_asset_class_name = stringtools.pluralize_string(
            space_delimited_lowercase_asset_class_name)
        getter.append_argument_range(plural_space_delimited_lowercase_asset_class_name, argument_list)
        result = getter._run()
        if self._session.backtrack():
            return
        asset_indices = [asset_number - 1 for asset_number in result]
        total_assets_removed = 0
        for asset_number in result:
            asset_index = asset_number - 1
            asset_filesystem_path = argument_list[asset_index]
            asset_proxy = self._get_asset_proxy(asset_filesystem_path)
            asset_proxy.remove()
            total_assets_removed += 1
        self._io.proceed('{} asset(s) removed.'.format(total_assets_removed))

    # TODO: write test
    def select_asset_filesystem_path_interactively(self, clear=True, cache=False):
        self._session.cache_breadcrumbs(cache=cache)
        menu, section = self._io.make_menu(where=self._where, is_parenthetically_numbered=True)
        tokens = [os.path.basename(x) for x in self.list_visible_asset_filesystem_paths()]
        section.tokens = tokens
        while True:
            breadcrumb = 'select {}'.format(self.asset_proxy_class._generic_class_name)
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
        if result is not None:
            # TODO: this is a hack and will break on user assets
            result = os.path.join(self.built_in_external_storehouse_filesystem_path[0], result)
            return result

    def svn_add_visible_assets(self, is_interactive=True):
        for asset_proxy in self.get_visible_asset_proxies():
            asset_proxy.svn_add(is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)

    def svn_ci_visible_assets(self, is_interactive=True):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._session.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self._io.display(line)
        if not self._io.confirm():
            return
        for asset_proxy in self.get_visible_asset_proxies():
            asset_proxy.svn_ci(commit_message=commit_message, is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)

    def svn_st_visible_assets(self, is_interactive=True):
        for asset_proxy in self.get_visible_asset_proxies():
            asset_proxy.svn_st(is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)

    def svn_up_visible_assets(self, is_interactive=True):
        for asset_proxy in self.get_visible_asset_proxies():
            asset_proxy.svn_up(is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)
