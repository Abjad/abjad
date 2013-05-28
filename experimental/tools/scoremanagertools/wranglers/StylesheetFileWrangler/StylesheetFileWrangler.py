import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.FileWrangler import FileWrangler


class StylesheetFileWrangler(FileWrangler):
    '''Stylesheet file wrangler.

        >>> wrangler = scoremanagertools.wranglers.StylesheetFileWrangler()
        >>> wrangler
        StylesheetFileWrangler()

    Return stylesheet file wrangler.
    '''

    ### CLASS VARIABLES ###

    built_in_external_storehouse_filesystem_path = os.path.join(
        FileWrangler.configuration.score_manager_tools_directory_path, 'built_in_stylesheets')

    storehouse_path_infix_parts = ('music', 'stylesheets')

    user_external_storehouse_filesystem_path = FileWrangler.configuration.user_stylesheets_directory_path

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'stylesheets'

    @property
    def _temporary_asset_name(self):
        return '__temporary_stylesheet.ly'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            self.edit_asset_interactively(result)

    def _make_main_menu(self):
        menu, section = self._io.make_menu(where=self._where, is_parenthetically_numbered=True)
        tokens = []
        for filesystem_path in self.list_asset_filesystem_paths():
            tokens.append(os.path.basename(filesystem_path))
        section.tokens = tokens
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

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.StylesheetFileProxy

    @property
    def storage_format(self):
        '''Stylesheet file wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.StylesheetFileWrangler()'
    
        Return string.
        '''
        return super(type(self), self).storage_format

    ### PUBLIC METHODS ###

    def edit_asset_interactively(self, asset_basename):
        filesystem_path = os.path.join(self.built_in_stylesheets_directory_path, asset_basename)
        proxy = self.asset_proxy_class(filesystem_path=filesystem_path, session=self._session)
        proxy._run()

    def list_asset_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''Stylesheet file wrangler list asset filesystem paths.
    
        Example. List built-in stylesheet filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_stylesheets/clean_letter_14.ly'
            '.../tools/scoremanagertools/built_in_stylesheets/clean_letter_16.ly'
            '.../tools/scoremanagertools/built_in_stylesheets/rhythm_letter_16.ly'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/stylesheets/red_example_score_stylesheet.ly'

        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_names(self, built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''Stylesheet file wrangler list asset names.
    
        Example. List built-in stylesheet names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     user_external=False, user_score=False):
            ...     x
            'clean letter 14'
            'clean letter 16'
            'rhythm letter 16'
            'red example score stylesheet'

        Return list.
        '''
        return super(type(self), self).list_asset_names(
            built_in_external=built_in_external, 
            user_external=user_external,
            built_in_score=built_in_score, 
            user_score=user_score,
            head=head)

    def list_asset_proxies(self, built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''Stylesheet file wrangler list asset proxies.

        Example. List built-in stylesheet proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     user_external=False, user_score=False):
            ...     x
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_stylesheets/clean_letter_14.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_stylesheets/clean_letter_16.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_stylesheets/rhythm_letter_16.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_scores/red_example_score/music/stylesheets/red_example_score_stylesheet.ly')

        Return list.
        '''
        return super(type(self), self).list_asset_proxies(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_storehouse_filesystem_paths(self, 
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''Stylesheet file wrangler list storehouse filesystem paths.

        Example. List built-in storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_stylesheets'
            '.../tools/scoremanagertools/built_in_scores/blue_example_score/music/stylesheets'
            '.../tools/scoremanagertools/built_in_scores/green_example_score/music/stylesheets'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/stylesheets'

        Return list.
        '''
        return super(type(self), self).list_storehouse_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

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
            self.built_in_stylesheets_directory_path, stylesheet_file_name)
        stylesheet_proxy = scoremanagertools.proxies.StylesheetFileProxy(
            stylesheet_file_name, session=self._session)
        stylesheet_proxy.edit()

    ### USER INPUT MAPPING ###

    user_input_to_action = {
        'new':      make_asset_interactively,
        }
