# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.managers.FilesystemAssetManager \
    import FilesystemAssetManager


class FileManager(FilesystemAssetManager):
    r'''File manager.

    '''

    ### CLASS VARIABLES ###

    _generic_class_name = 'file'

    _temporary_asset_name = 'temporary_file.txt'

    extension = ''

    ### PRIVATE METHODS ###

    def _execute_file_lines(self, return_attribute_name=None):
        if os.path.isfile(self.filesystem_path):
            file_pointer = open(self.filesystem_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            try:
                exec(file_contents_string)
            except Exception:
                return
            if isinstance(return_attribute_name, str):
                if return_attribute_name in locals():
                    return locals()[return_attribute_name]
            elif isinstance(return_attribute_name, (list, tuple)):
                result = []
                for name in return_attribute_name:
                    if name in locals():
                        result.append(locals()[name])
                    else:
                        result.append(None)
                result = tuple(result)
                return result

    def _get_space_delimited_lowercase_name(self):
        if self.filesystem_path:
            base_name = os.path.basename(self.filesystem_path)
            name = base_name.strip('.py')
            name = stringtools.string_to_space_delimited_lowercase(name)
            return name

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif result == 'user entered lone return':
            self.interactively_edit()

    def _interpret_in_external_process(self):
        command = 'python {}'.format(self.filesystem_path)
        result = systemtools.IOManager.spawn_subprocess(command)
        if result != 0:
            self.session.io_manager.display('')
            self.session.io_manager.proceed()

    def _is_editable(self):
        if self.filesystem_path.endswith(('.tex', '.py')):
            return True
        return False

    def _make_empty_asset(self, is_interactive=False):
        if not os.path.exists(self.filesystem_path):
            file_reference = file(self.filesystem_path, 'w')
            file_reference.write('')
            file_reference.close()
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        self._main_menu = main_menu
        command_section = main_menu.make_command_section()
        if self._is_editable():
            command_section.append(('edit', 'e'))
            command_section.default_index = len(command_section) - 1
        command_section.append(('rename', 'ren'))
        command_section.append(('remove', 'rm'))
        if self.filesystem_path.endswith('.py'):
            command_section.append(('run', 'run'))
        if self.filesystem_path.endswith('.tex'):
            command_section.append(('typeset', 'ts'))
        if self.filesystem_path.endswith('.pdf'):
            command_section.append(('view', 'v'))
        return main_menu

    def _read_lines(self):
        result = []
        if self.filesystem_path:
            if os.path.exists(self.filesystem_path):
                file_pointer = file(self.filesystem_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    def _run_abjad(self, prompt=True):
        command = 'abjad {}'.format(self.filesystem_path)
        systemtools.IOManager.spawn_subprocess(command)
        message = 'file executed.'
        self.session.io_manager.proceed(message, is_interactive=prompt)

    def _run_python(self, prompt=True):
        command = 'python {}'.format(self.filesystem_path)
        systemtools.IOManager.spawn_subprocess(command)
        message = 'file executed.'
        self.session.io_manager.proceed(message, is_interactive=prompt)

    def _write_stub_to_disk(self):
        file_pointer = open(self.filesystem_path, 'w')
        file_pointer.write('')
        file_pointer.close()

    ### PUBLIC METHODS ###

    def interactively_call_lilypond(self, prompt=True):
        r'''Interactively calls LilyPond on file.

        Returns none.
        '''
        command = 'lily {}'.format(self.filesystem_path)
        systemtools.IOManager.spawn_subprocess(command)
        self.session.io_manager.proceed('', is_interactive=prompt)

    def interactively_edit(self):
        r'''Interactively edits file.

        Returns none.
        '''
        command = 'vim + {}'.format(self.filesystem_path)
        systemtools.IOManager.spawn_subprocess(command)

    def interactively_open(self):
        r'''Interactively opens file.

        Returns none.
        '''
        systemtools.IOManager.open_file(self.filesystem_path)

    def interactively_typeset_tex_file(self, prompt=True):
        r'''Interactively typesets TeX file.

        Returns none.
        '''
        input_directory = os.path.dirname(self.filesystem_path)
        basename = os.path.basename(self.filesystem_path)
        input_file_name_stem, extension = os.path.splitext(basename)
        output_directory = input_directory
        command = 'pdflatex --jobname={} -output-directory={} {}/{}.tex'
        command = command.format(
            input_file_name_stem, 
            output_directory, 
            input_directory, 
            input_file_name_stem,
            )
        systemtools.IOManager.spawn_subprocess(command)
        command = 'rm {}/*.aux'.format(output_directory)
        systemtools.IOManager.spawn_subprocess(command)
        command = 'rm {}/*.log'.format(output_directory)
        systemtools.IOManager.spawn_subprocess(command)
        self.session.io_manager.proceed('', is_interactive=prompt)

    def interactively_view(self):
        r'''Interactively views file.

        Returns none.
        '''
        if self.filesystem_path.endswith('.pdf'):
            command = 'open {}'.format(self.filesystem_path)
        else:
            command = 'vim -R {}'.format(self.filesystem_path)
        systemtools.IOManager.spawn_subprocess(command)

    ### UI MANIFEST ###

    user_input_to_action = FilesystemAssetManager.user_input_to_action.copy()
    user_input_to_action.update({
        'e': interactively_edit,
        'ts': interactively_typeset_tex_file,
        'v': interactively_view,
        })
