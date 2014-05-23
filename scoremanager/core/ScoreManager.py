# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class ScoreManager(Controller):
    r'''Score Manager.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> score_manager
            ScoreManager()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from scoremanager import core
        if session is None:
            session = core.Session()
            session._is_test = is_test
        Controller.__init__(self, session=session)
        self._session._score_manager = self

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if not self._session.is_in_score:
            return 'Score Manager'

    @property
    @systemtools.Memoize
    def _build_file_wrangler(self):
        from scoremanager import wranglers
        return wranglers.BuildFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _distribution_file_wrangler(self):
        from scoremanager import wranglers
        return wranglers.DistributionFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _maker_file_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MakerFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _material_package_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MaterialPackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _score_package_wrangler(self):
        from scoremanager import wranglers
        return wranglers.ScorePackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _segment_package_wrangler(self):
        from scoremanager import wranglers
        return wranglers.SegmentPackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _stylesheet_wrangler(self):
        from scoremanager import wranglers
        return wranglers.StylesheetWrangler(session=self._session)

    ### PRIVATE METHODS ###

    def _run(self, input_=None):
        from scoremanager import iotools
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if input_:
            self._session._pending_input = input_
        controller = iotools.ControllerContext(
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
        interaction = self._io_manager._make_interaction()
        with controller, directory_change, state, interaction:
            while True:
                result = self._score_package_wrangler._get_sibling_score_path()
                if not result:
                    result = self._session.wrangler_navigation_directive
                if not result:
                    self._score_package_wrangler._run()
                else:
                    self._score_package_wrangler._handle_main_menu_result(
                        result)
                self._update_session_variables()
                if self._session.is_quitting:
                    return
    
    def _update_session_variables(self):
        self._session._is_backtracking_to_score = False
        self._session._is_backtracking_to_score_manager = False