# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from scoremanager.idetools.AssetController import AssetController


class AbjadIDE(AssetController):
    r'''Abjad IDE.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
            >>> score_manager
            AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from scoremanager import idetools
        if session is None:
            session = idetools.Session()
            session._is_test = is_test
        superclass = super(AbjadIDE, self)
        superclass.__init__(session=session)
        self._session._score_manager = self

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            return 'Abjad IDE'

    @property
    @systemtools.Memoize
    def _build_file_wrangler(self):
        from scoremanager import idetools
        return idetools.BuildFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _distribution_file_wrangler(self):
        from scoremanager import idetools
        return idetools.DistributionFileWrangler(session=self._session)

    @property
    def _input_to_method(self):
        superclass = super(AssetController, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'nls*': self.list_every_init_py,
            'no*': self.open_every_init_py,
            'ns*': self.write_every_init_py_stub,
            })
        return result

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

    ### PRIVATE METHODS ###

    def _make_init_py_menu_section(self, menu):
        commands = []
        commands.append(('__init__.py - list', 'nls*'))
        commands.append(('__init__.py - open', 'no*'))
        commands.append(('__init__.py - stub', 'ns*'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='__init__.py',
            )

    def _make_main_menu(self):
        superclass = super(AbjadIDE, self)
        menu = superclass._make_main_menu()
        self._make_init_py_menu_section(menu)
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
        path = self._configuration.cache_file_path
        state = systemtools.NullContextManager()
        if self._session.is_test:
            state = systemtools.FilesystemState(keep=[path])
        interaction = self._io_manager._make_interaction(task=False)
        with controller, directory_change, state, interaction:
            self._session._pending_redraw = True
            while True:
                result = self._score_package_wrangler._get_sibling_score_path()
                if not result:
                    result = self._session.wrangler_navigation_directive
                if not result:
                    self._score_package_wrangler._run()
                else:
                    self._score_package_wrangler._handle_main_menu_result(
                        result)
                if self._session.is_backtracking_to_library:
                    menu = self._make_main_menu()
                    result = menu._run()
                    if result:
                        self._handle_main_menu_result(result)
                self._update_session_variables()
                if self._session.is_quitting:
                    if not self._transcript[-1][-1] == '':
                        self._io_manager._display('')
                    return
    
    def _update_session_variables(self):
        self._session._is_backtracking_to_score = False
        self._session._is_backtracking_to_score_manager = False

    ### PUBLIC METHODS ###

    def add_to_repository(self):
        r'''Adds files to repository.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def commit_to_repository(self):
        r'''Commit modified files to repository.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def list_every_init_py(self):
        r'''Lists every ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def open_every_init_py(self):
        r'''Opens every ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def repository_clean(self):
        r'''Removes unadded files from filesystem.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def repository_status(self):
        r'''Displays repository status.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def revert_to_repository(self):
        r'''Reverts files to repository.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def update_from_repository(self):
        r'''Updates from repository.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def write_every_init_py_stub(self):
        r'''Writes stub to every ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()