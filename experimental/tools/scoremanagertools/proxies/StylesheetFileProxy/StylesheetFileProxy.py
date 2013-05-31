from experimental.tools.scoremanagertools.proxies.FileProxy import FileProxy


class StylesheetFileProxy(FileProxy):
    '''Stylesheet file proxy:

    ::

        >>> import os

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.stylesheet_file_wrangler
        >>> directory_name = wrangler.built_in_external_storehouse_filesystem_path
        >>> filesystem_path = os.path.join(directory_name, 'clean-letter-14.ly')
        >>> proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path=filesystem_path)

    ::

        >>> proxy
        StylesheetFileProxy('.../tools/scoremanagertools/stylesheets/clean-letter-14.ly')

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
        getter = self._io.make_getter()
        getter.append_hyphen_delimited_lowercase_file_name('new name')
        return getter

    def _make_main_menu(self):
        menu, section = self._io.make_menu(where=self.where)
        section.append(('cp', 'copy stylesheet'))
        section.append(('rm', 'delete stylesheet'))
        section.append(('ren', 'rename stylesheet'))
        section.append(('vi', 'vi stylesheet'))
        return menu

    def _space_delimited_lowercase_name_to_asset_name(self, space_delimited_lowercase_name):
        asset_name = FileProxy._space_delimited_lowercase_name_to_asset_name(
            self, space_delimited_lowercase_name)
        if not asset_name.endswith(self.extension):
            asset_name += self.extension
        return asset_name
