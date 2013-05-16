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

    ### INITIALIZER ###

    def __init__(self, session=None):
        PackageWrangler.__init__(
            self,
            built_in_asset_container_package_paths=['experimental.tools.scoremanagertools.built_in_scores'],
            user_asset_container_filesystem_paths=[self.configuration.user_scores_directory_path],
            session=session,
            )

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'scores'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self):
        self.print_not_yet_implemented()

    def _make_main_menu(self):
        self.print_not_yet_implemented()

    def _make_visible_asset_menu_tokens(self, head=None):
        menuing_pairs = self.list_visible_asset_package_path_and_score_title_pairs()
        tmp = stringtools.strip_diacritics_from_binary_string
        menuing_pairs.sort(lambda x, y: cmp(tmp(x[1]), tmp(y[1])))
        return menuing_pairs

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_container_proxy_class(self):
        '''Score package wrangler asset proxy class:

        ::

            >>> wrangler.asset_container_proxy_class.__name__
            'PackageProxy'

        Return class.
        '''
        return super(type(self), self).asset_container_proxy_class

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
    def built_in_asset_container_filesystem_paths(self):
        '''Score package wrangler built-in asset container directory paths:

        ::

            >>> wrangler.built_in_asset_container_filesystem_paths
            ['.../tools/scoremanagertools/built_in_scores']

        Return list.
        '''
        return super(type(self), self).built_in_asset_container_filesystem_paths

    @property
    def built_in_asset_container_package_paths(self):
        '''Score package wrangler built-in asset container package paths:

        ::

            >>> wrangler.built_in_asset_container_package_paths
            ['experimental.tools.scoremanagertools.built_in_scores']

        Return list.
        '''
        return super(type(self), self).built_in_asset_container_package_paths

    @property
    def current_asset_container_filesystem_path(self):
        '''Score package wrangler current asset container directory path:

        ::

            >>> wrangler.current_asset_container_filesystem_path
            '.../Documents/scores'

        While in built-in score:

        ::

            >>> wrangler_in_built_in_score.current_asset_container_filesystem_path
            '.../tools/scoremanagertools/built_in_scores'

        Return string.
        '''
        if self._session.is_in_score:
            if self._session.underscore_delimited_current_score_name in os.listdir(
                self.configuration.built_in_scores_directory_path):
                return self.configuration.built_in_scores_directory_path
            else:
                return self.configuration.user_scores_directory_path
        else:
            return self.configuration.user_scores_directory_path

    @property
    def current_asset_container_package_path(self):
        '''Score package wrangler current asset container package path:

        ::

            >>> wrangler.current_asset_container_package_path
            ''

        While in built-in score:

        ::

            >>> wrangler_in_built_in_score.current_asset_container_package_path
            'experimental.tools.scoremanagertools.built_in_scores'

        Return string.
        '''
        package_path = self.configuration.filesystem_path_to_packagesystem_path(
            self.current_asset_container_filesystem_path)
        return package_path

    @property
    def score_external_asset_proxies(self):
        '''Score package wrangler score-external asset proxies:

        ::

            >>> wrangler.score_external_asset_proxies
            []

        Return list.
        '''
        return super(type(self), self).score_external_asset_proxies

    @property
    def storage_format(self):
        '''Score package wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.ScorePackageWrangler()'

        Return string.
        '''
        return super(type(self), self).storage_format

    @property
    def user_asset_container_filesystem_paths(self):
        '''Score package wrangler user asset container directory paths:

        ::

            >>> wrangler.user_asset_container_filesystem_paths
            ['.../Documents/scores']

        Return list.
        '''
        return super(type(self), self).user_asset_container_filesystem_paths

    @property
    def user_score_external_asset_container_package_path(self):
        '''Score package wrangler user score-external asset container package path:

        ::

            >>> wrangler.user_score_external_asset_container_package_path
            ''

        Return string.
        '''
        return super(type(self), self).user_score_external_asset_container_package_path

    @property
    def visible_score_titles(self):
        '''Score package wrangler visible score titles:

        ::

            >>> 'Red Example Score' in wrangler.visible_score_titles
            True

        Return list.
        '''
        result = []
        for score_package_proxy in self.get_visible_asset_proxies():
            result.append(score_package_proxy.title or '(untitled score)')
        return result

    @property
    def visible_score_titles_with_years(self):
        '''Score package wrangler visible score titles with years:

        ::

            >>> 'Red Example Score (2013)' in wrangler.visible_score_titles_with_years
            True

        Return list.
        '''
        result = []
        for score_package_proxy in self.get_visible_asset_proxies():
            result.append(score_package_proxy.title_with_year or '(untitled score)')
        return result

    ### PUBLIC METHODS ###

    def fix_visible_assets(self, is_interactive=True):
        results = []
        for asset_proxy in self.get_visible_asset_proxies():
            results.append(asset_proxy.fix(is_interactive=is_interactive))
            if is_interactive:
                asset_proxy.profile()
        return results

    def get_asset_proxies(self, head=None):
        '''Score package wrangler get asset proxies:

        ::

            >>> for x in wrangler.get_asset_proxies():
            ...     x
            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/blue_example_score')
            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/green_example_score')
            ScorePackageProxy('.../tools/scoremanagertools/built_in_scores/red_example_score')
            ...

        Output lists built-in scores followed by user scores.

        Return list.
        '''
        return super(type(self), self).get_asset_proxies(head=head)        

    def get_visible_asset_proxies(self, head=None):
        '''Score package wrangler get visible asset proxies:

        ::

            >>> for x in wrangler.get_visible_asset_proxies():
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
        for asset_proxy in PackageWrangler.get_asset_proxies(self, head=head):
            is_mothballed = asset_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(asset_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(asset_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(asset_proxy)
        return result

    def list_asset_package_paths(self, head=None):
        '''Score package wrangler list asset package paths:

        ::

            >>> for x in wrangler.list_asset_package_paths():
            ...     x
            'experimental.tools.scoremanagertools.built_in_scores.blue_example_score'
            'experimental.tools.scoremanagertools.built_in_scores.green_example_score'
            'experimental.tools.scoremanagertools.built_in_scores.red_example_score'
            ...

        Output lists built-in scores followed by user scores.

        Return list.
        '''
        return super(type(self), self).list_asset_package_paths(head=head)

    def list_score_external_asset_filesystem_paths(self, head=None):
        '''Score package wrangler list score-external asset filesystem paths:

        ::

            >>> wrangler.list_score_external_asset_filesystem_paths()
            []
        
        Return list.
        '''
        # TODO: this should not have to be hard-coded
        return []

    def list_score_external_asset_package_paths(self, head=None):
        '''Score package wrangler list score-external asset package paths:

        ::

            >>> wrangler.list_score_external_asset_package_paths()
            []
        
        Return list.
        '''
        # TODO: this should not have to be hard-coded
        return []

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
        for visible_asset_proxy in self.get_visible_asset_proxies(head=head):
            result.append(visible_asset_proxy.filesystem_path)
        return result

    # TODO: change name to self.list_visible_asset_basenames() ... or remove if unused?
    def list_visible_asset_names(self, head=None):
        result = []
        for asset_filesystem_path in self.list_visible_asset_filesystem_paths(head=head):
            result.append(os.path.basename(asset_filesystem_path))
        return result

    def list_visible_asset_package_path_and_score_title_pairs(self, head=None):
        result = []
        scores_to_show = self._session.scores_to_show
        for asset_proxy in PackageWrangler.get_asset_proxies(self, head=head):
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
        score_package_proxy = self._get_asset_proxy(score_package_name)
        score_package_proxy.add_tag('title', title)
        score_package_proxy.year_of_completion = year
        self._session.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)

    def profile_visible_assets(self):
        for asset_proxy in self.get_visible_asset_proxies():
            asset_proxy.profile()
