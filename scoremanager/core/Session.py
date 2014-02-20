# -*- encoding: utf-8 -*-
import os
from abjad.tools import abctools
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerConfiguration \
    import ScoreManagerConfiguration


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
            >>> session_in_score.current_score_snake_case_name = 'foo'
            >>> session_in_score
            Session()

    '''

    ### CLASS VARIABLES ###

    configuration = ScoreManagerConfiguration()

    _variables_to_display = (
        'breadcrumb_stack',
        'controller_stack',
        'current_controller',
        'current_materials_directory_path',
        'current_score_directory_path',
        'current_score_package_manager',
        'current_segments_directory_path',
        'dump_transcript',
        'hidden_menu_sections_are_hidden',
        'hide_next_redraw',
        'is_backtracking_locally',
        'is_backtracking_to_score',
        'is_backtracking_to_score_manager',
        'is_complete',
        'is_displayable',
        'is_in_score',
        'is_navigating_to_sibling_score',
        'is_quitting',
        'last_controller',
        'nonnumbered_menu_sections_are_hidden',
        'rewrite_cache',
        'score_manager',
        'scores_to_show',
        'session_once_had_user_input',
        'show_example_scores',
        'current_score_snake_case_name',
        'transcribe_next_command',
        'use_current_user_input_values_as_default',
        'user_input_is_consumed',
        )

    ### INITIALIZER ###

    def __init__(self, pending_user_input=None):
        from scoremanager import iotools
        self._backtracking_stack = []
        self._breadcrumb_cache_stack = []
        self._breadcrumb_stack = []
        self._command_history = []
        self._controller_stack = []
        self._io_manager = iotools.IOManager(self)
        self._last_controller = None
        self._score_manager = None
        self._session_once_had_user_input = False
        self._transcript = iotools.IOTranscript()
        self.current_score_snake_case_name = None
        self.display_pitch_ranges_with_numbered_pitches = False
        self.dump_transcript = False
        self.enable_where = False
        self.hidden_menu_sections_are_hidden = True
        self.hide_next_redraw = False
        self.initial_user_input = pending_user_input
        self.is_autoadding = False
        self.is_backtracking_locally = False
        self.is_backtracking_to_score = False
        self.is_backtracking_to_score_manager = False
        self.is_navigating_to_next_score = False
        self.is_navigating_to_previous_score = False
        self.is_test = False
        self.last_command_was_composite = False
        self.menu_header_width = 160
        self.nonnumbered_menu_sections_are_hidden = False
        self.pending_user_input = pending_user_input
        self.rewrite_cache = False
        self.show_example_scores = True
        self.transcribe_next_command = True
        self.use_current_user_input_values_as_default = False
        self.is_quitting = False
        self.display_example_scores()

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

    def _backtrack(self, source=None):
        if self.is_complete:
            return True
        elif self.is_backtracking_to_score_manager and source == 'home':
            self.is_backtracking_to_score_manager = False
            return False
        elif self.is_backtracking_to_score_manager and not source == 'home':
            return True
        elif self.is_backtracking_to_score and source in ('score', 'home'):
            self.is_backtracking_to_score = False
            return False
        elif self.is_backtracking_to_score and not source in ('score', 'home'):
            return True
        elif self.is_backtracking_locally and not source == 'home' and \
            self._backtracking_stack:
            return True
        elif self.is_backtracking_locally and not source == 'home' and \
            not self._backtracking_stack:
            self.is_backtracking_locally = False
            return True

    def _cache_breadcrumbs(self, cache=False):
        if cache:
            self._breadcrumb_cache_stack.append(self._breadcrumb_stack[:])
            self._breadcrumb_stack[:] = []

    def _clean_up(self):
        if self.dump_transcript:
            self.io_transcript.write()

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
        return self.controller_stack.pop()

    def _push_backtrack(self):
        if self._backtracking_stack:
            last_number = self._backtracking_stack[-1]
            self._backtracking_stack.append(last_number + 1)
        else:
            self._backtracking_stack.append(0)

    def _push_controller(self, controller):
        self.controller_stack.append(controller)
        self._last_controller = controller

    def _push_breadcrumb(self, breadcrumb, rollback=True):
        if rollback:
            self._breadcrumb_stack.append(breadcrumb)

    def _restore_breadcrumbs(self, cache=False):
        if cache:
            self._breadcrumb_stack[:] = self._breadcrumb_cache_stack.pop()

    def _reinitialize(self):
        type(self).__init__(self)

    ### PUBLIC PROPERTIES ###

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
        from scoremanager import wranglers
        if self.is_in_score:
            parts = []
            parts.append(self.configuration.user_score_packages_directory_path)
            parts.append(self.current_score_snake_case_name)
            parts.extend(
                wranglers.MaterialPackageWrangler.score_package_asset_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.configuration.built_in_material_packages_directory_path

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
                self.configuration.built_in_score_package_names:
                return os.path.join(
                    self.configuration.built_in_score_packages_directory_path,
                    self.current_score_snake_case_name)
            else:
                return os.path.join(
                    self.configuration.user_score_packages_directory_path,
                    self.current_score_snake_case_name)

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
        packagesystem_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
            self.current_score_directory_path)
        if self.is_in_score:
            return managers.ScorePackageManager(
                packagesystem_path=packagesystem_path,
                session=self,
                )

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
        from scoremanager import wranglers
        if self.is_in_score:
            parts = []
            parts.append(self.configuration.user_score_packages_directory_path)
            parts.append(self.current_score_snake_case_name)
            parts.extend(
                wranglers.SegmentPackageWrangler.score_package_asset_storehouse_path_infix_parts)
            return os.path.join(*parts)

    @apply
    def dump_transcript():
        def fget(self):
            r'''Gets and sets flag to dump transcript at end of session.

            ..  container:: example

                ::

                    >>> session.dump_transcript
                    False

            Returns boolean.
            '''
            return self._dump_transcript
        def fset(self, dump_transcript):
            assert isinstance(dump_transcript, bool)
            self._dump_transcript = dump_transcript
        return property(**locals())

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

    @apply
    def hidden_menu_sections_are_hidden():
        def fget(self):
            r'''Gets and sets flag indicating that hidden menu sections
            are hidden.

            ..  container:: example

                ::

                    >>> session.hidden_menu_sections_are_hidden
                    True

            Returns boolean.
            '''
            return self._hidden_menu_sections_are_hidden
        def fset(self, hidden_menu_sections_are_hidden):
            assert isinstance(hidden_menu_sections_are_hidden, bool)
            self._hidden_menu_sections_are_hidden = \
                hidden_menu_sections_are_hidden
        return property(**locals())

    @apply
    def hide_next_redraw():
        def fget(self):
            r'''Gets and sets flag to hide next redraw.

            ..  container:: example

                ::

                    >>> session.hide_next_redraw
                    False

            Returns boolean.
            '''
            return self._hide_next_redraw
        def fset(self, hide_next_redraw):
            assert isinstance(hide_next_redraw, bool)
            self._hide_next_redraw = hide_next_redraw
        return property(**locals())

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
    def io_transcript(self):
        r'''Gets session IO transcript.

        ..  container:: example

            ::

                >>> session.io_transcript
                IOTranscript()

        Returns IO transcript.
        '''
        return self._transcript

    @apply
    def is_autoadding():
        def fget(self):
            r'''Is true when session is autoadding. Otherwise false.

            ..  container:: example

                ::

                    >>> session.is_autoadding
                    False

            Returns boolean.
            '''
            return self._is_autoadding
        def fset(self, is_autoadding):
            assert isinstance(is_autoadding, bool)
            self._is_autoadding = is_autoadding
        return property(**locals())

    @apply
    def is_backtracking_locally():
        def fget(self):
            r'''Is true when session is backtracking locally. 
            Otherwise false.

            ..  container:: example

                ::

                    >>> session.is_backtracking_locally
                    False

            Returns boolean.
            '''
            return self._is_backtracking_locally
        def fset(self, is_backtracking_locally):
            assert isinstance(is_backtracking_locally, bool)
            self._is_backtracking_locally = is_backtracking_locally
        return property(**locals())

    @apply
    def is_backtracking_to_score():
        def fget(self):
            r'''Is true when session is backtracking to score. 
            Otherwise false.

            ..  container:: example

                ::

                    >>> session.is_backtracking_to_score
                    False

            Returns boolean.
            '''
            return self._is_backtracking_to_score
        def fset(self, is_backtracking_to_score):
            assert isinstance(is_backtracking_to_score, bool)
            self._is_backtracking_to_score = is_backtracking_to_score
        return property(**locals())

    @apply
    def is_backtracking_to_score_manager():
        def fget(self):
            r'''Is true when session is backtracking to score manager. 
            Otherwise false.

            ..  container:: example

                ::

                    >>> session.is_backtracking_to_score_manager
                    False

            Returns boolean.
            '''
            return self._is_backtracking_to_score_manager
        def fset(self, is_backtracking_to_score_manager):
            assert isinstance(is_backtracking_to_score_manager, bool)
            self._is_backtracking_to_score_manager = \
                is_backtracking_to_score_manager
        return property(**locals())

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

    @apply
    def is_quitting():
        def fget(self):
            r'''Gets and sets flag that user specified quit.

            ..  container:: example

                ::

                    >>> session.is_quitting
                    False

            Returns boolean.
            '''
            return self._is_quitting
        def fset(self, is_quitting):
            assert isinstance(is_quitting, bool)
            self._is_quitting = is_quitting
        return property(**locals())

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
    def last_controller(self):
        r'''Gets last controller of session.

        ..  container:: example

            ::

                >>> session.last_controller is None
                True

        Useful for autopsy work after session ends.

        Returns wrangler, manager or none.
        '''
        return self._last_controller

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

    @apply
    def nonnumbered_menu_sections_are_hidden():
        def fget(self):
            r'''Gets and sets flag that nonnumbered menu sections are hidden.

            ..  container:: example:

                ::

                    >>> session.nonnumbered_menu_sections_are_hidden
                    False

            Returns boolean.
            '''
            return self._nonnumbered_menu_sections_are_hidden
        def fset(self, nonnumbered_menu_sections_are_hidden):
            assert isinstance(nonnumbered_menu_sections_are_hidden, bool)
            self._nonnumbered_menu_sections_are_hidden = \
                nonnumbered_menu_sections_are_hidden
        return property(**locals())

    @apply
    def pending_user_input():
        def fget(self):
            r'''Gets and sets pending user input.

            ..  container:: example

                ::

                    >>> session.pending_user_input is None
                    True

            Returns string.
            '''
            return self._pending_user_input
        def fset(self, pending_user_input):
            assert isinstance(pending_user_input, (str, type(None)))
            self._pending_user_input = pending_user_input
            if isinstance(pending_user_input, str):
                self._session_once_had_user_input = True
        return property(**locals())

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
    def scores_to_show(self):
        r'''Gets session scores to show.

        ..  container:: example

            ::

                >>> session.scores_to_show
                'example'

        Returns string.
        '''
        return self._scores_to_show

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

    @apply
    def rewrite_cache():
        def fget(self):
            r'''Gets and sets flag to rewrite cache.

            ..  container:: example

                ::

                    >>> session.rewrite_cache
                    True

            Returns boolean.
            '''
            return self._rewrite_cache
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._rewrite_cache = expr
        return property(**locals())

    @apply
    def show_example_scores():
        def fget(self):
            r'''Gets and sets flag to show example scores.

            ..  container:: example

                ::

                    >>> session.show_example_scores
                    True

            Returns boolean.
            '''
            return self._show_example_scores
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._show_example_scores = expr
        return property(**locals())

    @apply
    def current_score_snake_case_name():
        def fget(self):
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
            return self._snake_case_current_score_name
        def fset(self, current_score_snake_case_name):
            assert isinstance(current_score_snake_case_name, (str, type(None)))
            if isinstance(current_score_snake_case_name, str):
                assert '.' not in current_score_snake_case_name
            self._snake_case_current_score_name = current_score_snake_case_name
        return property(**locals())

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

    @apply
    def transcribe_next_command():
        def fget(self):
            r'''Gets and sets flag to transcribe next command.

            ..  container:: example

                ::

                    >>> session.transcribe_next_command
                    True

            Returns boolean.
            '''
            return self._transcribe_next_command
        def fset(self, transcribe_next_command):
            assert isinstance(transcribe_next_command, bool)
            self._transcribe_next_command = transcribe_next_command
        return property(**locals())

    @apply
    def use_current_user_input_values_as_default():
        def fget(self):
            r'''Gets and sets flag to use current user input values as default.

            ..  container:: example

                ::

                    >>> session.use_current_user_input_values_as_default
                    False

            Returns boolean.
            '''
            return self._use_current_user_input_values_as_default
        def fset(self, use_current_user_input_values_as_default):
            assert isinstance(use_current_user_input_values_as_default, bool)
            self._use_current_user_input_values_as_default = \
                use_current_user_input_values_as_default
        return property(**locals())

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

    ### PUBLIC METHODS ###

    def display_active_scores(self):
        r'''Sets scores to show to ``'active'``.

        Returns none.
        '''
        self._scores_to_show = 'active'
        self.rewrite_cache = True

    def display_all_scores(self):
        r'''Sets scores to show to ``'all'``.

        Returns none.
        '''
        self._scores_to_show = 'all'
        self.rewrite_cache = True

    def display_example_scores(self):
        r'''Sets scores to show to ``'example'``.

        Returns none.
        '''
        self._scores_to_show = 'example'
        self.rewrite_cache = True

    def display_mothballed_scores(self):
        r'''Sets scores to show to ``'mothballed'``.

        Returns none.
        '''
        self._scores_to_show = 'mothballed'
        self.rewrite_cache = True

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

    def swap_user_input_values_default_status(self):
        r'''Swaps boolean value of `use_current_user_input_values_as_default`.

        Returns none.
        '''
        current = self.use_current_user_input_values_as_default
        self.use_current_user_input_values_as_default = not current
