# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import systemtools
from scoremanager.idetools.Wrangler import Wrangler


class AbjadIDE(Wrangler):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> ide = scoremanager.idetools.AbjadIDE(is_test=True)
            >>> ide
            AbjadIDE()


    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_simple_score_annotation',
        '_sort_by_annotation',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from scoremanager import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        superclass = super(AbjadIDE, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'Abjad IDE'
        self._session._ide = self
        self._simple_score_annotation = True
        self._sort_by_annotation = True
        self._supply_missing_cache_file()
        self._supply_missing_views_files()

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            #superclass = super(AbjadIDE, self)
            #return superclass._breadcrumb
            return self._basic_breadcrumb

    @property
    @systemtools.Memoize
    def _build_file_wrangler(self):
        from scoremanager import idetools
        return idetools.BuildFileWrangler(session=self._session)

    @property
    def _command_to_method(self):
        superclass = super(AbjadIDE, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'ne*': self.edit_every_init_py,
            'nl*': self.list_every_init_py,
            'ns*': self.write_every_init_py_stub,
            })
        return result

    @property
    @systemtools.Memoize
    def _distribution_file_wrangler(self):
        from scoremanager import idetools
        return idetools.DistributionFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _maker_file_wrangler(self):
        from scoremanager import idetools
        return idetools.MakerFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _material_package_wrangler(self):
        from scoremanager import idetools
        return idetools.MaterialPackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _score_package_wrangler(self):
        from scoremanager import idetools
        return idetools.ScorePackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _segment_package_wrangler(self):
        from scoremanager import idetools
        return idetools.SegmentPackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _stylesheet_wrangler(self):
        from scoremanager import idetools
        return idetools.StylesheetWrangler(session=self._session)

    @property
    def _wranglers(self):
        return (
            self,
            self._build_file_wrangler,
            self._distribution_file_wrangler,
            self._maker_file_wrangler,
            self._material_package_wrangler,
            self._score_package_wrangler,
            self._segment_package_wrangler,
            self._stylesheet_wrangler,
            )

    ### PRIVATE METHODS ###

    def _list_asset_paths(self):
        paths = []
        storehouses = self._list_storehouse_paths()
        for storehouse in storehouses:
            if not os.path.exists(storehouse):
                continue
            entries = sorted(os.listdir(storehouse))
            for entry in entries:
                if not self._is_valid_directory_entry(entry):
                    continue
                path = os.path.join(storehouse, entry)
                paths.append(path)
        return paths

    def _list_storehouse_paths(self):
        paths = []
        paths.append(self._configuration.makers_library)
        paths.append(self._configuration.materials_library)
        paths.append(self._configuration.example_stylesheets_directory)
        paths.append(self._configuration.stylesheets_library)
        paths.append(self._configuration.example_score_packages_directory)
        paths.append(self._configuration.user_score_packages_directory)
        return paths

    def _list_visible_asset_paths(self):
        entries = self._make_asset_menu_entries()
        paths = [_[-1] for _ in entries]
        return paths

    def _make_init_py_menu_section(self, menu):
        commands = []
        commands.append(('all assets - repository - add', 'rad*'))
        commands.append(('all assets - repository - clean', 'rcn*'))
        commands.append(('all assets - repository - commit', 'rci*'))
        commands.append(('all assets - repository - revert', 'rrv*'))
        commands.append(('all assets - repository - status', 'rst*'))
        commands.append(('all assets - repository - update', 'rup*'))
        commands.append(('all packages - __init__.py - edit', 'ne*'))
        commands.append(('all packages - __init__.py - list', 'nl*'))
        commands.append(('all packages - __init__.py - stub', 'ns*'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='all',
            )

    def _make_main_menu(self):
        from scoremanager import idetools
        menu = idetools.AssetController._make_main_menu(self)
        self._make_asset_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_views_menu_section(menu)
        return menu

    def _run(self, input_=None):
        from scoremanager import idetools
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        controller = self._io_manager._controller(
            controller=self,
            consume_local_backtrack=True,
            on_exit_callbacks=(self._session._clean_up,)
            )
        path = self._configuration.score_manager_directory
        directory_change = systemtools.TemporaryDirectoryChange(path)
        state = systemtools.NullContextManager()
        wrangler_views = os.path.join(
            self._configuration.configuration_directory,
            'views',
            '__metadata__.py',
            )
        if self._session.is_test:
            paths_to_keep = []
            paths_to_keep.append(self._configuration.cache_file_path)
            paths_to_keep.append(wrangler_views)
            state = systemtools.FilesystemState(keep=paths_to_keep)
        interaction = self._io_manager._make_interaction(task=False)
        with controller, directory_change, state, interaction:
            self._session._pending_redraw = True
            if self._session.is_test:
                empty_views = os.path.join(
                    self._configuration.boilerplate_directory,
                    '__views_metadata__.py',
                    )
                shutil.copyfile(empty_views, wrangler_views)
            while True:
                result = self._score_package_wrangler._get_sibling_score_path()
                if not result:
                    result = self._session.wrangler_navigation_directive
                if result:
                    self._score_package_wrangler._handle_input(
                        result)
                elif not self._session.is_navigating_home:
                    self._score_package_wrangler._run()
                else:
                    menu = self._make_main_menu()
                    result = menu._run()
                    if result:
                        self._handle_input(result)
                self._update_session_variables()
                if self._session.is_quitting:
                    if not self._transcript[-1][-1] == '':
                        self._io_manager._display('')
                    return

    def _supply_missing_cache_file(self):
        if not os.path.exists(self._configuration.cache_file_path):
            with self._io_manager._silent():
                self._score_package_wrangler.write_cache()

    def _supply_missing_views_files(self):
        from scoremanager import idetools
        if not os.path.exists(self._views_py_path):
            view_inventory = idetools.ViewInventory()
            with self._io_manager._silent():
                self._write_view_inventory(view_inventory)
        if not os.path.exists(self._metadata_py_path):
            metadata = self._get_metadata()
            with self._io_manager._silent():
                self._write_metadata_py(metadata)
        if self._session.is_test:
            with self._io_manager._silent():
                for wrangler in self._wranglers:
                    if not os.path.exists(wrangler._views_py_path):
                        wrangler.write_views_py()
        else:
            with self._io_manager._silent():
                for wrangler in self._wranglers:
                    wrangler.write_views_py()

    def _update_session_variables(self):
        self._session._is_backtracking_to_score = False
        self._session._is_navigating_to_scores = False

    ### PUBLIC METHODS ###

    def edit_every_init_py(self):
        r'''Opens every ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def list_every_init_py(self):
        r'''Lists every ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def write_every_init_py_stub(self):
        r'''Writes stub to every ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()