import os
from experimental.tools.scoremanagertools.proxies.MusicSpecifierModuleProxy import \
    MusicSpecifierModuleProxy
from experimental.tools.scoremanagertools.wranglers.ModuleWrangler import ModuleWrangler


class MusicSpecifierModuleWrangler(ModuleWrangler):

    ### CLASS ATTRIBUTES ###

    storehouse_path_infix_parts = ('music', 'specifiers')

    ### INITIALIZER ###

    def __init__(self, session=None):
        ModuleWrangler.__init__(self,
            built_in_external_storehouse_packagesystem_path=\
                self.configuration.built_in_specifiers_package_path,
            user_external_storehouse_packagesystem_path=\
                self.configuration.user_external_specifiers_directory_path,
            session=session,
            )

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'music specifiers'

    @property
    def _temporary_asset_name(self):
        return '__temporary_specifier_module.py'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        elif result == 'ren':
            self.rename_asset_interactively()
        elif result == 'rm':
            self.remove_assets_interactively()
        elif result == 'missing':
            self.make_storehouse_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            package_proxy = self._get_asset_proxy(result)
            package_proxy.edit()

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(where=self._where, is_keyed=False, is_parenthetically_numbered=True)
        section.tokens = self._make_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('new', 'new music specifier'))
        section.append(('ren', 'rename music specifier'))
        section.append(('rm', 'remove music specifiers'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        return MusicSpecifierModuleProxy

    ### PUBLIC METHODS ###

    def make_asset_interactively(self):
        getter = self._io.make_getter()
        getter.append_space_delimited_lowercase_string('music specifier name')
        package_name = getter._run()
        if self._session.backtrack():
            return
        package_name = package_name.replace(' ', '_')
        self.debug(package_name)
        self.make_asset(package_name)
        self.debug('foo')
