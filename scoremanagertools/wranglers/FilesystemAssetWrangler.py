# -*- encoding: utf-8 -*-
import abc
import os
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanagertools.scoremanager.ScoreManagerObject \
    import ScoreManagerObject


class FilesystemAssetWrangler(ScoreManagerObject):
    r'''Filesystem asset wrangler.
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
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_filesystem_path(self):
        if self.session.is_in_score:
            parts = []
            parts.append(self.session.current_score_directory_path)
            parts.extend(self.score_package_asset_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.asset_storehouse_filesystem_path_in_built_in_asset_library

    @property
    def _temporary_asset_filesystem_path(self):
        return os.path.join(
            self._current_storehouse_filesystem_path, 
            self._temporary_asset_name)

    @property
    def _temporary_asset_manager(self):
        return self._initialize_asset_manager(
            self._temporary_asset_filesystem_path)

    @abc.abstractproperty
    def _temporary_asset_name(self):
        pass

    ### PRIVATE METHODS ###

    def _filesystem_path_to_space_delimited_lowercase_name(
        self, 
        filesystem_path,
        ):
        filesystem_path = os.path.normpath(filesystem_path)
        asset_name = os.path.basename(filesystem_path)
        if '.' in asset_name:
            asset_name = asset_name[:asset_name.rindex('.')]
        return stringtools.string_to_space_delimited_lowercase(asset_name)

    def _get_current_directory_path_of_interest(self):
        score_directory_path = self.session.current_score_directory_path
        if score_directory_path is not None:
            parts = (score_directory_path,)
            parts += self.score_package_asset_storehouse_path_infix_parts
            directory_path = os.path.join(*parts)
            assert '.' not in directory_path, repr(directory_path)
            return directory_path

    def _get_current_package_manager(self):
        from experimental.tools import scoremanagertools
        directory_path = self._get_current_directory_path_of_interest()
        if directory_path is None:
            return
        manager = scoremanagertools.managers.PackageManager(
            directory_path,
            session=self.session,
            )
        return manager

    def _get_current_view_file_path(self):
        directory_path = self._get_current_directory_path_of_interest()
        if directory_path:
            file_path = os.path.join(
                directory_path,
                '__views__.py',
                )
            return file_path

    def _get_current_view_module_manager(self):
        from experimental.tools import scoremanagertools
        file_path = self._get_current_view_file_path()
        manager = scoremanagertools.managers.FileManager(
            file_path,
            session=self.session,
            )
        return manager

    @abc.abstractmethod
    def _handle_main_menu_result(self, result):
        pass

    def _initialize_asset_manager(self, filesystem_path):
        assert os.path.sep in filesystem_path, repr(filesystem_path)
        return self._asset_manager_class(
            filesystem_path=filesystem_path, 
            session=self.session,
            )

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry not in self.forbidden_directory_entries:
            if directory_entry[0].isalpha():
                return True
        return False

    def _make_asset_selection_breadcrumb(
        self, 
        infinitival_phrase=None, 
        is_storehouse=False,
        ):
        if infinitival_phrase:
            return 'select {} {}:'.format(
                self._asset_manager_class._generic_class_name, 
                infinitival_phrase)
        elif is_storehouse:
            return 'select {} storehouse:'.format(
                self._asset_manager_class._generic_class_name)
        else:
            return 'select {}:'.format(
                self._asset_manager_class._generic_class_name)

    def _make_asset_selection_menu(self, head=None):
        menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        return menu

    def _make_asset_storehouse_menu_entries(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        ):
        from experimental.tools import scoremanagertools
        keys, display_strings = [], []
        keys.append(
            self.asset_storehouse_filesystem_path_in_user_asset_library)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = scoremanagertools.wranglers.ScorePackageWrangler(
            session=self.session)
        for manager in wrangler.list_asset_managers(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            ):
            display_strings.append(manager._get_title())
            path_parts = (manager.filesystem_path,) + \
                self.score_package_asset_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    @abc.abstractmethod
    def _make_main_menu(self, head=None):
        pass

    def _read_view_inventory_from_disk(self):
        from experimental.tools import scoremanagertools
        view_file_path = self._get_current_view_file_path()
        if view_file_path is None:
            return
        manager = scoremanagertools.managers.FileManager(
            view_file_path,
            session=self.session,
            )
        view_inventory = manager._execute_file_lines(
            return_attribute_name='view_inventory',
            )
        return view_inventory

    def _run(
        self, 
        cache=False, 
        clear=True, 
        head=None, 
        rollback=None, 
        pending_user_input=None,
        ):
        self.session.io_manager._assign_user_input(pending_user_input)
        breadcrumb = self.session.pop_breadcrumb(rollback=rollback)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu(head=head)
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)
        self.session.restore_breadcrumbs(cache=cache)

    ### PUBLIC METHODS ###

    def interactively_list_directory(self):
        manager = self._get_current_package_manager()
        manager.interactively_list_directory()

    def interactively_list_views(
        self,
        pending_user_input=None,
        ):
        self.session.io_manager._assign_user_input(pending_user_input)
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            message = 'no views found.'
            self.session.io_manager.proceed(message)
            return
        lines = []
        names = [x.name for x in view_inventory]
        view_count = len(view_inventory)
        view_string = 'view'
        if view_count != 1:
            view_string = stringtools.pluralize_string(view_string)
        message = '{} {} found:'
        message = message.format(view_count, view_string)
        lines.append(message)
        lines.append('')
        names = ['\t' + x for x in names]
        lines.extend(names)
        lines.append('')
        self.session.io_manager.display(lines)
        self.session.io_manager.proceed()

    @abc.abstractmethod
    def interactively_make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively makes asset.

        Returns none.
        '''
        pass

    def interactively_make_view(
        self,
        pending_user_input=None,
        ):
        from experimental.tools import scoremanagertools
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('view name')
        with self.backtracking:
            view_name = getter._run()
        if self.session.backtrack():
            return
        head = self.session.current_score_package_path
        menu_entries = self._make_asset_menu_entries(head=head)
        display_strings = [x[0] for x in menu_entries]
        editor = scoremanagertools.editors.ListEditor(
            session=self.session,
            target=display_strings,
            )
        breadcrumb = 'edit {} view'
        breadcrumb = breadcrumb.format(view_name)
        editor.explicit_breadcrumb = breadcrumb
        with self.backtracking:
            editor._run()
        if self.session.backtrack():
            return
        tokens = editor.target
        self.session.io_manager.display('')
        view = self.session.io_manager.make_view(tokens, custom_identifier=view_name)
        self.write_view_to_disk(view)

    # TODO: write test
    def interactively_remove_assets(
        self, 
        head=None,
        pending_user_input=None,
        ):
        r'''Interactively removes assets.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        getter = self.session.io_manager.make_getter(where=self._where)
        asset_section = self._main_menu._asset_section
        getter.append_menu_section_range(
            'number(s) to remove', 
            asset_section,
            )
        result = getter._run()
        if self.session.backtrack():
            return
        asset_indices = [asset_number - 1 for asset_number in result]
        total_assets_removed = 0
        for asset_number in result:
            asset_index = asset_number - 1
            menu_entry = asset_section.menu_entries[asset_index]
            asset_filesystem_path = menu_entry.return_value
            asset_manager = self._initialize_asset_manager(asset_filesystem_path)
            asset_manager._remove()
            total_assets_removed += 1
        if total_assets_removed == 1:
            asset_string = 'asset'
        else:
            asset_string = 'assets'
        message = '{} {} removed.'
        message = message.format(total_assets_removed, asset_string)
        self.session.io_manager.proceed(message)

    # TODO: write test
    def interactively_rename_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively renames asset.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            asset_filesystem_path = \
                self.interactively_select_asset_filesystem_path()
        if self.session.backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_filesystem_path)
        asset_manager.interactively_rename()

    def interactively_select_asset_filesystem_path(
        self, 
        clear=True, 
        cache=False,
        pending_user_input=None,
        ):
        r'''Interactively selects asset filesystem path.

        Returns string.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        menu = self._make_asset_selection_menu()
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb()
            self.session.push_breadcrumb(breadcrumb)
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

    def interactively_select_asset_storehouse_filesystem_path(
        self,
        clear=True, 
        cache=False,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        pending_user_input=None,
        ):
        r'''Interactively selects asset storehouse filesystem path.

        Returns string.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        menu_entries = self._make_asset_storehouse_menu_entries(
            in_built_in_asset_library=False,
            in_user_asset_library=True,
            in_built_in_score_packages=False,
            in_user_score_packages=False)
        asset_section.menu_entries = menu_entries
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb(
                is_storehouse=True)
            self.session.push_breadcrumb(breadcrumb)
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

    def interactively_select_view(
        self,
        pending_user_input=None,
        ):
        self.session.io_manager._assign_user_input(pending_user_input)
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            message = 'no views found.'
            self.session.io_manager.proceed(message)
            return
        lines = []
        view_names = [x.name for x in view_inventory]
        selector = self.session.io_manager.make_selector(where=self._where)
        selector.explicit_breadcrumb = 'select view'
        selector.items = view_names
        with self.backtracking:
            view_name = selector._run()
        if self.session.backtrack():
            return
        manager = self._get_current_package_manager()
        manager._add_metadata('view_name', view_name)

    def interactively_view_initializer(self):
        manager = self._get_current_package_manager()
        manager.interactively_view_initializer()

    def interactively_view_metadata_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_view_metadata_module()

    def interactively_view_views_module(self):
        manager = self._get_current_view_module_manager()
        #manager.interactively_view()
        manager.interactively_edit()

    def list_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Returns list.
        '''
        result = []
        for directory_path in self.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            ):
            if not directory_path:
                continue
            storehouse_package_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                directory_path)
            if not os.path.exists(directory_path):
                continue
            for directory_entry in sorted(os.listdir(directory_path)):
                if self._is_valid_directory_entry(directory_entry):
                    filesystem_path = os.path.join(
                        directory_path, directory_entry,
                        )
                    if head is None:
                        result.append(filesystem_path)
                    else:
                        package_path = '.'.join([
                            storehouse_package_path, directory_entry,
                            ])
                        if package_path.startswith(head):
                            result.append(filesystem_path)
        return result

    def list_asset_managers(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Returns list.
        '''
        if hasattr(self, 'list_visible_asset_managers'):
            return self.list_visible_asset_managers(head=head)
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head):
            asset_manager = self._initialize_asset_manager(filesystem_path)
            result.append(asset_manager)
        return result

    def list_asset_names(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        head=None, 
        include_extension=False,
        ):
        r'''Lists asset names.

        Returns list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            if include_extension:
                result.append(os.path.basename(filesystem_path))
            else:
                result.append(
                    self._filesystem_path_to_space_delimited_lowercase_name(
                        filesystem_path))
        return result

    def list_asset_storehouse_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Returns list.
        '''
        result = []
        if in_built_in_asset_library and \
            self.asset_storehouse_filesystem_path_in_built_in_asset_library is not None:
            result.append(
                self.asset_storehouse_filesystem_path_in_built_in_asset_library)
        if in_user_asset_library and \
            self.asset_storehouse_filesystem_path_in_user_asset_library is not None:
            result.append(
                self.asset_storehouse_filesystem_path_in_user_asset_library)
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
            for directory_path in \
                self.configuration.list_score_directory_paths(user=True):
                parts = [directory_path]
                if self.score_package_asset_storehouse_path_infix_parts:
                    parts.extend(
                        self.score_package_asset_storehouse_path_infix_parts)
                filesystem_path = os.path.join(*parts)
                result.append(filesystem_path)
        return result

    def make_asset(self, asset_name):
        r'''Makes asset.

        Returns none.
        '''
        assert stringtools.is_snake_case_string(asset_name)
        asset_filesystem_path = os.path.join(
            self._current_storehouse_filesystem_path, asset_name)
        asset_manager = self._initialize_asset_manager(asset_filesystem_path)
        asset_manager._write_stub_to_disk()

    def write_view_to_disk(self, new_view, prompt=True):
        view_inventory = self._read_view_inventory_from_disk()
        view_inventory = view_inventory or datastructuretools.TypedList()
        for i, view in enumerate(view_inventory):
            if view.name == new_view.name:
                view_inventory[i] = new_view
                break
        else:
            view_inventory.append(new_view)
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        line = 'from scoremanagertools import iotools\n'
        lines.append(line)
        lines.append('\n\n')
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        lines = ''.join(lines)
        view_file_path = self._get_current_view_file_path()
        file_pointer = file(view_file_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()
        message = 'view written to disk.'
        self.session.io_manager.proceed(message, is_interactive=prompt)

    ### UI MANIFEST ###

    user_input_to_action = {
        'initializer': interactively_view_initializer,
        'ls': interactively_list_directory,
        'metadata': interactively_view_metadata_module,
        'ren': interactively_rename_asset,
        'rm': interactively_remove_assets,
        'views': interactively_view_views_module,
        'vwl': interactively_list_views,
        'vwn': interactively_make_view,
        'vws': interactively_select_view,
        }
