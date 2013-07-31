# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class StylesheetFileProxy(FileProxy):
    r'''Stylesheet file proxy:

    ::

        >>> import os

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.stylesheet_file_wrangler
        >>> directory_name = \
        ...     wrangler.asset_storehouse_filesystem_path_in_built_in_asset_library
        >>> filesystem_path = os.path.join(
        ...     directory_name, 'clean-letter-14.ly')
        >>> proxy = scoremanagertools.proxies.StylesheetFileProxy(
        ...     filesystem_path=filesystem_path)

    ::

        >>> proxy
        StylesheetFileProxy('.../scoremanagertools/stylesheets/clean-letter-14.ly')

    Return stylesheet proxy.
    '''

    ### CLASS VARIABLES ###

    _generic_class_name = 'stylesheet'

    _temporary_asset_name = 'temporary_stylesheet.ly'

    extension = '.ly'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            raise ValueError

    def _initialize_file_name_getter(self):
        getter = self.session.io_manager.make_getter()
        getter.append_dash_case_file_name('new name')
        return getter

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        command_section = main_menu.make_command_section()
        command_section.append(('copy stylesheet', 'cp'))
        command_section.append(('delete stylesheet', 'rm'))
        command_section.append(('rename stylesheet', 'ren'))
        command_section.append(('vim stylesheet', 'vim'))
        return main_menu

    def _space_delimited_lowercase_name_to_asset_name(self, 
        space_delimited_lowercase_name):
        asset_name = FileProxy._space_delimited_lowercase_name_to_asset_name(
            self, space_delimited_lowercase_name)
        if not asset_name.endswith(self.extension):
            asset_name += self.extension
        return asset_name
