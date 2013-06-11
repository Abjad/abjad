import abc
import os
import readline
import types
from abjad.tools import iotools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class IO(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, session=None):
        self._session = session

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def session(self):
        return self._session

    ### PUBLIC METHODS ###

    def assign_user_input(self, user_input=None):
        if user_input is not None:
            if self._session.user_input:
                self._session.user_input = user_input + ' ' + \
                    self._session.user_input
            else:
                self._session.user_input = user_input

    def conditionally_clear_terminal(self):
        if self._session.is_displayable:
            iotools.clear_terminal()

    def confirm(self, prompt_string='ok?', include_chevron=False):
        getter = self.make_getter(where=None)
        getter.append_yes_no_string(prompt_string)
        getter.include_newlines = False
        result = getter._run(include_chevron=include_chevron)
        if self._session.backtrack():
            return
        return 'yes'.startswith(result.lower())

    def display(self, lines, capitalize_first_character=True):
        assert isinstance(lines, (str, list))
        if isinstance(lines, str):
            lines = [lines]
        if not self._session.hide_next_redraw:
            if capitalize_first_character:
                lines = [stringtools.capitalize_string_start(line) 
                    for line in lines]
            if lines:
                if self._session.transcribe_next_command:
                    self._session.transcript.append_lines(lines)
            if self._session.is_displayable:
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

    def handle_raw_input(self, 
        prompt, 
        include_chevron=True, 
        include_newline=True, 
        prompt_character='>',
        capitalize_prompt=True,
        ):
        if capitalize_prompt:
            prompt = stringtools.capitalize_string_start(prompt)
        if include_chevron:
            prompt = prompt + prompt_character + ' '
        else:
            prompt = prompt + ' '
        if self._session.is_displayable:
            user_response = raw_input(prompt)
            if include_newline:
                if not user_response == 'help':
                    print ''
        else:
            user_response = self.pop_next_user_response_from_user_input()
        if self._session.transcribe_next_command:
            self._session.command_history.append(user_response)
        if user_response == '.':
            last_semantic_command = self._session.last_semantic_command
            user_response = last_semantic_command
        if self._session.transcribe_next_command:
            menu_chunk = []
            menu_chunk.append('{}{}'.format(prompt, user_response))
            if include_newline:
                if not user_response == 'help':
                    menu_chunk.append('')
            self._session.transcript.append_lines(menu_chunk)
        return user_response

    def handle_raw_input_with_default(self, 
        prompt, 
        default=None, 
        include_chevron=True, 
        include_newline=True,
        prompt_character='>', 
        capitalize_prompt=True,
        ):
        if default in (None, 'None'):
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            return self.handle_raw_input(
                prompt, 
                include_chevron=include_chevron,
                include_newline=include_newline, 
                prompt_character=prompt_character,
                capitalize_prompt=capitalize_prompt,
                )
        finally:
            readline.set_startup_hook()

    def make_getter(self, where=None):
        from experimental.tools import scoremanagertools
        return scoremanagertools.menuing.UserInputGetter(
            where=where, session=self._session)

    def make_menu(self, 
        is_hidden=False, 
        is_internally_keyed=False, 
        is_keyed=True,
        is_numbered=False, 
        is_ranged=False, 
        is_modern=False,
        where=None,
        menu_tokens=None, 
        return_value_attribute='display_string',
        ):
        from experimental.tools import scoremanagertools
        menu = scoremanagertools.menuing.Menu(
            where=where, session=self._session)
        menu_section = menu.make_section(
            is_hidden=is_hidden,
            is_internally_keyed=is_internally_keyed,
            is_keyed=is_keyed,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            is_modern=is_modern,
            menu_tokens=menu_tokens,
            return_value_attribute=return_value_attribute,
            )
        return menu, menu_section

    def pop_next_user_response_from_user_input(self):
        self._session.last_command_was_composite = False
        if self._session.user_input is None:
            return None
        elif self._session.user_input == '':
            self._session.user_input = None
            return None
        elif '\n' in self._session.user_input:
            raise ValueError('no longer implemented.')
        elif self._session.user_input.startswith('{{'):
            index = self._session.user_input.find('}}')
            user_response = self._session.user_input[2:index]
            user_input = self._session.user_input[index+2:].strip()
            self._session.last_command_was_composite = True
        else:
            user_input = self._session.user_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(user_input):
                if not part.endswith((',', '-')):
                    break
            first_parts = user_input[:i+1]
            rest_parts = user_input[i+1:]
            user_response = ' '.join(first_parts)
            user_input = ' '.join(rest_parts)
        user_response = user_response.replace('~', ' ')
        self._session.user_input = user_input
        return user_response

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
        self.conditionally_clear_terminal()
