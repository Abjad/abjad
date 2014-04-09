# -*- encoding: utf-8 -*-
import os
from abjad.tools import abctools
from abjad.tools import stringtools


class Session(abctools.AbjadObject):
    r'''Score manager session.

    ..  container:: example

        Session outside of score:

        ::

            >>> session = scoremanager.core.Session()
            >>> session
            Session()

    ..  container:: example

        Session in score:

        ::

            >>> session_in_score = scoremanager.core.Session()
            >>> session_in_score._set_test_score('red_example_score')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attempted_to_add_to_repository',
        '_attempted_to_commit_to_repository',
        '_attempted_to_open_file',
        '_attempted_to_revert_to_repository',
        '_attempted_to_update_from_repository',
        '_command_history',
        '_configuration',
        '_controller_stack',
        '_controllers_visited',
        '_display_pitch_ranges_with_numbered_pitches',
        '_hide_hidden_commands',
        '_hide_next_redraw',
        '_initial_user_input',
        '_io_manager',
        '_is_autoadding',
        '_is_backtracking_locally',
        '_is_backtracking_to_score',
        '_is_backtracking_to_score_manager',
        '_is_in_confirmation_environment',
        '_is_in_score_setup_menu',
        '_is_in_user_input_getter',
        '_is_navigating_to_score_build_files',
        '_is_navigating_to_score_distribution_files',
        '_is_navigating_to_next_asset',
        '_is_navigating_to_next_score',
        '_is_navigating_to_previous_asset',
        '_is_navigating_to_previous_score',
        '_is_navigating_to_score_maker_modules',
        '_is_navigating_to_score_materials',
        '_is_navigating_to_score_segments',
        '_is_navigating_to_score_setup',
        '_is_navigating_to_score_stylesheets',
        '_is_quitting',
        '_is_repository_test',
        '_is_test',
        '_is_tracking_source_code',
        '_last_command_was_composite',
        '_last_asset_path',
        '_menu_header_width',
        '_pending_user_input',
        '_proceed_count',
        '_rewrite_cache',
        '_score_manager',
        '_scores_to_display',
        '_transcript',
        '_use_current_user_input_values_as_default',
        )

    _variables_to_display = (
        'command_history',
        'controller_stack',
        'current_score_package_manager',
        'hide_next_redraw',
        'hide_hidden_commands',
        'is_autoadding',
        'is_in_confirmation_environment',
        'is_in_editor',
        'is_in_user_input_getter',
        'last_asset_path',
        'scores_to_display',
        )

    ### INITIALIZER ###

    def __init__(self, pending_user_input=None, is_test=False):
        from scoremanager import core
        from scoremanager import iotools
        self._attempted_to_add_to_repository = False
        self._attempted_to_commit_to_repository = False
        self._attempted_to_open_file = False
        self._attempted_to_revert_to_repository = False
        self._attempted_to_update_from_repository = False
        self._command_history = []
        self._configuration = core.ScoreManagerConfiguration()
        self._controller_stack = []
        self._controllers_visited = []
        self._display_pitch_ranges_with_numbered_pitches = False
        self._hide_hidden_commands = True
        self._hide_next_redraw = False
        self._initial_user_input = pending_user_input
        self._io_manager = iotools.IOManager(self)
        self._is_repository_test = False
        self._is_autoadding = False
        self._is_backtracking_locally = False
        self._is_backtracking_to_score = False
        self._is_backtracking_to_score_manager = False
        self._is_in_confirmation_environment = False
        self._is_in_score_setup_menu = False
        self._is_navigating_to_score_build_files = False
        self._is_navigating_to_score_distribution_files = False
        self._is_navigating_to_next_asset = False
        self._is_navigating_to_next_score = False
        self._is_navigating_to_previous_asset = False
        self._is_navigating_to_previous_score = False
        self._is_navigating_to_score_maker_modules = False
        self._is_navigating_to_score_materials = False
        self._is_navigating_to_score_segments = False
        self._is_navigating_to_score_setup = False
        self._is_navigating_to_score_stylesheets = False
        self._is_quitting = False
        self._is_test = is_test
        self._is_tracking_source_code = None
        self._last_command_was_composite = False
        self._last_asset_path = None
        self._menu_header_width = 160
        self._pending_user_input = pending_user_input
        self._proceed_count = 0
        self._rewrite_cache = False
        self._score_manager = None
        if is_test:
            self._scores_to_display = 'example'
        else:
            self._scores_to_display = 'active'
        self._transcript = iotools.Transcript()
        self._use_current_user_input_values_as_default = False

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of session.

        ..  container:: example

            ::

                >>> session
                Session()

        Returns string.
        '''
        summary = []
        if self.initial_user_input is not None:
            string = 'initial_pending_user_input={!r}'
            string = string.format(self.initial_user_input)
            summary.append(string)
        if self.pending_user_input not in (None, ''):
            string = 'pending_user_input={!r}'
            string = string.format(self.pending_user_input)
            summary.append(string)
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    ### PRIVATE METHODS ###

    def _clean_up(self):
        if self.is_test:
            return
        transcripts_directory = self._configuration.transcripts_directory_path
        transcripts = os.listdir(transcripts_directory)
        count = len(transcripts)
        if 9000 <= count:
            messages = []
            message = 'transcripts directory contains {} transcripts.'
            message = message.format(count)
            messages.append(message)
            message = 'prune directory soon.'
            messages.append(message)
            self.io_manager.display(messages)
        self.transcript._write()

    def _format_controller_breadcrumbs(self):
        if not self.controller_stack:
            return ['']
        result_lines = []
        first_controller = self.controller_stack[0]
        breadcrumb = getattr(first_controller, 'breadcrumb', None)
        breadcrumb = breadcrumb or first_controller._breadcrumb
        #breadcrumb = self.controller_stack[0]._breadcrumb
        if breadcrumb:
            result_lines.append(breadcrumb)
        hanging_indent_width = 5
        for controller in self.controller_stack[1:]:
            breadcrumb = getattr(controller, 'breadcrumb', None)
            breadcrumb = breadcrumb or controller._breadcrumb
            if not breadcrumb:
                continue
            if result_lines:
                candidate_line = result_lines[-1] + ' - ' + breadcrumb
            else:
                candidate_line = breadcrumb
            if len(candidate_line) <= self.menu_header_width:
                if result_lines:
                    result_lines[-1] = candidate_line
                else:
                    result_lines.append(candidate_line)
            else:
                result_line = hanging_indent_width * ' ' + breadcrumb
                result_lines.append(result_line)
        return result_lines

    def _print_transcript(
        self,
        include_user_input=True,
        include_system_display=True,
        ):
        for entry in self.transcript:
            if entry.is_user_input and include_user_input:
                print entry
            elif entry.is_system_display and include_system_display:
                print entry

    def _print_transcript_titles(self):
        for title in self.transcript.titles:
            print repr(title)

    def _reinitialize(self):
        is_test = self._is_test
        is_add_to_repository_test = self._is_repository_test
        type(self).__init__(self, is_test=self.is_test)
        self._is_repository_test = is_add_to_repository_test

    def _set_test_score(self, score_package_name):
        from scoremanager import managers
        assert not self.controller_stack
        path = os.path.join(
            self._configuration.abjad_score_packages_directory_path,
            score_package_name,
            )
        assert os.path.exists(path)
        manager = managers.ScorePackageManager(
            path=path,
            session=self,
            )
        self._controller_stack.append(manager)

    ### PUBLIC PROPERTIES ###

    @property
    def command_history(self):
        r'''Gets session command history.

        ..  container:: example

            ::

                >>> session.command_history
                []

        Returns list.
        '''
        return self._command_history

    @property
    def command_history_string(self):
        r'''Gets session command history string.

        ..  container:: example

            ::

                >>> session.command_history_string
                ''

        Returns string.
        '''
        return ' '.join(self.explicit_command_history)

    @property
    def controller_stack(self):
        r'''Gets session controller stack.

        ..  container:: example

            ::

                >>> session.controller_stack
                []

        Returns list of objects all of which are either wranglers or managers.
        '''
        return self._controller_stack

    @property
    def controllers_visited(self):
        r'''Gets controllers visited during session.

        ..  container:: example

            ::

                >>> session.controllers_visited
                []

        Returs list.
        '''
        return self._controllers_visited

    @property
    def current_controller(self):
        r'''Gets current controller of session.

        ..  container:: example

            ::

                >>> session.current_controller is None
                True

        Returns wrangler or manager.
        '''
        if self.controller_stack:
            return self.controller_stack[-1]

    @property
    def current_materials_directory_path(self):
        r'''Gets session current materials directory path.

        ..  container:: example

            Materials directory path of session outside score:

            ::

                >>> session.current_materials_directory_path
                '.../scoremanager/materials'

        ..  container:: example

            Materials directory path of session in score:

            ::

                >>> session_in_score.current_materials_directory_path
                '.../red_example_score/materials'

        Returns string.
        '''
        if self.current_score_directory_path:
            return os.path.join(self.current_score_directory_path, 'materials')
        else:
            return self._configuration.abjad_material_packages_directory_path

    @property
    def current_score_directory_path(self):
        r'''Gets session current score directory path.

        ..  container:: example

            ::

                >>> session.current_score_directory_path is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_directory_path
                '.../red_example_score'

        Returns string or none.
        '''
        if self.current_score_package_manager:
            return self.current_score_package_manager._path

    @property
    def current_score_package_manager(self):
        r'''Gets session current score package manager.

        ..  container:: example:

            ::

                >>> session.current_score_package_manager is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_package_manager
                ScorePackageManager('.../red_example_score')

        (Ouput will vary according to configuration.)

        Returns score package manager or none.
        '''
        from scoremanager import managers
        for controller in reversed(self.controller_stack):
            if isinstance(controller, managers.ScorePackageManager):
                return controller

    @property
    def current_segments_directory_path(self):
        r'''Gets session current segments directory path.

        ..  container:: example

            ::

                >>> session.current_segments_directory_path is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_segments_directory_path
                '.../red_example_score/segments'

        Returns string.
        '''
        if self.current_score_directory_path:
            return os.path.join(self.current_score_directory_path, 'segments')

    @property
    def display_pitch_ranges_with_numbered_pitches(self):
        r'''Is true when session should display pitch ranges with numbered
        pitches. Otherwise false.

        ..  container:: example

            ::

                >>> session.display_pitch_ranges_with_numbered_pitches
                False

        Returns boolean.
        '''
        return self._display_pitch_ranges_with_numbered_pitches

    @property
    def explicit_command_history(self):
        r'''Gets session explicit command history.

        ..  container:: example

            ::

                >>> session.explicit_command_history
                []

        Returns list.
        '''
        result = []
        for command in self.command_history:
            if command == '':
                result.append('default')
            else:
                result.append(command)
        return result

    @property
    def hide_hidden_commands(self):
        r'''Is true when hidden commands are hidden. Otherwise false.

        ..  container:: example

            ::

                >>> session.hide_hidden_commands
                True

        Returns boolean.
        '''
        return self._hide_hidden_commands

    @property
    def hide_next_redraw(self):
        r'''Gets and sets flag to hide next redraw.

        ..  container:: example

            ::

                >>> session.hide_next_redraw
                False

        Returns boolean.
        '''
        return self._hide_next_redraw

    @property
    def initial_user_input(self):
        r'''Gets session initial user input.

        ..  container:: example

            ::

                >>> session.initial_user_input is None
                True

        Returns string or none.
        '''
        return self._initial_user_input

    @property
    def io_manager(self):
        r'''Gets session IO manager.

        ..  container:: example

            ::

                >>> session.io_manager
                IOManager()

        Returns IO manager.
        '''
        return self._io_manager

    @property
    def is_autoadding(self):
        r'''Is true when session is autoadding. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_autoadding
                False

        Returns boolean.
        '''
        from scoremanager import iotools
        for controller in reversed(self.controller_stack):
            if isinstance(controller, iotools.Editor):
                return controller.is_autoadding
        return False

    @property
    def is_autonavigating_within_score(self):
        r'''Is true when session is autonavigating. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_autonavigating_within_score
                False

        Returns boolean.
        '''
        if self.is_navigating_to_score_build_files:
            return True
        elif self.is_navigating_to_score_distribution_files:
            return True
        elif self.is_navigating_to_score_maker_modules:
            return True
        elif self.is_navigating_to_score_materials:
            return True
        elif self.is_navigating_to_score_segments:
            return True
        elif self.is_navigating_to_score_setup:
            return True
        elif self.is_navigating_to_score_stylesheets:
            return True
        else:
            return False

    @property
    def is_backtracking_locally(self):
        r'''Is true when session is backtracking locally.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_backtracking_locally
                False

        Returns boolean.
        '''
        return self._is_backtracking_locally

    @property
    def is_backtracking_to_score(self):
        r'''Is true when session is backtracking to score.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_backtracking_to_score
                False

        Returns boolean.
        '''
        return self._is_backtracking_to_score

    @property
    def is_backtracking_to_score_manager(self):
        r'''Is true when session is backtracking to score manager.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_backtracking_to_score_manager
                False

        Returns boolean.
        '''
        return self._is_backtracking_to_score_manager

    @property
    def is_complete(self):
        r'''Is true when session is complete. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_complete
                False

        Returns boolean.
        '''
        return self.is_quitting

    @property
    def is_in_confirmation_environment(self):
        r'''Is true when session is in confirmation environment.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_confirmation_environment
                False

        Returns boolean.
        '''
        return self._is_in_confirmation_environment

    @property
    def is_in_editor(self):
        r'''Is true when session is in editor. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_editor
                False

        Returns boolean.
        '''
        from scoremanager import iotools
        for controller in reversed(self.controller_stack):
            if isinstance(controller, iotools.Editor):
                return True
        return False

    @property
    def is_in_score(self):
        r'''Is true when session is in score. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_score
                False

        Returns boolean.
        '''
        if self.current_score_package_manager is not None:
            return True
        return False

    @property
    def is_in_score_setup_menu(self):
        r'''Is true when session in score setup menu. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_score_setup_menu
                False

        Returns boolean.
        '''
        return self._is_in_score_setup_menu

    @property
    def is_in_user_input_getter(self):
        r'''Is true when session is in user input getter. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_user_input_getter
                False

        Returns boolean.
        '''
        from scoremanager import iotools
        for controller in reversed(self.controller_stack):
            if isinstance(controller, iotools.UserInputGetter):
                return True
        return False

    @property
    def is_navigating_to_next_asset(self):
        r'''Is true when session is navigating to next material.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_asset
                False

        Returns boolean.
        '''
        return self._is_navigating_to_next_asset

    @property
    def is_navigating_to_next_score(self):
        r'''Is true when session is navigating to next score. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_score
                False

        Returns boolean.
        '''
        return self._is_navigating_to_next_score

    @property
    def is_navigating_to_previous_asset(self):
        r'''Is true when session is navigating to previous material.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_previous_asset
                False

        Returns boolean.
        '''
        return self._is_navigating_to_previous_asset

    @property
    def is_navigating_to_previous_score(self):
        r'''Is true when session is navigating to previous score.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_previous_score
                False

        Returns boolean.
        '''
        return self._is_navigating_to_previous_score

    @property
    def is_navigating_to_score_build_files(self):
        r'''Is true when session is navigating to build directory.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_build_files
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_build_files

    @property
    def is_navigating_to_score_distribution_files(self):
        r'''Is true when session is navigating to distribution directory.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_distribution_files
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_distribution_files

    @property
    def is_navigating_to_score_maker_modules(self):
        r'''Is true when session is navigating to score makers.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_maker_modules
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_maker_modules

    @property
    def is_navigating_to_score_materials(self):
        r'''Is true when session is navigating to score materials.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_materials
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_materials

    @property
    def is_navigating_to_score_segments(self):
        r'''Is true when session is navigating to score segments.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_segments
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_segments

    @property
    def is_navigating_to_score_setup(self):
        r'''Is true when session is navigating to score setup.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_setup
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_setup

    @property
    def is_navigating_to_score_stylesheets(self):
        r'''Is true when session is navigating to score stylesheets.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_score_stylesheets
                False

        Returns boolean.
        '''
        return self._is_navigating_to_score_stylesheets

    @property
    def is_navigating_to_sibling_asset(self):
        r'''Is true when session is navigating to sibling asset.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_navigating_to_sibling_asset
                False

        Returns boolean.
        '''
        if self.is_navigating_to_next_asset:
            return True
        if self.is_navigating_to_previous_asset:
            return True
        return False

    @property
    def is_navigating_to_sibling_score(self):
        r'''Is true when session is navigating to sibling score.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.is_navigating_to_sibling_score
                False

        Returns boolean.
        '''
        if self.is_navigating_to_next_score:
            return True
        if self.is_navigating_to_previous_score:
            return True
        return False

    @property
    def is_quitting(self):
        r'''Gets and sets flag that user specified quit.

        ..  container:: example

            ::

                >>> session.is_quitting
                False

        Returns boolean.
        '''
        return self._is_quitting

    @property
    def is_repository_test(self):
        r'''Is true when session is repository test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_repository_test
                False

        Returns boolean.
        '''
        return self._is_repository_test

    @property
    def is_test(self):
        r'''Is true when session is test. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_test
                False

        Returns boolean.
        '''
        return self._is_test

    @property
    def is_tracking_source_code(self):
        r'''Is true when session should enable source code tracking. Otherwise
        false.

        ..  container:: example

            ::

                >>> session.is_tracking_source_code
                True

        Returns boolean.
        '''
        if self._is_tracking_source_code is not None:
            return self._is_tracking_source_code
        if self.is_test:
            return False
        else:
            return True

    @property
    def last_asset_path(self):
        r'''Gets last material package path.

        Set on package manager entry and persists
        after package manager exit.

        ..  container:: example

            ::

                >>> session.last_asset_path is None
                True

        Returns string or none.
        '''
        return self._last_asset_path

    @property
    def last_command_was_composite(self):
        r'''Is true when last command was composite. Otherwise false.

        ..  container:: example

            ::

                >>> session.last_command_was_composite
                False

        Returns boolean.
        '''
        return self._last_command_was_composite

    @property
    def last_semantic_command(self):
        r'''Gets session last semantic command.

        ..  container:: example

            ::

                >>> session.last_semantic_command is None
                True

        Returns string or none.
        '''
        for command in reversed(self.command_history):
            if not command.startswith('.'):
                return command

    @property
    def menu_header(self):
        r'''Gets session menu header.

        ..  container:: example

            ::

                >>> session.menu_header
                ''

        Returns string.
        '''
        return '\n'.join(self._format_controller_breadcrumbs())

    @property
    def menu_header_width(self):
        r'''Gets session menu header width.

        ..  container:: example

            ::

                >>> session.menu_header_width
                160

        Returns nonnegative integer.
        '''
        return self._menu_header_width

    @property
    def pending_user_input(self):
        r'''Gets and sets pending user input.

        ..  container:: example

            ::

                >>> session.pending_user_input is None
                True

        Returns string.
        '''
        return self._pending_user_input

    @property
    def proceed_count(self):
        r'''Gets the number of times IOManager.proceed()
        has been called in session.

        ..  container:: example

            ::

                >>> session.proceed_count
                0

        Returns nonnegative integer.
        '''
        return self._proceed_count

    @property
    def rewrite_cache(self):
        r'''Gets and sets flag to rewrite cache.

        ..  container:: example

            ::

                >>> session.rewrite_cache
                False

        Returns boolean.
        '''
        return self._rewrite_cache

    @property
    def score_manager(self):
        r'''Gets session score manager.

        ..  container:: example

            ::

                >>> session.score_manager

        Returns score manager or none.
        '''
        return self._score_manager

    @property
    def scores_to_display(self):
        r'''Gets session scores to show.

        ..  container:: example

            ::

                >>> session.scores_to_display
                'active'

        Returns string.
        '''
        return self._scores_to_display

    @property
    def testable_command_history_string(self):
        r'''Gets session testable command history string.

        ..  container:: example

            ::

                >>> session.testable_command_history_string
                ''

        Returns string.
        '''
        result = []
        for part in self.explicit_command_history:
            if ' ' in part and ',' not in part:
                part = part.replace(' ', '~')
            result.append(part)
        return ' '.join(result)

    @property
    def transcript(self):
        r'''Gets session IO transcript.

        ..  container:: example

            ::

                >>> session.transcript
                Transcript()

        Returns IO transcript.
        '''
        return self._transcript

    @property
    def use_current_user_input_values_as_default(self):
        r'''Gets and sets flag to use current user input values as default.

        ..  container:: example

            ::

                >>> session.use_current_user_input_values_as_default
                False

        Returns boolean.
        '''
        return self._use_current_user_input_values_as_default

    ### PUBLIC METHODS ###

    def display_active_scores(self):
        r'''Sets scores to show to ``'active'``.

        Returns none.
        '''
        self._scores_to_display = 'active'
        self._rewrite_cache = True

    def display_all_scores(self):
        r'''Sets scores to show to ``'all'``.

        Returns none.
        '''
        self._scores_to_display = 'all'
        self._rewrite_cache = True

    def display_example_scores(self):
        r'''Sets scores to show to ``'example'``.

        Returns none.
        '''
        self._scores_to_display = 'example'
        self._rewrite_cache = True

    def display_mothballed_scores(self):
        r'''Sets scores to show to ``'mothballed'``.

        Returns none.
        '''
        self._scores_to_display = 'mothballed'
        self._rewrite_cache = True

    def display_user_scores(self):
        r'''Sets scores to show to ``'user'``.

        Returns none.
        '''
        self._scores_to_display = 'user'
        self._rewrite_cache = True

    def display_variables(self):
        r'''Displays session variables.

        Returns none.
        '''
        lines = []
        for variable_name in sorted(self._variables_to_display):
            if variable_name == 'controller_stack':
                line = '{}:'.format(variable_name)
                lines.append(line)
                variable_value = getattr(self, variable_name)
                for controller in variable_value:
                    tab_string = self._io_manager._make_tab()
                    line = '{}{}'.format(tab_string, controller)
                    lines.append(line)
            else:
                variable_value = getattr(self, variable_name)
                line = '{}: {!r}'
                line = line.format(variable_name, variable_value)
                lines.append(line)
        lines.append('')
        self.io_manager.display(lines, capitalize_first_character=False)
        if self.is_in_user_input_getter:
            self._hide_next_redraw = True
        self.io_manager.proceed()

    def get_controller_with(self, ui=None):
        r'''Gets most recent controller with `ui` in `_user_input_to_action`
        dictionary.

        Returns controller.
        '''
        for controller in reversed(self.controller_stack):
            if not ui:
                return controller
            user_input_to_action = getattr(
                controller,
                '_user_input_to_action',
                None,
                )
            if user_input_to_action:
                if ui in user_input_to_action:
                    return controller

    def toggle_hidden_commands(self):
        r'''Toggles `hide_hidden_commands`.

        Returns none.
        '''
        current = self.hide_hidden_commands
        self._hide_hidden_commands = not current

    def toggle_user_input_values_default_status(self):
        r'''Toggles `use_current_user_input_values_as_default`.

        Returns none.
        '''
        current = self.use_current_user_input_values_as_default
        self._use_current_user_input_values_as_default = not current