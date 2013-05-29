from experimental.tools.scoremanagertools.wranglers.ModuleWrangler import ModuleWrangler


class MusicSpecifierModuleWrangler(ModuleWrangler):
    '''Music specifier module wrangler.

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.music_specifier_module_wrangler
        >>> wrangler
        MusicSpecifierModuleWrangler()

    Return music specifier module wrangler.
    '''

    ### CLASS VARIABLES ###

    built_in_external_storehouse_packagesystem_path = \
        ModuleWrangler.configuration.built_in_specifiers_package_path

    storehouse_path_infix_parts = ('music', 'specifiers')

    user_external_storehouse_packagesystem_path = \
        ModuleWrangler.configuration.user_external_specifiers_directory_path

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'music specifiers'

    @property
    def _temporary_asset_name(self):
        return '__temporary_specifier_module.py'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            package_proxy = self._initialize_asset_proxy(result)
            package_proxy.edit()

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(
            where=self._where, is_keyed=False, is_parenthetically_numbered=True)
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
        '''Music specifier module wrangler proxy class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'MusicSpecifierModuleProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.MusicSpecifierModuleProxy

    @property
    def storage_format(self):
        '''Music specifier module wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.MusicSpecifierModuleWrangler()'

        Return string.
        '''
        return super(MusicSpecifierModuleWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def list_asset_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset filesystem paths.

        Example. List built-in music specifier module filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_specifiers/black_music.py'
            '.../tools/scoremanagertools/built_in_specifiers/green_music.py'

        Return list.
        '''
        return super(MusicSpecifierModuleWrangler, self).list_asset_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_names(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset names.

        Example. List built-in music specifier module names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     user_external=False, user_score=False):
            ...     x
            'black music'
            'green music'

        Return list.
        '''
        return super(MusicSpecifierModuleWrangler, self).list_asset_names(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_packagesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset packagesystem paths.

        Example. List built-in music specifier module paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            'experimental.tools.scoremanagertools.built_in_specifiers.black_music'
            'experimental.tools.scoremanagertools.built_in_specifiers.green_music'

        Return list.
        '''
        return super(MusicSpecifierModuleWrangler, self).list_asset_packagesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_proxies(self, 
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset proxies.

        Example. List built-in music specifier module proxies:
            
        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     user_external=False, user_score=False):
            ...     x
            MusicSpecifierModuleProxy('.../tools/scoremanagertools/built_in_specifiers/black_music.py')
            MusicSpecifierModuleProxy('.../tools/scoremanagertools/built_in_specifiers/green_music.py')

        Return list.
        '''
        return super(MusicSpecifierModuleWrangler, self).list_asset_proxies(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_storehouse_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List storehouse filesystem paths.

        Example. List built-in music specifier module storehouses:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_specifiers'
            '.../tools/scoremanagertools/built_in_scores/blue_example_score/music/specifiers'
            '.../tools/scoremanagertools/built_in_scores/green_example_score/music/specifiers'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/specifiers'

        Return list.
        '''
        return super(MusicSpecifierModuleWrangler, self).list_storehouse_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

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

    ### UI MANIFEST ###

    user_input_to_action = ModuleWrangler.user_input_to_action.copy()
    user_input_to_action.update({ 
        'new': make_asset_interactively,
        })
