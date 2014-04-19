# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class ScoreManager(Controller):
    r'''Score manager.

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
        if self._session.current_controller is self:
            result = 'score manager - {} scores'
            result = result.format(self._session.scores_to_display)
            return result
        elif self._session.is_in_score:
            return
        else:
            return 'score manager'

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
    def _maker_module_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MakerModuleWrangler(session=self._session)

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

    def _find_svn_score_name(self):
        from scoremanager import managers
        manager = self._find_up_to_date_manager(
            managers.ScorePackageManager,
            repository='svn',
            system=False,
            )
        if manager:
            title = manager._get_title()
            title = stringtools.to_accent_free_snake_case(title)
            return title

    def _find_up_to_date_manager(
        self,
        manager_class,
        repository='git',
        system=True,
        ):
        import scoremanager
        session = scoremanager.core.Session()
        dummy_path = os.path.sep
        manager = manager_class(path=dummy_path, session=session)
        suffix = ()
        if isinstance(suffix, str):
            suffix = (suffix,)
        assert isinstance(suffix, tuple)
        if system:
            scores_directory = \
                self._configuration.example_score_packages_directory_path
        else:
            scores_directory = \
                self._configuration.user_score_packages_directory_path
        for score_package_name in os.listdir(scores_directory):
            path = os.path.join(
                scores_directory,
                score_package_name,
                *suffix
                )
            if not os.path.isdir(path):
                continue
            session = scoremanager.core.Session(is_test=True)
            manager = manager_class(path=path, session=session)
            if (repository == 'git' and
                manager._is_git_versioned() and
                manager._is_up_to_date()):
                return manager
            elif (repository == 'svn' and
                manager._is_svn_versioned() and
                manager._is_up_to_date()):
                return manager

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context =  iotools.ControllerContext(
            self,
            on_exit_callbacks=(self._session._clean_up,)
            )
        wrangler = self._score_package_wrangler
        io_manager = self._io_manager
        with context:
            while True:
                result = wrangler._get_sibling_score_path()
                if not result:
                    result = io_manager._get_wrangler_navigation_directive()
                if not result:
                    menu = wrangler._make_main_menu()
                    result = menu._run()
                if self._should_backtrack():
                    return
                if result:
                    wrangler._handle_main_menu_result(result)
                    if self._should_backtrack():
                        return

    def _should_backtrack(self):
        self._update_session_variables()
        if self._session.is_complete:
            return True
        else:
            return False

    def _update_session_variables(self):
        if self._session.is_backtracking_to_score_manager:
            self._session._is_backtracking_to_score_manager = False
        if self._session.is_backtracking_to_score:
            self._session._is_backtracking_to_score = False