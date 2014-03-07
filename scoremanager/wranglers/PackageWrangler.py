# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        Wrangler.__init__(self, session=session)
        self._asset_manager_class = managers.PackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _temporary_asset_manager(self):
        return self._initialize_asset_manager(
            self._temporary_asset_package_path)

    @property
    def _temporary_asset_name(self):
        return '__temporary_package'

    @property
    def _temporary_asset_package_path(self):
        path = self._temporary_asset_path
        package = self._configuration.path_to_package_path(path)
        return package

    @property
    def _user_input_to_action(self):
        superclass = super(PackageWrangler, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'new': self.make_asset,
            'ren': self.rename,
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

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

    def _handle_main_menu_result(self, result):
        self._io_manager.print_not_yet_implemented()

    def _initialize_asset_manager(self, path):
        assert os.path.sep in path, repr(path)
        manager = self._asset_manager_class(
            path=path, 
            session=self._session,
            )
        return manager

    def _is_valid_directory_entry(self, expr):
        superclass = super(PackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_asset_managers(
        self,
        abjad_library=True,
        user_library=True,
        abjad_score_packages=True,
        user_score_packages=True,
        head=None,
        ):
        r'''Lists asset managers.

        Returns list.
        '''
        result = []
        for path in self._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            asset_manager = self._initialize_asset_manager(path)
            result.append(asset_manager)
        return result

    def _make_asset(self, asset_name):
        assert stringtools.is_snake_case_package_name(asset_name)
        asset_path = os.path.join(
            self._current_storehouse_path, asset_name)
        os.mkdir(asset_path)
        package_manager = self._initialize_asset_manager(asset_name)
        package_manager.fix(prompt=False)

    def _make_asset_menu_entries(self):
        names = self._list_visible_asset_names()
        if not names:
            return
        keys = len(names) * [None]
        prepopulated_return_values = len(names) * [None]
        paths = self._list_visible_asset_paths()
        sequences = (names, [None], [None], paths)
        entries = sequencetools.zip_sequences(sequences, cyclic=True)
        view = self._get_view_from_disk()
        if view is not None:
            entries = self._sort_asset_menu_entries_by_view(entries, view)
        return entries

    def _make_main_menu(self):
        self._io_manager.print_not_yet_implemented()

    @staticmethod
    def _sort_asset_menu_entries_by_view(entries, view):
        entries_found_in_view = len(entries) * [None]
        entries_not_found_in_view = []
        for entry in entries:
            name = entry[0]
            if name in view:
                index = view.index(name)
                entries_found_in_view[index] = entry
            else:
                entries_not_found_in_view.append(entry)
        entries_found_in_view = [
            x for x in entries_found_in_view 
            if not x is None
            ]
        sorted_entries = entries_found_in_view + entries_not_found_in_view
        assert len(sorted_entries) == len(entries)
        return sorted_entries

    ### PUBLIC METHODS ###

    def get_available_path(
        self, 
        pending_user_input=None,
        ):
        r'''Gets available package path.

        Returns string.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        while True:
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string('name')
            with self._backtracking:
                name = getter._run()
            if self._session._backtrack():
                return
            name = stringtools.string_to_accent_free_snake_case(name)
            path = os.path.join(
                self._current_storehouse_path, 
                name,
                )
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager.display([line, ''])
            else:
                return path

    def make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Makes asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            path = self.get_available_path()
        if self._session._backtrack():
            return
        self._make_asset(path)

    def rename(self, head=None, pending_user_input=None):
        r'''Renames asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            asset_package_path = self.select_asset_package_path(
                head=head, 
                infinitival_phrase='to rename',
                )
        if self._session._backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_package_path)
        asset_manager.rename()

    def select_asset_package_path(
        self,
        clear=True,
        cache=False,
        infinitival_phrase=None,
        pending_user_input=None,
        ):
        '''Selects asset package path.

        Returns string.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        while True:
            name = '_human_readable_target_name'
            human_readable_target_name = getattr(self, name, None)
            breadcrumb = self._make_asset_selection_breadcrumb(
                human_readable_target_name=human_readable_target_name,
                infinitival_phrase=infinitival_phrase,
                )
            self._session._push_breadcrumb(breadcrumb)
            menu = self._make_asset_selection_menu()
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
