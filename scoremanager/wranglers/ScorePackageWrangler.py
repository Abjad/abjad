# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    r'''Score package wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            ScorePackageWrangler()

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> session._current_score_snake_case_name = 'red_example_score'
            >>> wrangler_in_score = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(ScorePackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.ScorePackageManager
        path = self._configuration.abjad_score_packages_directory_path
        self._abjad_storehouse_path = path
        path = self._configuration.user_score_packages_directory_path
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            path = self._configuration.abjad_score_packages_directory_path
            directory_entries = sorted(os.listdir(path))
            current_score = self._session.current_score_snake_case_name
            if current_score in directory_entries:
                return path
            else:
                return self._configuration.user_score_packages_directory_path
        else:
            return self._configuration.user_score_packages_directory_path

    ### PRIVATE METHODS ###

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
        for path in paths:
            manager = self._initialize_asset_manager(path)
            if manager._is_visible() != False:
                visible_paths.append(path)
        return visible_paths

    ### PUBLIC METHODS ###

    def make_new_score(self, prompt=True):
        r'''Makes new score.

        Returns none.
        '''
        superclass = super(ScorePackageWrangler, self)
        superclass.make_asset()
        self._io_manager.write_cache(prompt=False)
