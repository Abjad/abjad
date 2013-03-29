from scf.proxies.ModuleProxy import ModuleProxy
import os


class UserInputModuleProxy(ModuleProxy):

    def __init__(self, module_importable_name=None, session=None):
        ModuleProxy.__init__(self, module_importable_name=module_importable_name, session=session)
        self.user_input_wrapper_lines = []
        self.parse()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def has_complete_user_input_wrapper_on_disk(self):
        user_input_wrapper = self.read_user_input_wrapper_from_disk()
        if user_input_wrapper is not None:
            return user_input_wrapper.is_complete
        return False

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.user_input_wrapper_lines, False, 0),
            )

    ### PUBLIC METHODS ###

    def parse(self):
        is_parsable = True
        output_material_module = file(self.path_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        user_input_wrapper_lines = []
        current_section = None
        for line in output_material_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
                    current_section = 'user input wrapper'
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
            elif current_section == 'user input wrapper':
                user_input_wrapper_lines.append(line)
            else:
                is_parsable = False
        output_material_module.close()
        self.encoding_directives = encoding_directives
        self.docstring_lines = docstring_lines
        self.setup_statements = setup_statements
        self.user_input_wrapper_lines = user_input_wrapper_lines
        return is_parsable

    def read_user_input_wrapper_from_disk(self):
        self.unimport()
        if os.path.exists(self.path_name):
            file_pointer = open(self.path_name, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            try:
                exec(file_contents_string)
                return locals().get('user_input_wrapper', None)
            except:
                self.display('Error reading user input module.')

    def write_user_input_wrapper_to_disk(self, user_input_wrapper_in_memory):
        self.setup_statements[:] = self.conditionally_add_terminal_newlines(
            user_input_wrapper_in_memory.user_input_module_import_statements)[:]
        self.user_input_wrapper_lines[:] = self.conditionally_add_terminal_newlines(
            user_input_wrapper_in_memory.formatted_lines)
        ModuleProxy.write_to_disk(self)
