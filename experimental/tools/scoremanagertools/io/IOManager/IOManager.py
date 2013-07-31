# -*- encoding: utf-8 -*-
import abc
import os
import readline
import types
from abjad.tools import iotools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class IOManager(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, session=None):
        self._session = session

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session

    ### PUBLIC METHODS ###

    def assign_user_input(self, pending_user_input=None):
        if pending_user_input is not None:
            if self.session.pending_user_input:
                self.session.pending_user_input = \
                    pending_user_input + ' ' + \
                    self.session.pending_user_input
            else:
                self.session.pending_user_input = pending_user_input

    def clear_terminal(self):
        if not self.session.hide_next_redraw:
            if self.session.is_displayable:
                iotools.clear_terminal()

    def confirm(self, prompt_string='ok?', include_chevron=False):
        getter = self.make_getter(where=None)
        getter.append_yes_no_string(prompt_string)
        getter.include_newlines = False
        result = getter._run(include_chevron=include_chevron)
        if self.session.backtrack():
            return
        return 'yes'.startswith(result.lower())

    def display(self, lines, capitalize_first_character=True):
        assert isinstance(lines, (str, list))
        if isinstance(lines, str):
            lines = [lines]
        if not self.session.hide_next_redraw:
            if capitalize_first_character:
                lines = [stringtools.capitalize_string_start(line) 
                    for line in lines]
            if lines:
                if self.session.transcribe_next_command:
                    self.session.io_transcript.append_lines(lines)
            if self.session.is_displayable:
                for line in lines:
                    print line

    @staticmethod
    def get_one_line_menuing_summary(expr):
        if isinstance(expr, (types.ClassType, abc.ABCMeta, types.TypeType)):
            return expr.__name__
        elif getattr(expr, '_one_line_menuing_summary', None):
            return expr._one_line_menuing_summary
        elif isinstance(expr, str):
            return expr
        else:
            return repr(expr)

    def handle_hidden_menu_section_return_value(self, directive):
        if isinstance(directive, list) and len(directive) == 1:
            key = directive[0]
        else:
            key = directive
        if key in ('b', 'back'):
            self.session.is_backtracking_locally = True
        elif key == 'exec':
            self.interactively_exec_statement()
        elif key == 'here':
            self.interactively_edit_calling_code()
        elif key == 'next':
            self.session.is_navigating_to_next_score = True
            self.session.is_backtracking_to_score_manager = True
        elif key == 'prev':
            self.session.is_navigating_to_prev_score = True
            self.session.is_backtracking_to_score_manager = True
        elif key in ('q', 'quit'):
            self.session.user_specified_quit = True
#        # TODO: make this redraw!
#        elif key == 'r':
#            pass
        elif isinstance(key, str) and \
            3 <= len(key) and 'score'.startswith(key):
            if self.session.is_in_score:
                self.session.is_backtracking_to_score = True
        elif isinstance(key, str) and \
            3 <= len(key) and 'home'.startswith(key):
            self.session.is_backtracking_to_score_manager = True
        elif key == 'twt':
            self.session.enable_where = not self.session.enable_where
        else:
            return directive

    def handle_raw_input(self, 
        prompt_string, 
        include_chevron=True, 
        include_newline=True, 
        prompt_character='>',
        capitalize_prompt=True,
        ):
        if capitalize_prompt:
            prompt_string = stringtools.capitalize_string_start(prompt_string)
        if include_chevron:
            prompt_string = prompt_string + prompt_character + ' '
        else:
            prompt_string = prompt_string + ' '
        if self.session.is_displayable:
            user_input = raw_input(prompt_string)
            if include_newline:
                if not user_input == 'help':
                    print ''
        else:
            user_input = self.pop_from_pending_user_input()
        if self.session.transcribe_next_command:
            self.session.command_history.append(user_input)
        if user_input == '.':
            last_semantic_command = self.session.last_semantic_command
            user_input = last_semantic_command
        if self.session.transcribe_next_command:
            menu_chunk = []
            menu_chunk.append('{}{}'.format(prompt_string, user_input))
            if include_newline:
                if not user_input == 'help':
                    menu_chunk.append('')
            self.session.io_transcript.append_lines(menu_chunk)
        return user_input

    def handle_raw_input_with_default(self, 
        prompt_string, 
        default_value=None, 
        include_chevron=True, 
        include_newline=True,
        prompt_character='>', 
        capitalize_prompt=True,
        ):
        if default_value in (None, 'None'):
            default_value = ''
        readline.set_startup_hook(lambda: readline.insert_text(default_value))
        try:
            return self.handle_raw_input(
                prompt_string, 
                include_chevron=include_chevron,
                include_newline=include_newline, 
                prompt_character=prompt_character,
                capitalize_prompt=capitalize_prompt,
                )
        finally:
            readline.set_startup_hook()

    def interactively_exec_statement(self):
        lines = []
        statement = self.handle_raw_input('XCF', include_newline=False)
        command = 'from abjad import *'
        exec(command)
        try:
            result = None
            command = 'result = {}'.format(statement)
            exec(command)
            lines.append('{!r}'.format(result))
        except:
            lines.append('expression not executable.')
        lines.append('')
        self.display(lines)
        self.session.hide_next_redraw = True

    def make_default_hidden_section(self):
        from experimental.tools import scoremanagertools
        hidden_section = scoremanagertools.io.MenuSection()
        hidden_section.return_value_attribute = 'key'
        hidden_section.is_hidden = True
        hidden_section.append(('back', 'b'))
        hidden_section.append(('exec statement', 'exec'))
        hidden_section.append(('edit client source', 'here'))
        hidden_section.append(('display hidden menu section', 'hidden'))
        hidden_section.append(('home', 'home'))
        hidden_section.append(('next score', 'next'))
        hidden_section.append(('prev score', 'prev'))
        hidden_section.append(('quit', 'q'))
        hidden_section.append(('redraw', 'r'))
        hidden_section.append(('current score', 'score'))
        hidden_section.append(('toggle menu commands', 'tmc'))
        hidden_section.append(('toggle where-tracking', 'twt'))
        hidden_section.append(('display calling code line number', 'where'))
        return hidden_section

    def make_getter(self, where=None):
        from experimental.tools import scoremanagertools
        return scoremanagertools.io.UserInputGetter(
            where=where, session=self.session)

    def make_menu(self, where=None):
        from experimental.tools import scoremanagertools
        return scoremanagertools.io.Menu(
            where=where, session=self.session)

    def pop_from_pending_user_input(self):
        self.session.last_command_was_composite = False
        if self.session.pending_user_input is None:
            return None
        elif self.session.pending_user_input == '':
            self.session.pending_user_input = None
            return None
        elif self.session.pending_user_input.startswith('{{'):
            index = self.session.pending_user_input.find('}}')
            user_input = self.session.pending_user_input[2:index]
            pending_user_input = self.session.pending_user_input[index+2:]
            pending_user_input = pending_user_input.strip()
            self.session.last_command_was_composite = True
        else:
            user_input_parts = self.session.pending_user_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(user_input_parts):
                if not part.endswith((',', '-')):
                    break
            first_parts = user_input_parts[:i+1]
            rest_parts = user_input_parts[i+1:]
            user_input = ' '.join(first_parts)
            pending_user_input = ' '.join(rest_parts)
        user_input = user_input.replace('~', ' ')
        self.session.pending_user_input = pending_user_input
        return user_input

    def print_not_yet_implemented(self):
        self.display(['not yet implemented', ''])
        self.proceed()

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
        self.handle_raw_input(
            'press return to continue.', include_chevron=False)
        if self.session.is_displayable:
            iotools.clear_terminal()
