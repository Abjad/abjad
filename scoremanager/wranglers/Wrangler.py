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
        self.abjad_storehouse_directory_path = None
        self.user_storehouse_directory_path = None
        self.score_storehouse_path_infix_parts = ()
        self.forbidden_directory_entries = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _current_package_manager(self):
        from scoremanager import managers
        directory_path = self._get_current_directory_path_of_interest()
        if directory_path is None:
            return
        return managers.PackageManager(
            directory_path,
            session=self._session,
            )

    @property
    def _current_storehouse_directory_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory_path)
            parts.extend(self.score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.abjad_storehouse_directory_path

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

    @property
    def _user_input_to_action(self):
        _user_input_to_action = {
            'inbp': self.write_initializer_boilerplate,
            'inrm': self.remove_initializer,
            'ins': self.write_initializer_stub,
            'inv': self.view_initializer,
            'ls': self.list_directory,
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdrm': self.remove_metadatum,
            'mdmrm': self.remove_metadata_module,
            'mdmrw': self.rewrite_metadata_module,
            'mdmv': self.view_metadata_module,
            'ren': self.rename_asset,
            'rm': self.remove_assets,
            'vwl': self.list_views,
            'vwn': self.make_view,
            'vws': self.select_view,
            'vwmrm': self.remove_views_module,
            'vwmv': self.view_views_module,
            }
        return _user_input_to_action

    @property
    def _views_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._views_module_path,
            session=self._session,
            )

    @property
    def _views_module_path(self):
        directory_path = self._get_current_directory_path_of_interest()
        file_path = os.path.join(directory_path, '__views__.py')
        return file_path

    ### PRIVATE METHODS ###

    @staticmethod
    def _filesystem_path_to_space_delimited_lowercase_name(filesystem_path):
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

    def _list_asset_filesystem_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        result = []
        for directory_path in self._list_storehouse_directory_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            ):
            if not directory_path:
                continue
            if not os.path.exists(directory_path):
                continue
            for directory_entry in sorted(os.listdir(directory_path)):
                if not self._is_valid_directory_entry(directory_entry):
                    continue
                path = os.path.join(directory_path, directory_entry)
                if head is None:
                    result.append(path)
                else:
                    package = self._configuration.path_to_package(path)
                    if package.startswith(head):
                        result.append(path)
        return result

    def _list_asset_managers(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        if hasattr(self, '_list_visible_asset_managers'):
            return self._list_visible_asset_managers(head=head)
        result = []
        for filesystem_path in self._list_asset_filesystem_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head):
            asset_manager = self._initialize_asset_manager(filesystem_path)
            result.append(asset_manager)
        return result

    def _list_asset_names(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        head=None, 
        include_extension=False,
        ):
        result = []
        for filesystem_path in self._list_asset_filesystem_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            if include_extension:
                result.append(os.path.basename(filesystem_path))
            else:
                result.append(
                    self._filesystem_path_to_space_delimited_lowercase_name(
                        filesystem_path))
        return result

    def _list_storehouse_directory_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        result = []
        if abjad_library and \
            self.abjad_storehouse_directory_path is not None:
            result.append(self.abjad_storehouse_directory_path)
        if user_library and self.user_storehouse_directory_path is not None:
            result.append(self.user_storehouse_directory_path)
        if abjad_score_packages and \
            self.score_storehouse_path_infix_parts:
            for score_directory_path in \
                self._configuration.list_score_directory_paths(abjad=True):
                parts = [score_directory_path]
                if self.score_storehouse_path_infix_parts:
                    parts.extend(self.score_storehouse_path_infix_parts)
                storehouse_directory_path = os.path.join(*parts)
                result.append(storehouse_directory_path)
        if user_score_packages and self.score_storehouse_path_infix_parts:
            for directory_path in \
                self._configuration.list_score_directory_paths(user=True):
                parts = [directory_path]
                if self.score_storehouse_path_infix_parts:
                    parts.extend(self.score_storehouse_path_infix_parts)
                filesystem_path = os.path.join(*parts)
                result.append(filesystem_path)
        return result

    def _make_asset(self, asset_name):
        assert stringtools.is_snake_case_string(asset_name)
        path = os.path.join(
            self._current_storehouse_directory_path, 
            asset_name,
            )
        manager = self._initialize_asset_manager(path)
        manager._write_stub()

    def _make_asset_selection_breadcrumb(
        self, 
        human_readable_target_name=None,
        infinitival_phrase=None, 
        is_storehouse=False,
        ):
        if human_readable_target_name is None:
            manager = self._asset_manager_class()
            generic_class_name = manager._generic_class_name
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
        menu = self._io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        return menu

    @abc.abstractmethod
    def _make_main_menu(self, head=None):
        pass

    def _make_storehouse_menu_entries(
        self,
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        ):
        from scoremanager import wranglers
        keys, display_strings = [], []
        keys.append(self.user_storehouse_directory_path)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        managers = wrangler._list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )
        for manager in managers:
            display_strings.append(manager._get_title())
            path_parts = (manager._filesystem_path,)
            path_parts = path_parts + self.score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _read_view_inventory_from_disk(self):
        if self._views_module_path is None:
            return
        view_inventory = self._views_module_manager._execute(
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
        from scoremanager import wranglers
        self._session._push_controller(self)
        self._io_manager._assign_user_input(pending_user_input)
        breadcrumb = self._session._pop_breadcrumb(rollback=rollback)
        self._session._cache_breadcrumbs(cache=cache)
        if type(self) is wranglers.MaterialPackageWrangler:
            self._session._is_navigating_to_score_materials = False
        elif type(self) is wranglers.SegmentPackageWrangler:
            self._session._is_navigating_to_score_segments = False
        while True:
            self._session._push_breadcrumb(self._breadcrumb)
            if self._session.is_navigating_to_next_material:
                result = self._get_next_material_package_name()
            elif self._session.is_navigating_to_previous_material:
                result = self._get_previous_material_package_name()
            else:
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
        self._session._push_breadcrumb(
            breadcrumb=breadcrumb, 
            rollback=rollback,
            )
        self._session._restore_breadcrumbs(cache=cache)

    ### PUBLIC METHODS ###

    def add_metadatum(self):
        r'''Adds metadatum to metadata module.

        Returns none.
        '''
        self._current_package_manager.add_metadatum()

    def get_metadatum(self):
        r'''Gets metadatum from metadata module.

        Returns object.
        '''
        self._current_package_manager.get_metadatum()

    def list_directory(self):
        r'''List directory of current package manager.
        
        Returns none.
        '''
        self._current_package_manager.list_directory()

    def list_views(
        self,
        pending_user_input=None,
        ):
        r'''List views in views module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager.proceed(message)
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
        tab_width = self._configuration.get_tab_width()
        tab = tab_width * ' '
        names = [tab + x for x in names]
        lines.extend(names)
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed()

    def make_view(
        self,
        pending_user_input=None,
        ):
        r'''Makes view.

        Returns none.
        '''
        from scoremanager import editors
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('view name')
        with self._backtracking:
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
        with self._backtracking:
            editor._run()
        if self._session._backtrack():
            return
        tokens = editor.target
        self._io_manager.display('')
        view = self._io_manager.make_view(
            tokens, 
            )
        self.write_view(view_name, view)

    def remove_assets(
        self, 
        pending_user_input=None,
        ):
        r'''Removes assets.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        getter = self._io_manager.make_getter(where=self._where)
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
            asset_manager = self._initialize_asset_manager(
                asset_filesystem_path)
            asset_manager._remove()
            total_assets_removed += 1
        if total_assets_removed == 1:
            asset_string = 'asset'
        else:
            asset_string = 'assets'
        message = '{} {} removed.'
        message = message.format(total_assets_removed, asset_string)
        self._io_manager.proceed(message)

    def remove_initializer(self):
        r'''Removes initializer module.

        Returns none.
        '''
        self._current_package_manager.remove_initializer()

    def remove_metadata_module(self):
        r'''Removes metadata module.

        Returns none.
        '''
        self._current_package_manager.remove_metadata_module()

    def remove_metadatum(self):
        r'''Removes metadatum from metadata module.

        Returns none.
        '''
        self._current_package_manager.remove_metadatum()

    def remove_views_module(self):
        r'''Removes views module.

        Returns none.
        '''
        self._current_package_manager.remove_views_module()

    def rename_asset(
        self,
        pending_user_input=None,
        ):
        r'''Renames asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            asset_filesystem_path = self.select_asset_filesystem_path()
        if self._session._backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_filesystem_path)
        asset_manager.rename()

    def rewrite_metadata_module(self, prompt=True):
        r'''Rewrites metadata module.

        Returns none.
        '''
        self._current_package_manager.rewrite_metadata_module(prompt=prompt)

    def run_doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        path = self._get_current_directory_path_of_interest()
        command = 'ajv doctest {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            if lines[0] == '':
                lines.remove('')
            lines.append('')
            self._io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def run_pytest(self, prompt=True):
        r'''Runs py.test.

        Returns none.
        '''
        path = self._get_current_directory_path_of_interest()
        command = 'py.test -rf {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def select_asset_filesystem_path(
        self, 
        clear=True, 
        cache=False,
        pending_user_input=None,
        ):
        r'''Selects asset filesystem path.

        Returns string.
        '''
        self._io_manager._assign_user_input(pending_user_input)
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

    def select_storehouse_directory_path(
        self,
        clear=True, 
        cache=False,
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        pending_user_input=None,
        ):
        r'''Selects asset storehouse filesystem path.

        Returns string.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        menu = self._io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        menu_entries = self._make_storehouse_menu_entries(
            abjad_library=False,
            user_library=True,
            abjad_score_packages=False,
            user_score_packages=False)
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

    def select_view(
        self,
        pending_user_input=None,
        ):
        r'''Selects view.

        Writes view name to metadata module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        view_inventory = self._read_view_inventory_from_disk()
        if view_inventory is None:
            message = 'no views found.'
            self._io_manager.proceed(message)
            return
        lines = []
        view_names = view_inventory.keys()
        selector = self._io_manager.make_selector(where=self._where)
        selector.explicit_breadcrumb = 'select view'
        selector.items = view_names
        with self._backtracking:
            view_name = selector._run()
        if self._session._backtrack():
            return
        self._current_package_manager._add_metadata('view_name', view_name)

    def view_initializer(self):
        r'''Views initializer module.

        Returns none.
        '''
        self._current_package_manager.view_initializer()

    def view_metadata_module(self):
        r'''Views metadata module.

        Returns none.
        '''
        self._current_package_manager.view_metadata_module()

    def view_views_module(self):
        r'''Views views module.

        Returns none.
        '''
        self._views_module_manager.edit()

    def write_initializer_boilerplate(self):
        r'''Writes boilerplate initializer module.

        Returns none.
        '''
        self._current_package_manager.write_initializer_boilerplate()

    def write_initializer_stub(self):
        r'''Writes stub initializer module.

        Returns none.
        '''
        self._current_package_manager.write_initializer_stub()

    def write_view(self, view_name, new_view, prompt=True):
        r'''Writes view to views module.

        Returns none.
        '''
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
        view_file_path = self._views_module_path
        file_pointer = file(view_file_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()
        message = 'view written to disk.'
        self._io_manager.proceed(message, prompt=prompt)
