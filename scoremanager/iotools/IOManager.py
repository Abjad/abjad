# -*- encoding: utf-8 -*-
import abc
import os
import readline
import types
from abjad.tools import stringtools
from abjad.tools.systemtools.IOManager import IOManager


class IOManager(IOManager):
    r'''Manages Abjad IO.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> io_manager = score_manager._session.io_manager

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        from scoremanager import core
        self._session = session
        self._configuration = core.ScoreManagerConfiguration()
        self._score_package_wrangler = \
            wranglers.ScorePackageWrangler(session=self._session)

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of IO manager.

        ..  container:: example

            ::

                >>> io_manager
                IOManager()

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PUBLIC PROPERTIES ###

    @property
    def configuration(self):
        r'''Gets configuration of IO manager.

        Returns configuration.
        '''
        return self._configuration

    ### PRIVATE METHODS ###

    def _assign_user_input(self, pending_user_input=None):
        if pending_user_input is not None:
            if self._session.pending_user_input:
                self._session.pending_user_input = \
                    pending_user_input + ' ' + \
                    self._session.pending_user_input
            else:
                self._session.pending_user_input = pending_user_input

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
            self._session.is_backtracking_locally = True
        elif key == 'pyd':
            message = 'running doctest ...'
            self.display([message, ''])
            controller = self._session.current_controller
            controller.run_doctest()
        elif key == 'pyt':
            message = 'running py.test ...'
            self.display([message, ''])
            controller = self._session.current_controller
            controller.run_pytest()
        elif key == 'pyi':
            self.interactively_exec_statement()
        elif key == 'lvl':
            self.view_last_log()
        elif key == 'next':
            self._session.is_navigating_to_next_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key == 'prev':
            self._session.is_navigating_to_previous_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key in ('q', 'quit'):
            self._session.is_quitting = True
        elif self._is_score_string(key) and self._session.is_in_score:
            self._session.is_backtracking_to_score = True
        elif self._is_score_string(key) and not self._session.is_in_score:
            directive = None
        elif self._is_home_string(key):
            self._session.is_backtracking_to_score_manager = True
        elif key == 'sct':
            self.toggle_location_tracking()
        else:
            return directive

    @staticmethod
    def _is_score_string(string):
        if isinstance(string, str):
            if 3 <= len(string) and 'score'.startswith(string):
                return True
            elif string == 's':
                return True
        return False

    @staticmethod
    def _is_home_string(string):
        if isinstance(string, str):
            if 3 <= len(string) and 'home'.startswith(string):
                return True
            elif string == 'h':
                return True
        return False

    def _make_initializer_menu_section(self, menu, has_initializer=True):
        if not has_initializer:
            command_section = menu.make_command_section()
            command_section.title = "package has no initializer: use 'ins'."
        section = menu.make_command_section(
            is_secondary=True,
            match_on_display_string=False,
            )
        section.append(('initializer module - boilerplate', 'inbp'))
        section.append(('initializer module - remove', 'inrm'))
        section.append(('initializer module - stub', 'ins'))
        section.append(('initializer module - view', 'inv'))

    def _make_metadata_menu_section(self, menu):
        section = menu.make_command_section(
            is_secondary=True,
            match_on_display_string=False,
            )
        section.append(('metadata - add', 'mda'))
        section.append(('metadata - get', 'mdg'))
        section.append(('metadata - remove', 'mdrm'))
        return section

    def _make_metadata_module_menu_section(self, menu):
        section = menu.make_command_section(
            is_secondary=True,
            match_on_display_string=False,
            )
        section.append(('metadata module - remove', 'mdmrm'))
        section.append(('metadata module - rewrite', 'mdmrw'))
        section.append(('metadata module - view', 'mdmv'))
        return section

    def _make_views_menu_section(self, menu):
        section = menu.make_command_section(
            is_secondary=True,
            match_on_display_string=False,
            )
        section.append(('views - list', 'vwl'))
        section.append(('views - new', 'vwn'))
        section.append(('views - select', 'vws'))
        return section

    def _make_views_module_menu_section(self, menu):
        section = menu.make_command_section(
            is_secondary=True,
            match_on_display_string=False,
            )
        section.append(('views module - remove', 'vwmrm'))
        section.append(('views module - view', 'vwmv'))
        return section

    def _pop_from_pending_user_input(self):
        self._session.last_command_was_composite = False
        if self._session.pending_user_input is None:
            return None
        elif self._session.pending_user_input == '':
            self._session.pending_user_input = None
            return None
        elif self._session.pending_user_input.startswith('{{'):
            index = self._session.pending_user_input.find('}}')
            user_input = self._session.pending_user_input[2:index]
            pending_user_input = self._session.pending_user_input[index+2:]
            pending_user_input = pending_user_input.strip()
            self._session.last_command_was_composite = True
        else:
            user_input_parts = self._session.pending_user_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(user_input_parts):
                if not part.endswith((',', '-')):
                    break
            first_parts = user_input_parts[:i+1]
            rest_parts = user_input_parts[i+1:]
            user_input = ' '.join(first_parts)
            pending_user_input = ' '.join(rest_parts)
        user_input = user_input.replace('~', ' ')
        self._session.pending_user_input = pending_user_input
        return user_input

    def _read_cache(self):
        start_menu_entries = []
        if os.path.exists(self.configuration.cache_file_path):
            with file(self.configuration.cache_file_path, 'r') as file_pointer:
                cache_lines = file_pointer.read()
            try:
                exec(cache_lines)
            except SyntaxError:
                pass
        return start_menu_entries

    ### PUBLIC METHODS ###

    def clear_terminal(self):
        r'''Clears terminal.

        Only clears terminal is _session is displayable.

        Returns none.
        '''
        if not self._session.hide_next_redraw:
            if self._session.is_displayable:
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
        if self._session._backtrack():
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
        if self._session.hide_next_redraw:
            return
        if capitalize_first_character:
            lines = [
                stringtools.capitalize_string_start(line) 
                for line in lines
                ]
        if lines and self._session.transcribe_next_command:
            self._session.io_transcript.append_lines(lines)
        if self._session.is_displayable:
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
            if self._session.is_displayable:
                user_input = raw_input(prompt_string)
                if include_newline:
                    if not user_input == 'help':
                        print ''
            else:
                user_input = self._pop_from_pending_user_input()
            if self._session.transcribe_next_command:
                self._session.command_history.append(user_input)
            if user_input == '.':
                last_semantic_command = self._session.last_semantic_command
                user_input = last_semantic_command
            if self._session.transcribe_next_command:
                menu_chunk = []
                menu_chunk.append('{}{}'.format(prompt_string, user_input))
                if include_newline:
                    if not user_input == 'help':
                        menu_chunk.append('')
                self._session.io_transcript.append_lines(menu_chunk)
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
        prompt = True
        if statement is None:
            statement = self.handle_user_input('>>', include_newline=False)
        else:
            prompt = False
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
        if prompt:
            self.display(lines)
        self._session.hide_next_redraw = True

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
            session=self._session,
            )
        return getter

    def make_menu(self, where=None, include_default_hidden_sections=True):
        r'''Makes menu.

        Returns menu.
        '''
        from scoremanager import iotools
        menu = iotools.Menu(
            where=where, 
            session=self._session,
            include_default_hidden_sections=include_default_hidden_sections,
            )
        return menu

    def make_selector(self, where=None):
        r'''Makes selector.

        Returns selector.
        '''
        from scoremanager import iotools
        selector = iotools.Selector(
            where=where,
            session=self._session,
            )
        return selector

    def make_view(self, tokens):
        r'''Makes view.

        Returns view.
        '''
        from scoremanager import iotools
        view = iotools.View(
            tokens=tokens,
            )
        return view

    def open_file(self, file_path, application=None):
        r'''Opens `file_path`.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        if not os.path.isfile(file_path):
            return
        return systemtools.IOManager.open_file(
            file_path,
            application=application,
            )

    def print_not_yet_implemented(self):
        r'''Prints not-yet-implemented message.

        Prompts user to proceed.

        Returns none.
        '''
        self.display(['not yet implemented', ''])
        self.proceed()

    def proceed(self, message=None, prompt=True):
        r'''Prompts user to proceed.

        Clears terminal.

        Returns none.
        '''
        message = message or 'press return to continue.'
        assert isinstance(message, str)
        if not prompt:
            return
        self.handle_user_input(
            message,
            include_chevron=False,
            )
        self.clear_terminal()

    def toggle_location_tracking(self):
        if self._session.enable_where:
            self._session.enable_where = False
            message = 'source code tracking off.'
        else:
            self._session.enable_where = True
            message = 'source code tracking on.'
        self._session.io_manager.proceed(message)

    def write_cache(self, prompt=True):
        cache_file_path = self.configuration.cache_file_path
        cache_file_pointer = file(cache_file_path, 'w')
        cache_file_pointer.write('# -*- encoding: utf-8 -*-\n')
        cache_file_pointer.write('\n\n')
        cache_file_pointer.write('start_menu_entries = [\n')
        menu_entries = self._score_package_wrangler._make_asset_menu_entries()
        for menu_entry in menu_entries:
            cache_file_pointer.write('{},\n'.format(menu_entry))
        cache_file_pointer.write(']\n')
        cache_file_pointer.close()
        if prompt:
            message = 'cache written.'
            self.proceed(message)
