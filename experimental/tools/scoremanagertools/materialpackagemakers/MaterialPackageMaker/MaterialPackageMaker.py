# -*- encoding: utf-8 -*-
import copy
import os
from experimental.tools.scoremanagertools.managers.MaterialPackageManager \
    import MaterialPackageManager


class MaterialPackageMaker(MaterialPackageManager):

    ### CLASS VARIABLES ###

    generic_output_name = None

    illustration_builder = None

    output_material_checker = None

    output_material_editor = None

    output_material_maker = None

    output_material_module_import_statements = []

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        MaterialPackageManager.__init__(
            self,
            packagesystem_path=packagesystem_path,
            session=session,
            )
        self._user_input_wrapper_in_memory = \
            self._initialize_user_input_wrapper_in_memory()

    ### PRIVATE METHODS ###

    def _initialize_user_input_wrapper_in_memory(self):
        from experimental.tools import scoremanagertools
        if not self.should_have_user_input_module:
            return
        user_input_module_packagesystem_path = '.'.join([
            self.package_path,
            'user_input',
            ])
        user_input_module_file_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            user_input_module_packagesystem_path,
            is_module=True,
            )
        if not os.path.exists(user_input_module_file_path):
            file(user_input_module_file_path, 'w').write('')
        manager = scoremanagertools.managers.UserInputModuleManager(
            #user_input_module_packagesystem_path,
            user_input_module_file_path,
            session=self.session,
            )
        user_input_wrapper = manager.read_user_input_wrapper_from_disk()
        if user_input_wrapper:
            user_input_wrapper._user_input_module_import_statements = \
                getattr(self, 'user_input_module_import_statements', [])[:]
        else:
            user_input_wrapper = self.initialize_empty_user_input_wrapper()
        return user_input_wrapper

    def _make_main_menu_section_for_user_input_module(self,
        main_menu, hidden_section):
        menu_entries = self.user_input_wrapper_in_memory.editable_lines
        numbered_section = main_menu.make_numbered_section()
        numbered_section.menu_entries = menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('user input - clear', 'uic'))
        command_section.append(('user input - load demo values', 'uil'))
        command_section.append(('user input - populate', 'uip'))
        command_section.append(('user input - show demo values', 'uis'))
        command_section.append(('user input module - view', 'uimv'))
        hidden_section.append(('user input - toggle default mode', 'uit'))
        hidden_section.append(('user input module - delete', 'uimdelete'))

    def _make_main_menu_sections(self, menu, hidden_section):
        if not self.has_output_material_editor:
            self._make_main_menu_section_for_user_input_module(
                menu, hidden_section)
        self._make_main_menu_section_for_output_material(menu, hidden_section)

    ### PUBLIC PROPERTIES ###

    # TODO: change property to method
    # TODO: make illustration work the same way as for segment PDF rendering;
    #       use something like _interpret_in_external_process()
    @property
    def illustration(self):
        # TODO: replace old and dangerous import_output_material_safely()
        output_material = \
            self.output_material_module_manager.import_output_material_safely()
        kwargs = {}
        kwargs['title'] = self._space_delimited_lowercase_name
        if self.session.is_in_score:
            title = self.session.current_score_package_manager.title
            string = '({})'.format(title)
            kwargs['subtitle'] = string
        illustration = self.illustration_builder(output_material, **kwargs)
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
            self.session.io_manager.proceed(
                'user input already empty.', is_interactive=prompt)
        else:
            self.user_input_wrapper_in_memory.clear()
            self.user_input_module_manager.write_user_input_wrapper_to_disk(
                self.user_input_wrapper_in_memory)
            self.session.io_manager.proceed(
                'user input wrapper cleared and written to disk.',
                is_interactive=prompt)

    def display_user_input_demo_values(self, prompt=True):
        lines = []
        for i, (key, value) in enumerate(self.user_input_demo_values):
            line = '    {}: {!r}'.format(key.replace('_', ' '), value)
            lines.append(line)
        lines.append('')
        self.session.io_manager.display(lines)
        self.session.io_manager.proceed(is_interactive=prompt)

    def initialize_empty_user_input_wrapper(self):
        from experimental.tools import scoremanagertools
        user_input_wrapper = scoremanagertools.editors.UserInputWrapper()
        user_input_wrapper._user_input_module_import_statements = \
            getattr(self, 'user_input_module_import_statements', [])[:]
        for user_input_attribute_name in self.user_input_attribute_names:
            user_input_wrapper[user_input_attribute_name] = None
        return user_input_wrapper

    def interactively_edit_user_input_wrapper_at_number(
        self,
        number,
        include_newline=True,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        number = int(number)
        if self.user_input_wrapper_in_memory is None:
            return
        if len(self.user_input_wrapper_in_memory) < number:
            return
        index = number - 1
        key, current_value = \
            self.user_input_wrapper_in_memory.list_items()[index]
        test_tuple = type(self).user_input_tests[index]
        test = test_tuple[1]
        if len(test_tuple) == 3:
            setup_statement = test_tuple[2]
        else:
            setup_statement = 'evaluated_user_input = {}'
        if self.session.use_current_user_input_values_as_default:
            default_value = current_value
        else:
            default_value = None
        getter = self.session.io_manager.make_getter()
        spaced_attribute_name = key.replace('_', ' ')
        message = "value for '{}' must satisfy " + test.__name__ + '().'
        getter._make_prompt(
            spaced_attribute_name,
            help_template=message,
            validation_function=test,
            setup_statements=['from abjad import *', setup_statement],
            default_value=default_value,
            )
        getter.include_newlines = include_newline
        getter.allow_none = True
        new_value = getter._run()
        if self.session.backtrack():
            return
        self.user_input_wrapper_in_memory[key] = new_value
        self.user_input_module_manager.write_user_input_wrapper_to_disk(
            self.user_input_wrapper_in_memory)

    def interactively_view_user_input_module(
        self,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        self.user_input_module_manager.interactively_view()

    def load_user_input_wrapper_demo_values(self, prompt=False):
        user_input_demo_values = copy.deepcopy(
            type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            self.user_input_wrapper_in_memory[key] = value
        self.user_input_module_manager.write_user_input_wrapper_to_disk(
            self.user_input_wrapper_in_memory)
        self.session.io_manager.proceed(
            'demo values loaded and written to disk.',
            is_interactive=prompt)

    def make_output_material_from_user_input_wrapper_in_memory(self):
        output_material = self.output_material_maker(
            *self.user_input_wrapper_in_memory.list_values())
        assert type(self).output_material_checker(
            output_material), repr(output_material)
        return output_material

    def make_output_material_module_body_lines(self, output_material):
        if hasattr(output_material, '_storage_format_specification'):
            lines = format(output_material, 'storage').splitlines()
        else:
            lines = [repr(output_material)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self.material_package_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines

    def populate_user_input_wrapper(self, prompt=False):
        total_elements = len(self.user_input_wrapper_in_memory)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_integer_in_range(
            'start at element number', 1, total_elements, default_value=1)
        with self.backtracking:
            start_element_number = getter._run()
        if self.session.backtrack():
            return
        current_element_number = start_element_number
        current_element_index = current_element_number - 1
        while True:
            with self.backtracking:
                self.interactively_edit_user_input_wrapper_at_number(
                    current_element_number, include_newline=False)
            if self.session.backtrack():
                return
            current_element_index += 1
            current_element_index %= total_elements
            current_element_number = current_element_index + 1
            if current_element_number == start_element_number:
                break

    def swap_user_input_values_default_status(self):
        self.session.swap_user_input_values_default_status()

    def write_stub_user_input_module_to_disk(self, is_interactive=False):
        empty_user_input_wrapper = self.initialize_empty_user_input_wrapper()
        self.user_input_module_manager.write_user_input_wrapper_to_disk(
            empty_user_input_wrapper)
        self.session.io_manager.proceed(
            'stub user input module written to disk.',
            is_interactive=is_interactive)

    ### UI MANIFEST ###

    user_input_to_action = MaterialPackageManager.user_input_to_action.copy()
    user_input_to_action.update({
        'uic': clear_user_input_wrapper,
        'uil': load_user_input_wrapper_demo_values,
        'uip': populate_user_input_wrapper,
        'uis': display_user_input_demo_values,
        'uit': swap_user_input_values_default_status,
        'uimv': interactively_view_user_input_module,
        })
