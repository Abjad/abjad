# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class ScorePackageWrangler(Wrangler):
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
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(ScorePackageWrangler, self)
        superclass.__init__(session=session)
        path = self._configuration.example_score_packages_directory_path
        self._abjad_storehouse_path = path
        path = self._configuration.user_score_packages_directory_path
        self._user_storehouse_path = path

    ### PRIVATE PROPERTIES ###

    @property
    def _asset_manager_class(self):
        from scoremanager import managers
        return managers.ScorePackageManager

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            path = self._configuration.example_score_packages_directory_path
            directory_entries = sorted(os.listdir(path))
            manager = self._session.current_score_package_manager
            score_name = manager._package_name
            if score_name in directory_entries:
                return path
            else:
                return self._configuration.user_score_packages_directory_path
        else:
            return self._configuration.user_score_packages_directory_path

    @property
    def _user_input_to_action(self):
        superclass = super(ScorePackageWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'new': self.make_score_package,
            'rm': self.remove_score_package,
            })
        return result

    ### PRIVATE METHODS ###

    def _find_git_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_git_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _find_svn_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_svn_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _is_valid_directory_entry(self, expr):
        superclass = super(ScorePackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_visible_asset_paths(
        self,
        abjad_library=True,
        user_library=True,
        example_score_packages=True,
        user_score_packages=True,
        ):
        visible_paths = []
        paths = self._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = self._initialize_manager(path)
            if manager._is_visible() != False:
                visible_paths.append(path)
        return visible_paths

    ### PUBLIC METHODS ###

    def make_score_package(self):
        r'''Makes score package.

        Returns none.
        '''
        path = self.get_available_path()
        if self._should_backtrack():
            return
        if not path:
            return
        self._make_asset(path)
        self._io_manager.write_cache(prompt=False)

    def remove_score_package(self):
        r'''Removes one or more score packages.
        
        Returns none.
        '''
        self._remove_asset(
            item_identifier='score package',
            )