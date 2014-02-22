# -*- encoding: utf-8 -*-
import abc
import os
import subprocess
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Wrangler(ScoreManagerObject):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None):
        ScoreManagerObject.__init__(self, session=session)
        self.built_in_storehouse_directory_path = None
        self.user_storehouse_directory_path = None
        self.score_storehouse_path_infix_parts = ()
        self.forbidden_directory_entries = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_directory_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory_path)
            parts.extend(self.score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.built_in_storehouse_directory_path

    @property
    def _temporary_asset_filesystem_path(self):
        return os.path.join(
            self._current_storehouse_directory_path, 
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
        score_directory_path = self._session.current_score_directory_path
        if score_directory_path is not None:
            parts = (score_directory_path,)
            parts += self.score_storehouse_path_infix_parts
            directory_path = os.path.join(*parts)
            assert '.' not in directory_path, repr(directory_path)
            return directory_path

    def _get_current_package_manager(self):
        from scoremanager import managers
        directory_path = self._get_current_directory_path_of_interest()
        if directory_path is None:
            return
        manager = managers.PackageManager(
            directory_path,
            session=self._session,
            )
        return manager

    def _get_current_view_module_manager(self):
        from scoremanager import managers
        file_path = self.views_module_path
        manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        return manager

    @abc.abstractmethod
    def _handle_main_menu_result(self, result):
        pass

    def _initialize_asset_manager(self, filesystem_path):
        assert os.path.sep in filesystem_path, repr(filesystem_path)
        return self._asset_manager_class(
            filesystem_path=filesystem_path, 
            session=self._session,
            )

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry not in self.forbidden_directory_entries:
            if directory_entry[0].isalpha():
                return True
        return False

    def _make_asset_selection_breadcrumb(
        self, 
        human_readable_target_name=None,
        infinitival_phrase=None, 
        is_storehouse=False,
        ):
        if human_readable_target_name is None:
            generic_class_name = self._asset_manager_class._generic_class_name
            human_readable_target_name = generic_class_name
        if infinitival_phrase:
            return 'select {} {}:'.format(
                human_readable_target_name,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select {} storehouse:'.format(human_readable_target_name)
        else:
            return 'select {}:'.format(human_readable_target_name)

    def _make_asset_selection_menu(self, head=None):
        menu = self._session.io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        return menu

    def _make_storehouse_menu_entries(
        self,
        in_built_in_library=True,
        in_user_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        ):
        from scoremanager import wranglers
        keys, display_strings = [], []
        keys.append(
            self.user_storehouse_directory_path)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = wranglers.ScorePackageWrangler(
            session=self._session)
        for manager in wrangler.list_asset_managers(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            ):
            display_strings.append(manager._get_title())
            path_parts = (manager.filesystem_path,) + \
                self.score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    @abc.abstractmethod
    def _make_main_menu(self, head=None):
        pass

    def _read_view_inventory_from_disk(self):
        from scoremanager import managers
        view_file_path = self.views_module_path
        if view_file_path is None:
            return
        manager = managers.FileManager(
            view_file_path,
            session=self._session,
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
        self._session._push_controller(self)
        self._session.io_manager._assign_user_input(pending_user_input)
        breadcrumb = self._session._pop_breadcrumb(rollback=rollback)
        self._session._cache_breadcrumbs(cache=cache)
        while True:
            self._session._push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu(head=head)
            result = menu._run(clear=clear)
            if self._session._backtrack():
                break
            elif not result:
                self._session._pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self._session._backtrack():
                break
            self._session._pop_breadcrumb()
        self._session._pop_controller()
        self._session._pop_breadcrumb()
        self._session._push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)
        self._session._restore_breadcrumbs(cache=cache)

    ### PUBLIC PROPERTIES ###

    @property
    def views_module_path(self):
        directory_path = self._get_current_directory_path_of_interest()
        file_path = os.path.join(directory_path, '__views__.py')
        return file_path

    ### PUBLIC METHODS ###

    def interactively_add_metadatum(self):
        manager = self._get_current_package_manager()
        manager.interactively_add_metadatum()

    def interactively_get_metadatum(self):
        manager = self._get_current_package_manager()
        manager.interactively_get_metadatum()

    def interactively_list_directory(self):
        manager = self._get_current_package_manager()
        manager.interactively_list_directory()

    def interactively_list_views(
        self,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            message = 'no views found.'
            self._session.io_manager.proceed(message)
            return
        lines = []
        names = view_inventory.keys()
        view_count = len(view_inventory)
        view_string = 'view'
        if view_count != 1:
            view_string = stringtools.pluralize_string(view_string)
        message = '{} {} found:'
        message = message.format(view_count, view_string)
        lines.append(message)
        lines.append('')
        tab_width = self.configuration.get_tab_width()
        tab = tab_width * ' '
        names = [tab + x for x in names]
        lines.extend(names)
        lines.append('')
        self._session.io_manager.display(lines)
        self._session.io_manager.proceed()

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
        from scoremanager import editors
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_string('view name')
        with self.backtracking:
            view_name = getter._run()
        if self._session._backtrack():
            return
        head = self._session.current_score_package_path
        menu_entries = self._make_asset_menu_entries(head=head)
        display_strings = [x[0] for x in menu_entries]
        editor = editors.ListEditor(
            session=self._session,
            target=display_strings,
            )
        breadcrumb = 'edit {} view'
        breadcrumb = breadcrumb.format(view_name)
        editor.explicit_breadcrumb = breadcrumb
        with self.backtracking:
            editor._run()
        if self._session._backtrack():
            return
        tokens = editor.target
        self._session.io_manager.display('')
        view = self._session.io_manager.make_view(
            tokens, 
            )
        self.write_view(view_name, view)

    # TODO: write test
    def interactively_remove_assets(
        self, 
        head=None,
        pending_user_input=None,
        ):
        r'''Interactively removes assets.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        getter = self._session.io_manager.make_getter(where=self._where)
        asset_section = self._main_menu._asset_section
        getter.append_menu_section_range(
            'number(s) to remove', 
            asset_section,
            )
        result = getter._run()
        if self._session._backtrack():
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
        self._session.io_manager.proceed(message)

    # TODO: write test
    def interactively_rename_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively renames asset.

        Returns none.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            asset_filesystem_path = \
                self.interactively_select_asset_filesystem_path()
        if self._session._backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_filesystem_path)
        asset_manager.interactively_rename()

    def interactively_remove_initializer_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_remove_initializer_module()

    def interactively_remove_metadata_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_remove_metadata_module()

    def interactively_remove_metadatum(self):
        manager = self._get_current_package_manager()
        manager.interactively_remove_metadatum()

    def interactively_remove_views_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_remove_views_module()

    def interactively_rewrite_metadata_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_rewrite_metadata_module()

    def run_doctest(self, prompt=True):
        path = self._get_current_directory_path_of_interest()
        command = 'ajv doctest {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            if lines[0] == '':
                lines.remove('')
            lines.append('')
            self._session.io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._session.io_manager.proceed(prompt=prompt)

    def run_pytest(self, prompt=True):
        path = self._get_current_directory_path_of_interest()
        command = 'py.test -rf {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._session.io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._session.io_manager.proceed(prompt=prompt)

    def interactively_select_asset_filesystem_path(
        self, 
        clear=True, 
        cache=False,
        pending_user_input=None,
        ):
        r'''Interactively selects asset filesystem path.

        Returns string.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        menu = self._make_asset_selection_menu()
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb()
            self._session._push_breadcrumb(breadcrumb)
            result = menu._run(clear=clear)
            if self._session._backtrack():
                break
            elif not result:
                self._session._pop_breadcrumb()
                continue
            else:
                break
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)
        return result

    def interactively_select_storehouse_directory_path(
        self,
        clear=True, 
        cache=False,
        in_built_in_library=True,
        in_user_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        pending_user_input=None,
        ):
        r'''Interactively selects asset storehouse filesystem path.

        Returns string.
        '''
        self._session.io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        menu = self._session.io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        menu_entries = self._make_storehouse_menu_entries(
            in_built_in_library=False,
            in_user_library=True,
            in_built_in_score_packages=False,
            in_user_score_packages=False)
        asset_section.menu_entries = menu_entries
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb(
                is_storehouse=True)
            self._session._push_breadcrumb(breadcrumb)
            result = menu._run(clear=clear)
            if self._session._backtrack():
                break
            elif not result:
                self._session._pop_breadcrumb()
                continue
            else:
                break
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)
        return result

    def interactively_select_view(
        self,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            message = 'no views found.'
            self._session.io_manager.proceed(message)
            return
        lines = []
        view_names = view_inventory.keys()
        selector = self._session.io_manager.make_selector(where=self._where)
        selector.explicit_breadcrumb = 'select view'
        selector.items = view_names
        with self.backtracking:
            view_name = selector._run()
        if self._session._backtrack():
            return
        manager = self._get_current_package_manager()
        manager._add_metadatum('view_name', view_name)

    def interactively_view_initializer_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_view_initializer_module()

    def interactively_view_metadata_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_view_metadata_module()

    def interactively_view_views_module(self):
        manager = self._get_current_view_module_manager()
        manager.interactively_edit()

    def interactively_write_boilerplate_initializer_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_write_boilerplate_initializer_module()

    def interactively_write_stub_initializer_module(self):
        manager = self._get_current_package_manager()
        manager.interactively_write_stub_initializer_module()

    def list_asset_filesystem_paths(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Returns list.
        '''
        result = []
        for directory_path in self.list_storehouse_directory_paths(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            ):
            if not directory_path:
                continue
            storehouse_package_path = \
                self.configuration.filesystem_path_to_package_path(
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
        in_built_in_library=True, 
        in_user_library=True,
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
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head):
            asset_manager = self._initialize_asset_manager(filesystem_path)
            result.append(asset_manager)
        return result

    def list_asset_names(
        self,
        in_built_in_library=True, 
        in_user_library=True,
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
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
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

    def list_storehouse_directory_paths(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Returns list.
        '''
        result = []
        if in_built_in_library and \
            self.built_in_storehouse_directory_path is not None:
            result.append(self.built_in_storehouse_directory_path)
        if in_user_library and self.user_storehouse_directory_path is not None:
            result.append(self.user_storehouse_directory_path)
        if in_built_in_score_packages and \
            self.score_storehouse_path_infix_parts:
            for score_directory_path in \
                self.configuration.list_score_directory_paths(built_in=True):
                parts = [score_directory_path]
                if self.score_storehouse_path_infix_parts:
                    parts.extend(self.score_storehouse_path_infix_parts)
                storehouse_directory_path = os.path.join(*parts)
                result.append(storehouse_directory_path)
        if in_user_score_packages and self.score_storehouse_path_infix_parts:
            for directory_path in \
                self.configuration.list_score_directory_paths(user=True):
                parts = [directory_path]
                if self.score_storehouse_path_infix_parts:
                    parts.extend(self.score_storehouse_path_infix_parts)
                filesystem_path = os.path.join(*parts)
                result.append(filesystem_path)
        return result

    def make_asset(self, asset_name):
        r'''Makes asset.

        Returns none.
        '''
        assert stringtools.is_snake_case_string(asset_name)
        asset_filesystem_path = os.path.join(
            self._current_storehouse_directory_path, asset_name)
        asset_manager = self._initialize_asset_manager(asset_filesystem_path)
        asset_manager._write_stub()

    def write_view(self, view_name, new_view, prompt=True):
        from scoremanager import iotools
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            view_inventory = datastructuretools.TypedOrderedDict(
                item_class=iotools.View,
                )
        view_inventory[view_name] = new_view
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        line = 'from scoremanager import iotools\n'
        lines.append(line)
        lines.append('\n\n')
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        lines = ''.join(lines)
        view_file_path = self.views_module_path
        file_pointer = file(view_file_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()
        message = 'view written to disk.'
        self._session.io_manager.proceed(message, prompt=prompt)

    ### UI MANIFEST ###

    user_input_to_action = {
        'inbp': interactively_write_boilerplate_initializer_module,
        'inrm': interactively_remove_initializer_module,
        'ins': interactively_write_stub_initializer_module,
        'inv': interactively_view_initializer_module,
        'ls': interactively_list_directory,
        'mda': interactively_add_metadatum,
        'mdg': interactively_get_metadatum,
        'mdrm': interactively_remove_metadatum,
        'mdmrm': interactively_remove_metadata_module,
        'mdmrw': interactively_rewrite_metadata_module,
        'mdmv': interactively_view_metadata_module,
        'ren': interactively_rename_asset,
        'rm': interactively_remove_assets,
        'vwl': interactively_list_views,
        'vwn': interactively_make_view,
        'vws': interactively_select_view,
        'vwmrm': interactively_remove_views_module,
        'vwmv': interactively_view_views_module,
        }
