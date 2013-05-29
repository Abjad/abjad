import copy
import os
from experimental.tools.scoremanagertools.proxies.MaterialPackageProxy import MaterialPackageProxy


class MaterialPackageMaker(MaterialPackageProxy):

    ### CLASS VARIABLES ###

    generic_output_name = None
    illustration_maker = None
    output_material_checker = None
    output_material_editor = None
    output_material_maker = None
    output_material_module_import_statements = []

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        MaterialPackageProxy.__init__(self, packagesystem_path=packagesystem_path, session=session)
        self._user_input_wrapper_in_memory = self._initialize_user_input_wrapper_in_memory()

    ### PRIVATE METHODS ###

    def _initialize_user_input_wrapper_in_memory(self):
        from experimental.tools import scoremanagertools
        if not self.should_have_user_input_module:
            return
        user_input_module_path = '.'.join([self.package_path, 'user_input'])
        user_input_module_file_path = self.configuration.packagesystem_path_to_filesystem_path(
            user_input_module_path, is_module=True)
        if not os.path.exists(user_input_module_file_path):
            file(user_input_module_file_path, 'w').write('')
        proxy = scoremanagertools.proxies.UserInputModuleProxy(user_input_module_path, session=self._session)
        user_input_wrapper = proxy.read_user_input_wrapper_from_disk()
        if user_input_wrapper:
            user_input_wrapper._user_input_module_import_statements = \
                getattr(self, 'user_input_module_import_statements', [])[:]
        else:
            user_input_wrapper = self.initialize_empty_user_input_wrapper()
        return user_input_wrapper

    def _make_main_menu_section_for_user_input_module(self, main_menu, hidden_section):
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

    def _make_main_menu_sections(self, menu, hidden_section):
        if not self.has_output_material_editor:
            self._make_main_menu_section_for_user_input_module(menu, hidden_section)
        self._make_main_menu_section_for_output_material(menu, hidden_section)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def illustration(self):
        output_material = self.output_material_module_proxy.import_output_material_safely()
        kwargs = {}
        kwargs['title'] = self._space_delimited_lowercase_name
        if self._session.is_in_score:
            kwargs['subtitle'] = '({})'.format(self._session.current_score_package_proxy.title)
        illustration = self.illustration_maker(output_material, **kwargs)
        return illustration

    @property
    def user_input_attribute_names(self):
        return tuple([x[0] for x in self.user_input_demo_values])

    @property
    def user_input_wrapper_in_memory(self):
        return self._user_input_wrapper_in_memory

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt=False):
        if self.user_input_wrapper_in_memory.is_empty:
            self._io.proceed('user input already empty.', is_interactive=prompt)
        else:
            self.user_input_wrapper_in_memory.clear()
            self.user_input_module_proxy.write_user_input_wrapper_to_disk(self.user_input_wrapper_in_memory)
            self._io.proceed('user input wrapper cleared and written to disk.', is_interactive=prompt)

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
        if self._session.use_current_user_input_values_as_default:
            default = current_value
        else:
            default = None
        getter = self._io.make_getter()
        spaced_attribute_name = key.replace('_', ' ')
        message = "value for '{}' must satisfy " + test.__name__ + '().'
        getter.append_something(spaced_attribute_name, message, default=default)
        getter.tests.append(test)
        getter.execs[-1].append('from abjad import *')
        getter.execs[-1].append(exec_string)
        getter.include_newlines = include_newline
        getter.allow_none = True
        new_value = getter._run()
        if self._session.backtrack():
            return
        self.user_input_wrapper_in_memory[key] = new_value
        self.user_input_module_proxy.write_user_input_wrapper_to_disk(self.user_input_wrapper_in_memory)

    def initialize_empty_user_input_wrapper(self):
        from experimental.tools import scoremanagertools
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper()
        user_input_wrapper._user_input_module_import_statements = \
            getattr(self, 'user_input_module_import_statements', [])[:]
        for user_input_attribute_name in self.user_input_attribute_names:
            user_input_wrapper[user_input_attribute_name] = None
        return user_input_wrapper

    #def load_user_input_wrapper_demo_values(self, prompt=True):
    def load_user_input_wrapper_demo_values(self, prompt=False):
        user_input_demo_values = copy.deepcopy(type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            self.user_input_wrapper_in_memory[key] = value
        self.user_input_module_proxy.write_user_input_wrapper_to_disk(self.user_input_wrapper_in_memory)
        self._io.proceed('demo values loaded and written to disk.', is_interactive=prompt)

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
        lines[0] = '{} = {}'.format(self.material_package_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines

    def populate_user_input_wrapper(self, prompt=False):
        total_elements = len(self.user_input_wrapper_in_memory)
        getter = self._io.make_getter(where=self._where)
        getter.append_integer_in_range('start at element number', 1, total_elements, default=1)
        self._session.push_backtrack()
        start_element_number = getter._run()
        self._session.pop_backtrack()
        if self._session.backtrack():
            return
        current_element_number = start_element_number
        current_element_index = current_element_number - 1
        while True:
            self._session.push_backtrack()
            self.edit_user_input_wrapper_at_number(current_element_number, include_newline=False)
            self._session.pop_backtrack()
            if self._session.backtrack():
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
        self._io.display(lines)
        self._io.proceed(is_interactive=prompt)

    def write_stub_user_input_module_to_disk(self, is_interactive=False):
        empty_user_input_wrapper = self.initialize_empty_user_input_wrapper()
        self.user_input_module_proxy.write_user_input_wrapper_to_disk(empty_user_input_wrapper)
        self._io.proceed('stub user input module written to disk.', is_interactive=is_interactive)

    ### UI MANIFEST ###

    def swap_user_input_values_default_status(self):
        self._session.swap_user_input_values_default_status()

    def view_user_input_module(self):
        self.user_input_module_proxy.view()

    user_input_to_action = MaterialPackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'uic': clear_user_input_wrapper,
        'uil': load_user_input_wrapper_demo_values,
        'uip': populate_user_input_wrapper,
        'uis': show_user_input_demo_values,
        'uit': swap_user_input_values_default_status,
        'uimv': view_user_input_module,
        })
