# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.proxies.ModuleManager \
    import ModuleManager


class UserInputModuleManager(ModuleManager):

    ### PUBLIC PROPERTIES ###

    @property
    def has_complete_user_input_wrapper_on_disk(self):
        user_input_wrapper = self.read_user_input_wrapper_from_disk()
        if user_input_wrapper is not None:
            return user_input_wrapper.is_complete
        return False

    ### PUBLIC METHODS ###

    def read_user_input_wrapper_from_disk(self):
        result = self.execute_file_lines(
            return_attribute_name='user_input_wrapper',
            )
        return result

    def write_user_input_wrapper_to_disk(self, user_input_wrapper_in_memory):
        wrapper = user_input_wrapper_in_memory
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        import_statements = wrapper.user_input_module_import_statements[:]
        import_statements = \
            stringtools.add_terminal_newlines(import_statements)
        lines.extend(import_statements)
        lines.append('\n\n')
        formatted_lines = wrapper.formatted_lines
        formatted_lines = stringtools.add_terminal_newlines(formatted_lines)
        lines.extend(formatted_lines)
        lines = ''.join(lines)
        file_pointer = file(self.filesystem_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()
