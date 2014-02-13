# -*- encoding: utf-8 -*-
import copy
import os
import shutil
import traceback
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools import topleveltools
from scoremanager import wizards
from scoremanager.managers.PackageManager import PackageManager


class MaterialPackageManager(PackageManager):
    r'''Material package manager.

    ::

        >>> package_path = 'scoremanager'
        >>> package_path += '.materialpackages.red_numbers'
        >>> mpp = scoremanager.managers.MaterialPackageManager(package_path)
        >>> mpp
        MaterialPackageManager('.../materialpackages/red_numbers')

    '''

    ### CLASS VARIABLES ###

    generic_output_name = None

    illustration_builder = None

    output_material_checker = None

    output_material_editor = None

    output_material_maker = None

    output_material_module_import_statements = []

    should_have_user_input_module = False

    ### INTIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        PackageManager.__init__(
            self,
            packagesystem_path=packagesystem_path,
            session=session,
            )
        self._user_input_wrapper_in_memory = \
            self._initialize_user_input_wrapper_in_memory()
        self._generic_output_name = None
        self.stylesheet_file_path_in_memory = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif mathtools.is_integer_equivalent_expr(result):
            self.interactively_edit_user_input_wrapper_at_number(
                result, include_newline=False)
        else:
            raise ValueError(result)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        hidden_section = main_menu.make_command_section(is_hidden=True)
        self._make_main_menu_section_for_initializer(
            main_menu, hidden_section)
        if self.should_have_user_input_module:
            self._make_main_menu_sections_with_user_input_wrapper(
                main_menu, hidden_section)
        else:
            self._make_main_menu_sections(main_menu, hidden_section)
        self._make_main_menu_section_for_illustration_ly(hidden_section)
        self._make_main_menu_section_for_illustration_pdf(
            main_menu, hidden_section)
        self._make_main_menu_section_for_hidden_entries(main_menu)
        return main_menu

    def _make_main_menu_section_for_hidden_entries(self, main_menu):
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('remove package', 'rm'))
        hidden_section.append(('list package', 'ls'))
        hidden_section.append(('rename package', 'ren'))
        hidden_section.append(('manage stylesheets', 'stl'))
        hidden_section.append(('manage metadata', 'metadata'))

    def _make_main_menu_section_for_illustration_builder(
        self,
        main_menu,
        hidden_section,
        ):
        if self.has_output_material:
            if self.should_have_illustration:
                if not self.has_illustration_builder_module:
                    material_package_path = self.package_path
                    material_package_name = \
                        material_package_path.split('.')[-1]
                    self.write_stub_illustration_builder_module(
                        material_package_path,
                        material_package_name,
                        prompt=False,
                        )
                command_section = main_menu.make_command_section()
                command_section.append(
                    ('illustration builder - edit', 'ibe'))
                if self.has_output_material:
                    command_section.append(
                        ('illustration builder - execute', 'ibx'))
                hidden_section.append(
                    ('illustration builder - delete', 'ibd'))
                hidden_section.append(
                    ('illustration builder - stub', 'ibt'))
                hidden_section.append(
                    ('illustration builder - edit & execute', 'ibex'))
                command_section.append(
                    ('score stylesheet - select', 'sss'))
                hidden_section.append(
                    ('source stylesheet - edit', 'ssm'))

    def _make_main_menu_section_for_illustration_ly(self, hidden_section):
        if self.has_output_material:
            if self.has_illustration_builder_module or \
                self.has_material_package_manager:
                hidden_section.append(('output ly - make', 'lym'))
        if self.has_illustration_ly:
            hidden_section.append(('output ly - delete', 'lyd'))
            hidden_section.append(('output ly - view', 'ly'))

    def _make_main_menu_section_for_illustration_pdf(
        self,
        main_menu,
        hidden_section,
        ):
        has_illustration_pdf_section = False
        if self.has_output_material:
            if self.has_illustration_builder_module or \
                (self.has_material_package_manager and
                getattr(self, 'illustration_builder', None)):
                command_section = main_menu.make_command_section()
                command_section.append(('output pdf - make', 'pdfm'))
                has_illustration_pdf_section = True
        if self.has_illustration_pdf:
            if not has_illustration_pdf_section:
                command_section = main_menu.make_command_section()
            hidden_section.append(('output pdf - delete', 'pdfd'))
            command_section.append(('output pdf - view', 'pdfv'))

    def _make_main_menu_section_for_initializer(self,
        main_menu, hidden_section):
        if not self.has_initializer:
            command_section = main_menu.make_command_section()
            command_section.title = '(Note: package has no initializer.)'
        hidden_section.append(('initializer - copy canned', 'incanned'))
        hidden_section.append(('initializer - restore', 'inr'))
        hidden_section.append(('initializer - view', 'inv'))
        hidden_section.append(('initializer - write stub', 'instub'))

    def _make_main_menu_section_for_material_definition(self,
        main_menu, hidden_section):
        if not self.has_initializer:
            return
        if self.has_material_definition_module:
            command_section = main_menu.make_command_section()
            command_section.append(
                ('material definition - edit', 'mde'))
            command_section.default_index = len(command_section) - 1
            command_section.append(
                ('material definition - execute', 'mdx'))
            hidden_section.append(
                ('material definition - copy canned module', 'mdcanned'))
            hidden_section.append(
                ('material definition - delete', 'mddelete'))
            hidden_section.append(
                ('material definition - stub', 'mdstub'))
            hidden_section.append(
                ('material definition - execute & edit', 'mdxe'))
        elif self.material_package_manager_class_name is None:
            command_section = main_menu.make_command_section()
            command_section.return_value_attribute = 'key'
            command_section.append(
                ('material definition - stub', 'mdstub'))

    def _make_main_menu_section_for_output_material(
        self,
        main_menu,
        hidden_section,
        ):
        if not self.has_initializer:
            return
        has_output_material_section = False
        if self.has_material_definition_module or \
            self.has_complete_user_input_wrapper_in_memory or \
            self.has_output_material_editor:
            if self.has_material_definition or \
                self.has_complete_user_input_wrapper_in_memory:
                command_section = main_menu.make_command_section()
                command_section.append(('output material - make', 'omm'))
                has_output_material_section = True
            if self.has_output_material_editor:
                command_section = main_menu.make_command_section()
                command_section.append(('output material - interact', 'omi'))
                if self.has_output_material:
                    output_material_editor = self.output_material_editor(
                        target=self.output_material,
                        session=self.session)
                    target_summary_lines = \
                        output_material_editor.target_summary_lines
                    if target_summary_lines:
                        command_section.title = target_summary_lines
                has_output_material_section = True
            if self.has_output_material_module:
                if not has_output_material_section:
                    command_section = main_menu.make_command_section()
                command_section.append(
                    ('output material - view', 'omv'))
                hidden_section.append(
                    ('output material - delete', 'omdelete'))
        hidden_section.append(
            ('output material - copy canned module', 'omcanned'))

    def _make_main_menu_sections(self, menu, hidden_section):
        self._make_main_menu_section_for_material_definition(
            menu, hidden_section)
        self._make_main_menu_section_for_output_material(
            menu, hidden_section)
        self._make_main_menu_section_for_illustration_builder(
            menu, hidden_section)

    ### PUBLIC PROPERTIES ###

    @property
    def has_complete_user_input_wrapper_in_memory(self):
        if self.has_user_input_wrapper_in_memory:
            return self.user_input_wrapper_in_memory.is_complete
        return False

    @property
    def has_complete_user_input_wrapper_on_disk(self):
        if self.has_user_input_wrapper_on_disk:
            return self.user_input_wrapper_on_disk.is_complete

    @property
    def has_illustration_builder_module(self):
        if self.should_have_illustration_builder_module:
            return os.path.exists(self.illustration_builder_module_file_path)
        return False

    @property
    def has_illustration_ly(self):
        if self.should_have_illustration_ly:
            return os.path.exists(self.illustration_ly_file_path)
        return False

    @property
    def has_illustration_pdf(self):
        if self.should_have_illustration_pdf:
            return os.path.exists(self.illustration_pdf_fil_path)
        return False

    @property
    def has_initializer(self):
        if self.should_have_initializer:
            return os.path.exists(self.initializer_file_path)
        return False

    @property
    def has_material_definition(self):
        if self.should_have_material_definition_module:
            if self.has_material_definition_module:
                return self.material_definition is not None
        return False

    @property
    def has_material_definition_module(self):
        if self.should_have_material_definition_module:
            return os.path.exists(self.material_definition_module_file_path)
        return False

    @property
    def has_material_package_manager(self):
        return bool(self.material_package_manager_class_name)

    @property
    def has_output_material(self):
        if self.should_have_output_material_module:
            if self.has_output_material_module:
                return True
        return False

    @property
    def has_output_material_editor(self):
        return bool(getattr(self, 'output_material_editor', None))

    @property
    def has_output_material_module(self):
        if self.should_have_output_material_module:
            return os.path.exists(self.output_material_module_file_path)
        return False

    # TODO: impelement
    @property
    def has_stylesheet(self):
        return False

    @property
    def has_user_input_module(self):
        if self.should_have_user_input_module:
            return os.path.exists(self.user_input_module_file_path)
        return False

    @property
    def has_user_input_wrapper_in_memory(self):
        if self.should_have_user_input_module:
            return bool(self.user_input_wrapper_in_memory)
        return False

    @property
    def has_user_input_wrapper_on_disk(self):
        if self.should_have_user_input_module:
            return bool(self.read_user_input_wrapper_from_disk())
        return False

    @property
    def illustration_builder_module_file_path(self):
        if self.should_have_illustration_builder_module:
            return os.path.join(self.filesystem_path, 'illustration_builder.py')

    @property
    def illustration_builder_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self.illustration_builder_module_file_path,
            session=self.session,
            )

    @property
    def illustration_builder_packagesystem_path(self):
        if self.should_have_illustration_builder_module:
            return '.'.join([self.package_path, 'illustration_builder'])

    @property
    def illustration_ly_file_manager(self):
        from scoremanager import managers
        file_path = os.path.join(self.filesystem_path, 'illustration.ly')
        manager = managers.FileManager(
            file_path,
            session=self.session,
            )
        return manager

    @property
    def illustration_ly_file_path(self):
        if self.should_have_illustration_ly:
            return os.path.join(self.filesystem_path, 'illustration.ly')

    @property
    def illustration_pdf_file_manager(self):
        from scoremanager import managers
        file_path = os.path.join(self.filesystem_path, 'illustration.pdf')
        manager = managers.FileManager(
            file_path,
            session=self.session,
            )
        return manager

    @property
    def illustration_pdf_fil_path(self):
        if self.should_have_illustration_pdf:
            return os.path.join(self.filesystem_path, 'illustration.pdf')

    @property
    def illustration_with_stylesheet(self):
        illustration = self.illustration
        if illustration and self.stylesheet_file_path_in_memory:
            illustration.file_initial_user_includes.append(
                self.stylesheet_file_path_in_memory)
        return illustration

    @property
    def is_data_only(self):
        return not self.should_have_illustration

    @property
    def is_handmade(self):
        return not(self.has_material_package_manager)

    @property
    def is_makermade(self):
        return self.has_material_package_manager

    @property
    def material_definition(self):
        from scoremanager import managers
        if not self.has_material_definition_module:
            return
        manager = managers.FileManager(
            self.material_definition_module_file_path,
            session=self.session,
            )
        result = manager._execute_file_lines(
            return_attribute_name=self.material_package_name,
            )
        return result

    @property
    def material_definition_module_file_path(self):
        if self.should_have_material_definition_module:
            return os.path.join(self.filesystem_path, 'material_definition.py')

    @property
    def material_definition_packagesystem_path(self):
        if self.should_have_material_definition_module:
            return '.'.join([self.package_path, 'material_definition'])

    @property
    def material_package_directory(self):
        if self.session.current_materials_directory_path:
            if self.material_package_name:
                return os.path.join(
                    self.session.current_materials_directory_path,
                    self.material_package_name)

    @property
    def material_package_manager(self):
        if self.material_package_manager_class_name is None:
            return
        directory_path = \
            self.configuration.built_in_material_package_managers_directory_path
        package_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
            directory_path)
        import_statement = 'from {} import {}'
        import_statement = import_statement.format(
            package_path,
            self.material_package_manager_class_name,
            )
        try:
            exec(import_statement)
        except:
            return
        result = locals()[self.material_package_manager_class_name]
        return result

    @property
    def material_package_manager_class_name(self):
        return self._get_metadatum('material_package_manager_class_name')

    @property
    def material_package_name(self):
        return os.path.basename(self.filesystem_path)

    @property
    def output_material(self):
        try:
            output_material = \
                self.output_material_module_manager._execute_file_lines(
                    return_attribute_name=self.material_package_name,
                    )
        except:
            traceback.print_exc()
            output_material = None
        return output_material

    @property
    def output_material_module_body_lines(self):
        if self.should_have_material_definition_module:
            return self.output_material_module_import_statements_and_output_material_module_body_lines[1]

    @property
    def output_material_module_file_path(self):
        if self.should_have_output_material_module:
            return os.path.join(self.filesystem_path, 'output_material.py')

    @property
    def output_material_module_import_statements_and_material_definition(self):
        from scoremanager import managers
        if not self.should_have_material_definition_module:
            return
        return_attribute_name = [
            'output_material_module_import_statements',
            self.material_package_name,
            ]
        manager = managers.FileManager(
            self.material_definition_module_file_path,
            session=self.session,
            )
        result = manager._execute_file_lines(
            return_attribute_name=return_attribute_name,
            )
        return result

    @property
    def output_material_module_import_statements_and_output_material_module_body_lines(
        self):
        if self.should_have_material_definition_module:
            pair = \
                self.output_material_module_import_statements_and_material_definition
            output_material_module_import_statements, output_material = pair
        elif self.has_material_package_manager:
            output_material_module_import_statements = \
                self.output_material_module_import_statements
            output_material = \
                self.make_output_material_from_user_input_wrapper_in_memory()
        else:
            raise ValueError
        if self.should_have_user_input_module:
        #if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = \
                self.make_output_material_module_body_lines(output_material)
        else:
            line = '{} = {}'
            output_material_storage_format = \
                self.get_tools_package_qualified_repr(output_material)
            line = line.format(
                self.material_package_name,
                output_material_storage_format,
                )
            output_material_module_body_lines = [line]
        return (
            output_material_module_import_statements,
            output_material_module_body_lines,
            )

    @property
    def output_material_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self.output_material_module_file_path,
            session=self.session,
            )

    @property
    def output_material_module_path(self):
        if self.should_have_output_material_module:
            return '{}.output_material'.format(self.package_path)

    @property
    def should_have_illustration(self):
        return self._get_metadatum('should_have_illustration')

    @property
    def should_have_illustration_builder_module(self):
        if self.should_have_illustration:
            if self.material_package_manager_class_name is None:
                return True
        return False

    @property
    def should_have_illustration_ly(self):
        return self.should_have_illustration

    @property
    def should_have_illustration_pdf(self):
        return self.should_have_illustration

    @property
    def should_have_initializer(self):
        return True

    @property
    def should_have_material_definition_module(self):
        return self.material_package_manager_class_name is None

    @property
    def should_have_output_material_module(self):
        return True

    @property
    def should_have_stylesheet(self):
        return self.should_have_illustration

    @property
    def space_delimited_material_package_name(self):
        return self.material_package_name.replace('_', ' ')

    @property
    def stylesheet_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self.stylesheet_file_path,
            session=self.session,
            )

    @property
    def stylesheet_file_path_on_disk(self):
        if self.has_illustration_ly:
            for line in self.illustration_ly_file_manager.read_lines():
                if line.startswith(r'\include') and 'stylesheets' in line:
                    file_name = line.split()[-1].replace('"', '')
                    return file_name

    @property
    def user_input_module_file_path(self):
        if self.should_have_user_input_module:
            return os.path.join(self.filesystem_path, 'user_input.py')

    @property
    def user_input_module_packagesystem_path(self):
        if self.should_have_user_input_module:
            return '.'.join([self.package_path, 'user_input'])

    ### PUBLIC METHODS ###

    def conditionally_write_stub_material_definition_module(
        self,
        is_interactive=False,
        ):
        if not self._get_metadatum('material_package_manager_class_name'):
            is_data_only = not self._get_metadatum('should_have_illustration')
            self._write_stub_material_definition_module(
                is_data_only, 
                is_interactive=is_interactive,
                )

    def conditionally_write_stub_user_input_module(
        self,
        is_interactive=False,
        ):
        if self.should_have_user_input_module:
            self.write_stub_user_input_module(
                is_interactive=is_interactive)

    def get_tools_package_qualified_repr(self, expr):
        if hasattr(expr, '_make_storage_format_with_overrides'):
            return expr._make_storage_format_with_overrides()
        elif hasattr(expr, '_storage_format_specification'):
            return format(expr, 'storage')
        return repr(expr)

    def interactively_edit_illustration_builder_module(self):
        self.illustration_builder_module_manager.interactively_edit()

    def interactively_edit_material_definition_module(self):
        file_path = self.material_definition_module_file_path
        self.session.io_manager.interactively_edit(file_path)

    def interactively_edit_output_material(self):
        if not self.has_output_material_editor:
            return
        output_material = self.output_material
        if not hasattr(self, 'output_material_maker'):
            output_material_handler_callable = self.output_material_editor
        elif output_material is None and self.output_material_maker and \
            issubclass(self.output_material_maker, wizards.Wizard):
            output_material_handler_callable = self.output_material_maker
        else:
            output_material_handler_callable = self.output_material_editor
        output_material_handler = output_material_handler_callable(
            target=output_material, session=self.session)
        output_material_handler._run()
        if self.session.backtrack():
            return
        output_material_module_import_statements = \
            self.output_material_module_import_statements
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = \
                self.make_output_material_module_body_lines(
                    output_material_handler.target)
        else:
            line = '{} = {}'
            target_repr = self.get_tools_package_qualified_repr(
                output_material_handler.target)
            line = line.format(
                self.material_package_name,
                target_repr,
                )
            output_material_module_body_lines = [line]
        self.write_output_material(
            output_material_module_import_statements=\
                output_material_module_import_statements,
            output_material_module_body_lines=\
                output_material_module_body_lines,
            )

    def interactively_edit_stylesheet_file(self):
        self.stylesheet_file_manager.interactively_edit()

    def interactively_remove(self):
        PackageManager.interactively_remove(self)

    def interactively_rename_package(self):
        base_name = os.path.basename(self.filesystem_path)
        line = 'current name: {}'.format(base_name)
        self.session.io_manager.display(line)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self.session.backtrack():
            return
        lines = []
        lines.append('current name: {}'.format(base_name))
        lines.append('new name:     {}'.format(new_package_name))
        lines.append('')
        self.session.io_manager.display(lines)
        if not self.session.io_manager.confirm():
            return
        new_directory_path = self.filesystem_path.replace(
            base_name,
            new_package_name,
            )
        if self._is_versioned():
            # rename package
            command = 'svn mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            self.session.io_manager.spawn_subprocess(command)
            # replace output material variable name
            new_output_material_module_name = os.path.join(
                new_directory_path,
                'output_material.py',
                )
            result = os.path.splitext(base_name)
            old_package_name, extension = result
            self.replace_in_file(
                new_output_material_module_name,
                old_package_name,
                new_package_name,
                )
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                base_name,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            parent_directory_path = os.path.dirname(self.filesystem_path)
            command = 'svn commit -m "{}" {}'
            command = command.format(
                commit_message,
                parent_directory_path,
                )
            self.session.io_manager.spawn_subprocess(command)
        else:
            # rename package
            command = 'mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            self.session.io_manager.spawn_subprocess(command)
            # replace output material variable name
            new_output_material_module_name = os.path.join(
                new_directory_path,
                'output_material.py',
                )
            result = os.path.splitext(base_name)
            old_package_name, extension = result
            self.replace_in_file(
                new_output_material_module_name,
                old_package_name,
                new_package_name,
                )
        # update path name to reflect change
        self._path = new_directory_path
        self.session.is_backtracking_locally = True

    def interactively_select_material_package_manager(self, prompt=True):
        from scoremanager import wranglers
        material_manager_wrangler = wranglers.MaterialPackageManagerWrangler(
            session=self.session)
        with self.backtracking:
            material_package_manager = \
                material_manager_wrangler.select_material_manager_class_name_interactively()
        if self.session.backtrack():
            return
        self._add_metadata(
            'material_package_manager',
            material_package_manager.class_name,
            )
        line = 'user input handler selected.'
        self.session.io_manager.proceed(line, is_interactive=prompt)

    def interactively_select_stylesheet(self, prompt=True):
        from scoremanager import wranglers
        stylesheet_file_wrangler = wranglers.StylesheetFileWrangler(
            session=self.session)
        with self.backtracking:
            stylesheet_file_path = \
                stylesheet_file_wrangler.interactively_select_asset_filesystem_path()
        if self.session.backtrack():
            return
        self.stylesheet_file_path_in_memory = stylesheet_file_path
        self.session.io_manager.proceed(
            'stylesheet selected.', 
            is_interactive=prompt,
            )

    def interactively_view_illustration_ly(self):
        self.illustration_ly_file_manager.interactively_view()

    def interactively_view_illustration_pdf(self):
        self.illustration_pdf_file_manager.interactively_view()

    def interactively_view_output_material_module(self):
        self.output_material_module_manager.interactively_view()

    def interactively_write_material_definition_module_boilerplate(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.material_definition_module_file_path,
            session=self.session,
            )
        manager.interactively_write_boilerplate()

    def interactively_write_output_material_module_boilerplate(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.output_material_module_file_path,
            session=self.session,
            )
        manager.interactively_write_boilerplate()

    def manage_stylesheets(self):
        from scoremanager import wranglers
        stylesheet_file_wrangler = wranglers.StylesheetFileWrangler(
            session=self.session)
        stylesheet_file_wrangler._run()

    def remove(self):
        PackageManager._remove(self)

    def remove_illustration_builder_module(self, prompt=True):
        self.remove_illustration_pdf(prompt=False)
        if self.has_illustration_builder_module:
            self.illustration_builder_module_manager._remove()

    def remove_illustration_ly(self, prompt=True):
        if self.has_illustration_ly:
            self.illustration_ly_file_manager._remove()

    def remove_illustration_pdf(self, prompt=True):
        self.remove_illustration_ly(prompt=False)
        if self.has_illustration_pdf:
            self.illustration_pdf_file_manager._remove()

    def remove_material_definition_module(self, prompt=True):
        from scoremanager import managers
        self.remove_output_material_module(prompt=False)
        self.remove_illustration_builder_module(prompt=False)
        if self.has_material_definition_module:
            manager = managers.FileManager(
                self.material_definition_module_file_path,
                session=self.session,
                )
            manager._remove()

    def remove_output_material_module(self, prompt=True):
        self.remove_illustration_builder_module(prompt=False)
        if self.has_output_material_module:
            self.output_material_module_manager._remove()

    def remove_user_input_module(self, prompt=True):
        from scoremanager import managers
        if self.has_user_input_module:
            manager = managers.FileManager(
                self.user_input_module_file_path,
                session=self.session,
                )
            manager._remove()

    @staticmethod
    def replace_in_file(file_path, old, new):
        with file(file_path, 'r') as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(new_file_lines))

    def run_abjad_on_illustration_builder_module(self):
        self.illustration_builder_module_manager._run_abjad(prompt=True)

    def run_abjad_on_material_definition_module(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.material_definition_module_file_path,
            session=self.session,
            )
        manager._run_abjad()

    def run_first_time(self):
        self._run(pending_user_input='omi')

    def run_python_on_illustration_builder_module(self):
        self.illustration_builder_module_manager._run_python(prompt=True)

    def run_python_on_material_definition_module(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.material_definition_module_file_path,
            session=self.session,
            )
        manager._run_python()

    def write_illustration_ly_and_pdf(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        topleveltools.persist(illustration).as_pdf(
            self.illustration_pdf_fil_path,
            )
        self.session.io_manager.proceed(
            'PDF and LilyPond file written to disk.',
            is_interactive=prompt,
            )

    def write_illustration_ly(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        topleveltools.persist(illustration).as_pdf(
            self.illustration_ly_file_path,
            )
        self.session.io_manager.proceed(
            'LilyPond file written to disk.',
            is_interactive=prompt,
            )

    def write_illustration_pdf(self, prompt=True):
        illustration = self.illustration_with_stylesheet
        topleveltools.persist(illustration).as_pdf(
            self.illustration_pdf_fil_path,
            )
        self.session.io_manager.proceed(
            'PDF written to disk.',
            is_interactive=prompt)

    def write_output_material(
        self,
        output_material_module_import_statements=None,
        output_material_module_body_lines=None,
        prompt=True,
        ):
        if self._get_metadatum('is_static'):
            source_path = self.material_definition_module_file_path
            target_path = self.output_material_module_file_path
            shutil.copy(source_path, target_path)
            return
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        if output_material_module_import_statements is None or \
            output_material_module_body_lines is None:
            pair = self.output_material_module_import_statements_and_output_material_module_body_lines
            output_material_module_import_statements = pair[0]
            output_material_module_body_lines = pair[1]
        output_material_module_import_statements = [
            x + '\n'
            for x in output_material_module_import_statements
            ]
        lines.extend(output_material_module_import_statements)
        lines.extend(output_material_module_body_lines)
        lines = ''.join(lines)
        manager = self.output_material_module_manager
        with file(manager.filesystem_path, 'w') as file_pointer:
            file_pointer.write(lines)
        self._add_metadata('is_material_package', True)
        if hasattr(self, 'generic_output_name'):
            self._add_metadata('generic_output_name', self.generic_output_name)
        message = 'output material written to disk.'
        self.session.io_manager.proceed(message, is_interactive=prompt)

    def _write_stub_material_definition_module(
        self, 
        is_data_only, 
        is_interactive=True,
        ):
        if is_data_only:
            self.write_stub_data_material_definition()
        else:
            self.write_stub_music_material_definition()
        message = 'stub material definition written to disk.'
        self.session.io_manager.proceed(message, is_interactive=is_interactive)

    def write_stub_data_material_definition(self):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        lines.append('\n\n')
        #line = '{} = None'.format(self.material_package_name)
        line = '{} = None'.format(self.package_root_name)
        lines.append(line)
        lines = ''.join(lines)
        #file_pointer = file(self.filesystem_path, 'w')
        file_pointer = file(self.material_definition_module_file_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    def write_stub_music_material_definition(self):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        line = 'output_material_module_import_statements'
        line += " = ['from abjad import *']\n"
        lines.append(line)
        lines.append('\n\n')
        #line = '{} = None'.format(self.material_package_name)
        line = '{} = None'.format(self.package_root_name)
        lines.append(line)
        lines = ''.join(lines)
        #file_pointer = file(self.filesystem_path, 'w')
        file_pointer = file(self.material_definition_module_file_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    def write_stub_illustration_builder_module(
        self,
        material_package_path,
        material_package_name,
        prompt=True,
        ):
        lines = []
        lines.append('from abjad import *\n')
        line = 'from {}.output_material import {}\n'
        line = line.format(material_package_path, material_package_name)
        lines.append(line)
        lines.append('\n')
        lines.append('\n')
        line = 'score, treble_staff, bass_staff ='
        line += ' scoretools.make_piano_score_from_leaves({})\n'
        line = line.format(material_package_name)
        line = 'illustration = lilypondfiletools.'
        line += 'make_basic_lilypond_file(score)\n'
        lines.append(line)
        file_path = os.path.join(
            self.filesystem_path,
            'illustration_builder.py',
            )
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(lines))
        message = 'stub illustration builder written to disk.'
        self.session.io_manager.proceed(message, is_interactive=prompt)

    def write_stub_material_definition_module(self):
        if self.should_have_material_definition_module:
            with file(
                self.material_definition_module_file_path,
                'w',
                ) as file_pointer:
                file_pointer.write('')
            self._write_stub_material_definition_module(
                self.is_data_only, 
                is_interactive=True,
                )

    ### USER INPUT WRAPPER METHODS ###

    def has_complete_user_input_wrapper_on_disk(self):
        user_input_wrapper = self.read_user_input_wrapper_from_disk()
        if user_input_wrapper is not None:
            return user_input_wrapper.is_complete
        return False

    def read_user_input_wrapper_from_disk(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.user_input_module_file_path,
            session=self.session,
            )
        result = manager._execute_file_lines(
            file_path=self.user_input_module_file_path,
            return_attribute_name='user_input_wrapper',
            )
        return result

    def write_user_input_wrapper(self, wrapper):
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
        file_pointer = file(self.user_input_module_file_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    def _initialize_user_input_wrapper_in_memory(self):
        from scoremanager import managers
        if not self.should_have_user_input_module:
            return
        if self.package_path.endswith('PackageManager'):
            parts = self.package_path.split('.')
            parts = parts[:-1]
            parent_package_path = '.'.join(parts)
            package_path = parent_package_path
        else:
            package_path = self.package_path
        user_input_module_packagesystem_path = '.'.join([
            package_path,
            'user_input',
            ])
        user_input_module_file_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            user_input_module_packagesystem_path,
            is_module=True,
            )
        if not os.path.exists(user_input_module_file_path):
            file(user_input_module_file_path, 'w').write('')
        user_input_wrapper = self.read_user_input_wrapper_from_disk()
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

    def _make_main_menu_sections_with_user_input_wrapper(
        self, menu, hidden_section):
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
            wrapper = self.user_input_wrapper_in_memory
            self.write_user_input_wrapper(wrapper)
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
        from scoremanager import editors
        user_input_wrapper = editors.UserInputWrapper()
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
        self.session.io_manager._assign_user_input(pending_user_input)
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
        wrapper = self.user_input_wrapper_in_memory
        self.write_user_input_wrapper(wrapper)

    def interactively_view_user_input_module(
        self,
        pending_user_input=None,
        ):
        from scoremanager import managers
        self.session.io_manager._assign_user_input(pending_user_input)
        file_path = self.user_input_module_file_path
        self.session.io_manager.interactively_view(file_path)

    def load_user_input_wrapper_demo_values(self, prompt=False):
        user_input_demo_values = copy.deepcopy(
            type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            self.user_input_wrapper_in_memory[key] = value
        wrapper = self.user_input_wrapper_in_memory
        self.write_user_input_wrapper(wrapper)
        self.session.io_manager.proceed(
            'demo values loaded and written to disk.',
            is_interactive=prompt,
            )

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

    def write_stub_user_input_module(self, is_interactive=False):
        wrapper = self.initialize_empty_user_input_wrapper()
        self.write_user_input_wrapper(wrapper)
        self.session.io_manager.proceed(
            'stub user input module written to disk.',
            is_interactive=is_interactive,
            )

    ### UI MANIFEST ###

    user_input_to_action = PackageManager.user_input_to_action.copy()
    user_input_to_action.update({
        'ibd': remove_illustration_builder_module,
        'ibe': interactively_edit_illustration_builder_module,
        'ibt': write_stub_illustration_builder_module,
        'ibx': run_python_on_illustration_builder_module,
        'ibxi': run_abjad_on_illustration_builder_module,
        'lyd': remove_illustration_ly,
        'lym': write_illustration_ly,
        'ly': illustration_ly_file_manager,
        'mdcanned': interactively_write_material_definition_module_boilerplate,
        'mde': interactively_edit_material_definition_module,
        'mddelete': remove_material_definition_module,
        'mdstub': write_stub_material_definition_module,
        'mdx': run_python_on_material_definition_module,
        'mdxe': run_abjad_on_material_definition_module,
        'omcanned': interactively_write_output_material_module_boilerplate,
        'omdelete': remove_output_material_module,
        'omm': write_output_material,
        'omi': interactively_edit_output_material,
        'omv': interactively_view_output_material_module,
        'pdfm': write_illustration_ly_and_pdf,
        'pdfd': remove_illustration_pdf,
        'pdfv': interactively_view_illustration_pdf,
        'ren': interactively_rename_package,
        'ssm': interactively_edit_stylesheet_file,
        'sss': interactively_select_stylesheet,
        'stl': manage_stylesheets,
        'uid': remove_user_input_module,

        'uic': clear_user_input_wrapper,
        'uil': load_user_input_wrapper_demo_values,
        'uip': populate_user_input_wrapper,
        'uis': display_user_input_demo_values,
        'uit': swap_user_input_values_default_status,
        'uimv': interactively_view_user_input_module,

        })
