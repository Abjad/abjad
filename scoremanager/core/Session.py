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
            >>> session_in_score._current_score_snake_case_name = 'foo'
            >>> session_in_score
            Session()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attempted_to_open_file',
        '_backtracking_stack',
        '_breadcrumb_cache_stack',
        '_breadcrumb_stack',
        '_command_history',
        '_configuration',
        '_controller_stack',
        '_controllers_visited',
        '_current_score_snake_case_name',
        '_display_pitch_ranges_with_numbered_pitches',
        '_enable_where',
        '_hide_hidden_commands',
        '_hide_next_redraw',
        '_hide_secondary_commands',
        '_initial_user_input',
        '_io_manager',
        '_is_autoadding',
        '_is_backtracking_locally',
        '_is_backtracking_to_score',
        '_is_backtracking_to_score_manager',
        '_is_navigating_to_build_directory',
        '_is_navigating_to_next_material',
        '_is_navigating_to_next_score',
        '_is_navigating_to_previous_material',
        '_is_navigating_to_previous_score',
        '_is_navigating_to_score_materials',
        '_is_navigating_to_score_segments',
        '_is_quitting',
        '_is_test',
        '_last_line',
        '_last_command_was_composite',
        '_last_material_package_path',
        '_menu_header_width',
        '_nonnumbered_menu_sections_are_hidden',
        '_pending_user_input',
        '_rewrite_cache',
        '_score_manager',
        '_scores_to_display',
        '_session_once_had_user_input',
        '_transcribe_next_command',
        '_transcript',
        '_use_current_user_input_values_as_default',
        '_write_transcript',
        )

    _variables_to_display = (
        'attempted_to_open_file',
        'breadcrumb_stack',
        'command_history',
        'controller_stack',
        'controllers_visited',
        'current_controller',
        'current_materials_directory_path',
        'current_score_directory_path',
        'current_score_package_manager',
        'current_score_snake_case_name',
        'current_segments_directory_path',
        'write_transcript',
        'hide_next_redraw',
        'hide_hidden_commands',
        'hide_secondary_commands',
        'is_displayable',
        'is_in_score',
        'is_navigating_to_build_directory',
        'is_navigating_to_next_material',
        'is_navigating_to_previous_material',
        'is_navigating_to_score_materials',
        'is_navigating_to_score_segments',
        'is_navigating_to_sibling_score',
        'last_line',
        'last_material_package_path',
        'nonnumbered_menu_sections_are_hidden',
        'rewrite_cache',
        'score_manager',
        'scores_to_display',
        'session_once_had_user_input',
        'transcribe_next_command',
        'use_current_user_input_values_as_default',
        'user_input_is_consumed',
        )

    ### INITIALIZER ###

    def __init__(self, pending_user_input=None):
        from scoremanager import core
        from scoremanager import iotools
        self._attempted_to_open_file = False
        self._backtracking_stack = []
        self._breadcrumb_cache_stack = []
        self._breadcrumb_stack = []
        self._command_history = []
        self._configuration = core.ScoreManagerConfiguration()
        self._controller_stack = []
        self._controllers_visited = []
        self._current_score_snake_case_name = None
        self._display_pitch_ranges_with_numbered_pitches = False
        self._enable_where = False
        self._hide_hidden_commands = True
        self._hide_next_redraw = False
        self._hide_secondary_commands = True
        self._initial_user_input = pending_user_input
        self._io_manager = iotools.IOManager(self)
        self._is_autoadding = False
        self._is_backtracking_locally = False
        self._is_backtracking_to_score = False
        self._is_backtracking_to_score_manager = False
        self._is_navigating_to_build_directory = False
        self._is_navigating_to_next_material = False
        self._is_navigating_to_next_score = False
        self._is_navigating_to_previous_material = False
        self._is_navigating_to_previous_score = False
        self._is_navigating_to_score_materials = False
        self._is_navigating_to_score_segments = False
        self._is_quitting = False
        self._is_test = False
        self._last_line = ''
        self._last_command_was_composite = False
        self._last_material_package_path = None
        self._menu_header_width = 160
        self._nonnumbered_menu_sections_are_hidden = False
        self._pending_user_input = pending_user_input
        self._rewrite_cache = False
        self._score_manager = None
        self._scores_to_display = 'example'
        self._session_once_had_user_input = False
        self._transcribe_next_command = True
        self._transcript = iotools.Transcript()
        self._use_current_user_input_values_as_default = False
        self._write_transcript = False

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
            summary.append('initial_pending_user_input={!r}'.format(
                self.initial_user_input))
        if self.pending_user_input is not None:
            summary.append('pending_user_input={!r}'.format(
                self.pending_user_input))
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    ### PRIVATE METHODS ###

    # return true to break out of current io loop
    def _backtrack(self, source=None):
        if self.is_complete:
            return True
        elif self.is_backtracking_to_score_manager and source == 'home':
            self._is_backtracking_to_score_manager = False
            return False
        elif self.is_backtracking_to_score_manager and not source == 'home':
            return True
        elif self.is_backtracking_to_score and source in ('score', 'home'):
            self._is_backtracking_to_score = False
            return False
        elif self.is_backtracking_to_score and not source in ('score', 'home'):
            return True
        elif self.is_backtracking_locally and not source == 'home' and \
            self._backtracking_stack:
            return True
        elif self.is_backtracking_locally and not source == 'home' and \
            not self._backtracking_stack:
            self._is_backtracking_locally = False
            return True
        elif self.is_navigating_to_build_directory and \
            not source in ('score', 'home'):
            return True
        elif self.is_navigating_to_score_materials and \
            not source in ('score', 'home'):
            return True
        elif self.is_navigating_to_score_segments and \
            not source in ('score', 'home'):
            return True

    def _cache_breadcrumbs(self, cache=False):
        if cache:
            self._breadcrumb_cache_stack.append(self._breadcrumb_stack[:])
            self._breadcrumb_stack[:] = []

    def _clean_up(self):
        if self.write_transcript:
            self.transcript._write()

    def _format_breadcrumb_stack(self):
        if not self._breadcrumb_stack:
            return ''
        result_lines = [self._breadcrumb_stack[0]]
        hanging_indent_width = 5
        for breadcrumb in self._breadcrumb_stack[1:]:
            candidate_line = result_lines[-1] + ' - ' + breadcrumb
            if len(candidate_line) <= self.menu_header_width:
                result_lines[-1] = candidate_line
            else:
                result_line = hanging_indent_width * ' ' + breadcrumb
                result_lines.append(result_line)
        return result_lines

    def _pop_backtrack(self):
        return self._backtracking_stack.pop()

    def _pop_breadcrumb(self, rollback=True):
        if rollback:
            return self._breadcrumb_stack.pop()

    def _pop_controller(self):
        controller = self.controller_stack.pop()
        self._hide_secondary_commands = True

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

    def _push_backtrack(self):
        if self._backtracking_stack:
            last_number = self._backtracking_stack[-1]
            self._backtracking_stack.append(last_number + 1)
        else:
            self._backtracking_stack.append(0)

    def _push_breadcrumb(self, breadcrumb, rollback=True):
        if rollback:
            self._breadcrumb_stack.append(breadcrumb)

    def _push_controller(self, controller):
        self.controller_stack.append(controller)
        if controller not in self._controllers_visited:
            self._controllers_visited.append(controller)
        self._hide_secondary_commands = True

    def _reinitialize(self):
        type(self).__init__(self)

    def _restore_breadcrumbs(self, cache=False):
        if cache:
            self._breadcrumb_stack[:] = self._breadcrumb_cache_stack.pop()

    ### PUBLIC PROPERTIES ###

    @property
    def attempted_to_open_file(self):
        r'''Is true when call to ``IOManager.open_file()`` has been made
        during session. Otherwise false.

        ..  container:: example

            ::

                >>> session.attempted_to_open_file
                False

        Returns boolean.
        '''
        return self._attempted_to_open_file

    @property
    def breadcrumb_stack(self):
        r'''Gets session breadcrumb stack.

        ..  container:: example

            ::

                >>> session._breadcrumb_stack
                []

        Returns list.
        '''
        return self._breadcrumb_stack

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
                '.../scoremanager/materialpackages'

        ..  container:: example

            Materials directory path of session in score:

            ::

                >>> session_in_score.current_materials_directory_path
                '.../foo/materials'

        (Output will vary according to configuration.)

        Returns string.
        '''
        if self.is_in_score:
            manager = self.current_score_package_manager
            wrangler = manager._material_package_wrangler
            path = wrangler._get_current_directory_path_of_interest()
            return path
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
                '.../foo'

        Returns string or none.
        '''
        if self.current_score_snake_case_name:
            if self.current_score_snake_case_name in \
                self._configuration.abjad_score_package_names:
                return os.path.join(
                    self._configuration.abjad_score_packages_directory_path,
                    self.current_score_snake_case_name,
                    )
            else:
                return os.path.join(
                    self._configuration.user_score_packages_directory_path,
                    self.current_score_snake_case_name,
                    )

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
                ScorePackageManager('.../foo')

        (Ouput will vary according to configuration.)

        Returns score package manager or none.
        '''
        from scoremanager import managers
        package_path = \
            self._configuration.path_to_package(
            self.current_score_directory_path)
        if self.is_in_score:
            return managers.ScorePackageManager(
                package_path=package_path,
                session=self,
                )

    @property
    def current_score_snake_case_name(self):
        r'''Gets and sets snake-case current score name of session.

        ..  container:: example

            ::

                >>> session.current_score_snake_case_name is None
                True

        ..  container:: example

            ::

                >>> session_in_score.current_score_snake_case_name
                'foo'

        Returns string or none.
        '''
        return self._current_score_snake_case_name

    @property
    def current_segments_directory_path(self):
        r'''Gets session current segments directory path.

        ..  container:: example

            ::

                >>> session.current_segments_directory_path is None
                True

            (Output will vary according to configuration.)

        ..  container:: example

            ::

                >>> session_in_score.current_segments_directory_path
                '.../foo/segments'

            (Output will vary according to configuration.)

        Returns string.
        '''
        if self.is_in_score:
            manager = self.current_score_package_manager
            wrangler = manager._segment_package_wrangler
            path = wrangler._get_current_directory_path_of_interest()
            return path

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
    def enable_where(self):
        r'''Is true when session should enable source code tracking. Otherwise
        false.

        ..  container:: example

            ::

                >>> session.enable_where
                False

        Returns boolean.
        '''
        return self._enable_where

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
    def hide_secondary_commands(self):
        r'''Gets and sets flag indicating that hidden menu sections
        are hidden.

        ..  container:: example

            ::

                >>> session.hide_secondary_commands
                True

        Returns boolean.
        '''
        return self._hide_secondary_commands

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
    def is_autoadding(self):
        r'''Is true when session is autoadding. Otherwise false.

        ..  container:: example

            ::

                >>> session.is_autoadding
                False

        Returns boolean.
        '''
        return self._is_autoadding

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
    def is_displayable(self):
        r'''Is true when session is displayable. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_displayable
                True

        Returns boolean.
        '''
        return not self.pending_user_input

    @property
    def is_in_score(self):
        r'''Is true when session is in score. Otherwise false:

        ..  container:: example

            ::

                >>> session.is_in_score
                False

        Returns boolean.
        '''
        return self.current_score_snake_case_name is not None

    @property
    def is_navigating_to_build_directory(self):
        r'''Is true when session is navigating to build directory.
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_build_directory
                False

        Returns boolean.
        '''
        return self._is_navigating_to_build_directory

    @property
    def is_navigating_to_next_material(self):
        r'''Is true when session is navigating to next material. 
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_next_material
                False

        Returns boolean.
        '''
        return self._is_navigating_to_next_material

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
    def is_navigating_to_previous_material(self):
        r'''Is true when session is navigating to previous material. 
        Otherwise false.

        ..  container:: example

            ::

                >>> session.is_navigating_to_previous_material
                False

        Returns boolean.
        '''
        return self._is_navigating_to_previous_material

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
    def last_line(self):
        r'''Gets last line of session.

        ..  container:: example

            ::

                >>> session.last_line
                ''

        Useful for autopsy work after session ends.

        Returns string.
        '''
        return self._last_line

    @property
    def last_material_package_path(self):
        r'''Gets last material package path.

        ..  container:: example

            ::

                >>> session.last_material_package_path is None
                True

        Returns string or none.
        '''
        return self._last_material_package_path

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
        return '\n'.join(self._format_breadcrumb_stack())

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
    def nonnumbered_menu_sections_are_hidden(self):
        r'''Gets and sets flag that nonnumbered menu sections are hidden.

        ..  container:: example:

            ::

                >>> session.nonnumbered_menu_sections_are_hidden
                False

        Returns boolean.
        '''
        return self._nonnumbered_menu_sections_are_hidden

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
                'example'

        Returns string.
        '''
        return self._scores_to_display

    @property
    def session_once_had_user_input(self):
        r'''Is true when session once had user input. Otherwise false:

        ..  container:: example

            ::

                >>> session.session_once_had_user_input
                False

        Returns boolean.
        '''
        return self._session_once_had_user_input

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
    def transcribe_next_command(self):
        r'''Gets and sets flag to transcribe next command.

        ..  container:: example

            ::

                >>> session.transcribe_next_command
                True

        Returns boolean.
        '''
        return self._transcribe_next_command

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

    @property
    def user_input_is_consumed(self):
        r'''Is true when session user input is consumed.
        Otherwise false:

        ..  container:: example

            ::

                >>> session.user_input_is_consumed
                False

        Returns boolean.
        '''
        if self._session_once_had_user_input:
            if self.pending_user_input is None:
                return True
        return False

    @property
    def write_transcript(self):
        r'''Gets and sets flag to dump transcript at end of session.

        ..  container:: example

            ::

                >>> session.write_transcript
                False

        Returns boolean.
        '''
        return self._write_transcript

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

    def display_variables(self):
        r'''Displays session variables.

        Returns none.
        '''
        lines = []
        for variable_name in sorted(self._variables_to_display):
            variable_value = getattr(self, variable_name)
            line = '{}: {!r}'
            line = line.format(variable_name, variable_value)
            lines.append(line)
        lines.append('')
        self.io_manager.display(lines, capitalize_first_character=False)
        self.io_manager.proceed()

    def toggle_hidden_commands(self):
        r'''Toggles `hide_hidden_commands`.

        Returns none.
        '''
        if self._hide_hidden_commands:
            self._hide_hidden_commands = False
        else:
            self._hide_hidden_commands = True

    def toggle_secondary_commands(self):
        r'''Toggles `hide_secondary_commands`.

        Returns none.
        '''
        if self.hide_secondary_commands:
            self._hide_secondary_commands = False
        else:
            self._hide_secondary_commands = True
        self._hide_hidden_commands = True

    def toggle_source_code_tracking(self, prompt=True):
        r'''Toggles source code tracking.

        Returns none.
        '''
        if self.enable_where:
            self._enable_where = False
            message = 'source code tracking off.'
        else:
            self._enable_where = True
            message = 'source code tracking on.'
        if prompt:
            self.io_manager.display([message, ''])
        self._hide_next_redraw = True

    def toggle_user_input_values_default_status(self):
        r'''Toggles `use_current_user_input_values_as_default`.

        Returns none.
        '''
        current = self.use_current_user_input_values_as_default
        self._use_current_user_input_values_as_default = not current
