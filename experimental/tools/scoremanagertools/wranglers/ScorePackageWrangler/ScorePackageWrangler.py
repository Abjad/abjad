# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler \
    import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    r'''Score package wrangler.

    ::

        >>> wrangler = scoremanagertools.wranglers.ScorePackageWrangler()
        >>> wrangler
        ScorePackageWrangler()

    ::

        >>> wrangler_in_built_in_score = \
        ...     scoremanagertools.wranglers.ScorePackageWrangler()
        >>> session = wrangler_in_built_in_score.session
        >>> session._snake_case_current_score_name = 'red_example_score'
        >>> wrangler_in_built_in_score
        ScorePackageWrangler()

    '''

    ### CLASS VARIABLES ###

    asset_storehouse_filesystem_path_in_built_in_asset_library = \
        PackageWrangler.configuration.built_in_score_packages_directory_path

    asset_storehouse_packagesystem_path_in_built_in_asset_library = \
        PackageWrangler.configuration.built_in_score_packages_package_path

    score_package_asset_storehouse_path_infix_parts = None

    asset_storehouse_filesystem_path_in_user_asset_library = \
        PackageWrangler.configuration.user_score_packages_directory_path

    asset_storehouse_packagesystem_path_in_user_asset_library = \
        PackageWrangler.configuration.user_score_packages_package_path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def _current_storehouse_filesystem_path(self):
        if self.session.is_in_score:
            if self.session.snake_case_current_score_name in \
                    os.listdir(
                self.configuration.built_in_score_packages_directory_path):
                return \
                    self.configuration.built_in_score_packages_directory_path
            else:
                return self.configuration.user_score_packages_directory_path
        else:
            return self.configuration.user_score_packages_directory_path

    @property
    def _current_storehouse_packagesystem_path(self):
        package_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
            self._current_storehouse_filesystem_path)
        return package_path

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self):
        self.session.io_manager.print_not_yet_implemented()

    def _make_main_menu(self):
        self.session.io_manager.print_not_yet_implemented()

    def _make_asset_menu_entries(self, head=None):
        menuing_pairs = \
            self.list_visible_asset_package_path_and_score_title_pairs()
        tmp = stringtools.strip_diacritics_from_binary_string
        menuing_pairs.sort(key=lambda x: tmp(x[1]))
        menuing_entries = [(x[1], None, None, x[0]) for x in menuing_pairs]
        return menuing_entries

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        r'''Asset proxy class of score package wrangler.

        ::

            >>> wrangler.asset_proxy_class.__name__
            'ScorePackageManager'

        Returns class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.ScorePackageManager

    ### PUBLIC METHODS ###

    def fix_visible_assets(self, is_interactive=True):
        r'''Fixes visible assets.

        Returns result list.
        '''
        results = []
        for asset_proxy in self.list_visible_asset_proxies():
            result = asset_proxy.interactively_fix(
                is_interactive=False,
                )
            results.append(result)
            if is_interactive:
                asset_proxy.interactively_profile(prompt=False)
        self.session.io_manager.proceed(is_interactive=is_interactive)
        return results

    def interactively_make_asset(
        self, 
        rollback=False,
        pending_user_input=None,
        ):
        r'''Interactively makes asset.

        Return none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        breadcrumb = self.session.pop_breadcrumb(rollback=rollback)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.indent_level = 1
        getter.prompt_character = ':'
        getter.capitalize_prompts = False
        getter.include_newlines = False
        getter.number_prompts = True
        getter.append_string('score title')
        getter.append_snake_case_package_name('package name')
        getter.append_integer_in_range('year', start=1, allow_none=True)
        result = getter._run()
        if self.session.backtrack():
            return
        title, score_package_name, year = result
        self.make_asset(score_package_name)
        score_package_proxy = self._initialize_asset_proxy(score_package_name)
        score_package_proxy.add_tag('title', title)
        score_package_proxy.year_of_completion = year
        self.session.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)

    def list_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Example. List built-in score package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/scorepackages/blue_example_score'
            '.../tools/scoremanagertools/scorepackages/green_example_score'
            '.../tools/scoremanagertools/scorepackages/red_example_score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_names(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Example. List built-in score package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'blue example score'
            'green example score'
            'red example score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass.list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Example. List built-in score package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'experimental.tools.scoremanagertools.scorepackages.blue_example_score'
            'experimental.tools.scoremanagertools.scorepackages.green_example_score'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass.list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_proxies(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset proxies.

        Example. List built-in score package proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            ScorePackageManager('.../tools/scoremanagertools/scorepackages/blue_example_score')
            ScorePackageManager('.../tools/scoremanagertools/scorepackages/green_example_score')
            ScorePackageManager('.../tools/scoremanagertools/scorepackages/red_example_score')

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass.list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_storehouse_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Example. List built-in score storehouse:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/scorepackages'

        Returns list.
        '''
        superclass = super(ScorePackageWrangler, self)
        return superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    def list_visible_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists visible asset filesystem paths.

        Example. List visible built-in score package filesystem paths:

        ::

            >>> for x in wrangler.list_visible_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/scorepackages/blue_example_score'
            '.../tools/scoremanagertools/scorepackages/green_example_score'
            '.../tools/scoremanagertools/scorepackages/red_example_score'

        Returns list.
        '''
        result = []
        for visible_asset_proxy in self.list_visible_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            result.append(visible_asset_proxy.filesystem_path)
        return result

    def list_visible_asset_package_path_and_score_title_pairs(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        head=None,
        ):
        r'''Lists visible asset package path and score title pairs.

        Example. List visible built-in score package path and title pairs:

        ::

            >>> for x in wrangler.list_visible_asset_package_path_and_score_title_pairs(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            ('experimental.tools.scoremanagertools.scorepackages.blue_example_score', 'Blue Example Score (2013)')
            ('experimental.tools.scoremanagertools.scorepackages.green_example_score', 'Green Example Score (2013)')
            ('experimental.tools.scoremanagertools.scorepackages.red_example_score', 'Red Example Score (2013)')

        Returns list.
        '''
        result = []
        scores_to_show = self.session.scores_to_show
        for asset_proxy in PackageWrangler.list_asset_proxies(
            self,
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            tags = asset_proxy.get_tags()
            is_mothballed = tags.get('is_mothballed', False)
            if scores_to_show == 'all' or \
                (scores_to_show == 'active' and not is_mothballed) or \
                (scores_to_show == 'mothballed' and is_mothballed):
                year_of_completion = tags.get('year_of_completion')
                if year_of_completion:
                    title_with_year = '{} ({})'.format(tags['title'], year_of_completion)
                else:
                    title_with_year = '{}'.format(tags['title'])
                result.append((asset_proxy.package_path, title_with_year))
        return result

    def list_visible_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists visible asset packagesystem paths.

        Example. List visible built-in score package packagesystem paths:

        ::

            >>> for x in wrangler.list_visible_asset_packagesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'experimental.tools.scoremanagertools.scorepackages.blue_example_score'
            'experimental.tools.scoremanagertools.scorepackages.green_example_score'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score'

        Returns list.
        '''
        result = []
        for filesystem_path in self.list_visible_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_visible_asset_proxies(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        head=None,
        ):
        r'''Lists visible asset proxies.

        Example. List visible score package proxies:

        ::

            >>> for x in wrangler.list_visible_asset_proxies(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            ScorePackageManager('.../tools/scoremanagertools/scorepackages/blue_example_score')
            ScorePackageManager('.../tools/scoremanagertools/scorepackages/green_example_score')
            ScorePackageManager('.../tools/scoremanagertools/scorepackages/red_example_score')

        Returns list.
        '''
        result = []
        scores_to_show = self.session.scores_to_show
        for asset_proxy in PackageWrangler.list_asset_proxies(
            self,
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            is_mothballed = asset_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(asset_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(asset_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(asset_proxy)
        return result

    def profile_visible_assets(self):
        r'''Profiles visible assets.

        Returns none.
        '''
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.profile()

    def repository_add_assets(self, is_interactive=True):
        r'''Adds assets to repository.

        Return none.
        '''
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                in_built_in_asset_library=True, in_user_asset_library=True,
                in_built_in_score_packages=True, in_user_score_packages=True)
        for proxy in proxies:
            proxy.repository_add(is_interactive=False)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def repository_ci_assets(self, is_interactive=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('commit message')
        commit_message = getter._run(clear_terminal=False)
        if self.session.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.session.io_manager.display(line)
        if not self.session.io_manager.confirm():
            return
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                in_built_in_asset_library=True, 
                in_user_asset_library=True,
                in_built_in_score_packages=True, 
                in_user_score_packages=True,
                )
        for proxy in proxies:
            proxy.repository_ci(commit_message=commit_message, is_interactive=False)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def repository_st_assets(self, is_interactive=True):
        r'''Check asset status in repository.

        Returns none.
        '''
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                in_built_in_asset_library=True, in_user_asset_library=True,
                in_built_in_score_packages=True, in_user_score_packages=True)
        for proxy in proxies:
            proxy.repository_st(is_interactive=False)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def repository_up_assets(self, is_interactive=True):
        r'''Updates assets from repository.

        Returns none.
        '''
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                in_built_in_asset_library=True, in_user_asset_library=True,
                in_built_in_score_packages=True, in_user_score_packages=True)
        for proxy in proxies:
            proxy.repository_up(is_interactive=False)
        self.session.io_manager.proceed(is_interactive=is_interactive)
