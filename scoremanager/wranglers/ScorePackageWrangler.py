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

    @property
    def _current_storehouse_package_path(self):
        package = self._configuration.path_to_package(
            self._current_storehouse_path)
        return package

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self):
        self._io_manager.print_not_yet_implemented()

    def _list_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad score package filesystem paths:

        ::

            >>> for x in wrangler._list_asset_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../scoremanager/scores/blue_example_score'
            '.../scoremanager/scores/green_example_score'
            '.../scoremanager/scores/red_example_score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_managers(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Lists abjad score package managers:

        ::

            >>> for x in wrangler._list_asset_managers(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            ScorePackageManager('.../scores/blue_example_score')
            ScorePackageManager('.../scores/green_example_score')
            ScorePackageManager('.../scores/red_example_score')

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_names(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Lists abjad score package names:

        ::

            >>> for x in wrangler._list_asset_names(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'blue example score'
            'green example score'
            'red example score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_asset_names(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad score storehouse:

        ::

            >>> for x in wrangler._list_storehouse_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../scoremanager/scores'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_storehouse_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

    def _list_visible_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists visible asset filesystem paths.

        Lists visible abjad score package filesystem paths:

        ::

            >>> for x in wrangler._list_visible_asset_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../scoremanager/scores/blue_example_score'
            '.../scoremanager/scores/green_example_score'
            '.../scoremanager/scores/red_example_score'

        Returns list.
        '''
        result = []
        for visible_asset_manager in self._list_visible_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            result.append(visible_asset_manager._path)
        return result

    def _list_visible_asset_managers(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        head=None,
        ):
        r'''Lists visible asset managers.

        Lists visible score package managers:

        ::

            >>> for x in wrangler._list_visible_asset_managers(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            ScorePackageManager('.../scores/blue_example_score')
            ScorePackageManager('.../scores/green_example_score')
            ScorePackageManager('.../scores/red_example_score')

        Returns list.
        '''
        result = []
        scores_to_display = self._session.scores_to_display
        for asset_manager in PackageWrangler._list_asset_managers(
            self,
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            is_mothballed = asset_manager._get_metadatum('is_mothballed')
            is_example = asset_manager._get_metadatum('is_example')
            if scores_to_display == 'all':
                result.append(asset_manager)
            elif (scores_to_display == 'active' and not is_mothballed and
                not is_example):
                result.append(asset_manager)
            elif (scores_to_display == 'example' and is_example and
                not is_mothballed):
                result.append(asset_manager)
            elif scores_to_display == 'mothballed' and is_mothballed:
                result.append(asset_manager)
        return result

    def _list_visible_asset_package_path_and_score_title_pairs(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        head=None,
        ):
        r'''Lists visible asset package path and score title pairs.

        Lists visible abjad score package path and title pairs:

        ::

            >>> for x in wrangler._list_visible_asset_package_path_and_score_title_pairs(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x[0]
            ...     x[1]
            ...     print
            'blue_example_score'
            'Blue Example Score (2013)'
            <BLANKLINE>
            'green_example_score'
            'Green Example Score (2013)'
            <BLANKLINE>
            'red_example_score'
            'Red Example Score (2013)'
            <BLANKLINE>

        Returns list.
        '''
        result = []
        scores_to_display = self._session.scores_to_display
        for asset_manager in PackageWrangler._list_asset_managers(
            self,
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            metadata = asset_manager._get_metadata()
            is_example = metadata.get('is_example', False)
            is_mothballed = metadata.get('is_mothballed', False)
            if scores_to_display == 'all' or \
                (scores_to_display == 'active' and not is_mothballed
                    and not is_example) or \
                (scores_to_display == 'example' and is_example 
                    and not is_mothballed) or \
                (scores_to_display == 'mothballed' and is_mothballed):
                year_of_completion = metadata.get('year_of_completion')
                if year_of_completion:
                    title_with_year = '{} ({})'.format(
                        metadata['title'], 
                        year_of_completion,
                        )
                else:
                    title_with_year = '{}'.format(metadata['title'])
                result.append((asset_manager._package_path, title_with_year))
        return result

    def _list_visible_asset_package_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists visible asset packagesystem paths.

        Lists visible abjad score package packagesystem paths:

        ::

            >>> for x in wrangler._list_visible_asset_package_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            'blue_example_score'
            'green_example_score'
            'red_example_score'

        Returns list.
        '''
        result = []
        for path in self._list_visible_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            package_path = self._configuration.path_to_package(
                path)
            result.append(package_path)
        return result

    def _make_asset_menu_entries(self, head=None):
        menuing_pairs = \
            self._list_visible_asset_package_path_and_score_title_pairs()
        tmp = stringtools.strip_diacritics_from_binary_string
        menuing_pairs.sort(key=lambda x: tmp(x[1]))
        menuing_entries = [(x[1], None, None, x[0]) for x in menuing_pairs]
        return menuing_entries

    def _make_main_menu(self):
        self._io_manager.print_not_yet_implemented()
