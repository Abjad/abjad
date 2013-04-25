import copy
import os
from experimental.tools.scoremanagertools.proxies.MaterialPackageProxy import MaterialPackageProxy
from experimental.tools.scoremanagertools.editors.UserInputWrapper import UserInputWrapper


class MaterialPackageMaker(MaterialPackageProxy):

    ### CLASS ATTRIBUTES ###

    generic_output_name = None
    illustration_maker = None
    output_material_checker = None
    output_material_editor = None
    output_material_maker = None
    output_material_module_import_statements = []

    ### INITIALIZER ###

    def __init__(self, package_importable_name=None, session=None):
        MaterialPackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self._user_input_wrapper_in_memory = self._initialize_user_input_wrapper_in_memory()

    ### PRIVATE METHODS ###

    def _initialize_user_input_wrapper_in_memory(self):
        from experimental.tools import scoremanagertools
        if not self.should_have_user_input_module:
            return
        user_input_module_importable_name = self.dot_join([self.importable_name, 'user_input'])
        user_input_module_file_name = self.module_importable_name_to_path_name(
            user_input_module_importable_name)
        if not os.path.exists(user_input_module_file_name):
            file(user_input_module_file_name, 'w').write('')
        proxy = scoremanagertools.proxies.UserInputModuleProxy(user_input_module_importable_name, session=self.session)
        user_input_wrapper = proxy.read_user_input_wrapper_from_disk()
        if user_input_wrapper:
            user_input_wrapper._user_input_module_import_statements = \
                getattr(self, 'user_input_module_import_statements', [])[:]
        else:
            user_input_wrapper = self.initialize_empty_user_input_wrapper()
        return user_input_wrapper

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def illustration(self):
        output_material = self.output_material_module_proxy.import_output_material_safely()
        kwargs = {}
        kwargs['title'] = self.human_readable_name
        if self.session.is_in_score:
            kwargs['subtitle'] = '({})'.format(self.session.current_score_package_proxy.title)
        illustration = self.illustration_maker(output_material, **kwargs)
        return illustration

    @property
    def user_input_attribute_names(self):
        return tuple([x[0] for x in self.user_input_demo_values])

    @property
    def user_input_wrapper_in_memory(self):
        return self._user_input_wrapper_in_memory

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt=True):
        if self.user_input_wrapper_in_memory.is_empty:
            self.proceed('user input already empty.')
        else:
            self.user_input_wrapper_in_memory.clear()
            self.user_input_module_proxy.write_user_input_wrapper_to_disk(self.user_input_wrapper_in_memory)
            self.proceed('user input wrapper cleared and written to disk.', is_interactive=prompt)

    def edit_user_input_wrapper_at_number(self, number, include_newline=True):
        number = int(number)
        if self.user_input_wrapper_in_memory is None:
            return
        if len(self.user_input_wrapper_in_memory) < number:
            return
        index = number - 1
        key, current_value = self.user_input_wrapper_in_memory.list_items()[index]
        test_tuple = type(self).user_input_tests[index]
        test = test_tuple[1]
        if len(test_tuple) == 3:
            exec_string = test_tuple[2]
        else:
            exec_string = 'value = {}'
        if self.session.use_current_user_input_values_as_default:
            default = current_value
        else:
            default = None
        getter = self.make_getter()
        spaced_attribute_name = key.replace('_', ' ')
        message = "value for '{}' must satisfy " + test.__name__ + '().'
        getter.append_something(spaced_attribute_name, message, default=default)
        getter.tests.append(test)
        getter.execs[-1].append('from abjad import *')
        getter.execs[-1].append(exec_string)
        getter.include_newlines = include_newline
        getter.allow_none = True
        new_value = getter.run()
        if self.backtrack():
            return
        self.user_input_wrapper_in_memory[key] = new_value
        self.user_input_module_proxy.write_user_input_wrapper_to_disk(self.user_input_wrapper_in_memory)

    def initialize_empty_user_input_wrapper(self):
        user_input_wrapper = UserInputWrapper()
        user_input_wrapper._user_input_module_import_statements = \
            getattr(self, 'user_input_module_import_statements', [])[:]
        for user_input_attribute_name in self.user_input_attribute_names:
            user_input_wrapper[user_input_attribute_name] = None
        return user_input_wrapper

    def load_user_input_wrapper_demo_values(self, prompt=True):
        user_input_demo_values = copy.deepcopy(type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            self.user_input_wrapper_in_memory[key] = value
        self.user_input_module_proxy.write_user_input_wrapper_to_disk(self.user_input_wrapper_in_memory)
        self.proceed('demo values loaded and written to disk.', is_interactive=prompt)

    def make_main_menu_section_for_user_input_module(self, main_menu, hidden_section):
        section = main_menu.make_section(is_parenthetically_numbered=True)
        section.tokens = self.user_input_wrapper_in_memory.editable_lines
        section.return_value_attribute = 'number'
        section = main_menu.make_section()
        section.append(('uic', 'user input - clear'))
        section.append(('uil', 'user input - load demo values'))
        section.append(('uip', 'user input - populate'))
        section.append(('uis', 'user input - show demo values'))
        section.append(('uimv', 'user input module - view'))
        hidden_section.append(('uit','user input - toggle default mode'))
        hidden_section.append(('uimdelete', 'user input module - delete'))

    def make_main_menu_sections(self, menu, hidden_section):
        if not self.has_output_material_editor:
            self.make_main_menu_section_for_user_input_module(menu, hidden_section)
        self.make_main_menu_section_for_output_material(menu, hidden_section)

    def make_output_material_from_user_input_wrapper_in_memory(self):
        output_material = self.output_material_maker(*self.user_input_wrapper_in_memory.list_values())
        assert type(self).output_material_checker(output_material), repr(output_material)
        return output_material

    def make_output_material_module_body_lines(self, output_material):
        if hasattr(output_material, '_get_tools_package_qualified_repr_pieces'):
            lines = output_material._get_tools_package_qualified_repr_pieces(is_indented=True)
        else:
            lines = [repr(output_material)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self.material_underscored_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines

    def populate_user_input_wrapper(self, prompt=True):
        total_elements = len(self.user_input_wrapper_in_memory)
        getter = self.make_getter(where=self.where())
        getter.append_integer_in_range('start at element number', 1, total_elements, default=1)
        self.push_backtrack()
        start_element_number = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        current_element_number = start_element_number
        current_element_index = current_element_number - 1
        while True:
            self.push_backtrack()
            self.edit_user_input_wrapper_at_number(current_element_number, include_newline=False)
            self.pop_backtrack()
            if self.backtrack():
                return
            current_element_index += 1
            current_element_index %= total_elements
            current_element_number = current_element_index + 1
            if current_element_number == start_element_number:
                break

    def show_user_input_demo_values(self, prompt=True):
        lines = []
        for i, (key, value) in enumerate(self.user_input_demo_values):
            line = '    {}: {!r}'.format(key.replace('_', ' '), value)
            lines.append(line)
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=prompt)

    def write_stub_user_input_module_to_disk(self, is_interactive=False):
        empty_user_input_wrapper = self.initialize_empty_user_input_wrapper()
        self.user_input_module_proxy.write_user_input_wrapper_to_disk(empty_user_input_wrapper)
        self.proceed('stub user input module written to disk.', is_interactive=is_interactive)
