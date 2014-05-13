from scoremanager.core.Controller import Controller


class AssetController(Controller):
    r'''Asset controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superclass = super(AssetController, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _make_go_wranglers_menu_section(self, menu):
        commands = []
        commands.append(('go - build', 'u'))
        commands.append(('go - distribution', 'd'))
        commands.append(('go - makers', 'k'))
        commands.append(('go - materials', 'm'))
        commands.append(('go - segments', 'g'))
        commands.append(('go - stylesheets', 'y'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='go - wranglers',
            )

    ### PUBLIC METHODS ###

    def go_to_build_files(self):
        r'''Goes to build files.

        Returns none.
        '''
        self._session._score_manager._build_file_wrangler._run()

    def go_to_distribution_files(self):
        r'''Goes to distribution files.

        Returns none.
        '''
        self._session._score_manager._distribution_file_wrangler._run()

    def go_to_maker_files(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._score_manager._maker_file_wrangler._run()

    def go_to_material_packages(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._score_manager._material_package_wrangler._run()

    def go_to_segment_packages(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._score_manager._segment_package_wrangler._run()

    def go_to_stylesheets(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._score_manager._stylesheet_wrangler._run()