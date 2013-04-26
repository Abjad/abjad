import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler
from experimental.tools.scoremanagertools.proxies.StylesheetFileProxy import StylesheetFileProxy


class StylesheetFileWrangler(PackageWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
#        PackageWrangler.__init__(self,
#            score_external_asset_container_package_importable_names=[self.configuration.stylesheets_package_importable_name],
#            score_internal_asset_container_package_importable_name_infix=None,
#            session=session)
        PackageWrangler.__init__(self, session=session)
        self._score_external_asset_container_package_importable_names = [
            self.configuration.stylesheets_package_importable_name]
        self._score_internal_asset_container_package_importable_name_infix = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return StylesheetFileProxy

    @property
    def breadcrumb(self):
        return 'stylesheets'

    # TODO: write test
    @property
    def stylesheet_file_names(self):
        result = []
        for file_name in os.listdir(self.configuration.stylesheets_directory_path):
            if file_name.endswith('.ly'):
                result.append(file_name)
        return result

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        else:
            stylesheet_file_name = os.path.join(self.configuration.stylesheets_directory_path, result)
            stylesheet_proxy = StylesheetFileProxy(stylesheet_file_name, session=self.session)
            stylesheet_proxy.run()

    # TODO: write test
    def make_asset_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('stylesheet name')
        stylesheet_name = getter.run()
        if self.backtrack():
            return
        stylesheet_name = stringtools.string_to_strict_directory_name(stylesheet_name)
        if not stylesheet_name.endswith('.ly'):
            stylesheet_name = stylesheet_name + '.ly'
        stylesheet_file_name = os.path.join(self.configuration.stylesheets_directory_path, stylesheet_name)
        stylesheet_proxy = StylesheetFileProxy(stylesheet_file_name, session=self.session)
        stylesheet_proxy.edit()

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.stylesheet_file_names
        section = menu.make_section()
        section.append(('new', 'new stylesheet'))
        return menu

    # TODO: write test
    def select_stylesheet_file_name_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.stylesheet_file_names
        while True:
            self.push_breadcrumb('select stylesheet')
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        result = os.path.join(self.configuration.stylesheets_directory_path, result)
        return result
