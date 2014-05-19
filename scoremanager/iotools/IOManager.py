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
        '_client',
        '_configuration',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(self, client=None, session=None):
        from scoremanager import core
        self._client = client
        self._configuration = core.ScoreManagerConfiguration()
        self._session = session

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
    def _input_to_method(self):
        result = {
            }
        return result

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    @property
    def _wrangler_navigation_alias_to_action(self):
        result = {
            'd': self._handle_to_distribution_file_wrangler_directive,
            'g': self._handle_to_segment_package_wrangler_directive,
            'k': self._handle_to_maker_file_wrangler_directive,
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

    def _handle_directive(self, directive):
        if not isinstance(directive, str):
            pass
        elif directive in self._wrangler_navigation_alias_to_action:
            self._wrangler_navigation_alias_to_action[directive]()
        elif (self._session.is_in_confirmation_environment and
            directive in ('y', 'Y', 'n', 'N')):
            return directive
        elif directive in self._input_to_method:
            self._input_to_method[directive]()
            directive = None
        return directive

    def _handle_to_build_file_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_build_files = True

    def _handle_to_distribution_file_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_distribution_files = True

    def _handle_to_maker_file_wrangler_directive(self):
        if self._is_in_open_environment():
            self._session._is_navigating_to_score_maker_files = True

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
            input_ = self._session.pending_input[2:index]
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
            input_ = ' '.join(first_parts)
            pending_input = ' '.join(rest_parts)
        input_ = input_.replace('~', ' ')
        self._session._pending_input = pending_input
        return input_

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

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of IO manager.

        Returns score manager object.
        '''
        return self._client

    @property
    def selector(self):
        r'''Gets dummy selector.

        Use for access to selector make methods.

        Returns selector.
        '''
        from scoremanager import iotools
        return iotools.Selector(session=self._session)

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
        if self._session._hide_next_redraw:
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
        include_newline=False,
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
                input_ = raw_input(prompt_string)
                if include_newline:
                    if not input_ == 'help':
                        print('')
            else:
                input_ = self._pop_from_pending_input()
                if input_ == 'default':
                    found_default_token = True
            if not found_default_token:
                self._session.command_history.append(input_)
            if input_ == '.':
                last_semantic_command = self._session.last_semantic_command
                input_ = last_semantic_command
            if found_default_token:
                menu_chunk = [prompt_string.strip()]
                if include_newline:
                    if not input_ == 'help':
                        menu_chunk.append('')
                self._session.transcript._append_entry(menu_chunk)
                menu_chunk = ['> ']
                if include_newline:
                    if not input_ == 'help':
                        menu_chunk.append('')
                self._session.transcript._append_entry(menu_chunk)
            else:
                menu_chunk = []
                menu_chunk.append('{}{}'.format(prompt_string, input_))
                if include_newline:
                    if not input_ == 'help':
                        menu_chunk.append('')
                self._session.transcript._append_entry(menu_chunk)
            return input_
        finally:
            readline.set_startup_hook()

    def invoke_lilypond(self, file_path, confirm=True, display=True):
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
        if display:
            self.display('')
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

    def interpret(self, path, confirm=True, display=True):
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
        elif display:
            message = 'interpreted {}.'.format(path)
            self.display([message])
        return result

    def make_autoeditor(
        self, 
        allow_item_edit=True,
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
            return class_(
                allow_item_edit=allow_item_edit,
                breadcrumb=breadcrumb,
                session=self._session,
                target=target,
                )
        else:
            class_ = iotools.Autoeditor
            return class_(
                breadcrumb=breadcrumb,
                session=self._session,
                target=target,
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

    def make_interaction(self, display=True):
        r'''Makes interaction context manager.

        Returns interaction context manager.
        '''
        from scoremanager import iotools
        context = iotools.Interaction(controller=self.client, display=display)
        return context

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

    def print_not_yet_implemented(self):
        r'''Prints not-yet-implemented message.

        Returns none.
        '''
        self.display(['not yet implemented.', ''])
        self._session._hide_next_redraw = True

    def run_command(self, command, capitalize=True):
        r'''Makes subprocess with `command` and then runs and displays
        output of subprocess.

        Returns none.
        '''
        process = self.make_subprocess(command)
        lines = [line.strip() for line in process.stdout.readlines()]
        if not lines:
            return
        self.display(
            lines,
            capitalize=capitalize,
            )

    def write(self, path, string):
        r'''Write `string` to `path`.

        Returns none.
        '''
        with open(path, 'w') as file_pointer:
            file_pointer.write(string)

    def write_stub(self, path):
        r'''Writes Unicode directive to otherwise empty file at `path`.

        Returns none.
        '''
        with open(path, 'w') as file_pointer:
            file_pointer.write(self._unicode_directive)