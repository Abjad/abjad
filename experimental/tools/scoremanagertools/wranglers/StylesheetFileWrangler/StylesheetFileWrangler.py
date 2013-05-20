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

    ### CLASS ATTRIBUTES ###

    storehouse_path_infix_parts = ('music', 'stylesheets')
    built_in_stylesheets_directory_path = os.path.join(
        FileWrangler.configuration.score_manager_tools_directory_path, 'built_in_stylesheets')

    ### INITIALIZER ###

    def __init__(self, session=None):
        FileWrangler.__init__(self,
            built_in_external_storehouse_filesystem_path=\
                self.built_in_stylesheets_directory_path,
            user_external_storehouse_filesystem_path=\
                self.configuration.user_stylesheets_directory_path,
            session=session,
            )

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'stylesheets'

    @property
    def _temporary_asset_name(self):
        return '__temporary_stylesheet.ly'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        from experimental.tools import scoremanagertools
        if result == 'new':
            self.make_asset_interactively()
        else:
            stylesheet_file_name = os.path.join(self.built_in_stylesheets_directory_path, result)
            stylesheet_proxy = scoremanagertools.proxies.StylesheetFileProxy(
                stylesheet_file_name, session=self._session)
            stylesheet_proxy._run()

    def _make_main_menu(self):
        menu, section = self._io.make_menu(where=self._where, is_parenthetically_numbered=True)
        tokens = []
        for filesystem_path in self.list_asset_filesystem_paths(
            built_in_external=True,
            user_external=True,
            built_in_score=True,
            user_score=True):
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
    def built_in_external_storehouse_filesystem_path(self):
        '''Stylesheet file wrangler built-in storehouse directory path:

        ::

            >>> wrangler.built_in_external_storehouse_filesystem_path
            '.../tools/scoremanagertools/built_in_stylesheets'

        Return list.
        '''
        return super(type(self), self).built_in_external_storehouse_filesystem_path

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

    def list_asset_filesystem_paths(self,
        built_in_external=False, user_external=False,
        built_in_score=False, user_score=False, head=None):
        '''Stylesheet file wrangler list asset filesystem paths.
    
        Example. List built-in asset filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     built_in_external=True, built_in_score=True):
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

    def list_asset_proxies(self, built_in_external=False, user_external=False,
        built_in_score=False, user_score=False, head=None):
        '''Stylesheet file wrangler initialize asset proxies.

        Example. Initialize built-in asset proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     built_in_external=True, built_in_score=True):
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
        built_in_external=False, user_external=False,
        built_in_score=False, user_score=False, head=None):
        '''Stylesheet file wrangler list storehouse filesystem paths.

        Example. List built-in storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     built_in_external=True, built_in_score=True):
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

    def list_visible_asset_names(self, head=None):
        '''Stylesheet file wrangler list space-delimited lowercase visible asset names:

        ::

            >>> for x in wrangler.list_visible_asset_names():
            ...     x
            'clean letter 14'
            'clean letter 16'
            'rhythm letter 16'
            ...

        (Output will vary with to user collateral.)

        Return list.
        '''
        return super(type(self), self).list_visible_asset_names(head=head)

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
