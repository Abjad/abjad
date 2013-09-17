# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.FilesystemAssetProxy \
    import FilesystemAssetProxy


class FileProxy(FilesystemAssetProxy):
    r'''File proxy.
    '''

    ### CLASS VARIABLES ###

    _generic_class_name = 'file'

    _temporary_asset_name = 'temporary_file.txt'

    extension = ''

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif result == 'user entered lone return':
            self.interactively_edit()

    def _is_editable(self):
        if self.filesystem_path.endswith(('.tex', '.py')):
            return True
        return False

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

    ### PUBLIC METHODS ###

    def interactively_edit(self):
        r'''Interactively edits file.

        Returns none.
        '''
        command = 'vim + {}'.format(self.filesystem_path)
        iotools.spawn_subprocess(command)

    def interactively_view(self):
        r'''Interactively views file.

        Returns none.
        '''
        if self.filesystem_path.endswith('.pdf'):
            command = 'open {}'.format(self.filesystem_path)
        else:
            command = 'vim -R {}'.format(self.filesystem_path)
        iotools.spawn_subprocess(command)

    def make_empty_asset(self, is_interactive=False):
        r'''Makes emtpy file.

        Returns none.
        '''
        if not self.exists():
            file_reference = file(self.filesystem_path, 'w')
            file_reference.write('')
            file_reference.close()
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def read_lines(self):
        r'''Reads lines in file.

        Returns list.
        '''
        result = []
        if self.filesystem_path:
            if os.path.exists(self.filesystem_path):
                file_pointer = file(self.filesystem_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    def run_python_file(self):
        r'''Runs Python on Python file.

        Returns none.
        '''
        command = 'python {}'.format(self.filesystem_path)
        iotools.spawn_subprocess(command)

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
        iotools.spawn_subprocess(command)
        command = 'rm {}/*.aux'.format(output_directory)
        iotools.spawn_subprocess(command)
        command = 'rm {}/*.log'.format(output_directory)
        iotools.spawn_subprocess(command)
        self.session.io_manager.proceed('', is_interactive=prompt)

    ### UI MANIFEST ###

    user_input_to_action = FilesystemAssetProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'e': interactively_edit,
        'run': run_python_file,
        'ts': interactively_typeset_tex_file,
        'v': interactively_view,
        })
