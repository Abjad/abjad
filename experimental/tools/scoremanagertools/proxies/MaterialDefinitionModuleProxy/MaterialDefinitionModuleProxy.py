from experimental.tools.scoremanagertools.proxies.MaterialModuleProxy import MaterialModuleProxy
from experimental.tools.scoremanagertools.helpers import safe_import
import os


class MaterialDefinitionModuleProxy(MaterialModuleProxy):

    def __init__(self, module_importable_name, session=None):
        MaterialModuleProxy.__init__(self, module_importable_name, session=session)
        self.output_material_module_import_lines = []
        self.body_lines = []
        self.parse()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_user_finalized(self):
        # TODO: maybe replace with bool(self.material_definition)
        return bool(self.import_output_material_module_import_statements_and_material_definition()[1])

    @property
    def output_material_module_import_statements(self):
        self.unimport()
        result = safe_import(
            locals(), self.module_short_name, 'output_material_module_import_statements',
            source_parent_package_importable_name=self.parent_package_importable_name)
        # keep list from persisting between multiple calls to this method
        if result:
            result = list(result)
            return result

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 0),
            (self.output_material_module_import_lines, True, 2),
            (self.body_lines, False, 0),
            )

    ### PUBLIC METHODS ###

    def edit(self):
        columns = len(self.material_underscored_name) + 3
        os.system("vi + -c'norm {}l' {}".format(columns, self.path_name))

    def import_output_material_module_import_statements_and_material_definition(self):
        if os.path.exists(self.path_name):
            file_pointer = open(self.path_name, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            material_definition = locals().get(self.material_underscored_name)
            output_material_module_import_statements = locals().get(
                'output_material_module_import_statements')
            return output_material_module_import_statements, material_definition

    def parse(self):
        is_parsable = True
        if not self.exists:
            return
        material_definition_module = file(self.path_name, 'r')
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
                    current_section = 'body'
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
            elif current_section == 'body':
                body_lines.append(line)
            else:
                is_parsable = False
        material_definition_module.close()
        self.encoding_directives = encoding_directives[:]
        self.docstring_lines = docstring_lines[:]
        self.setup_statements = setup_statements[:]
        self.output_material_module_import_lines = output_material_module_import_lines[:]
        self.body_lines = body_lines[:]
        return is_parsable

    def write_stub_data_material_definition_to_disk(self):
        self.clear()
        self.setup_statements.append('from abjad.tools import sequencetools\n')
        self.output_material_module_import_lines.append('output_material_module_import_statements = []\n')
        self.body_lines.append('{} = None'.format(self.material_underscored_name))
        self.write_to_disk()

    def write_stub_music_material_definition_to_disk(self):
        self.clear()
        self.setup_statements.append('from abjad import *\n')
        line = "output_material_module_import_statements = ['from abjad import *']\n"
        self.output_material_module_import_lines.append(line)
        self.body_lines.append('{} = None'.format(self.material_underscored_name))
        self.write_to_disk()

    def write_stub_to_disk(self, is_data_only, is_interactive=True):
        if is_data_only:
            self.write_stub_data_material_definition_to_disk()
        else:
            self.write_stub_music_material_definition_to_disk()
        self.proceed('stub material definitiion written to disk.', is_interactive=is_interactive)
