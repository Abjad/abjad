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

    __slots__ = (
        '_abjad_storehouse_path',
        '_forbidden_directory_entries',
        '_main_menu',
        '_score_storehouse_path_infix_parts',
        '_user_storehouse_path',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        Controller.__init__(self, session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = None
        self._score_storehouse_path_infix_parts = ()
        self._forbidden_directory_entries = ()

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _asset_manager_class(self):
        pass

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
            'new': self.make_asset,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'ren': self.rename,
            'rm': self.remove,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rup': self.update_from_repository,
            'vl': self.list_views,
            'vn': self.make_view,
            'vs': self.select_view,
            'vmrm': self.remove_views_module,
            'vmro': self.view_views_module,
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

    def _enter_run(self):
        pass

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

    def _find_git_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=True,
            repository='git',
            )
        return manager

    def _find_svn_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=False,
            repository='svn',
            )
        return manager

    def _find_up_to_date_manager(
        self, 
        inside_score=True,
        must_have_file=False,
        system=True,
        repository='git',
        ):
        import scoremanager
        abjad_library = False
        abjad_score_packages = False
        user_library = False
        user_score_packages = False
        if system and inside_score:
            abjad_score_packages = True
        elif system and not inside_score:
            abjad_library = True
        elif not system and inside_score:
            user_score_packages = True
        elif not system and not inside_score:
            user_library = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            abjad_library=abjad_library,
            abjad_score_packages=abjad_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        session = scoremanager.core.Session()
        for asset_path in asset_paths:
            manager = self._asset_manager_class(
                path=asset_path,
                session=session,
                )
            if (repository == 'git' and
                manager._is_git_versioned() and 
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager
            elif (repository == 'svn' and
                manager._is_svn_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager

    def _get_current_directory_path_of_interest(self):
        score_directory_path = self._session.current_score_directory_path
        if score_directory_path is not None:
            parts = (score_directory_path,)
            parts += self._score_storehouse_path_infix_parts
            directory_path = os.path.join(*parts)
            assert '.' not in directory_path, repr(directory_path)
            return directory_path

    def _get_next_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory_path
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[0]
        if last_path not in paths:
            return paths[0]
        index = paths.index(last_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path
        
    def _get_previous_asset_path(self):
        last_path = self._session.last_asset_path
        menu_entries = self._make_asset_menu_entries()
        paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_directory = self._session.current_score_directory_path
            paths = [x for x in paths if x.startswith(score_directory)]
        if last_path is None:
            return paths[-1]
        if last_path not in paths:
            return paths[-1]
        index = paths.index(last_path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _get_sibling_asset_path(self):
        if self._session.is_navigating_to_next_asset:
            return self._get_next_asset_path()
        if self._session.is_navigating_to_previous_asset:
            return self._get_previous_asset_path()

    def _get_view_from_disk(self):
        package_manager = self._current_package_manager
        if not package_manager:
            return
        view_name = package_manager._get_metadatum('view_name')
        if not view_name:
            return
        view_inventory = self._read_view_inventory_from_disk()
        if not view_inventory:
            return
        view = view_inventory.get(view_name)
        return view

    def _initialize_asset_manager(self, path):
        assert os.path.sep in path, repr(path)
        return self._asset_manager_class(
            path=path, 
            session=self._session,
            )

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry not in self._forbidden_directory_entries:
            if directory_entry[0].isalpha():
                return True
        return False

    def _list(self, public_entries_only=False):
        result = []
        path = self._get_current_directory_path_of_interest()
        if not os.path.exists(path):
            return result
        if public_entries_only:
            for directory_entry in sorted(os.listdir(path)):
                if directory_entry[0].isalpha():
                    if not directory_entry.endswith('.pyc'):
                        if not directory_entry in ('test',):
                            result.append(directory_entry)
        else:
            for directory_entry in sorted(os.listdir(path)):
                if not directory_entry.startswith('.'):
                    if not directory_entry.endswith('.pyc'):
                        result.append(directory_entry)
        return result

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
        if os.path.sep in asset_name:
            asset_name = os.path.basename(asset_name)
        assert stringtools.is_snake_case_string(asset_name)
        path = os.path.join(
            self._current_storehouse_path, 
            asset_name,
            )
        manager = self._initialize_asset_manager(path)
        if hasattr(manager, '_write_stub'):
            manager._write_stub()
        elif hasattr(manager, 'fix'):
            manager.fix(prompt=False)

    def _make_asset_selection_breadcrumb(
        self, 
        human_readable_target_name=None,
        infinitival_phrase=None, 
        is_storehouse=False,
        ):
        if human_readable_target_name is None:
            manager = self._asset_manager_class(session=self._session)
            name = type(manager).__name__
            name = stringtools.upper_camel_case_to_space_delimited_lowercase(
                name)
            human_readable_target_name = name
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
        section = menu.make_asset_section()
        include_extensions = getattr(self, '_include_extensions', False)
        asset_menu_entries = self._make_asset_menu_entries(
            include_extensions=include_extensions,
            packages_instead_of_paths=packages_instead_of_paths,
            )
        for menu_entry in asset_menu_entries:
            section.append(menu_entry)
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

    def _navigate_to_next_asset(self):
        pass

    def _navigate_to_previous_asset(self):
        pass

    def _read_view_inventory_from_disk(self):
        if self._views_module_path is None:
            return
        result = self._views_module_manager._execute(
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            message = 'views module is corrupt.'
            self._io_manager.display([message, ''])
            return
        if not result:
            return
        assert len(result) == 1
        view_inventory = result[0]
        return view_inventory

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(
            self,
            on_enter_callbacks=(self._enter_run,),
            )
        with context:
            while True:
                result = self._get_sibling_asset_path()
                if not result:
                    menu = self._make_main_menu()
                    result = menu._run()
                if self._should_backtrack():
                    return
                if result:
                    self._handle_main_menu_result(result)
                    if self._should_backtrack():
                        return

    def _select_asset_path(self):
        menu = self._make_asset_selection_menu()
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb()
            result = menu._run()
            if self._should_backtrack():
                break
            elif not result:
                continue
            else:
                break
        return result

    def _select_storehouse_path(
        self,
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        ):
        menu = self._io_manager.make_menu(
            where=self._where,
            name='storehouse selection',
            )
        section = menu.make_asset_section()
        menu_entries = self._make_storehouse_menu_entries(
            abjad_library=False,
            user_library=True,
            abjad_score_packages=False,
            user_score_packages=False)
        for menu_entry in menu_entries:
            section.append(menu_entry)
        while True:
            breadcrumb = self._make_asset_selection_breadcrumb(
                is_storehouse=True)
            result = menu._run()
            if self._should_backtrack():
                break
            elif not result:
                continue
            else:
                break
        return result

    def _set_is_navigating_to_sibling_asset(self):
        message = 'implement on concrete wrangler classes.'
        raise Exception(message)

    ### PUBLIC METHODS ###

    def add_metadatum(self):
        r'''Adds metadatum to metadata module.

        Returns none.
        '''
        self._current_package_manager.add_metadatum()

    def add_to_repository(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        self._session._attempted_to_add_to_repository = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            manager.add_to_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def commit_to_repository(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        self._session._attempted_to_commit_to_repository = True
        if self._session.is_repository_test:
            return
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._should_backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self._io_manager.display(line)
        if not self._io_manager.confirm():
            return
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            manager.commit_to_repository(
                commit_message=commit_message, 
                prompt=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        self._current_package_manager.doctest(prompt=prompt)

    def get_available_path(
        self, 
        storehouse_path=None,
        prompt_string=None,
        ):
        r'''Gets available path in `storehouse_path`.

        Sets `storehouse_path` equal to current storehouse path when
        `storehouse_path` is none.

        Returns string.
        '''
        storehouse_path = storehouse_path or self._current_storehouse_path
        while True:
            prompt_string = prompt_string or 'package name'
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string(prompt_string)
            name = getter._run()
            if self._should_backtrack():
                return
            name = stringtools.string_to_accent_free_snake_case(name)
            path = os.path.join(storehouse_path, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager.display([line, ''])
            else:
                return path
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

    def list_views(self):
        r'''List views in views module.

        Returns none.
        '''
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

    def make_asset(self):
        r'''Makes asset.

        Returns none.
        '''
        path = self.get_available_path()
        if self._should_backtrack():
            return
        self._make_asset(path)

    def make_view(self):
        r'''Makes view.

        Returns none.
        '''
        from scoremanager import iotools
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('view name')
        view_name = getter._run()
        if self._should_backtrack():
            return
        menu_entries = self._make_asset_menu_entries()
        display_strings = [x[0] for x in menu_entries]
        editor = iotools.ListEditor(
            session=self._session,
            target=display_strings,
            )
        editor._run()
        if self._should_backtrack():
            return
        tokens = editor.target
        self._io_manager.display('')
        view = self._io_manager.make_view(
            tokens, 
            )
        self.write_view(view_name, view)

    def pytest(self, prompt=True):
        r'''Runs py.test.

        Returns none.
        '''
        self._current_package_manager.pytest(prompt=prompt)

    def remove(self):
        r'''Removes asset.

        Returns none.
        '''
        asset_path = self._select_asset_path()
        if self._should_backtrack():
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

    def rename(self):
        r'''Renames asset.

        Returns none.
        '''
        asset_path = self._select_asset_path()
        if self._should_backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_path)
        asset_manager.rename()

    def repository_status(self, prompt=True):
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
            manager.repository_status(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def revert_to_repository(self, prompt=True):
        r'''Reverts assets from repository.

        Returns none.
        '''
        from scoremanager import managers
        self._session._attempted_to_revert_to_repository = True
        if self._session.is_repository_test:
            return
        paths = self._list_visible_asset_paths()
        paths = self._extract_common_parent_directories(paths)
        for path in paths:
            manager = managers.DirectoryManager(
                path=path,
                session=self._session,
                )
            manager.revert_to_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def rewrite_metadata_module(self, prompt=True):
        r'''Rewrites metadata module.

        Returns none.
        '''
        self._current_package_manager.rewrite_metadata_module(prompt=prompt)

    def select_asset_package_path(self, infinitival_phrase=None):
        '''Selects asset package path.

        Returns string.
        '''
        with self._controller_context:
            while True:
                name = '_human_readable_target_name'
                human_readable_target_name = getattr(self, name, None)
                breadcrumb = self._make_asset_selection_breadcrumb(
                    human_readable_target_name=human_readable_target_name,
                    infinitival_phrase=infinitival_phrase,
                    )
                menu = self._make_asset_selection_menu(
                    packages_instead_of_paths=True,
                    )
                result = menu._run()
                if self._should_backtrack():
                    break
                elif not result:
                    continue
                else:
                    break
            return result

    def select_view(self):
        r'''Selects view.

        Writes view name to metadata module.

        Returns none.
        '''
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
        view_name = selector._run()
        if self._should_backtrack():
            return
        self._current_package_manager._add_metadatum('view_name', view_name)

    def update_from_repository(self, prompt=True):
        r'''Updates assets from repository.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            manager.update_from_repository(prompt=False)
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