import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler
from experimental.tools.scoremanagertools.proxies.ScorePackageProxy import ScorePackageProxy


class ScorePackageWrangler(PackageWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        PackageWrangler.__init__(self,
            built_in_asset_container_package_paths=[],
            session=session)

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
    def asset_proxy_class(self):
        return ScorePackageProxy

    @property
    def current_asset_container_directory_path(self):
        return self.configuration.user_scores_directory_path

    @property
    def visible_score_titles(self):
        result = []
        for score_package_proxy in self.get_visible_asset_proxies():
            result.append(score_package_proxy.title or '(untitled score)')
        return result

    @property
    def visible_score_titles_with_years(self):
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

    def get_visible_asset_proxies(self, head=None):
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

    def list_visible_asset_filesystem_paths(self, head=None):
        result = []
        for visible_asset_proxy in self.get_visible_asset_proxies(head=head):
            result.append(visible_asset_proxy.filesystem_path)
        return result

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
