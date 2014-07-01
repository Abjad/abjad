# -*- encoding: utf-8 -*-
from scoremanager.idetools.AssetController import AssetController


class ScoreInternalAssetController(AssetController):
    r'''Score-internal asset controller.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(ScoreInternalAssetController, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            '<<': self.go_to_previous_score,
            '>>': self.go_to_next_score,
            #
            'd': self.go_to_score_distribution_files,
            'g': self.go_to_score_segments,
            'k': self.go_to_score_maker_files,
            'm': self.go_to_score_materials,
            'u': self.go_to_score_build_files,
            'y': self.go_to_score_stylesheets,
            #
            'sse': self.edit_score_stylesheet,
            })
        return result

    @property
    def _navigation_commands(self):
        superclass = super(ScoreInternalAssetController, self)
        result = superclass._navigation_commands
        result = result + (
            'd', 'g', 'k', 'm', 's', 'u', 'y',
            )

    ### PUBLIC METHODS ###

    def edit_score_stylesheet(self):
        r'''Edits score stylesheet.

        Returns none.
        '''
        path = self._session.current_stylesheet_path
        if path:
            self._io_manager.edit(path)
        else:
            message = 'no file ending in *stylesheet.ily found.'
            self._io_manager._display(message)

    def go_to_next_score(self):
        r'''Goes to next score.

        Returns none.
        '''
        self._session._is_navigating_to_next_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_available_commands = False

    def go_to_previous_score(self):
        r'''Goes to previous score.

        Returns none.
        '''
        self._session._is_navigating_to_previous_score = True
        self._session._is_navigating_to_scores = True
        self._session._display_available_commands = False

    def go_to_score_build_files(self):
        r'''Goes to build files.

        Returns none.
        '''
        self._session._ide._build_file_wrangler._run()

    def go_to_score_distribution_files(self):
        r'''Goes to distribution files.

        Returns none.
        '''
        self._session._ide._distribution_file_wrangler._run()

    def go_to_score_maker_files(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._ide._maker_file_wrangler._run()

    def go_to_score_materials(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._ide._material_package_wrangler._run()

    def go_to_score_segments(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._ide._segment_package_wrangler._run()

    def go_to_score_stylesheets(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._ide._stylesheet_wrangler._run()