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
        self.abjad_storehouse_directory_path = \
            self._configuration.abjad_score_packages_directory_path
        self.user_storehouse_directory_path = \
            self._configuration.user_score_packages_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def _current_storehouse_directory_path(self):
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
        package_path = \
            self._configuration.path_to_package(
            self._current_storehouse_directory_path)
        return package_path

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self):
        self._io_manager.print_not_yet_implemented()

    def _list_asset_filesystem_paths(
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

            >>> for x in wrangler._list_asset_filesystem_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../scoremanager/scorepackages/blue_example_score'
            '.../scoremanager/scorepackages/green_example_score'
            '.../scoremanager/scorepackages/red_example_score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_asset_filesystem_paths(
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
            ScorePackageManager('.../scorepackages/blue_example_score')
            ScorePackageManager('.../scorepackages/green_example_score')
            ScorePackageManager('.../scorepackages/red_example_score')

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

    def _list_asset_package_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Lists abjad score package paths:

        ::

            >>> for x in wrangler._list_asset_package_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'blue_example_score'
            'green_example_score'
            'red_example_score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_asset_package_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_directory_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad score storehouse:

        ::

            >>> for x in wrangler._list_storehouse_directory_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../scoremanager/scorepackages'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass._list_storehouse_directory_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

    def _list_visible_asset_filesystem_paths(
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

            >>> for x in wrangler._list_visible_asset_filesystem_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../scoremanager/scorepackages/blue_example_score'
            '.../scoremanager/scorepackages/green_example_score'
            '.../scoremanager/scorepackages/red_example_score'

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
            result.append(visible_asset_manager._filesystem_path)
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
            ScorePackageManager('.../scorepackages/blue_example_score')
            ScorePackageManager('.../scorepackages/green_example_score')
            ScorePackageManager('.../scorepackages/red_example_score')

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
        for filesystem_path in self._list_visible_asset_filesystem_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            ):
            package_path = self._configuration.path_to_package(
                filesystem_path)
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

    ### PUBLIC METHODS ###

    def add_assets_to_repository(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        if hasattr(self, '_list_visible_asset_managers'):
            managers = self._list_visible_asset_managers()
        else:
            managers = self._list_asset_managers(
                abjad_library=True, 
                user_library=True,
                abjad_score_packages=True, 
                user_score_packages=True,
                )
        for manager in managers:
            manager.add_assets_to_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def commit_assets_to_repository(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('commit message')
        commit_message = getter._run(clear_terminal=False)
        if self._session._backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self._io_manager.display(line)
        if not self._io_manager.confirm():
            return
        if hasattr(self, '_list_visible_asset_managers'):
            managers = self._list_visible_asset_managers()
        else:
            managers = self._list_asset_managers(
                abjad_library=True, 
                user_library=True,
                abjad_score_packages=True, 
                user_score_packages=True,
                )
        for manager in managers:
            manager.commit_assets_to_repository(
                commit_message=commit_message, 
                prompt=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def display_repository_status(self, prompt=True):
        r'''Check asset status in repository.

        Returns none.
        '''
        if hasattr(self, '_list_visible_asset_managers'):
            managers = self._list_visible_asset_managers()
        else:
            managers = self._list_asset_managers(
                abjad_library=True, 
                user_library=True,
                abjad_score_packages=True, 
                user_score_packages=True,
                )
        for manager in managers:
            manager.display_repository_status(prompt=False)
        self._io_manager.proceed(prompt=prompt)

    def fix_visible_assets(self, prompt=True):
        r'''Fixes visible assets.

        Returns result list.
        '''
        results = []
        for asset_manager in self._list_visible_asset_managers():
            result = asset_manager.fix(
                prompt=False,
                )
            results.append(result)
        self._io_manager.proceed(prompt=prompt)
        return results

    def make_asset(
        self, 
        rollback=False,
        pending_user_input=None,
        ):
        r'''Makes asset.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        breadcrumb = self._session._pop_breadcrumb(rollback=rollback)
        getter = self._io_manager.make_getter(where=self._where)
        getter.indent_level = 1
        getter.prompt_character = ':'
        getter.capitalize_prompts = False
        getter.include_newlines = False
        getter.number_prompts = True
        getter.append_string('score title')
        getter.append_snake_case_package_name('package name')
        getter.append_integer_in_range('year', start=1, allow_none=True)
        result = getter._run()
        if self._session._backtrack():
            return
        title, score_package_name, year = result
        self._make_asset(score_package_name)
        score_package_manager = self._initialize_asset_manager(
            score_package_name)
        score_package_manager._add_metadatum('title', title)
        score_package_manager.year_of_completion = year
        self._session._push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)

    def update_from_repository(self, prompt=True):
        r'''Updates assets from repository.

        Returns none.
        '''
        if hasattr(self, '_list_visible_asset_managers'):
            managers = self._list_visible_asset_managers()
        else:
            managers = self._list_asset_managers(
                abjad_library=True, 
                user_library=True,
                abjad_score_packages=True, 
                user_score_packages=True,
                )
        for manager in managers:
            manager.update_from_repository(prompt=False)
        self._io_manager.proceed(prompt=prompt)
