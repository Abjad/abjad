import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.FileWrangler import FileWrangler


class StylesheetFileWrangler(FileWrangler):
    '''Stylesheet file wrangler.

        >>> wrangler = scoremanagertools.wranglers.StylesheetFileWrangler()
        >>> wrangler
        StylesheetFileWrangler('.../abjad/experimental/tools/scoremanagertools/stylesheets')

    Return stylesheet file wrangler.
    '''

    ### CLASS ATTRIBUTES ###

    system_stylesheets_directory_path = os.path.join(
        FileWrangler.configuration.score_manager_tools_directory_path, 'stylesheets')

    ### INITIALIZER ###

    def __init__(self, session=None):
        FileWrangler.__init__(self,
            system_asset_container_directory_paths=[self.system_stylesheets_directory_path],
            session=session)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _temporary_asset_name(self):
        return '__temporary_stylesheet.ly'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        from experimental.tools import scoremanagertools
        if result == 'new':
            self.make_asset_interactively()
        else:
            stylesheet_file_name = os.path.join(self.system_stylesheets_directory_path, result)
            stylesheet_proxy = scoremanagertools.proxies.StylesheetFileProxy(
                stylesheet_file_name, session=self._session)
            stylesheet_proxy._run()

    def _make_main_menu(self):
        menu, section = self._io.make_menu(where=self._where, is_parenthetically_numbered=True)
        section.tokens = self.stylesheet_file_names
        section = menu.make_section()
        section.append(('new', 'new stylesheet'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        '''Stylesheet file wrangler asset class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'StylesheetFileProxy'

        Return proxy class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.StylesheetFileProxy

    @property
    def breadcrumb(self):
        '''Stylesheet file wrangler breadcrumb:

        ::

            >>> wrangler.breadcrumb
            'stylesheets'

        Return string.
        '''
        return 'stylesheets'

    # TODO: write test; also rename to something general without 'stylehsset' in name
    @property
    def stylesheet_file_names(self):
        '''Stylesheet file wrangler stylesheet file names:

            >>> for x in wrangler.stylesheet_file_names:
            ...     x
            'clean_letter_14.ly'
            'clean_letter_16.ly'
            'rhythm_letter_16.ly'

        Return list.
        '''
        result = []
        for directory_entry in os.listdir(self.system_stylesheets_directory_path):
            if directory_entry.endswith('.ly'):
                result.append(directory_entry)
        return result

    ### PUBLIC METHODS ###

    # TODO: write test
    def make_asset_interactively(self):
        from experimental.tools import scoremanagertools
        getter = self._io.make_getter(where=self._where)
        getter.append_string('stylesheet name')
        stylesheet_file_name = getter._run()
        if self._session.backtrack():
            return
        stylesheet_file_name = stringtools.string_to_accent_free_underscored_delimited_lowercase(
            stylesheet_file_name)
        if not stylesheet_file_name.endswith('.ly'):
            stylesheet_file_name = stylesheet_file_name + '.ly'
        stylesheet_file_name = os.path.join(
            self.system_stylesheets_directory_path, stylesheet_file_name)
        stylesheet_proxy = scoremanagertools.proxies.StylesheetFileProxy(
            stylesheet_file_name, session=self._session)
        stylesheet_proxy.edit()

    # TODO: write test
    def select_stylesheet_file_name_interactively(self, clear=True, cache=False):
        self._session.cache_breadcrumbs(cache=cache)
        menu, section = self._io.make_menu(where=self._where, is_parenthetically_numbered=True)
        section.tokens = self.stylesheet_file_names
        while True:
            self._session.push_breadcrumb('select stylesheet')
            result = menu._run(clear=clear)
            if self._session.backtrack():
                break
            elif not result:
                self._session.pop_breadcrumb()
                continue
            else:
                break
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        result = os.path.join(self.system_stylesheets_directory_path, result)
        return result
