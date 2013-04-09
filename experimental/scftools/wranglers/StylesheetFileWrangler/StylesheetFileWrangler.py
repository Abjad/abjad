from abjad.tools import iotools
from scftools.wranglers.PackageWrangler import PackageWrangler
from scftools.proxies.StylesheetFileProxy import StylesheetFileProxy
import os


class StylesheetFileWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self,
            score_external_asset_container_importable_names=[self.stylesheets_package_importable_name],
            score_internal_asset_container_importable_name_infix=None,
            session=session)

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
        for file_name in os.listdir(self.stylesheets_directory_name):
            if file_name.endswith('.ly'):
                result.append(file_name)
        return result

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        else:
            stylesheet_file_name = os.path.join(self.stylesheets_directory_name, result)
            stylesheet_proxy = StylesheetFileProxy(stylesheet_file_name, session=self.session)
            stylesheet_proxy.run()

    # TODO: write test
    def make_asset_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('stylesheet name')
        stylesheet_name = getter.run()
        if self.backtrack():
            return
        stylesheet_name = iotools.string_to_strict_directory_name(stylesheet_name)
        if not stylesheet_name.endswith('.ly'):
            stylesheet_name = stylesheet_name + '.ly'
        stylesheet_file_name = os.path.join(self.stylesheets_directory_name, stylesheet_name)
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
        result = os.path.join(self.stylesheets_directory_name, result)
        return result
