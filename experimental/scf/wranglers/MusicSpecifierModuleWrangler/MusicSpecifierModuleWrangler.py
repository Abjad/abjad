from scf.proxies.MusicSpecifierModuleProxy import MusicSpecifierModuleProxy
from scf.wranglers.ModuleWrangler import ModuleWrangler
import os


class MusicSpecifierModuleWrangler(ModuleWrangler):

    def __init__(self, session=None):
        ModuleWrangler.__init__(self,
            score_external_asset_container_importable_names=\
                [self.score_external_specifiers_package_importable_name],
            score_internal_asset_container_importable_name_infix=\
                self.score_internal_specifiers_package_importable_name_infix,
            session=session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return MusicSpecifierModuleProxy

    @property
    def breadcrumb(self):
        return 'music specifiers'

    @property
    def temporary_asset_short_name(self):
        return 'temporary_specifier_module.py'

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        elif result == 'ren':
            self.rename_asset_interactively()
        elif result == 'rm':
            self.remove_assets_interactively()
        elif result == 'missing':
            self.conditionally_make_asset_container_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            package_proxy = self.get_asset_proxy(result)
            package_proxy.edit()

    def make_asset_interactively(self):
        getter = self.make_getter()
        getter.append_space_delimited_lowercase_string('music specifier name')
        specifier_name = getter.run()
        if self.backtrack():
            return
        package_short_name = specifier_name.replace(' ', '_')
        self.debug(package_short_name)
        self.make_asset(package_short_name)
        self.debug('foo')

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_keyed=False, is_parenthetically_numbered=True)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('new', 'new music specifier'))
        section.append(('ren', 'rename music specifier'))
        section.append(('rm', 'remove music specifiers'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
        return menu
