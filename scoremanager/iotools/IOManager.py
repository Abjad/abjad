# -*- encoding: utf-8 -*-
import abc
import os
import subprocess
import readline
import traceback
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
    @systemtools.Memoize
    def _input_to_action(self):
        result = {
            'b': self._handle_backtrack_navigation_directive,
            'h': self._handle_home_navigation_directive,
            'q': self._handle_quit_directive,
            's': self._handle_score_navigation_directive,
            '?': self._handle_display_all_commands_directive,
            'n': self._handle_display_all_commands_directive,
            'll': self.open_lilypond_log,
            'pyd': self.doctest,
            'pyi': self.invoke_python,
            'pyt': self.pytest,
            'sv': self._session.display_variables,
            'Y': self.edit_score_stylesheet,
            '>>': self._handle_next_score_directive,
            '<<': self._handle_previous_score_directive,
            '>': self._handle_next_sibling_asset_directive,
            '<': self._handle_previous_sibling_asset_directive,
            }
        return result

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

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

    def _get_wrangler_navigation_directive(self):
        if self._session.is_navigating_to_score_build_files:
            return 'u'
        elif self._session.is_navigating_to_score_distribution_files:
            return 'd'
        elif self._session.is_navigating_to_score_maker_modules:
            return 'k'
        elif self._session.is_navigating_to_score_materials:
            return 'm'
        elif self._session.is_navigating_to_score_segments:
            return 'g'
        elif self._session.is_navigating_to_score_stylesheets:
            return 'y'

    def _handle_backtrack_navigation_directive(self):
        self._session._is_backtracking_locally = True
        self._session._hide_hidden_commands = True

    def _handle_directive(self, directive):
        if not isinstance(directive, str):
            pass
        elif directive in self._wrangler_navigation_alias_to_action:
            self._wrangler_navigation_alias_to_action[directive]()
        elif (self._session.is_in_confirmation_environment and
            directive in ('y', 'Y', 'n', 'N')):
            return directive
        elif directive in self._input_to_action:
            self._input_to_action[directive]()
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

    def _pop_from_pending_input(self):
        self._session._last_command_was_composite = False
        if self._session.pending_input is None:
            return None
        elif self._session._pending_input == '':
            self._session._pending_input = None
            return None
        elif self._session.pending_input.startswith('{{'):
            index = self._session.pending_input.find('}}')
            input = self._session.pending_input[2:index]
            pending_input = self._session.pending_input[index+2:]
            pending_input = pending_input.strip()
            self._session._last_command_was_composite = True
        else:
            input_parts = self._session.pending_input.split(' ')
            first_parts, rest_parts = [], []
            for i, part in enumerate(input_parts):
                if not part.endswith((',', '-')):
                    break
            first_parts = input_parts[:i+1]
            rest_parts = input_parts[i+1:]
            input = ' '.join(first_parts)
            pending_input = ' '.join(rest_parts)
        input = input.replace('~', ' ')
        self._session._pending_input = pending_input
        return input

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
            if not self._session.pending_input:
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
        if not self._session.pending_input:
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
        path = self._session.current_stylesheet_path
        if path:
            self.edit(path)
        else:
            message = 'no file ending in *stylesheet.ily found.'
            self.proceed(message)

    def execute_file(self, path=None, attribute_names=None):
        r'''Executes file `path`.

        Returns `attribute_names` from file.
        '''
        assert path is not None
        assert isinstance(attribute_names, tuple)
        if not os.path.isfile(path):
            return
        with open(path, 'r') as file_pointer:
            file_contents_string = file_pointer.read()
        try:
            exec(file_contents_string)
        except:
            traceback.print_exc()
            self.display('')
            return 'corrupt'
        result = []
        for name in attribute_names:
            if name in locals():
                result.append(locals()[name])
            else:
                result.append(None)
        result = tuple(result)
        return result

    def get_greatest_version_number(self, version_directory):
        r'''Gets greatest version number in `version_directory`.

        Returns ``0`` when `version_directory` does not exist.

        Returns nonnegative integer.
        '''
        if not os.path.isdir(version_directory):
            return 0
        greatest_number = 0
        for entry in os.listdir(version_directory):
            base_name, extension = os.path.splitext(entry)
            number = 0
            try:
                number = int(base_name[-4:])
            except ValueError:
                pass
            if greatest_number < number:
                greatest_number = number
        return greatest_number

    def handle_input(
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
            if not self._session.pending_input:
                input = raw_input(prompt_string)
                if include_newline:
                    if not input == 'help':
                        print('')
            else:
                input = self._pop_from_pending_input()
                if input == 'default':
                    found_default_token = True
            if not found_default_token:
                self._session.command_history.append(input)
            if input == '.':
                last_semantic_command = self._session.last_semantic_command
                input = last_semantic_command
            if found_default_token:
                menu_chunk = [prompt_string.strip()]
                if include_newline:
                    if not input == 'help':
                        menu_chunk.append('')
                self._session.transcript._append_entry(menu_chunk)
                menu_chunk = ['> ']
                if include_newline:
                    if not input == 'help':
                        menu_chunk.append('')
                self._session.transcript._append_entry(menu_chunk)
            else:
                menu_chunk = []
                menu_chunk.append('{}{}'.format(prompt_string, input))
                if include_newline:
                    if not input == 'help':
                        menu_chunk.append('')
                self._session.transcript._append_entry(menu_chunk)
            return input
        finally:
            readline.set_startup_hook()

    def invoke_lilypond(self, file_path, prompt=True):
        r'''Invokes LilyPond on file.

        Returns none.
        '''
        if self.find_executable('lily'):
            executable = 'lily'
        elif self.find_executable('lilypond'):
            executable = 'lilypond'
        else:
            message = 'cannot find LilyPond executable.'
            raise ValueError(message)
        command = '{} {}'.format(
            executable,
            file_path,
            )
        input_directory = os.path.dirname(file_path)
        with systemtools.TemporaryDirectoryChange(input_directory):
            self.spawn_subprocess(command)
        self.display('')
        self._session._hide_next_redraw = True

    def invoke_python(self, statement=None):
        r'''Invokes Python on `statement`.

        Returns none.
        '''
        lines = []
        prompt = True
        if statement is None:
            statement = self.handle_input('>>', include_newline=False)
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
            statement = self.handle_input(
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

    def interpret(self, path, prompt=True):
        r'''Invokes Python or LilyPond on `path`.

        Returns integer success code.
        '''
        _, extension = os.path.splitext(path)
        if extension == '.py':
            command = 'python {}'.format(path)
        elif extension == '.ly':
            command = 'lilypond {}'.format(path)
        else:
            message = 'can not interpret {}.'.format(path)
            raise Exception(message)
        directory = os.path.dirname(path)
        context = systemtools.TemporaryDirectoryChange(directory)
        with context:
            result = self.spawn_subprocess(command)
        if result != 0:
            self.display('')
        elif prompt:
            message = 'interpreted {}.'.format(path)
            self.display([message])
        return result

    def make_autoeditor(
        self, 
        breadcrumb=None,
        target=None,
        ):
        r'''Makes autoeditor with optional `target`.

        Returns autoeditor or list autoeditor.
        '''
        from scoremanager import iotools
        prototype = (
            list,
            datastructuretools.TypedList,
            )
        if isinstance(target, prototype):
            class_ = iotools.ListAutoeditor
        else:
            class_ = iotools.Autoeditor
        return class_(
            breadcrumb=breadcrumb,
            session=self._session,
            target=target,
            )

    def make_directory_manager(self, path):
        r'''Makes directory manager.

        Returns directory manager.
        '''
        from scoremanager import managers
        return managers.DirectoryManager(
            path=path,
            session=self._session,
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

    def open_file(self, file_path):
        r'''Opens `file_path`.

        Also works when `file_path` is a list.

        Returns none.
        '''
        if not isinstance(file_path, list) and not os.path.isfile(file_path):
            return
        if (isinstance(file_path, list) and
            all(x.endswith('.pdf') for x in file_path)):
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

    def open_lilypond_log(self):
        r'''Opens last LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.open_lilypond_log()

    def print_not_yet_implemented(self):
        r'''Prints not-yet-implemented message.

        Returns none.
        '''
        self.display(['not yet implemented.', ''])
        self._session._hide_next_redraw = True

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
        self.handle_input(
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
            apply_view=False,
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