# -*- encoding: utf-8 -*-
import abc
import os
import readline
import types
from abjad.tools import stringtools
from abjad.tools.systemtools.IOManager import IOManager


class IOManager(IOManager):
    r'''IO manager.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> io_manager = score_manager._session.io_manager

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        from scoremanager import core
        self._session = session
        self._configuration = core.ScoreManagerConfiguration()
        self.__score_package_wrangler = None

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

    ### PRIVATE PROPERTIES ###

    @property
    def _score_package_wrangler(self):
        from scoremanager import wranglers
        if self.__score_package_wrangler is None:
            wrangler = wranglers.ScorePackageWrangler(session=self._session)
            self.__score_package_wrangler = wrangler
        return self.__score_package_wrangler

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    ### PRIVATE METHODS ###

    def _assign_user_input(self, pending_user_input=None):
        if pending_user_input is not None:
            if self._session.pending_user_input:
                self._session._pending_user_input = \
                    pending_user_input + ' ' + \
                    self._session.pending_user_input
            else:
                self._session._pending_user_input = pending_user_input

    @staticmethod
    def _get_one_line_menu_summary(expr):
        if isinstance(expr, (types.ClassType, abc.ABCMeta, types.TypeType)):
            return expr.__name__
        elif getattr(expr, '_one_line_menu_summary', None):
            return expr._one_line_menu_summary
        elif isinstance(expr, str):
            return expr
        else:
            return repr(expr)

    def _handle_io_manager_directive(self, directive):
        if isinstance(directive, list) and len(directive) == 1:
            key = directive[0]
        else:
            key = directive
        if key in ('b', 'back'):
            self._session._is_backtracking_locally = True
            self._session._hide_hidden_commands = True
        elif key == 'd' and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_distribution_directory = True
            return 'd'
        elif key == 'g' and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_score_segments = True
            return 'g'
        elif key == 'k' and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_score_makers = True
            return 'k'
        elif key == 'llro':
            self.view_last_log()
        elif key == 'm' and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_score_materials = True
            return 'm'
        elif key == '>>':
            self._session._is_navigating_to_score_materials = True
            self._session._is_navigating_to_next_material = True
            self._session._hide_hidden_commands = True
        elif key == '<<':
            self._session._is_navigating_to_score_materials = True
            self._session._is_navigating_to_previous_material = True
            self._session._hide_hidden_commands = True
        elif directive in ('n', '?') and \
            not self._session.is_in_confirmation_environment and \
            not self._session.is_in_editor:
            self._session.toggle_hidden_commands()
        elif key == 'sdv':
            self._session.display_variables()
        elif key == 'p' and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_score_setup = True
            return 'p'
        elif key == 'pyd':
            message = 'running doctest ...'
            self.display([message, ''])
            controller = self._session.current_controller
            controller.doctest()
        elif key == 'pyt':
            message = 'running py.test ...'
            self.display([message, ''])
            controller = self._session.current_controller
            controller.pytest()
        elif key == 'pyi':
            self.exec_statement()
        elif key in ('q', 'quit'):
            self._session._is_quitting = True
            self._session._hide_hidden_commands = True
        elif key == 'sce':
            self.edit_calling_code()
        elif key == 'scl':
            self.display_calling_code_line_number()
        elif key == '>':
            self._session._is_navigating_to_next_score = True
            self._session._is_backtracking_to_score_manager = True
            self._session._hide_hidden_commands = True
        elif key == '<':
            self._session._is_navigating_to_previous_score = True
            self._session._is_backtracking_to_score_manager = True
            self._session._hide_hidden_commands = True
        elif key == 'u' and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_build_directory = True
            return 'u'
        elif self._is_score_string(key) and self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._hide_hidden_commands = True
        elif key == 'y' and \
            not self._session.is_in_confirmation_environment and \
            not self._session.is_in_editor:
            self._session._is_navigating_to_score_stylesheets = True
            return 'y'
        elif key == 'Y':
            self.edit_score_stylesheet()
        elif self._is_score_string(key) and not self._session.is_in_score:
            directive = None
        elif self._is_home_string(key):
            self._session._current_score_snake_case_name = None
            self._session._is_backtracking_to_score_manager = True
            self._session._hide_hidden_commands = True
        else:
            return directive

    @staticmethod
    def _is_home_string(string):
        if isinstance(string, str):
            if 3 <= len(string) and 'home'.startswith(string):
                return True
            elif string == 'h':
                return True
        return False

    @staticmethod
    def _is_score_string(string):
        if isinstance(string, str):
            if 3 <= len(string) and 'score'.startswith(string):
                return True
            elif string == 's':
                return True
        return False

    def _make_tab(self, n):
        return 4 * n * ' '

    def _pop_from_pending_user_input(self):
        self._session._last_command_was_composite = False
        if self._session.pending_user_input is None:
            return None
        elif self._session._pending_user_input == '':
            self._session._pending_user_input = None
            return None
        elif self._session.pending_user_input.startswith('{{'):
            index = self._session.pending_user_input.find('}}')
            user_input = self._session.pending_user_input[2:index]
            pending_user_input = self._session.pending_user_input[index+2:]
            pending_user_input = pending_user_input.strip()
            self._session._last_command_was_composite = True
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
        self._session._pending_user_input = pending_user_input
        return user_input

    def _read_cache(self):
        start_menu_entries = []
        if os.path.exists(self._configuration.cache_file_path):
            path = self._configuration.cache_file_path
            with file(path, 'r') as file_pointer:
                cache_lines = file_pointer.read()
            try:
                exec(cache_lines)
            except SyntaxError:
                pass
        return start_menu_entries

    ### PUBLIC METHODS ###

    def clear_terminal(self):
        r'''Clears terminal.

        Only clears terminal if session is displayable.

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
        getter = self.make_getter(
            where=None, 
            include_newlines=False,
            )
        getter.append_yes_no_string(prompt_string)
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
            self._session.transcript._append_entry(lines)
        if self._session.is_displayable:
            if clear_terminal:
                self.clear_terminal()
            for line in lines:
                print line

    def display_calling_code_line_number(self):
        r'''Displays calling code line number.

        Returns none.
        '''
        lines = []
        where = self._session.where
        if where is not None:
            file_path = where[1]
            file_name = os.path.basename(file_path)
            line = '{}   file: {}'.format(self._make_tab(1), file_name)
            lines.append(line)
            line = '{} method: {}'.format(self._make_tab(1), where[3])
            lines.append(line)
            line = '{}   line: {}'.format(self._make_tab(1), where[2])
            lines.append(line)
            lines.append('')
            self.display(lines, capitalize_first_character=False)
            self._session._hide_next_redraw = True
        else:
            message = 'source code tracking is not turned on.'
            self.display([message, ''])

    def edit(self, file_path, line_number=None):
        r'''Edits `file_path`.

        Returns none.
        '''
        if not os.path.isfile(file_path):
            return
        if line_number is None:
            command = 'vim + {}'.format(file_path)
        else:
            command = 'vim +{} {}'.format(line_number, file_path)
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        self.spawn_subprocess(command)

    def edit_calling_code(self):
        r'''Edits calling code.

        Returns none.
        '''
        where = self._session.where
        if where is not None:
            file_path = where[1]
            line_number = where[2]
            self.open_file(
                file_path,
                line_number=line_number,
                )
        else:
            self.display([message, ''])
            self._session._hide_next_redraw = True

    def edit_score_stylesheet(self):
        r'''Edits current stylesheet.

        Returns none.
        '''
        if not self._session.is_in_score:
            return
        directory = self._session.current_score_directory_path
        stylesheets_directory = os.path.join(directory, 'stylesheets')
        found_score_stylesheet = False
        for directory_entry in os.listdir(stylesheets_directory):
            if directory_entry.endswith('stylesheet.ily'):
                found_score_stylesheet = True
                break
        if found_score_stylesheet:
            file_path = os.path.join(stylesheets_directory, directory_entry)
            self.edit(file_path)
        else:
            message = 'no file ending in *stylesheet.ily found.'
            self.proceed(message)

    def exec_statement(self, statement=None):
        r'''Executes `statement`.

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
        self._session._hide_next_redraw = True

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

        Appends user input to IO transcript.

        Returns command selected by user.
        '''
        if default_value in (None, 'None'):
            default_value = ''
        readline.set_startup_hook(lambda: readline.insert_text(default_value))
        found_default_token = False
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
                if user_input == 'default':
                    found_default_token = True
            if self._session.transcribe_next_command:
                if found_default_token:
                    self._session.command_history.append('')
                else:
                    self._session.command_history.append(user_input)
            if user_input == '.':
                last_semantic_command = self._session.last_semantic_command
                user_input = last_semantic_command
            if self._session.transcribe_next_command:
                if found_default_token:
                    menu_chunk = [prompt_string.strip()]
                    if include_newline:
                        if not user_input == 'help':
                            menu_chunk.append('')
                    self._session.transcript._append_entry(menu_chunk)
                    menu_chunk = ['> ']
                    if include_newline:
                        if not user_input == 'help':
                            menu_chunk.append('')
                    self._session.transcript._append_entry(menu_chunk)
                else:
                    menu_chunk = []
                    menu_chunk.append('{}{}'.format(prompt_string, user_input))
                    if include_newline:
                        if not user_input == 'help':
                            menu_chunk.append('')
                    self._session.transcript._append_entry(menu_chunk)
            return user_input
        finally:
            readline.set_startup_hook()

    def make_getter(
        self, 
        where=None, 
        allow_none=False,
        include_newlines=False,
        ):
        r'''Makes getter.

        Returns getter.
        '''
        from scoremanager import iotools
        getter = iotools.UserInputGetter(
            where=where, 
            session=self._session,
            allow_none=allow_none,
            include_newlines=include_newlines,
            )
        return getter

    def make_menu(
        self, 
        where=None, 
        name=None,
        include_default_hidden_sections=True,
        ):
        r'''Makes menu.

        Returns menu.
        '''
        from scoremanager import iotools
        menu = iotools.Menu(
            where=where, 
            session=self._session,
            name=name,
            include_default_hidden_sections=include_default_hidden_sections,
            )
        return menu

    def make_selector(
        self, 
        where=None,
        items=None,
        ):
        r'''Makes selector.

        Returns selector.
        '''
        from scoremanager import iotools
        selector = iotools.Selector(
            where=where,
            session=self._session,
            items=items,
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

    def open_file(self, file_path, application=None, line_number=None):
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
            line_number=line_number,
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

    def view(self, file_path):
        r'''Views `file_path`.

        Also works when `file_path` is a list of PDFs.

        Returns none.
        '''
        if not isinstance(file_path, list) and not os.path.isfile(file_path):
            return
        if isinstance(file_path, list) and \
            all(x.endswith('.pdf') for x in file_path):
            file_paths = file_path
            file_paths = ' '.join(file_paths)
            command = 'open {}'.format(file_paths)
        elif isinstance(file_path, list):
            file_paths = file_path
            file_paths = ' '.join(file_paths)
            command = 'vim {}'.format(file_paths)
        elif file_path.endswith('.pdf'):
            command = 'open {}'.format(file_path)
        else:
            command = 'vim -R {}'.format(file_path)
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        self.spawn_subprocess(command)

    def view_last_log(self):
        r'''Views last LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.view_last_log()

    def write_cache(self, prompt=True):
        r'''Writes cache.

        Returns none.
        '''
        lines = []
        lines.append(self._unicode_directive + '\n')
        lines.append('\n\n')
        lines.append('start_menu_entries = [\n')
        wrangler = self._score_package_wrangler
        menu_entries = wrangler._make_asset_menu_entries(
            include_asset_name=False,
            include_year=True,
            sort_by_annotation=True, 
            )
        for menu_entry in menu_entries:
            lines.append('{},\n'.format(menu_entry))
        lines.append(']\n')
        cache_file_path = self._configuration.cache_file_path
        with file(cache_file_path, 'w') as cache_file_pointer:
            lines = ''.join(lines)
            cache_file_pointer.write(lines)
        if prompt:
            message = 'cache written.'
            self.proceed(message)