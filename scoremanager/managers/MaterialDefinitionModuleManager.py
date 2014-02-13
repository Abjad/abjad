# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from scoremanager.managers.FileManager \
    import FileManager


class MaterialDefinitionModuleManager(FileManager):

    ### PUBLIC PROPERTIES ###

    @property
    def material_package_name(self):
        if self.filesystem_path:
            return os.path.dirname(self.filesystem_path)

    ### PRIVATE METHODS ###

    def _write_stub_to_disk(self, is_data_only, is_interactive=True):
        if is_data_only:
            self.write_stub_data_material_definition_to_disk()
        else:
            self.write_stub_music_material_definition_to_disk()
        message = 'stub material definition written to disk.'
        self.session.io_manager.proceed(message, is_interactive=is_interactive)

    ### PUBLIC METHODS ###

    def interactively_edit(self, line_number=None):
        if line_number is not None:
            command = 'vim + {}'.format(line_number)
        else:
            columns = len(self.material_package_name) + 3
            command = "vim + -c'norm {}l' {}"
            command = command.format(columns, self.filesystem_path)
        systemtools.IOManager.spawn_subprocess(command)

    def write_stub_data_material_definition_to_disk(self):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad.tools import sequencetools\n')
        lines.append('\n\n')
        line = '{} = None'.format(self.material_package_name)
        lines.append(line)
        lines = ''.join(lines)
        file_pointer = file(self.filesystem_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    def write_stub_music_material_definition_to_disk(self):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        line = 'output_material_module_import_statements'
        line += " = ['from abjad import *']\n"
        lines.append(line)
        lines.append('\n\n')
        line = '{} = None'.format(self.material_package_name)
        lines.append(line)
        lines = ''.join(lines)
        file_pointer = file(self.filesystem_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()
