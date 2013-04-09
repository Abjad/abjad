from scftools.editors.MusicSpecifierEditor import MusicSpecifierEditor
from scftools.proxies.ModuleProxy import ModuleProxy
from scftools.specifiers.MusicSpecifier import MusicSpecifier
import os


class MusicSpecifierModuleProxy(ModuleProxy):

    def __init__(self, module_importable_name=None, session=None):
        ModuleProxy.__init__(self, module_importable_name=module_importable_name, session=session)
        self.load_target_into_memory()
        self._editor = self.editor_class(target=self.target_in_memory, session=self.session)
        self.target_lines = []
        #self.conditionally_make_empty_asset()
        #self.parse()

    ### CLASS ATTRIUBTES ###

    editor_class = MusicSpecifierEditor
    generic_class_name = 'music specifier'
    target_class = MusicSpecifier
    target_name_in_storage_module = 'music_specifier'

    ### READ-ONLY PROPERTIES ###

    @property
    def editor(self):
        return self._editor

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.target_lines, False, 0),
            )

    @property
    def target_in_memory(self):
        return self._target_in_memory

    ### PUBLIC METHODS ###

    def edit(self):
        self.editor.run(breadcrumb=self.human_readable_name)
        self._target_in_memory = self.editor.target
        self.write_target_to_disk(self.target_in_memory)

    def fix(self):
        self.print_not_yet_implemented()

    def load_target_into_memory(self):
        self._target_in_memory = self.read_target_from_disk() or self.target_class()

    def parse(self):
        is_parsable = True
        output_material_module = file(self.path_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        target_lines = []
        current_section = None
        for line in output_material_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
                    current_section = 'music specifier'
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'music specifier':
                target_lines.append(line)
            else:
                is_parsable = False
        output_material_module.close()
        self.encoding_directives = encoding_directives
        self.docstring_lines = docstring_lines
        self.setup_statements = setup_statements
        self.target_lines = target_lines
        return is_parsable

    def prepend_target_name(self, target_format_pieces):
        if target_format_pieces:
            target_format_pieces[0] = '{} = {}'.format(
                self.target_name_in_storage_module, target_format_pieces[0])
        return target_format_pieces

    def read_target_from_disk(self):
        self.unimport()
        if os.path.exists(self.path_name):
            file_pointer = open(self.path_name, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            target = locals().get(self.target_name_in_storage_module, None)
            return target

    def write_stub_to_disk(self):
        self.conditionally_make_empty_asset()

    def write_target_to_disk(self, target_in_memory):
        self.parse()
        self.setup_statements[:] = self.conditionally_add_terminal_newlines(
            self.target_in_memory.storage_module_import_statements)[:]
        self.target_lines[:] = self.conditionally_add_terminal_newlines(
            self.prepend_target_name(
                self.target_in_memory._get_tools_package_qualified_repr_pieces(is_indented=True)))
        ModuleProxy.write_to_disk(self)
