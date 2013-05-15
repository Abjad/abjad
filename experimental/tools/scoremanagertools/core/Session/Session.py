# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
from abjad.tools import abctools
from experimental.tools.scoremanagertools.core.ScoreManagerConfiguration import \
    ScoreManagerConfiguration


class Session(abctools.AbjadObject):
    '''Score manager session.

        >>> session = scoremanagertools.core.Session()

    ::

        >>> session
        Session()

    Session in score:

    ::

        >>> session_in_score = scoremanagertools.core.Session()
        >>> session_in_score.underscore_delimited_current_score_name = 'foo'

    ::

        >>> session_in_score
        Session()

    Return session.
    '''

    ### CLASS ATTRIBUTES ###

    configuration = ScoreManagerConfiguration()
    # this is a temporary hack to avoid constantly reading from disk;
    # this will eventually be replaced with something more robust, perhaps a real cache.
    cache_of_built_in_score_names = (
        'red_example_score',
        'green_example_score',
        'blue_example_score',
        )

    ### INITIALIZER ###

    def __init__(self, user_input=None):
        from experimental.tools import scoremanagertools
        self._backtracking_stack = []
        self._breadcrumb_cache_stack = []
        self._breadcrumb_stack = []
        self._command_history = []
        self._session_once_had_user_input = False
        self._transcript = scoremanagertools.core.Transcript()
        self.underscore_delimited_current_score_name = None
        self.display_pitch_ranges_with_numbered_pitches = False
        self.dump_transcript = False
        self.enable_where = False
        self.hide_next_redraw = False
        self.initial_user_input = user_input
        self.is_autoadding = False
        self.is_backtracking_locally = False
        self.is_backtracking_to_score = False
        self.is_backtracking_to_score_manager = False
        self.is_navigating_to_next_score = False
        self.is_navigating_to_prev_score = False
        self.last_command_was_composite = False
        self.menu_header_width = 100
        self.nonnumbered_menu_sections_are_hidden = False
        self.transcribe_next_command = True
        self.use_current_user_input_values_as_default = False
        self.user_input = user_input
        self.user_specified_quit = False
        self.show_active_scores()

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Session repr.

        Return string.
        '''
        summary = []
        if self.initial_user_input is not None:
            summary.append('initial_user_input={!r}'.format(self.initial_user_input))
        if self.user_input is not None:
            summary.append('user_input={!r}'.format(self.user_input))
        summary = ', '.join(summary)
        return '{}({})'.format(type(self).__name__, summary)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def backtracking_stack(self):
        '''Session backtracking stack:

        ::

            >>> session.backtracking_stack
            []

        Return list.
        '''
        return self._backtracking_stack

    @property
    def breadcrumb_cache_stack(self):
        '''Session breadcrumb cache stack:

        ::

            >>> session._breadcrumb_cache_stack
            []

        Return list.
        '''
        return self._breadcrumb_cache_stack

    @property
    def breadcrumb_stack(self):
        '''Session breadcrumb stack:

        ::

            >>> session._breadcrumb_stack
            []

        Return list.
        '''
        return self._breadcrumb_stack

    @property
    def command_history(self):
        '''Session command history:

        ::

            >>> session.command_history
            []
        
        Return list.
        '''
        return self._command_history

    @property
    def command_history_string(self):
        '''Session command history string:

        ::

            >>> session.command_history_string
            ''

        Return string.
        '''
        return ' '.join(self.explicit_command_history)

    @property
    def current_materials_directory_path(self):
        '''Session current materials directory path:

        ::

            >>> session.current_materials_directory_path
            '.../abjad/experimental/built_in_materials'

        Session in score:

        ::

            >>> session_in_score.current_materials_directory_path
            '.../scores/foo/music/materials'

        (Output will vary according to configuration.)

        Return string.
        '''
        from experimental.tools import scoremanagertools
        if self.is_in_score:
            parts = []
            parts.append(self.configuration.user_scores_directory_path)
            parts.append(self.underscore_delimited_current_score_name)
            parts.extend(
                scoremanagertools.wranglers.MaterialPackageWrangler.asset_container_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.configuration.built_in_materials_directory_path

    @property
    def current_materials_package_path(self):
        '''Session current materials package path:

        ::

            >>> session.current_materials_package_path
            'built_in_materials'

        Session in score:

        ::

            >>> session_in_score.current_materials_package_path
            'foo.music.materials'

        Return string.
        '''
        from experimental.tools import scoremanagertools
        if self.is_in_score:
            parts = []
            parts.append(self.underscore_delimited_current_score_name)
            parts.extend(
                scoremanagertools.wranglers.MaterialPackageWrangler.asset_container_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.configuration.built_in_materials_package_path

    @property
    def current_score_directory_path(self):
        '''Session current score directory path:

        .. note:: add example.

        Return string.
        '''
        if self.underscore_delimited_current_score_name:
            if self.underscore_delimited_current_score_name in \
                self.cache_of_built_in_score_names:
                return os.path.join(
                    self.configuration.built_in_scores_directory_path,
                    self.underscore_delimited_current_score_name)
            else:
                return os.path.join(
                    self.configuration.user_scores_directory_path,
                    self.underscore_delimited_current_score_name)

    @property
    def current_score_package_path(self):
        '''Session current score package path:

        .. note:: add example.

        Return string.
        '''
        if self.underscore_delimited_current_score_name:
            if self.underscore_delimited_current_score_name in \
                self.cache_of_built_in_score_names:
                return '.'.join([
                    self.configuration.built_in_scores_package_path,
                    self.underscore_delimited_current_score_name])
            else:
                return self.underscore_delimited_current_score_name

    @property
    def current_score_package_proxy(self):
        '''Session current score package proxy:

        ::

            >>> session.current_score_package_proxy is None
            True

        Session in score:

        ::

            >>> session_in_score.current_score_package_proxy
            ScorePackageProxy('.../scores/foo')

        (Ouput will vary according to configuration.)

        Return score package proxy or none.
        '''
        from experimental.tools.scoremanagertools.proxies.ScorePackageProxy import ScorePackageProxy
        if self.is_in_score:
            return ScorePackageProxy(
                packagesystem_path=self.current_score_package_path, session=self)

    @property
    def current_segments_directory_path(self):
        '''Session current segments directory path:

        ::

            >>> session.current_segments_directory_path # doctest: +SKIP
            '~/score_manager/sketches'

        (Output will vary according to configuration.)

        Session in score:

        ::

            >>> session_in_score.current_segments_directory_path
            '.../scores/foo/music/segments'

        (Output will vary according to configuration.)

        Return string.
        '''
        from experimental.tools import scoremanagertools
        if self.is_in_score:
            parts = []
            parts.append(self.configuration.user_scores_directory_path)
            parts.append(self.underscore_delimited_current_score_name)
            parts.extend(
                scoremanagertools.wranglers.SegmentPackageWrangler.asset_container_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.configuration.user_sketches_directory_path

    @property
    def current_segments_package_path(self):
        '''Session current segments package path:

        ::

            >>> session.current_segments_package_path
            'sketches'

        Session in score:

        ::

            >>> session_in_score.current_segments_package_path
            'foo.music.segments'

        Return string.
        '''
        from experimental.tools import scoremanagertools
        if self.is_in_score:
            parts = []
            parts.append(self.underscore_delimited_current_score_name)
            parts.extend(
                scoremanagertools.wranglers.SegmentPackageWrangler.asset_container_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.configuration.user_sketches_package_path

    @property
    def current_specifiers_directory_path(self):
        '''Session current specifiers directory path:

        ::

            >>> session.current_specifiers_directory_path
            '.../tools/scoremanagertools/built_in_specifiers'

        Session in score:

        ::

            >>> session_in_score.current_specifiers_directory_path
            '.../scores/foo/music/specifiers'

        (Output will vary according to configuration.)

        Return string.
        '''
        from experimental.tools import scoremanagertools
        if self.is_in_score:
            parts = []
            parts.append(self.configuration.user_scores_directory_path)
            parts.append(self.underscore_delimited_current_score_name)
            parts.extend(
                scoremanagertools.wranglers.MusicSpecifierModuleWrangler.asset_container_path_infix_parts)
            return os.path.join(*parts)
        else:
            return self.configuration.built_in_specifiers_directory_path

    @property
    def current_specifiers_package_path(self):
        '''Session current specifiers package path:

        ::

            >>> session.current_specifiers_package_path
            'experimental.tools.scoremanagertools.built_in_specifiers'

        Session in score:

        ::

            >>> session_in_score.current_specifiers_package_path
            'foo.music.specifiers'

        Return string.
        '''
        from experimental.tools import scoremanagertools
        if self.is_in_score:
            parts = []
            parts.append(self.underscore_delimited_current_score_name)
            parts.extend(
                scoremanagertools.wranglers.MusicSpecifierModuleWrangler.asset_container_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.configuration.built_in_specifiers_package_path

    @property
    def explicit_command_history(self):
        '''Session explicit command history:

        ::

            >>> session.explicit_command_history
            []

        Return list.
        '''
        result = []
        for command in self.command_history:
            if command == '':
                result.append('default')
            else:
                result.append(command)
        return result

    @property
    def is_complete(self):
        '''True when session is complete. Otherwise false:

        ::

            >>> session.is_complete
            False

        Return boolean.
        '''
        return self.user_specified_quit

    @property
    def is_displayable(self):
        '''True when session is displayable. Otherwise false:

        ::

            >>> session.is_displayable
            True

        Return boolean.
        '''
        return not self.user_input

    @property
    def is_in_score(self):
        '''True when session is in score. Otherwise false:

        ::

            >>> session.is_in_score
            False

        Return boolean.
        '''
        return self.underscore_delimited_current_score_name is not None

    @property
    def is_navigating_to_sibling_score(self):
        '''True when session is navigating to sibling score.
        Otherwise false:

        ::
            
            >>> session.is_navigating_to_sibling_score
            False

        Return boolean.
        '''
        if self.is_navigating_to_next_score:
            return True
        if self.is_navigating_to_prev_score:
            return True
        return False

    @property
    def last_semantic_command(self):
        '''Session last semantic command:

        ::

            >>> session.last_semantic_command is None
            True

        Return string or none.
        '''
        for command in reversed(self.command_history):
            if not command.startswith('.'):
                return command

    @property
    def menu_header(self):
        '''Session menu header:

        ::

            >>> session.menu_header
            ''

        Return string.
        '''
        return '\n'.join(self.format_breadcrumb_stack())

    @property
    def scores_to_show(self):
        '''Session scores to show:

        ::

            >>> session.scores_to_show
            'active'

        Return string.
        '''
        return self._scores_to_show

    @property
    def session_once_had_user_input(self):
        '''True when session once had user input. Otherwise false:

        ::

            >>> session.session_once_had_user_input
            False

        Return boolean.
        '''
        return self._session_once_had_user_input

    @property
    def testable_command_history_string(self):
        '''Session testable command history string:

        ::

            >>> session.testable_command_history_string
            ''

        Return string.
        '''
        result = []
        for part in self.explicit_command_history:
            if ' ' in part and ',' not in part:
                part = part.replace(' ', '~')
            result.append(part)
        return ' '.join(result)

    @property
    def transcript(self):
        '''Session transcript:

        ::

            >>> session.transcript
            Transcript()

        Return transcript.
        '''
        return self._transcript

    @property
    def user_input_is_consumed(self):
        '''True when session user input is consumed.
        Otherwise false:

        ::

            >>> session.user_input_is_consumed
            False

        Return boolean.
        '''
        if self._session_once_had_user_input:
            if self.user_input is None:
                return True
        return False

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def dump_transcript():
        def fget(self):
            return self._dump_transcript
        def fset(self, dump_transcript):
            assert isinstance(dump_transcript, bool)
            self._dump_transcript = dump_transcript
        return property(**locals())

    @apply
    def hide_next_redraw():
        def fget(self):
            return self._hide_next_redraw
        def fset(self, hide_next_redraw):
            assert isinstance(hide_next_redraw, bool)
            self._hide_next_redraw = hide_next_redraw
        return property(**locals())

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
            self._is_backtracking_to_score_manager = is_backtracking_to_score_manager
        return property(**locals())

    @apply
    def nonnumbered_menu_sections_are_hidden():
        def fget(self):
            return self._nonnumbered_menu_sections_are_hidden
        def fset(self, nonnumbered_menu_sections_are_hidden):
            assert isinstance(nonnumbered_menu_sections_are_hidden, bool)
            self._nonnumbered_menu_sections_are_hidden = nonnumbered_menu_sections_are_hidden
        return property(**locals())

    @apply
    def transcribe_next_command():
        def fget(self):
            return self._transcribe_next_command
        def fset(self, transcribe_next_command):
            assert isinstance(transcribe_next_command, bool)
            self._transcribe_next_command = transcribe_next_command
        return property(**locals())

    @apply
    def underscore_delimited_current_score_name():
        def fget(self):
            return self._underscore_delimited_current_score_name
        def fset(self, underscore_delimited_current_score_name):
            assert isinstance(underscore_delimited_current_score_name, (str, type(None)))
            self._underscore_delimited_current_score_name = underscore_delimited_current_score_name
        return property(**locals())

    @apply
    def use_current_user_input_values_as_default():
        def fget(self):
            return self._use_current_user_input_values_as_default
        def fset(self, use_current_user_input_values_as_default):
            assert isinstance(use_current_user_input_values_as_default, bool)
            self._use_current_user_input_values_as_default = use_current_user_input_values_as_default
        return property(**locals())

    @apply
    def user_input():
        def fget(self):
            return self._user_input
        def fset(self, user_input):
            assert isinstance(user_input, (str, type(None)))
            self._user_input = user_input
            if isinstance(user_input, str):
                self._session_once_had_user_input = True
        return property(**locals())

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
            self.transcript.write_to_disk()

    def format_breadcrumb_stack(self):
        if not self._breadcrumb_stack:
            return ''
        result_lines = [self._breadcrumb_stack[0]]
        hanging_indent_width = len(stringtools.strip_diacritics_from_binary_string(
            self._breadcrumb_stack[0]))
        hanging_indent_width += len(' - ')
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

    def show_active_scores(self):
        self._scores_to_show = 'active'

    def show_all_scores(self):
        self._scores_to_show = 'all'

    def show_mothballed_scores(self):
        self._scores_to_show = 'mothballed'

    def swap_user_input_values_default_status(self):
        current = self.use_current_user_input_values_as_default
        self.use_current_user_input_values_as_default = not current
