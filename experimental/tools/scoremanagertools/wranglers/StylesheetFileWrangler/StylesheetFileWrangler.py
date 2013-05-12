import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.FileWrangler import FileWrangler


class StylesheetFileWrangler(FileWrangler):
    '''Stylesheet file wrangler.

        >>> wrangler = scoremanagertools.wranglers.StylesheetFileWrangler()
        >>> wrangler
        StylesheetFileWrangler('.../tools/scoremanagertools/built_in_stylesheets')

    Return stylesheet file wrangler.
    '''

    ### CLASS ATTRIBUTES ###

    built_in_stylesheets_directory_path = os.path.join(
        FileWrangler.configuration.score_manager_tools_directory_path, 'built_in_stylesheets')
    score_internal_assets_exist = False

    ### INITIALIZER ###

    def __init__(self, session=None):
        FileWrangler.__init__(self,
            built_in_asset_container_directory_paths=[self.built_in_stylesheets_directory_path],
            user_asset_container_directory_paths=[self.configuration.user_stylesheets_directory_path],
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
        tokens = [os.path.basename(x) for x in self.list_visible_asset_filesystem_paths()]
        section.tokens = tokens
        section = menu.make_section()
        section.append(('new', 'new stylesheet'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_container_proxy_class(self):
        '''Stylesheet file wrangler asset container proxy class:

        ::

            >>> wrangler.asset_container_proxy_class.__name__
            'DirectoryProxy'

        Return class.
        '''
        return super(type(self), self).asset_container_proxy_class
        
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
    def built_in_asset_container_directory_paths(self):
        '''Stylesheet file wrangler built-in asset container directory paths:

        ::

            >>> wrangler.built_in_asset_container_directory_paths
            ['.../tools/scoremanagertools/built_in_stylesheets']

        Return list.
        '''
        return super(type(self), self).built_in_asset_container_directory_paths

    @property
    def current_asset_container_directory_path(self):
        '''Stylesheet file wrangler current asset container directory path:

        ::

            >>> wrangler.current_asset_container_directory_path
            '.../tools/scoremanagertools/built_in_stylesheets'

        Return string.
        '''
        return super(type(self), self).current_asset_container_directory_path

    @property
    def storage_format(self):
        '''Stylesheet file wrangler storage format:

        ::

            >>> z(wrangler)
            wranglers.StylesheetFileWrangler()
    
        Return string.
        '''
        return super(type(self), self).storage_format

    @property
    def user_asset_container_directory_paths(self):
        '''Stylesheet file wrangler built-in asset container directory paths:

        ::

            >>> wrangler.user_asset_container_directory_paths
            ['.../score_manager/stylesheets']

        (Output will vary according to configuration.)

        Return list.
        '''
        return super(type(self), self).user_asset_container_directory_paths

    ### PUBLIC METHODS ###

    def get_asset_container_proxies(self, head=None):
        '''Stylesheet file wrangler get asset container proxies:

        ::

            >>> for x in wrangler.get_asset_container_proxies():
            ...     x
            DirectoryProxy('.../tools/scoremanagertools/built_in_stylesheets')
            DirectoryProxy('.../score_manager/stylesheets')

        Return list.
        '''
        return super(type(self), self).get_asset_container_proxies(head=head)

    def get_asset_proxies(self, head=None):
        '''Stylesheet file wrangler get asset proxies:

        ::

            >>> for x in wrangler.get_asset_proxies():
            ...     x
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_stylesheets/clean_letter_14.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_stylesheets/clean_letter_16.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/built_in_stylesheets/rhythm_letter_16.ly')
            StylesheetFileProxy('.../score_manager/stylesheets/baca_letter_14.ly')

        Return list.
        '''
        return super(type(self), self).get_asset_proxies(head=head)

    def get_score_external_asset_container_proxies(self, head=None):
        '''Stylesheet file wrangler get score-external asset container proxies:

        ::

            >>> for x in wrangler.get_score_external_asset_container_proxies():
            ...     x
            DirectoryProxy('.../tools/scoremanagertools/built_in_stylesheets')
            DirectoryProxy('.../score_manager/stylesheets')

        Return list.
        '''
        return super(type(self), self).get_score_external_asset_container_proxies(head=head)

    def list_asset_container_directory_paths(self, head=None):
        '''Stylesheet file wrangler list asset container directory paths:

        ::

            >>> for x in wrangler.list_asset_container_directory_paths():
            ...     x
            '.../tools/scoremanagertools/built_in_stylesheets'
            '.../score_manager/stylesheets'

        Return list.
        '''
        return super(type(self), self).list_asset_container_directory_paths(head=head)

    def list_asset_filesystem_paths(self, head=None):
        '''Stylesheet file wrangler list asset filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths():
            ...     x
            '.../tools/scoremanagertools/built_in_stylesheets/clean_letter_14.ly'
            '.../tools/scoremanagertools/built_in_stylesheets/clean_letter_16.ly'
            '.../tools/scoremanagertools/built_in_stylesheets/rhythm_letter_16.ly'
            '.../score_manager/stylesheets/baca_letter_14.ly'

        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(head=head)
        
    def list_score_external_asset_container_directory_paths(self, head=None):
        '''Stylesheet file wrangler list score-external asset container directory paths:

        ::

            >>> for x in wrangler.list_score_external_asset_container_directory_paths():
            ...     x
            '.../tools/scoremanagertools/built_in_stylesheets'
            '.../score_manager/stylesheets'

        Return list.
        '''
        return super(type(self), self).list_score_external_asset_container_directory_paths(head=head)

    def list_score_internal_asset_container_directory_paths(self, head=None):
        '''Stylesheet file wrangler list score-internal asset container directory paths:

        ::

            >>> wrangler.list_score_internal_asset_container_directory_paths()
            []

        Return list.
        '''
        return super(type(self), self).list_score_internal_asset_container_directory_paths(head=head)

    def get_score_internal_asset_container_proxies(self, head=None):
        '''Stylesheet file wrangler get score-internal asset container proxies:

        ::

            >>> wrangler.get_score_internal_asset_container_proxies()
            []

        Return list.
        '''
        return super(type(self), self).get_score_internal_asset_container_proxies(head=head)
        
    def list_user_asset_container_directory_paths(self, head=None):
        '''Stylesheet file wrangler list user asset container directory paths:

        ::

            >>> wrangler.list_user_asset_container_directory_paths()
            ['.../score_manager/stylesheets']

        (Output will vary according to configuration.)

        Return list.
        '''
        return super(type(self), self).list_user_asset_container_directory_paths(head=head) 

    def list_visible_asset_filesystem_paths(self, head=None):
        '''Stylesheet file wrangler list visible asset filesystem paths:

        ::

            >>> for x in wrangler.list_visible_asset_filesystem_paths():
            ...     x
            '.../tools/scoremanagertools/built_in_stylesheets/clean_letter_14.ly'
            '.../tools/scoremanagertools/built_in_stylesheets/clean_letter_16.ly'
            '.../tools/scoremanagertools/built_in_stylesheets/rhythm_letter_16.ly'
            '.../score_manager/stylesheets/baca_letter_14.ly'

        Return list.
        '''
        return super(type(self), self).list_visible_asset_filesystem_paths(head=head)

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

    # TODO: rename to something general without 'stylesheet' in name
    # TODO: write test
    def select_stylesheet_file_name_interactively(self, clear=True, cache=False):
        self._session.cache_breadcrumbs(cache=cache)
        menu, section = self._io.make_menu(where=self._where, is_parenthetically_numbered=True)
        tokens = [os.path.basename(x) for x in self.list_visible_asset_filesystem_paths()]
        section.tokens = tokens
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
        if result is not None:
            result = os.path.join(self.built_in_stylesheets_directory_path, result)
            return result
