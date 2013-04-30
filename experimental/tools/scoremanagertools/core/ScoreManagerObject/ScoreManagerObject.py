import abc
import inspect
import os
import pprint
import readline
import sys
import types
from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import filesystemtools
from experimental.tools.scoremanagertools.core.ScoreManagerConfiguration import \
    ScoreManagerConfiguration


class ScoreManagerObject(AbjadObject):

    ### CLASS ATTRIBUTES ###

    configuration = ScoreManagerConfiguration()

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.core.Session()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return

    @property
    def _human_readable_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(self._class_name)

    @property
    def _spaced_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(self._class_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session

    @property
    def transcript_signature(self):
        return self.session.complete_transcript.signature

    ### PUBLIC METHODS ###

    # TODO: migrate to [menuing.]IO class
    def assign_user_input(self, user_input=None):
        if user_input is not None:
            if self.session.user_input:
                self.session.user_input = user_input + ' ' + self.session.user_input
            else:
                self.session.user_input = user_input

    # TODO: move to Session
    def backtrack(self, source=None):
        return self.session.backtrack(source=source)

    # TODO: move to Session
    def cache_breadcrumbs(self, cache=False):
        if cache:
            self.session.breadcrumb_cache_stack.append(self.session._breadcrumb_stack[:])
            self.session._breadcrumb_stack[:] = []

    # TODO: migrate to [menuing.]IO class
    def conditionally_clear_terminal(self):
        if self.session.is_displayable:
            iotools.clear_terminal()

    # TODO: migrate to [menuing.]IO class
    def confirm(self, prompt_string='ok?', include_chevron=False):
        getter = self.make_getter(where=self.where())
        getter.append_yes_no_string(prompt_string)
        getter.include_newlines = False
        result = getter.run(include_chevron=include_chevron)
        if self.backtrack():
            return
        return 'yes'.startswith(result.lower())

    # TODO: move to ScoreManagerConfiguration ... or eliminate?
    def directory_path_to_package_path(self, directory_path):
        if directory_path is None:
            return
        directory_path = os.path.normpath(directory_path)
        if directory_path.endswith('.py'):
            directory_path = directory_path[:-3]
        if directory_path.startswith(self.configuration.score_manager_tools_directory_path):
            prefix_length = len(os.path.dirname(self.configuration.score_manager_tools_directory_path)) + 1
        elif directory_path.startswith(self.configuration.score_external_materials_directory_path):
            prefix_length = \
                len(os.path.dirname(self.configuration.score_external_materials_directory_path)) + 1
        elif directory_path.startswith(self.configuration.score_external_segments_directory_path):
            prefix_length = len(os.path.dirname(self.configuration.score_external_segments_directory_path)) + 1
        elif directory_path.startswith(self.configuration.score_external_specifiers_directory_path):
            prefix_length = \
                len(os.path.dirname(self.configuration.score_external_specifiers_directory_path)) + 1
        elif directory_path.startswith(self.configuration.scores_directory_path):
            prefix_length = len(self.configuration.scores_directory_path) + 1
        else:
            return
        package_path = directory_path[prefix_length:]
        package_path = package_path.replace(os.path.sep, '.')
        return package_path

    # TODO: migrate to [menuing.]IO class
    def display(self, lines, capitalize_first_character=True):
        assert isinstance(lines, (str, list))
        if isinstance(lines, str):
            lines = [lines]
        if not self.session.hide_next_redraw:
            if capitalize_first_character:
                lines = [stringtools.capitalize_string_start(line) for line in lines]
            if lines:
                if self.session.transcribe_next_command:
                    self.session.complete_transcript.append_lines(lines)
            if self.session.is_displayable:
                for line in lines:
                    print line

    # TODO: eventually remove after all configuration info is encapsulated somewhere
    def dot_join(self, expr):
        return '.'.join(expr)

    # TODO: move to somewhere in menuing package
    def get_one_line_menuing_summary(self, expr):
        if isinstance(expr, (types.ClassType, abc.ABCMeta)):
            return expr.__name__
        elif getattr(expr, 'one_line_menuing_summary', None):
            return expr.one_line_menuing_summary
        elif getattr(expr, '_one_line_menuing_summary', None):
            return expr._one_line_menuing_summary
        elif isinstance(expr, type(type)):
            return expr.__name__
        elif isinstance(expr, str):
            return expr
        else:
            return repr(expr)

    # TODO: remove or hoist to AbjadObject, as necessary
    def get_tools_package_qualified_repr(self, expr):
        return getattr(expr, '_tools_package_qualified_repr', repr(expr))

    # TODO: migrate to [menuing.]IO class
    def handle_raw_input(self, prompt, include_chevron=True, include_newline=True, prompt_character='>',
        capitalize_prompt=True):
        if capitalize_prompt:
            prompt = stringtools.capitalize_string_start(prompt)
        if include_chevron:
            prompt = prompt + prompt_character + ' '
        else:
            prompt = prompt + ' '
        if self.session.is_displayable:
            user_response = raw_input(prompt)
            if include_newline:
                if not user_response == 'help':
                    print ''
        else:
            user_response = self.pop_next_user_response_from_user_input()
        if self.session.transcribe_next_command:
            self.session.command_history.append(user_response)
        if user_response == '.':
            last_semantic_command = self.session.last_semantic_command
            user_response = last_semantic_command
        if self.session.transcribe_next_command:
            menu_chunk = []
            menu_chunk.append('{}{}'.format(prompt, user_response))
            if include_newline:
                if not user_response == 'help':
                    menu_chunk.append('')
            self.session.complete_transcript.append_lines(menu_chunk)
        return user_response

    # TODO: migrate to [menuing.]IO class
    def handle_raw_input_with_default(self, prompt, default=None, include_chevron=True, include_newline=True,
        prompt_character='>', capitalize_prompt=True):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(prompt, include_chevron=include_chevron,
                include_newline=include_newline, prompt_character=prompt_character,
                capitalize_prompt=capitalize_prompt)
        finally:
            readline.set_startup_hook()

    # TODO: migrate to [menuing.]IO class
    def make_getter(self, where=None):
        from experimental.tools import scoremanagertools
        return scoremanagertools.menuing.UserInputGetter(where=where, session=self.session)

    # TODO: migrate to [menuing.]IO class
    def make_menu(self, is_hidden=False, is_internally_keyed=False, is_keyed=True,
        is_numbered=False, is_parenthetically_numbered=False, is_ranged=False, where=None):
        from experimental.tools import scoremanagertools
        menu = scoremanagertools.menuing.Menu(where=where, session=self.session)
        section = menu.make_section(
            is_hidden=is_hidden, is_internally_keyed=is_internally_keyed, is_keyed=is_keyed,
            is_numbered=is_numbered, is_parenthetically_numbered=is_parenthetically_numbered,
            is_ranged=is_ranged)
        return menu, section

    # TODO: move to Session
    def pop_backtrack(self):
        return self.session.backtracking_stack.pop()

    # TODO: move to Session
    def pop_breadcrumb(self, rollback=True):
        if rollback:
            return self.session._breadcrumb_stack.pop()

    # TODO: migrate to [menuing.]IO class
    def pop_next_user_response_from_user_input(self):
        self.session.last_command_was_composite = False
        if self.session.user_input is None:
            return None
        elif self.session.user_input == '':
            self.session.user_input = None
            return None
        elif '\n' in self.session.user_input:
            raise ValueError('no longer implemented.')
        elif self.session.user_input.startswith('{{'):
            index = self.session.user_input.find('}}')
            user_response = self.session.user_input[2:index]
            user_input = self.session.user_input[index+2:].strip()
            self.session.last_command_was_composite = True
        else:
            user_input = self.session.user_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(user_input):
                if not part.endswith((',', '-')):
                    break
            first_parts = user_input[:i+1]
            rest_parts = user_input[i+1:]
            user_response = ' '.join(first_parts)
            user_input = ' '.join(rest_parts)
        user_response = user_response.replace('~', ' ')
        self.session.user_input = user_input
        return user_response

    # TODO: migrate to [menuing.]IO class
    def print_not_yet_implemented(self):
        self.display(['not yet implemented', ''])
        self.proceed()

    # TODO: migrate to [menuing.]IO class
    def proceed(self, lines=None, is_interactive=True):
        assert isinstance(lines, (tuple, list, str, type(None)))
        if not is_interactive:
            return
        if isinstance(lines, str):
            lines = [lines]
        elif lines is None:
            lines = []
        if lines:
            lines.append('')
            self.display(lines)
        self.handle_raw_input('press return to continue.', include_chevron=False)
        self.conditionally_clear_terminal()

    # TODO: move to Session
    def pprint_transcript(self):
        pprint.pprint(self.transcript)
        print len(self.transcript)

    # TODO: move to Session
    def push_backtrack(self):
        if self.session.backtracking_stack:
            last_number = self.session.backtracking_stack[-1]
            self.session.backtracking_stack.append(last_number + 1)
        else:
            self.session.backtracking_stack.append(0)

    # TODO: move to Session
    def push_breadcrumb(self, breadcrumb=None, rollback=True):
        if rollback:
            if breadcrumb is not None:
                self.session._breadcrumb_stack.append(breadcrumb)
            else:
                self.session._breadcrumb_stack.append(self.breadcrumb)

    def remove_package_path_from_sys_modules(self, package_path):
        '''Total hack. But works.'''
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_path, package_path)
        exec(command)

    # TODO: move to Session
    def restore_breadcrumbs(self, cache=False):
        if cache:
            self.session._breadcrumb_stack[:] = self.session.breadcrumb_cache_stack.pop()

    def where(self):
        if self.session.enable_where:
            return inspect.stack()[1]
