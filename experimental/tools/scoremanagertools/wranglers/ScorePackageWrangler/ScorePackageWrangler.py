import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    '''Score package wrangler:

    ::

        >>> wrangler = scoremanagertools.wranglers.ScorePackageWrangler()
        >>> wrangler
        ScorePackageWrangler()

    ::

        >>> wrangler_in_built_in_score = scoremanagertools.wranglers.ScorePackageWrangler()
        >>> wrangler_in_built_in_score._session._underscore_delimited_current_score_name = 'red_example_score'
        >>> wrangler_in_built_in_score
        ScorePackageWrangler()

    Return score package wrangler.
    '''

    ### CLASS VARIABLES ###

    built_in_external_storehouse_filesystem_path = \
        PackageWrangler.configuration.built_in_scores_directory_path
    built_in_external_storehouse_packagesystem_path = \
        PackageWrangler.configuration.built_in_scores_package_path
    user_external_storehouse_filesystem_path = \
        PackageWrangler.configuration.user_scores_directory_path
    user_external_storehouse_packagesystem_path = \
        PackageWrangler.configuration.user_scores_package_path

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    @property
    def _current_storehouse_filesystem_path(self):
        if self._session.is_in_score:
            if self._session.underscore_delimited_current_score_name in os.listdir(
                self.configuration.built_in_scores_directory_path):
                return self.configuration.built_in_scores_directory_path
            else:
                return self.configuration.user_scores_directory_path
        else:
            return self.configuration.user_scores_directory_path

    @property
    def _current_storehouse_packagesystem_path(self):
        package_path = self.configuration.filesystem_path_to_packagesystem_path(
            self._current_storehouse_filesystem_path)
        return package_path

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self):
        self.print_not_yet_implemented()

    def _make_main_menu(self):
        self.print_not_yet_implemented()

    def _make_menu_tokens(self, head=None):
        menuing_pairs = self.list_visible_asset_package_path_and_score_title_pairs()
        tmp = stringtools.strip_diacritics_from_binary_string
        menuing_pairs.sort(lambda x, y: cmp(tmp(x[1]), tmp(y[1])))
        return menuing_pairs

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        '''Score package wrangler asset proxy class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'ScorePackageProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.ScorePackageProxy

    @property
    def storage_format(self):
        '''Score package wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.ScorePackageWrangler()'

        Return string.
        '''
        return super(type(self), self).storage_format

    ### PUBLIC METHODS ###

    def fix_visible_assets(self, is_interactive=True):
        results = []
        for asset_proxy in self.list_visible_asset_proxies():
            results.append(asset_proxy.fix(is_interactive=is_interactive))
            if is_interactive:
                asset_proxy.profile()
        return results

    def list_asset_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''Score package manager list specific asset filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_scores/blue_example_score'
            '.../tools/scoremanagertools/built_in_scores/green_example_score'
            '.../tools/scoremanagertools/built_in_scores/red_example_score'
    
        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(
            built_in_external=built_in_external, 
            user_external=user_external,
            built_in_score=built_in_score, 
            user_score=user_score, 
            head=head)

    def list_asset_names(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset names.

        Example. List built-in score names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     user_external=False, user_score=False):
            ...     x
            'blue example score'
            'green example score'
            'red example score'

        Return list.
        '''
        return super(type(self), self).list_asset_names(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    # TODO: this is fine; just uncomment once MaterialPackageWrangler works the same way
#    def list_asset_packagesystem_paths(self, 
#        built_in_external=True, user_external=True,
#        built_in_score=True, user_score=True, head=None):
#        '''List asset packagesystem paths.
#
#        Example. List built-in score package paths:
#
#        ::
#
#            >>> for x in wrangler.list_asset_packagesystem_paths(
#            ...     user_external=False, user_score=False):
#            ...     x
#            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score'
#            'experimental.tools.scoremanagertools.built_in_scores.green_example_score'
#            'experimental.tools.scoremanagertools.built_in_scores.red_example_score'
#
#        Return list.
#        '''
#        return super(type(self), self).list_asset_packagesystem_paths(
#            built_in_external=built_in_external,
#            user_external=user_external,
#            built_in_score=built_in_score,
#            user_score=user_score,
#            head=head)

#    def list_asset_proxies(self, head=None):
#        '''Score package wrangler get asset proxies:
#
#        ::
#
#            >>> for x in wrangler.list_asset_proxies():
#            ...     x
#            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/blue_example_score')
#            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/green_example_score')
#            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/red_example_score')
#            ...
#
#        Output lists built-in scores followed by user scores.
#
#        Return list.
#        '''
#        return super(type(self), self).list_asset_proxies(head=head)        

    def list_external_asset_packagesystem_paths(self, head=None):
        '''Score package wrangler list external asset package paths:

        ::

            >>> wrangler.list_external_asset_packagesystem_paths()
            []

        Return list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_score=False, user_score=False, head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_score_asset_packagesystem_paths(self, head=None):
        '''List score asset packagesystem paths.

        ::

            >>> for x in wrangler.list_score_asset_packagesystem_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score'
            'experimental.tools.scoremanagertools.built_in_scores.green_example_score'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score'
            'aracilik'
            'archipel'
            'betoerung'
            'cary'
            'chrysanthemums'
            'desir'
            'gebiete'
            'imaginaire'
            'jivan'
            'lidercfeny'
            'mannigfaltigkeiten'
            'manos'
            'recursif'
            'red_shift'
            'sekka'
            'tack'
            'territoires'
            'zeit'

        Return list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_external=False, user_external=False, head=head):
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_storehouse_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List storehouse filesystem paths.

        Example. List built-in score storehouse:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_scores'

        Return list.
        '''
        result = []
        if built_in_score:
            result.append(self.configuration.built_in_scores_directory_path)
        if user_score:
            result.append(self.configuration.user_scores_directory_path)
        return result

    def list_visible_asset_filesystem_paths(self, head=None):
        '''Score package wrangler list visible asset filesystem paths:

        ::

            >>> for x in wrangler.list_visible_asset_filesystem_paths():
            ...     x
            '.../tools/scoremanagertools/built_in_scores/blue_example_score'
            '.../tools/scoremanagertools/built_in_scores/green_example_score'
            '.../tools/scoremanagertools/built_in_scores/red_example_score'
            ...

        Output lists built-in scores followed by user scores.

        Return list.
        '''
        result = []
        for visible_asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(visible_asset_proxy.filesystem_path)
        return result

    def list_visible_asset_package_path_and_score_title_pairs(self, head=None):
        result = []
        scores_to_show = self._session.scores_to_show
        for asset_proxy in PackageWrangler.list_asset_proxies(self, head=head):
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

    def list_visible_asset_proxies(self, head=None):
        '''Score package wrangler get visible asset proxies:

        ::

            >>> for x in wrangler.list_visible_asset_proxies():
            ...     x
            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/blue_example_score')
            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/green_example_score')
            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/red_example_score')
            ...
        
        Output lists built-in scores followed by user scores.

        Return list.
        '''
        result = []
        scores_to_show = self._session.scores_to_show
        for asset_proxy in PackageWrangler.list_asset_proxies(self, head=head):
            is_mothballed = asset_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(asset_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(asset_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(asset_proxy)
        return result

    def make_asset_interactively(self, rollback=False):
        breadcrumb = self._session.pop_breadcrumb(rollback=rollback)
        getter = self._io.make_getter(where=self._where)
        getter.indent_level = 1
        getter.prompt_character = ':'
        getter.capitalize_prompts = False
        getter.include_newlines = False
        getter.number_prompts = True
        getter.append_string('score title')
        getter.append_underscore_delimited_lowercase_package_name('package name')
        getter.append_integer_in_range('year', start=1, allow_none=True)
        result = getter._run()
        if self._session.backtrack():
            return
        title, score_package_name, year = result
        self.make_asset(score_package_name)
        score_package_proxy = self._initialize_asset_proxy(score_package_name)
        score_package_proxy.add_tag('title', title)
        score_package_proxy.year_of_completion = year
        self._session.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)

    def profile_visible_assets(self):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.profile()

    def svn_add_assets(self, is_interactive=True):
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                built_in_external=True, user_external=True,
                built_in_score=True, user_score=True)
        for proxy in proxies:
            proxy.svn_add(is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)

    def svn_ci_assets(self, is_interactive=True):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('commit message')
        commit_message = getter._run()
        if self._session.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self._io.display(line)
        if not self._io.confirm():
            return
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                built_in_external=True, user_external=True,
                built_in_score=True, user_score=True)
        for proxy in proxies:
            proxy.svn_ci(commit_message=commit_message, is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)

    def svn_st_assets(self, is_interactive=True):
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                built_in_external=True, user_external=True,
                built_in_score=True, user_score=True)
        for proxy in proxies:
            proxy.svn_st(is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)

    def svn_up_assets(self, is_interactive=True):
        if hasattr(self, 'list_visible_asset_proxies'):
            proxies = self.list_visible_asset_proxies()
        else:
            proxies = self.list_asset_proxies(
                built_in_external=True, user_external=True,
                built_in_score=True, user_score=True)
        for proxy in proxies:
            proxy.svn_up(is_interactive=False)
        self._io.proceed(is_interactive=is_interactive)
