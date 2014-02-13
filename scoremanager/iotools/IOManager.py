# -*- encoding: utf-8 -*-
import abc
import os
import readline
import types
from abjad.tools import stringtools
from abjad.tools.systemtools.IOManager import IOManager


class IOManager(IOManager):
    r'''Manages Abjad IO.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        self._session = session

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        r'''Gets session.

        Returns session.
        '''
        return self._session

    ### PRIVATE METHODS ###

    def _assign_user_input(self, pending_user_input=None):
        if pending_user_input is not None:
            if self.session.pending_user_input:
                self.session.pending_user_input = \
                    pending_user_input + ' ' + \
                    self.session.pending_user_input
            else:
                self.session.pending_user_input = pending_user_input

    @staticmethod
    def _get_one_line_menuing_summary(expr):
        if isinstance(expr, (types.ClassType, abc.ABCMeta, types.TypeType)):
            return expr.__name__
        elif getattr(expr, '_one_line_menuing_summary', None):
            return expr._one_line_menuing_summary
        elif isinstance(expr, str):
            return expr
        else:
            return repr(expr)

    def _handle_hidden_menu_section_return_value(self, directive):
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
        elif key == 'log':
            self.view_last_log()
        elif key == 'next':
            self.session.is_navigating_to_next_score = True
            self.session.is_backtracking_to_score_manager = True
        elif key == 'prev':
            self.session.is_navigating_to_previous_score = True
            self.session.is_backtracking_to_score_manager = True
        elif key in ('q', 'quit'):
            self.session.user_specified_quit = True
#        # TODO: make this redraw!
#        elif key == 'r':
#            pass
        elif self._is_score_string(key):
            self.session.is_backtracking_to_score = True
        elif self._is_home_string(key):
            self.session.is_backtracking_to_score_manager = True
        elif key == 'twt':
            self.session.enable_where = not self.session.enable_where
        else:
            return directive

    @staticmethod
    def _is_score_string(string):
        if isinstance(string, str):
            if 3 <= len(string) and 'score'.startswith(string):
                return True
            elif string == 'S':
                return True
        return False

    @staticmethod
    def _is_home_string(string):
        if isinstance(string, str):
            if 3 <= len(string) and 'home'.startswith(string):
                return True
            elif string == 'H':
                return True
        return False

    def _make_initializer_menu_section(
        self, 
        main_menu, 
        hidden_section,
        has_initializer=True,
        ):
        if not has_initializer:
            command_section = main_menu.make_command_section()
            command_section.title = "package has no initializer: use 'ins'."
        hidden_section.append(('initializer - boilerplate', 'inbp'))
        hidden_section.append(('initializer - remove', 'inrm'))
        hidden_section.append(('initializer - stub', 'ins'))
        hidden_section.append(('initializer - view', 'inv'))

    def _pop_from_pending_user_input(self):
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

    ### PUBLIC METHODS ###

    def clear_terminal(self):
        r'''Clears terminal.

        Only clears terminal is session is displayable.

        Returns none.
        '''
        if not self.session.hide_next_redraw:
            if self.session.is_displayable:
                superclass = super(IOManager, self)
                superclass.clear_terminal()

    def confirm(
        self, 
        prompt_string='ok?', 
        clear_terminal=False,
        include_chevron=False,
        ):
        r'''Prompts user to confirm.

        Returns boolean.
        '''
        getter = self.make_getter(where=None)
        getter.append_yes_no_string(prompt_string)
        getter.include_newlines = False
        result = getter._run(
            clear_terminal=clear_terminal,
            include_chevron=include_chevron,
            )
        if self.session.backtrack():
            return
        return 'yes'.startswith(result.lower())

    def display(
        self, 
        lines, 
        capitalize_first_character=True,
        clear_terminal=False,
        ):
        r'''Displays `lines`.

        Clears terminal first.

        Returns none.
        '''
        assert isinstance(lines, (str, list))
        if isinstance(lines, str):
            lines = [lines]
        if not self.session.hide_next_redraw:
            if capitalize_first_character:
                lines = [
                    stringtools.capitalize_string_start(line) 
                    for line in lines
                    ]
            if lines:
                if self.session.transcribe_next_command:
                    self.session.io_transcript.append_lines(lines)
            if self.session.is_displayable:
                if clear_terminal:
                    self.clear_terminal()
                for line in lines:
                    print line

    def handle_user_input(
        self, 
        prompt_string, 
        default_value=None, 
        include_chevron=True, 
        include_newline=True,
        prompt_character='>', 
        capitalize_prompt=True,
        ):
        r'''Handles user input.

        Appends user input to command history.

        Appends user input to IO transscript.

        Returns command selected by user.
        '''
        if default_value in (None, 'None'):
            default_value = ''
        readline.set_startup_hook(lambda: readline.insert_text(default_value))
        try:
            if capitalize_prompt:
                prompt_string = stringtools.capitalize_string_start(
                    prompt_string)
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
                user_input = self._pop_from_pending_user_input()
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
        finally:
            readline.set_startup_hook()

    def interactively_edit(self, file_path, line_number=None):
        r'''Interactively edits `file_path`.

        Returns none.
        '''
        if not os.path.isfile(file_path):
            return
        if line_number is None:
            command = 'vim + {}'.format(file_path)
        else:
            command = 'vim +{} {}'.format(line_number, file_path)
        self.spawn_subprocess(command)

    def interactively_exec_statement(self, statement=None):
        r'''Interactively executes `statement`.

        Hides next redraw.

        Returns none.
        '''
        lines = []
        is_interactive = True
        if statement is None:
            statement = self.handle_user_input('XCF', include_newline=False)
        else:
            is_interactive = False
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
        if is_interactive:
            self.display(lines)
        self.session.hide_next_redraw = True

    def interactively_view(self, file_path):
        r'''Interactively views `file_path`.

        Returns none.
        '''
        if not os.path.isfile(file_path):
            return
        if file_path.endswith('.pdf'):
            command = 'open {}'.format(file_path)
        else:
            command = 'vim -R {}'.format(file_path)
        self.spawn_subprocess(command)

    def make_getter(self, where=None):
        r'''Makes getter.

        Returns getter.
        '''
        from scoremanager import iotools
        getter = iotools.UserInputGetter(
            where=where, 
            session=self.session,
            )
        return getter

    def make_menu(self, where=None):
        r'''Makes menu.

        Returns menu.
        '''
        from scoremanager import iotools
        menu = iotools.Menu(
            where=where, 
            session=self.session,
            )
        return menu

    def make_selector(self, where=None):
        r'''Makes selector.

        Returns selector.
        '''
        from scoremanager import iotools
        selector = iotools.Selector(
            where=where,
            session=self.session,
            )
        return selector

    def make_view(self, tokens, custom_identifier=None):
        r'''Makes view.

        Returns view.
        '''
        from scoremanager import iotools
        view = iotools.View(
            tokens=tokens,
            custom_identifier=custom_identifier,
            )
        return view

    def print_not_yet_implemented(self):
        r'''Prints not-yet-implemented message.

        Prompts user to proceed.

        Returns none.
        '''
        self.display(['not yet implemented', ''])
        self.proceed()

    def proceed(self, lines=None, is_interactive=True):
        r'''Prompts user to proceed.

        Clears terminal.

        Returns none.
        '''
        assert isinstance(lines, (tuple, list, str, type(None)))
        if not is_interactive:
            return
        if isinstance(lines, str):
            lines = [lines]
        elif lines is None:
            lines = []
        if lines:
            if lines != ['']:
                lines.append('')
            self.display(lines)
        self.handle_user_input(
            'press return to continue.', 
            include_chevron=False,
            )
        self.clear_terminal()
