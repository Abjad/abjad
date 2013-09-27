# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.ModuleManager \
    import ModuleManager
from experimental.tools.scoremanagertools.proxies.ParseableModuleMixin \
    import ParseableModuleMixin


class MaterialDefinitionModuleManager(ModuleManager, ParseableModuleMixin):

    ### INITIALIZER ###

    def __init__(self, module_path, session=None):
        ModuleManager.__init__(self, module_path, session=session)
        ParseableModuleMixin.__init__(self)
        self.output_material_module_import_lines = []
        self.body_lines = []
        self.parse()

    ### PUBLIC PROPERTIES ###

    @property
    def file_sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 0),
            (self.output_material_module_import_lines, True, 2),
            (self.body_lines, False, 0),
            )

    @property
    def material_package_name(self):
        return self.packagesystem_path.split('.')[-2]

    ### PUBLIC METHODS ###

    def interactively_edit(self):
        columns = len(self.material_package_name) + 3
        command = "vim + -c'norm {}l' {}"
        command = command.format(columns, self.filesystem_path)
        iotools.spawn_subprocess(command)

    def parse(self):
        is_parsable = True
        if not self.exists():
            return
        material_definition_module = file(self.filesystem_path, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        output_material_module_import_lines = []
        body_lines = []
        current_section = None
        for line in material_definition_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
                    current_section = 'display_string'
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            elif line.startswith('output_material_module_import_statements'):
                current_section = 'output material module imports'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'output material module imports':
                output_material_module_import_lines.append(line)
            elif current_section == 'display_string':
                body_lines.append(line)
            else:
                is_parsable = False
        material_definition_module.close()
        self.encoding_directives = encoding_directives[:]
        self.docstring_lines = docstring_lines[:]
        self.setup_statements = setup_statements[:]
        self.output_material_module_import_lines = \
            output_material_module_import_lines[:]
        self.body_lines = body_lines[:]
        return is_parsable

    def write_stub_data_material_definition_to_disk(self):
        self.clear()
        line = 'from abjad.tools import sequencetools\n'
        self.setup_statements.append(line)
        line = 'output_material_module_import_statements = []\n'
        self.output_material_module_import_lines.append(line)
        line = '{} = None'.format(self.material_package_name)
        self.body_lines.append(line)
        self.write_to_disk()

    def write_stub_music_material_definition_to_disk(self):
        self.clear()
        self.setup_statements.append('from abjad import *\n')
        line = 'output_material_module_import_statements'
        line += " = ['from abjad import *']\n"
        self.output_material_module_import_lines.append(line)
        line = '{} = None'.format(self.material_package_name)
        self.body_lines.append(line)
        self.write_to_disk()

    def write_stub_to_disk(self, is_data_only, is_interactive=True):
        if is_data_only:
            self.write_stub_data_material_definition_to_disk()
        else:
            self.write_stub_music_material_definition_to_disk()
        message = 'stub material definition written to disk.'
        self.session.io_manager.proceed(message, is_interactive=is_interactive)
