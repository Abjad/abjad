# -*- encoding: utf-8 -*-
import abc
import copy
import os
import subprocess
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.core.Controller import Controller


class Wrangler(Controller):
    r'''Wrangler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        Controller.__init__(self, session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = None
        self._score_storehouse_path_infix_parts = ()
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
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            parts = []
            parts.append(self._session.current_score_directory_path)
            parts.extend(self._score_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self._abjad_storehouse_path

    @property
    def _temporary_asset_manager(self):
        return self._initialize_asset_manager(
            self._temporary_asset_path)

    @abc.abstractproperty
    def _temporary_asset_name(self):
        pass

    @property
    def _temporary_asset_path(self):
        return os.path.join(
            self._current_storehouse_path, 
            self._temporary_asset_name)

    @property
    def _user_input_to_action(self):
        superclass = super(Wrangler, self)
        result = superclass._user_input_to_action
        result = copy.deepcopy(result)
        result.update({
            'inrm': self.remove_initializer,
            'ins': self.write_initializer_stub,
            'inro': self.view_initializer,
            'ls': self.list,
            'll': self.list_long,
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdrm': self.remove_metadatum,
            'mdmrm': self.remove_metadata_module,
            'mdmrw': self.rewrite_metadata_module,
            'mdmro': self.view_metadata_module,
            'pwd': self.pwd,
            'rad': self.add,
            'rci': self.commit,
            'ren': self.rename,
            'rm': self.remove,
            'rrv': self.revert_from_repository,
            'rst': self.status,
            'rup': self.update,
            'vwl': self.list_views,
            'vwn': self.make_view,
            'vws': self.select_view,
            'vwmrm': self.remove_views_module,
            'vwmro': self.view_views_module,
            })
        return result

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

    def _extract_common_parent_directories(self, paths):
        parent_directories = []
        user_score_packages_directory_path = \
            self._configuration.user_score_packages_directory_path
        for path in paths:
            parent_directory = os.path.dirname(path)
            if parent_directory == user_score_packages_directory_path:
                parent_directories.append(path)
            elif parent_directory not in parent_directories:
                parent_directories.append(parent_directory)
        return parent_directories

    def _get_current_directory_path_of_interest(self):
        score_directory_path = self._session.current_score_directory_path
        if score_directory_path is not None:
            parts = (score_directory_path,)
            parts += self._score_storehouse_path_infix_parts
            directory_path = os.path.join(*parts)
            assert '.' not in directory_path, repr(directory_path)
            return directory_path

    def _initialize_asset_manager(self, path):
        assert os.path.sep in path, repr(path)
        return self._asset_manager_class(
            path=path, 
            session=self._session,
            )

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry not in self.forbidden_directory_entries:
            if directory_entry[0].isalpha():
                return True
        return False

    def _list_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        ):
        result = []
        directory_paths = self._list_storehouse_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )
        for directory_path in directory_paths:
            if not directory_path:
                continue
            if not os.path.exists(directory_path):
                continue
            directory_entries =  sorted(os.listdir(directory_path))
            for directory_entry in directory_entries:
                if not self._is_valid_directory_entry(directory_entry):
                    continue
                path = os.path.join(directory_path, directory_entry)
                result.append(path)
        return result

    def _list_storehouse_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        result = []
        if abjad_library and \
            self._abjad_storehouse_path is not None:
            result.append(self._abjad_storehouse_path)
        if user_library and self._user_storehouse_path is not None:
            result.append(self._user_storehouse_path)
        if abjad_score_packages and \
            self._score_storehouse_path_infix_parts:
            for score_directory_path in \
                self._configuration.list_score_directory_paths(abjad=True):
                parts = [score_directory_path]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                storehouse_path = os.path.join(*parts)
                result.append(storehouse_path)
        if user_score_packages and self._score_storehouse_path_infix_parts:
            for directory_path in \
                self._configuration.list_score_directory_paths(user=True):
                parts = [directory_path]
                if self._score_storehouse_path_infix_parts:
                    parts.extend(self._score_storehouse_path_infix_parts)
                path = os.path.join(*parts)
                result.append(path)
        return result

    def _list_visible_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        ):
        visible_paths = []
        paths = self._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            ) 
        current_path = self._get_current_directory_path_of_interest()
        for path in paths:
            if current_path is None or path.startswith(current_path):
                visible_paths.append(path)
        return visible_paths

    def _make_asset(self, asset_name):
        assert stringtools.is_snake_case_string(asset_name)
        path = os.path.join(
            self._current_storehouse_path, 
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
            manager = self._asset_manager_class(session=self._session)
            generic_class_name = manager._generic_class_name
            human_readable_target_name = generic_class_name
        if infinitival_phrase:
            return 'select {} {}:'.format(
                human_readable_target_name,
                infinitival_phrase,
                )
        elif is_storehouse:
            return 'select storehouse'
        else:
            return 'select {}:'.format(human_readable_target_name)

    def _make_asset_selection_menu(self, packages_instead_of_paths=False):
        menu = self._io_manager.make_menu(
            where=self._where,
            name='asset selection',
            )
        asset_section = menu.make_asset_section()
        include_extensions = getattr(self, '_include_extensions', False)
        asset_menu_entries = self._make_asset_menu_entries(
            include_extensions=include_extensions,
            packages_instead_of_paths=packages_instead_of_paths,
            )
        for menu_entry in asset_menu_entries:
            asset_section.append(menu_entry)
        return menu

    def _make_storehouse_menu_entries(
        self,
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        ):
        from scoremanager import wranglers
        keys, display_strings = [], []
        keys.append(self._user_storehouse_path)
        display_strings.append('My {}'.format(self._breadcrumb))
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        paths = wrangler._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = wrangler._initialize_asset_manager(path)
            display_strings.append(manager._get_title())
            path_parts = (manager._path,)
            path_parts = path_parts + self._score_storehouse_path_infix_parts
            key = os.path.join(*path_parts)
            keys.append(key)
        sequences = [display_strings, [None], [None], keys]
        return sequencetools.zip_sequences(sequences, cyclic=True)

    def _read_view_inventory_from_disk(self):
        if self._views_module_path is None:
            return
        result = self._views_module_manager._execute(
            attribute_names=('view_inventory',),
            )
        assert len(result) == 1
        view_inventory = result[0]
        return view_inventory

    def _run(
        self, 
        cache=False, 
        clear=True, 
        rollback=None, 
        pending_user_input=None,
        ):
        from scoremanager import wranglers
        self._session._push_controller(self)
        self._io_manager._assign_user_input(pending_user_input)
        breadcrumb = self._session._pop_breadcrumb(rollback=rollback)
        self._session._cache_breadcrumbs(cache=cache)
        if type(self) is wranglers.MakerModuleWrangler:
            self._session._is_navigating_to_score_makers = False
        elif type(self) is wranglers.MaterialPackageWrangler:
            self._session._is_navigating_to_score_materials = False
        elif type(self) is wranglers.SegmentPackageWrangler:
            self._session._is_navigating_to_score_segments = False
        elif type(self) is wranglers.StylesheetWrangler:
            self._session._is_navigating_to_score_stylesheets = False
        while True:
            self._session._push_breadcrumb(self._breadcrumb)
            if self._session.is_navigating_to_next_material:
                result = self._get_next_material_path()
            elif self._session.is_navigating_to_previous_material:
                result = self._get_previous_material_path()
            else:
                menu = self._make_main_menu()
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

    def _select_asset_path(
        self, 
        clear=True, 
        cache=False,
        pending_user_input=None,
        ):
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

    def _select_storehouse_path(
        self,
        clear=True, 
        cache=False,
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        menu = self._io_manager.make_menu(
            where=self._where,
            name='storehouse selection',
            )
        asset_section = menu.make_asset_section()
        menu_entries = self._make_storehouse_menu_entries(
            abjad_library=False,
            user_library=True,
            abjad_score_packages=False,
            user_score_packages=False)
        for menu_entry in menu_entries:
            asset_section.append(menu_entry)
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

    ### PUBLIC METHODS ###

    def add(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            manager.add(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def add_metadatum(self):
        r'''Adds metadatum to metadata module.

        Returns none.
        '''
        self._current_package_manager.add_metadatum()

    def commit(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('commit message')
        commit_message = getter._run(clear_terminal=False)
        if self._session._backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self._io_manager.display(line)
        if not self._io_manager.confirm():
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            manager.commit(
                commit_message=commit_message, 
                prompt=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        self._current_package_manager.doctest(prompt=prompt)

    def get_metadatum(self):
        r'''Gets metadatum from metadata module.

        Returns object.
        '''
        self._current_package_manager.get_metadatum()

    def list(self):
        r'''List directory of current package manager.
        
        Returns none.
        '''
        self._current_package_manager.list()

    def list_long(self):
        r'''List directory of current package manager with ``ls -l``.
        
        Returns none.
        '''
        self._current_package_manager.list_long()

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
        menu_entries = self._make_asset_menu_entries()
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

    def pwd(self):
        r'''Displays current working directory of current package manager.
        
        Returns none.
        '''
        self._current_package_manager.pwd()

    def pytest(self, prompt=True):
        r'''Runs py.test.

        Returns none.
        '''
        self._current_package_manager.pytest(prompt=prompt)

    def remove(self, pending_user_input=None):
        r'''Removes asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            asset_path = self._select_asset_path()
        if self._session._backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_path)
        asset_manager.remove()

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

    def rename(self, pending_user_input=None):
        r'''Renames asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            asset_path = self._select_asset_path()
        if self._session._backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_path)
        asset_manager.rename()

    def rewrite_metadata_module(self, prompt=True):
        r'''Rewrites metadata module.

        Returns none.
        '''
        self._current_package_manager.rewrite_metadata_module(prompt=prompt)

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
        selector = self._io_manager.make_selector(
            where=self._where,
            items=view_names,
            )
        # TODO: make attribute read only and not assignable after init
        selector.explicit_breadcrumb = 'select view'
        with self._backtracking:
            view_name = selector._run()
        if self._session._backtrack():
            return
        self._current_package_manager._add_metadatum('view_name', view_name)

    def revert_from_repository(self, prompt=True):
        r'''Reverts assets from repository.

        Returns none.
        '''
        from scoremanager import managers
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        for path in paths:
            manager = managers.DirectoryManager(
                path=path,
                session=self._session,
                )
            manager.revert_from_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def status(self, prompt=True):
        r'''Display asset status in repository.

        Returns none.
        '''
        from scoremanager import managers
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        for path in paths:
            manager = managers.DirectoryManager(
                path=path,
                session=self._session,
                )
            manager.status(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def update(self, prompt=True):
        r'''Updates assets from repository.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            manager.update(prompt=False)
        self._io_manager.proceed(prompt=prompt)

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
        lines.append(self._unicode_directive + '\n')
        lines.append(self._abjad_import_statement + '\n')
        line = 'from scoremanager import iotools\n'
        lines.append(line)
        lines.append('\n\n')
        line = 'view_inventory={}'.format(format(view_inventory))
        lines.append(line)
        lines = ''.join(lines)
        view_file_path = self._views_module_path
        with file(view_file_path, 'w') as file_pointer:
            file_pointer.write(lines)
        message = 'view written to disk.'
        self._io_manager.proceed(message, prompt=prompt)