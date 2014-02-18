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
            >>> session_in_score.snake_case_current_score_name = 'foo'
            >>> session_in_score
            Session()

    '''

    ### CLASS VARIABLES ###

    configuration = ScoreManagerConfiguration()

    # TODO: this can probably be removed now
    # this is a temporary hack to avoid constantly reading from disk;
    # this will eventually be replaced with something more robust.
    cache_of_built_in_score_names = (
        'red_example_score',
        'green_example_score',
        'blue_example_score',
        )

    ### INITIALIZER ###

    def __init__(self, pending_user_input=None):
        from scoremanager import iotools
        self._backtracking_stack = []
        self._breadcrumb_cache_stack = []
        self._breadcrumb_stack = []
        self._command_history = []
        self._io_manager = iotools.IOManager(self)
        self._session_once_had_user_input = False
        self._transcript = iotools.IOTranscript()
        self.snake_case_current_score_name = None
        self.developer_menu_sections_are_hidden = True
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
        self.is_first_run = True
        self.is_navigating_to_next_score = False
        self.is_navigating_to_previous_score = False
        self.is_test = False
        self.last_command_was_composite = False
        self.menu_header_width = 160
        self.nonnumbered_menu_sections_are_hidden = False
        self.transcribe_next_command = True
        self.use_current_user_input_values_as_default = False
        self.pending_user_input = pending_user_input
        self.user_specified_quit = False
        self.display_active_scores()

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of session.

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

    ### PUBLIC PROPERTIES ###

    @property
    def backtracking_stack(self):
        r'''Session backtracking stack.

        ::

            >>> session.backtracking_stack
            []

        Returns list.
        '''
        return self._backtracking_stack

    @property
    def breadcrumb_cache_stack(self):
        r'''Session breadcrumb cache stack.

        ::

            >>> session._breadcrumb_cache_stack
            []

        Returns list.
        '''
        return self._breadcrumb_cache_stack

    @property
    def breadcrumb_stack(self):
        r'''Session breadcrumb stack.

        ::

            >>> session._breadcrumb_stack
            []

        Returns list.
        '''
        return self._breadcrumb_stack

    @property
    def command_history(self):
        r'''Session command history.

        ::

            >>> session.command_history
            []

        Returns list.
        '''
        return self._command_history

    @property
    def command_history_string(self):
        r'''Session command history string.

        ::

            >>> session.command_history_string
            ''

        Returns string.
        '''
        return ' '.join(self.explicit_command_history)

    @property
    def current_materials_directory_path(self):
        r'''Session current materials directory path.

        ..  container:: example

            **Example 1.** Materials directory path of session outside score:

            ::

                >>> session.current_materials_directory_path
                '.../scoremanager/materialpackages'

        ..  container:: example

            **Example 2.** Materials directory path of session in score:

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
            parts.append(self.snake_case_current_score_name)
            parts.extend(
                wranglers.MaterialPackageWrangler.score_package_asset_storehouse_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.configuration.built_in_material_packages_directory_path

    @property
    def current_materials_package_path(self):
        r'''Session current materials package path.

        ..  container:: example

            **Example 1.** Currents materials package path of session 
            out of score:

            ::

                >>> session.current_materials_package_path
                'scoremanager.materialpackages'

        ..  container:: example

            **Example 2.** Current materials package path of session
            in score:

            ::

                >>> session_in_score.current_materials_package_path
                'foo.materials'

        Returns string.
        '''
        from scoremanager import wranglers
        if self.is_in_score:
            parts = []
            parts.append(self.snake_case_current_score_name)
            parts.extend(
                wranglers.MaterialPackageWrangler.score_package_asset_storehouse_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.configuration.built_in_material_packages_package_path

    @property
    def current_score_directory_path(self):
        r'''Session current score directory path.

        .. note:: add example.

        Returns string.
        '''
        if self.snake_case_current_score_name:
            if self.snake_case_current_score_name in \
                self.cache_of_built_in_score_names:
                return os.path.join(
                    self.configuration.built_in_score_packages_directory_path,
                    self.snake_case_current_score_name)
            else:
                return os.path.join(
                    self.configuration.user_score_packages_directory_path,
                    self.snake_case_current_score_name)

    @property
    def current_score_package_manager(self):
        r'''Session current score package manager.

        ::

            >>> session.current_score_package_manager is None
            True

        Session in score:

        ::

            >>> session_in_score.current_score_package_manager
            ScorePackageManager('.../foo')

        (Ouput will vary according to configuration.)

        Returns score package manager or none.
        '''
        from scoremanager.managers.ScorePackageManager \
            import ScorePackageManager
        if self.is_in_score:
            return ScorePackageManager(
                packagesystem_path=self.current_score_package_path,
                session=self)

    @property
    def current_score_package_path(self):
        r'''Session current score package path.

        .. note:: add example.

        Returns string.
        '''
        if self.snake_case_current_score_name:
            if self.snake_case_current_score_name in \
                self.cache_of_built_in_score_names:
                return '.'.join([
                    self.configuration.built_in_score_packages_package_path,
                    self.snake_case_current_score_name])
            else:
                return self.snake_case_current_score_name

    @property
    def current_segments_directory_path(self):
        r'''Session current segments directory path.

        ::

            >>> session.current_segments_directory_path is None
            True

        (Output will vary according to configuration.)

        Session in score:

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
            parts.append(self.snake_case_current_score_name)
            parts.extend(
                wranglers.SegmentPackageWrangler.score_package_asset_storehouse_path_infix_parts)
            return os.path.join(*parts)

    @property
    def current_segments_package_path(self):
        r'''Session current segments package path.

        Session out of score:

        ::

            >>> session.current_segments_package_path is None
            True

        Session in score:

        ::

            >>> session_in_score.current_segments_package_path
            'foo.segments'

        Returns none or string.
        '''
        from scoremanager import wranglers
        if self.is_in_score:
            parts = []
            parts.append(self.snake_case_current_score_name)
            parts.extend(
                wranglers.SegmentPackageWrangler.score_package_asset_storehouse_path_infix_parts)
            return '.'.join(parts)

    @apply
    def developer_menu_sections_are_developer():
        def fget(self):
            return self._developer_menu_sections_are_developer
        def fset(self, developer_menu_sections_are_developer):
            assert isinstance(developer_menu_sections_are_developer, bool)
            self._developer_menu_sections_are_developer = \
                developer_menu_sections_are_developer
        return property(**locals())

    @apply
    def dump_transcript():
        r'''Set to true to dump transcript at end of session.

        .. note:: add example.

        Returns boolean.
        '''
        def fget(self):
            return self._dump_transcript
        def fset(self, dump_transcript):
            assert isinstance(dump_transcript, bool)
            self._dump_transcript = dump_transcript
        return property(**locals())

    @property
    def explicit_command_history(self):
        r'''Session explicit command history.

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
            return self._hidden_menu_sections_are_hidden
        def fset(self, hidden_menu_sections_are_hidden):
            assert isinstance(hidden_menu_sections_are_hidden, bool)
            self._hidden_menu_sections_are_hidden = \
                hidden_menu_sections_are_hidden
        return property(**locals())

    @apply
    def hide_next_redraw():
        r'''Set to true to hide next redraw.

        Returns boolean.
        '''
        def fget(self):
            return self._hide_next_redraw
        def fset(self, hide_next_redraw):
            assert isinstance(hide_next_redraw, bool)
            self._hide_next_redraw = hide_next_redraw
        return property(**locals())

    @property
    def io_manager(self):
        r'''Session IO manager.

        Returns IO manager.
        '''
        return self._io_manager

    @property
    def io_transcript(self):
        r'''Session IO transcript.

        ::

            >>> session.io_transcript
            IOTranscript()

        Returns IO transcript.
        '''
        return self._transcript

    @apply
    def is_autoadding():
        def fget(self):
            return self._is_autoadding
        def fset(self, is_autoadding):
            assert isinstance(is_autoadding, bool)
            self._is_autoadding = is_autoadding
        return property(**locals())

    @apply
    def is_backtracking_locally():
        def fget(self):
            return self._is_backtracking_locally
        def fset(self, is_backtracking_locally):
            assert isinstance(is_backtracking_locally, bool)
            self._is_backtracking_locally = is_backtracking_locally
        return property(**locals())

    @apply
    def is_backtracking_to_score():
        def fget(self):
            return self._is_backtracking_to_score
        def fset(self, is_backtracking_to_score):
            assert isinstance(is_backtracking_to_score, bool)
            self._is_backtracking_to_score = is_backtracking_to_score
        return property(**locals())

    @apply
    def is_backtracking_to_score_manager():
        def fget(self):
            return self._is_backtracking_to_score_manager
        def fset(self, is_backtracking_to_score_manager):
            assert isinstance(is_backtracking_to_score_manager, bool)
            self._is_backtracking_to_score_manager = \
                is_backtracking_to_score_manager
        return property(**locals())

    @property
    def is_complete(self):
        r'''Is true when session is complete. Otherwise false:

        ::

            >>> session.is_complete
            False

        Returns boolean.
        '''
        return self.user_specified_quit

    @property
    def is_displayable(self):
        r'''Is true when session is displayable. Otherwise false:

        ::

            >>> session.is_displayable
            True

        Returns boolean.
        '''
        return not self.pending_user_input

    @property
    def is_in_score(self):
        r'''Is true when session is in score. Otherwise false:

        ::

            >>> session.is_in_score
            False

        Returns boolean.
        '''
        return self.snake_case_current_score_name is not None

    @property
    def is_navigating_to_sibling_score(self):
        r'''Is true when session is navigating to sibling score.
        Otherwise false:

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
    def last_semantic_command(self):
        r'''Session last semantic command.

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
        r'''Session menu header.

        ::

            >>> session.menu_header
            ''

        Returns string.
        '''
        return '\n'.join(self.format_breadcrumb_stack())

    @apply
    def nonnumbered_menu_sections_are_hidden():
        def fget(self):
            return self._nonnumbered_menu_sections_are_hidden
        def fset(self, nonnumbered_menu_sections_are_hidden):
            assert isinstance(nonnumbered_menu_sections_are_hidden, bool)
            self._nonnumbered_menu_sections_are_hidden = \
                nonnumbered_menu_sections_are_hidden
        return property(**locals())

    @apply
    def pending_user_input():
        def fget(self):
            return self._pending_user_input
        def fset(self, pending_user_input):
            assert isinstance(pending_user_input, (str, type(None)))
            self._pending_user_input = pending_user_input
            if isinstance(pending_user_input, str):
                self._session_once_had_user_input = True
        return property(**locals())

    @property
    def scores_to_show(self):
        r'''Session scores to show.

        ::

            >>> session.scores_to_show
            'active'

        Returns string.
        '''
        return self._scores_to_show

    @property
    def session_once_had_user_input(self):
        r'''Is true when session once had user input. Otherwise false:

        ::

            >>> session.session_once_had_user_input
            False

        Returns boolean.
        '''
        return self._session_once_had_user_input

    @apply
    def snake_case_current_score_name():
        def fget(self):
            return self._snake_case_current_score_name
        def fset(self, snake_case_current_score_name):
            assert isinstance(snake_case_current_score_name, (str, type(None)))
            if isinstance(snake_case_current_score_name, str):
                assert '.' not in snake_case_current_score_name
            self._snake_case_current_score_name = snake_case_current_score_name
        return property(**locals())

    @property
    def testable_command_history_string(self):
        r'''Session testable command history string.

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
            return self._transcribe_next_command
        def fset(self, transcribe_next_command):
            assert isinstance(transcribe_next_command, bool)
            self._transcribe_next_command = transcribe_next_command
        return property(**locals())

    @apply
    def use_current_user_input_values_as_default():
        def fget(self):
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

        ::

            >>> session.user_input_is_consumed
            False

        Returns boolean.
        '''
        if self._session_once_had_user_input:
            if self.pending_user_input is None:
                return True
        return False

    @apply
    def user_specified_quit():
        def fget(self):
            return self._user_specified_quit
        def fset(self, user_specified_quit):
            assert isinstance(user_specified_quit, bool)
            self._user_specified_quit = user_specified_quit
        return property(**locals())

    ### PUBLIC METHODS ###

    def backtrack(self, source=None):
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
            self.backtracking_stack:
            return True
        elif self.is_backtracking_locally and not source == 'home' and \
            not self.backtracking_stack:
            self.is_backtracking_locally = False
            return True

    def cache_breadcrumbs(self, cache=False):
        if cache:
            self._breadcrumb_cache_stack.append(self._breadcrumb_stack[:])
            self._breadcrumb_stack[:] = []

    def clean_up(self):
        if self.dump_transcript:
            self.io_transcript.write()

    def display_active_scores(self):
        self._scores_to_show = 'active'

    def display_all_scores(self):
        self._scores_to_show = 'all'

    def display_mothballed_scores(self):
        self._scores_to_show = 'mothballed'

    def format_breadcrumb_stack(self):
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

    def pop_backtrack(self):
        return self.backtracking_stack.pop()

    def pop_breadcrumb(self, rollback=True):
        if rollback:
            return self._breadcrumb_stack.pop()

    def push_backtrack(self):
        if self.backtracking_stack:
            last_number = self.backtracking_stack[-1]
            self.backtracking_stack.append(last_number + 1)
        else:
            self.backtracking_stack.append(0)

    def push_breadcrumb(self, breadcrumb, rollback=True):
        if rollback:
            self._breadcrumb_stack.append(breadcrumb)

    def reinitialize(self):
        type(self).__init__(self)

    def restore_breadcrumbs(self, cache=False):
        if cache:
            self._breadcrumb_stack[:] = self._breadcrumb_cache_stack.pop()

    def swap_user_input_values_default_status(self):
        current = self.use_current_user_input_values_as_default
        self.use_current_user_input_values_as_default = not current
