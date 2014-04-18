# -*- encoding: utf-8 -*-
import abc
import os
import subprocess
import readline
import types
from abjad.tools import datastructuretools
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.systemtools.IOManager import IOManager


class IOManager(IOManager):
    r'''IO manager.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> io_manager = score_manager._session.io_manager

    '''

    ### CLASS VARAIBLES ###

    __slots__ = (
        '_session',
        '_configuration',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import core
        self._session = session
        self._configuration = core.ScoreManagerConfiguration()

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
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    @property
    @systemtools.Memoize
    def _user_input_to_action(self):
        result = {
            'b': self._handle_backtrack_navigation_directive,
            'h': self._handle_home_navigation_directive,
            'q': self._handle_quit_directive,
            's': self._handle_score_navigation_directive,
            '?': self._handle_display_all_commands_directive,
            'n': self._handle_display_all_commands_directive,
            'llro': self.view_last_log,
            'pyd': self.doctest,
            'pyi': self.invoke_python,
            'pyt': self.pytest,
            'sdv': self._session.display_variables,
            'Y': self.edit_score_stylesheet,
            '>>': self._handle_next_score_directive,
            '<<': self._handle_previous_score_directive,
            '>': self._handle_next_sibling_asset_directive,
            '<': self._handle_previous_sibling_asset_directive,
            }
        return result

    @property
    @systemtools.Memoize
    def _wrangler_navigation_alias_to_action(self):
        result = {
            'd': self._handle_to_distribution_file_wrangler_directive,
            'g': self._handle_to_segment_package_wrangler_directive,
            'k': self._handle_to_maker_module_wrangler_directive,
            'm': self._handle_to_material_package_wrangler_directive,
            'u': self._handle_to_build_file_wrangler_directive,
            'y': self._handle_to_stylesheet_wrangler_directive,
        }
        return result

    ### PRIVATE METHODS ###

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

    def _handle_backtrack_navigation_directive(self):
        self._session._is_backtracking_locally = True
        self._session._hide_hidden_commands = True

    def _handle_directive(self, directive):
        if not isinstance(directive, str):
            pass
        elif directive in self._wrangler_navigation_alias_to_action:
            self._wrangler_navigation_alias_to_action[directive]()
        elif directive in self._user_input_to_action:
            self._user_input_to_action[directive]()
            directive = None
        elif directive.startswith('!'):
            statement = directive.replace('!', '')
            self.invoke_shell(statement=statement)
            directive = None
        return directive

    def _handle_display_all_commands_directive(self):
        if (not self._session.is_in_confirmation_environment and
            not self._session.is_in_editor):
            self._session.toggle_hidden_commands()

    def _handle_home_navigation_directive(self):
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_hidden_commands = True

    def _handle_next_score_directive(self):
        self._session._is_navigating_to_next_score = True
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_hidden_commands = True

    def _handle_next_sibling_asset_directive(self):
        controller = self._session.get_controller_with(ui='<')
        controller._set_is_navigating_to_sibling_asset()
        self._session._is_navigating_to_next_asset = True
        self._session._hide_hidden_commands = True

    def _handle_previous_score_directive(self):
        self._session._is_navigating_to_previous_score = True
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_hidden_commands = True

    def _handle_previous_sibling_asset_directive(self):
        controller = self._session.get_controller_with(ui='>')
        controller._set_is_navigating_to_sibling_asset()
        self._session._is_navigating_to_previous_asset = True
        self._session._hide_hidden_commands = True

    def _handle_quit_directive(self):
        self._session._is_quitting = True
        self._session._hide_hidden_commands = True

    def _handle_score_navigation_directive(self):
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._hide_hidden_commands = True

    def _handle_to_build_file_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_build_files = True

    def _handle_to_distribution_file_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_distribution_files = True

    def _handle_to_maker_module_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_maker_modules = True

    def _handle_to_material_package_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_materials = True

    def _handle_to_segment_package_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_segments = True

    def _handle_to_stylesheet_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_stylesheets = True

    def _is_in_open_environment(self):
        if self._session.is_in_confirmation_environment:
            return False
        if self._session.is_in_editor:
            return False
        return True

    def _make_tab(self, n=1):
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
            if not self._session.pending_user_input:
                superclass = super(IOManager, self)
                superclass.clear_terminal()

    def confirm(
        self,
        prompt_string='ok?',
        include_chevron=False,
        ):
        r'''Prompts user to confirm.

        Returns boolean.
        '''
        getter = self.make_getter(
            include_chevron=include_chevron,
            include_newlines=False,
            )
        getter.append_yes_no_string(prompt_string)
        result = getter._run()
        if isinstance(result, str):
            if 'yes'.startswith(result.lower()):
                return True

    def display(
        self,
        lines,
        capitalize=True,
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
        if capitalize:
            lines = [
                stringtools.capitalize_start(line)
                for line in lines
                ]
        if lines:
            self._session.transcript._append_entry(lines)
        if not self._session.pending_user_input:
            for line in lines:
                print(line)

    def doctest(self):
        r'''Runs doctest on most recent doctestable controller in controller
        stack.

        Returns none.
        '''
        message = 'running doctest ...'
        self.display([message, ''])
        controller = self._session.get_controller_with(ui='pyd')
        controller.doctest()

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
                prompt_string = stringtools.capitalize_start(
                    prompt_string)
            if include_chevron:
                prompt_string = prompt_string + prompt_character + ' '
            else:
                prompt_string = prompt_string + ' '
            if not self._session.pending_user_input:
                user_input = raw_input(prompt_string)
                if include_newline:
                    if not user_input == 'help':
                        print('')
            else:
                user_input = self._pop_from_pending_user_input()
                if user_input == 'default':
                    found_default_token = True
            if not found_default_token:
                self._session.command_history.append(user_input)
            if user_input == '.':
                last_semantic_command = self._session.last_semantic_command
                user_input = last_semantic_command
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

    def invoke_python(self, statement=None):
        r'''Invokes Python on `statement`.

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

    def invoke_shell(self, statement=None):
        r'''Invokes shell on `statement`.

        Hides next redraw.

        Returns none.
        '''
        lines = []
        prompt = True
        if statement is None:
            statement = self.handle_user_input(
                '$',
                include_chevron=False,
                include_newline=False,
                )
        statement = statement.strip()
        process = subprocess.Popen(
            statement,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
        try:
            lines = process.stdout.readlines()
        except:
            lines.append('expression not executable.')
        lines = lines or []
        lines = [_.strip() for _ in lines]
        lines.append('')
        if prompt:
            self.display(lines, capitalize=False)
        self._session._hide_next_redraw = True

    def make_directory_manager(self, path):
        r'''Makes directory manager.

        Returns directory manager.
        '''
        from scoremanager import managers
        return managers.DirectoryManager(
            path=path,
            session=self._session,
            )

    def make_editor(
        self, 
        breadcrumb=None,
        target=None,
        ):
        r'''Makes editor with optional `target`.

        Returns editor or list editor.
        '''
        from scoremanager import iotools
        prototype = (
            list,
            datastructuretools.TypedList,
            )
        if isinstance(target, prototype):
            class_ = iotools.ListEditor
        else:
            class_ = iotools.Editor
        return class_(
            breadcrumb=breadcrumb,
            session=self._session,
            target=target,
            )

    def make_file_manager(self, path):
        r'''Makes file manager.

        Returns file manager.
        '''
        from scoremanager import managers
        return managers.FileManager(
            path=path,
            session=self._session,
            )

    def make_getter(
        self,
        allow_none=False,
        include_chevron=True,
        include_newlines=False,
        ):
        r'''Makes getter.

        Returns getter.
        '''
        from scoremanager import iotools
        getter = iotools.UserInputGetter(
            session=self._session,
            allow_none=allow_none,
            include_chevron=include_chevron,
            include_newlines=include_newlines,
            )
        return getter

    def make_menu(
        self,
        breadcrumb_callback=None,
        name=None,
        ):
        r'''Makes menu.

        Returns menu.
        '''
        from scoremanager import iotools
        menu = iotools.Menu(
            breadcrumb_callback=breadcrumb_callback,
            name=name,
            session=self._session,
            )
        menu._make_default_hidden_sections()
        return menu

    def make_package_manager(self, path):
        r'''Makes package manager.

        Returns package manager.
        '''
        from scoremanager import managers
        return managers.PackageManager(
            path=path,
            session=self._session,
            )

    def make_selector(
        self,
        breadcrumb=None,
        is_ranged=False,
        items=None,
        ):
        r'''Makes selector.

        Returns selector.
        '''
        from scoremanager import iotools
        return iotools.Selector(
            breadcrumb=breadcrumb,
            is_ranged=is_ranged,
            items=items,
            session=self._session,
            )

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
        self._session._proceed_count += 1
        message = message or 'press return to continue.'
        assert isinstance(message, str)
        if not prompt:
            return
        self.handle_user_input(
            message,
            include_chevron=False,
            )
        self.clear_terminal()

    def pytest(self):
        r'''Runs Pytest on most recent pytestable controller in controller
        stack.

        Returns none.
        '''
        message = 'running py.test ...'
        self.display([message, ''])
        controller = self._session.get_controller_with(ui='pyt')
        controller.pytest()

    def run_command(self, command, capitalize=True):
        r'''Makes subprocess with `command` and then runs and displays
        output of subprocess.

        Returns none.
        '''
        process = self.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        if not lines:
            return
        lines.append('')
        self.display(
            lines,
            capitalize=capitalize,
            )

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
        lines.append(self._unicode_directive)
        lines.append('')
        lines.append('')
        lines.append('start_menu_entries = [')
        wrangler = self._session.score_manager._score_package_wrangler
        menu_entries = wrangler._make_asset_menu_entries(
            include_asset_name=False,
            include_year=True,
            sort_by_annotation=True,
            )
        for menu_entry in menu_entries:
            lines.append('{},'.format(menu_entry))
        lines.append(']')
        contents = '\n'.join(lines)
        cache_file_path = self._configuration.cache_file_path
        with file(cache_file_path, 'w') as cache_file_pointer:
            cache_file_pointer.write(contents)
        if prompt:
            message = 'cache written.'
            self.proceed(message)