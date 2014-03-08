# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    r'''Score package wrangler.

    ..  container:: example

        ::

            >>> from scoremanager import wranglers
            >>> wrangler = wranglers.ScorePackageWrangler()
            >>> wrangler
            ScorePackageWrangler()

    ..  container:: example

        ::

            >>> wrangler_in_score = wranglers.ScorePackageWrangler()
            >>> session = wrangler_in_score._session
            >>> session._current_score_snake_case_name = 'red_example_score'
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(ScorePackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.ScorePackageManager
        self.abjad_storehouse_path = \
            self._configuration.abjad_score_packages_directory_path
        self.user_storehouse_path = \
            self._configuration.user_score_packages_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            if self._session.current_score_snake_case_name in \
                    sorted(os.listdir(
                self._configuration.abjad_score_packages_directory_path)):
                return \
                    self._configuration.abjad_score_packages_directory_path
            else:
                return self._configuration.user_score_packages_directory_path
        else:
            return self._configuration.user_score_packages_directory_path

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self):
        self._io_manager.print_not_yet_implemented()

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
            if manager._is_visible():
                visible_paths.append(path)
        return visible_paths

    def _make_asset_menu_entries(self):
        menu_pairs = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = self._initialize_asset_manager(path)
            metadata = manager._get_metadata()
            year_of_completion = metadata.get('year_of_completion')
            title = metadata.get('title')
            if year_of_completion:
                title_with_year = '{} ({})'.format(
                    title,
                    year_of_completion,
                    )
            else:
                title_with_year = str(title)
            pair = (manager._path, title_with_year)
            menu_pairs.append(pair)
        tmp = stringtools.strip_diacritics_from_binary_string
        menu_pairs.sort(key=lambda x: tmp(x[1]))
        menu_entries = []
        for menu_pair in menu_pairs:
            path, score_title = menu_pair
            entry = (score_title, None, None, path)
            menu_entries.append(entry)
        return menu_entries

    def _make_main_menu(self):
        self._io_manager.print_not_yet_implemented()
