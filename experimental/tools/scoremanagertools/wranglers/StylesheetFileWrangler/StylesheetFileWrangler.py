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
        FileWrangler.configuration.score_manager_tools_directory_path, 'stylesheets')

    storehouse_path_infix_parts = ('music', 'stylesheets')

    user_external_storehouse_filesystem_path = FileWrangler.configuration.user_external_stylesheets_directory_path

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
            self.edit_asset(result)

    def _make_menu_tokens(self, head=None, include_extension=False):
        keys = self.list_asset_filesystem_paths(head=head)
        bodies = []
        for filesystem_path in keys:
            body = os.path.basename(filesystem_path)
            annotation = self._filesystem_path_to_annotation(filesystem_path)
            if annotation:
                body = '{} ({})'.format(body, annotation)
            bodies.append(body)
        return zip(keys, bodies)

    def _filesystem_path_to_annotation(self, filesystem_path):
        from experimental.tools import scoremanagertools
        annotation = None
        if filesystem_path.startswith(self.configuration.built_in_score_packages_directory_path) or \
            filesystem_path.startswith(self.configuration.user_score_packages_directory_path):
            tmp = os.path.join('music', 'stylesheets')
            score_filesystem_path = filesystem_path.rpartition(tmp)[0]
            packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(score_filesystem_path)
            score_package_proxy = scoremanagertools.proxies.ScorePackageProxy( 
                packagesystem_path=packagesystem_path)
            annotation = score_package_proxy.title
        elif filesystem_path.startswith(self.configuration.built_in_stylesheets_directory_path):
            annotation = 'built-in'
        return annotation

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(
            where=self._where, is_parenthetically_numbered=True, is_keyed=False)
        section.tokens = self._make_menu_tokens(include_extension=True)
        section = menu.make_section()
        section.append(('new', 'new'))
        section.append(('cp', 'copy'))
        section.append(('ren', 'rename'))
        section.append(('rm', 'remove'))
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
        return super(StylesheetFileWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def edit_asset(self, asset_basename):
        # TODO: this will break with user assets; built-in directory path should not be hardcoded here
        filesystem_path = os.path.join(
            self.configuration.built_in_stylesheets_directory_path, asset_basename)
        proxy = self.asset_proxy_class(filesystem_path=filesystem_path, session=self._session)
        proxy.edit()

    def list_asset_filesystem_paths(self,
        in_built_in_library=True, in_user_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''Stylesheet file wrangler list asset filesystem paths.
    
        Example. List built-in stylesheet filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_library=False, in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/stylesheets/clean-letter-14.ly'
            '.../tools/scoremanagertools/stylesheets/clean-letter-16.ly'
            '.../tools/scoremanagertools/stylesheets/rhythm-letter-16.ly'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/stylesheets/red-example-score-stylesheet.ly'

        Return list.
        '''
        return super(StylesheetFileWrangler, self).list_asset_filesystem_paths(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_names(self, in_built_in_library=True, in_user_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None, include_extension=False):
        '''Stylesheet file wrangler list asset names.
    
        Example. List built-in stylesheet names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_library=False, in_user_score_packages=False, include_extension=True):
            ...     x
            'clean-letter-14.ly'
            'clean-letter-16.ly'
            'rhythm-letter-16.ly'
            'red-example-score-stylesheet.ly'

        Return list.
        '''
        return super(StylesheetFileWrangler, self).list_asset_names(
            in_built_in_library=in_built_in_library, 
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages, 
            in_user_score_packages=in_user_score_packages,
            head=head,
            include_extension=include_extension)

    def list_asset_proxies(self, in_built_in_library=True, in_user_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''Stylesheet file wrangler list asset proxies.

        Example. List built-in stylesheet proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_library=False, in_user_score_packages=False):
            ...     x
            StylesheetFileProxy('.../tools/scoremanagertools/stylesheets/clean-letter-14.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/stylesheets/clean-letter-16.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/stylesheets/rhythm-letter-16.ly')
            StylesheetFileProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/stylesheets/red-example-score-stylesheet.ly')

        Return list.
        '''
        return super(StylesheetFileWrangler, self).list_asset_proxies(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_storehouse_filesystem_paths(self, 
        in_built_in_library=True, in_user_library=True,
        in_built_in_score_packages=True, in_user_score_packages=True, head=None):
        '''Stylesheet file wrangler list storehouse filesystem paths.

        Example. List built-in storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     in_user_library=False, in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/stylesheets'
            '.../tools/scoremanagertools/scorepackages/blue_example_score/music/stylesheets'
            '.../tools/scoremanagertools/scorepackages/green_example_score/music/stylesheets'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/stylesheets'

        Return list.
        '''
        return super(StylesheetFileWrangler, self).list_storehouse_filesystem_paths(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def make_asset_interactively(self):
        from experimental.tools import scoremanagertools

        with self.backtracking:
            storehouse_path = self.select_user_storehouse_filesystem_path_interactively()
        if self._session.backtrack():
            return

        getter = self._io.make_getter(where=self._where)
        getter.append_string('stylesheet name')
        stylesheet_file_name = getter._run()
        if self._session.backtrack():
            return

        stylesheet_file_name = stringtools.string_to_accent_free_underscored_delimited_lowercase(
            stylesheet_file_name)

        if not stylesheet_file_name.endswith('.ly'):
            stylesheet_file_name = stylesheet_file_name + '.ly'

        stylesheet_file_path = os.path.join(
            storehouse_path,
            stylesheet_file_name,
            )

        proxy = scoremanagertools.proxies.StylesheetFileProxy(
            stylesheet_file_path, session=self._session)

        if self._session.is_test:
            proxy.make_empty_asset()
        else:
            proxy.edit()

    ### UI MANIFEST ###

    user_input_to_action = FileWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'new': make_asset_interactively,
        })
