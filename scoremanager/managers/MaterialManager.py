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


class MaterialManager(PackageManager):
    r'''Material manager.

    ..  container:: example

        ::

            >>> import os
            >>> configuration = scoremanager.core.ScoreManagerConfiguration()
            >>> filesystem_path = os.path.join(
            ...     configuration.abjad_material_packages_directory_path,
            ...     'example_numbers',
            ...     )
            >>> manager = scoremanager.managers.MaterialManager(
            ...     filesystem_path=filesystem_path,
            ...     )
            >>> manager
            MaterialManager('.../materials/example_numbers')

    '''

    ### CLASS VARIABLES ###

    _generic_class_name = 'material manager'

    _output_material_checker = None

    _output_material_editor = None

    _output_material_maker = None

    _output_material_module_import_statements = []

    _should_have_user_input_module = False

    ### INTIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        if filesystem_path is not None:
            assert os.path.sep in filesystem_path
        PackageManager.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )
        wrapper = self._initialize_user_input_wrapper_in_memory()
        self._user_input_wrapper_in_memory = wrapper
        self._generic_output_name = None
        self.stylesheet_file_path_in_memory = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

    @property
    def _illustration_builder_module_path(self):
        return os.path.join(
            self._filesystem_path, 
            'illustration_builder.py',
            )

    @property
    def _illustration_ly_file_path(self):
        return os.path.join(
            self._filesystem_path, 
            'illustration.ly',
            )

    @property
    def _illustration_pdf_file_path(self):
        return os.path.join(
            self._filesystem_path, 
            'illustration.pdf',
            )

    @property
    def _material_definition_module_path(self):
        path = os.path.join(
            self._filesystem_path, 
            'material_definition.py',
            )
        return path

    @property
    def _output_material_module_import_statements_and_material_definition(
        self):
        from scoremanager import managers
        if not self._should_have_material_definition_module:
            return
        return_attribute_name = [
            '_output_material_module_import_statements',
            self.material_package_name,
            ]
        manager = managers.FileManager(
            self._material_definition_module_path,
            session=self._session,
            )
        result = manager._execute_file_lines(
            return_attribute_name=return_attribute_name,
            )
        return result

    @property
    def _output_material_module_import_statements_and_output_material_module_body_lines(
        self):
        if self._should_have_material_definition_module:
            pair = \
                self._output_material_module_import_statements_and_material_definition
            _output_material_module_import_statements, output_material = pair
        elif self._read_material_manager_class_name():
            _output_material_module_import_statements = \
                self._output_material_module_import_statements
            output_material = \
                self.make_output_material_from_user_input_wrapper_in_memory()
        else:
            raise ValueError
        if self._should_have_user_input_module:
            output_material_module_body_lines = \
                self.make_output_material_module_body_lines(output_material)
        else:
            line = '{} = {}'
            output_material_storage_format = \
                self._get_storage_format(output_material)
            line = line.format(
                self.material_package_name,
                output_material_storage_format,
                )
            output_material_module_body_lines = [line]
        return (
            _output_material_module_import_statements,
            output_material_module_body_lines,
            )

    @property
    def _should_have_material_definition_module(self):
        return self._read_material_manager_class_name() is None

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialManager, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'ibe': self.edit_illustration_builder_module,
            'ibex': self.edit_and_execute_illustration_builder_module,
            'ibm': self.write_stub_illustration_builder_module,
            'ibrm': self.remove_illustration_builder_module,
            'ibs': self.write_stub_illustration_builder_module,
            'ibx': self.run_python_on_illustration_builder_module,
            'ibxi': self.run_abjad_on_illustration_builder_module,
            'lym': self.write_illustration_ly,
            'lyrm': self.remove_illustration_ly,
            'ly': self.illustration_ly_file_manager,
            'mdbp': self.write_material_definition_module_boilerplate,
            'mde': self.edit_material_definition_module,
            'mdrm': self.remove_material_definition_module,
            'mds': self.write_stub_music_material_definition,
            'mdx': self.run_python_on_material_definition_module,
            'mdxe': self.run_abjad_on_material_definition_module,
            'ombp': self.write_output_material_module_boilerplate,
            'omm': self.write_output_material,
            'omi': self.edit_output_material,
            'omrm': self.remove_output_material_module,
            'omv': self.view_output_material_module,
            'pdfm': self.write_illustration_ly_and_pdf,
            'pdfrm': self.remove_illustration_pdf,
            'pdfv': self.view_illustration_pdf,
            'ren': self.rename_package,
            'sse': self.edit_stylesheet_file,
            'sss': self.select_stylesheet,
            'uid': self.remove_user_input_module,
            'uic': self.clear_user_input_wrapper,
            'uil': self.load_user_input_wrapper_demo_values,
            'uip': self.populate_user_input_wrapper,
            'uis': self.display_user_input_demo_values,
            'uit': self.toggle_user_input_values_default_status,
            'uimv': self.view_user_input_module,
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _edit_user_input_wrapper_at_number(
        self,
        number,
        include_newline=True,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
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
        if self._session.use_current_user_input_values_as_default:
            default_value = current_value
        else:
            default_value = None
        getter = self._io_manager.make_getter()
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
        if self._session._backtrack():
            return
        self.user_input_wrapper_in_memory[key] = new_value
        wrapper = self.user_input_wrapper_in_memory
        self.write_user_input_wrapper(wrapper)

    def _execute_material_definition_module(self):
        from scoremanager import managers
        if not os.path.isfile(self._material_definition_module_path):
            return
        manager = managers.FileManager(
            self._material_definition_module_path,
            session=self._session,
            )
        result = manager._execute_file_lines(
            return_attribute_name=self.material_package_name,
            )
        return result

    # TODO: change property to method
    # TODO: make illustration work the same way as for segment PDF rendering;
    #       use something like _interpret_in_external_process()
    def _illustrate(self):
        # TODO: replace old and dangerous import_output_material_safely()
        output_material = \
            self.output_material_module_manager.import_output_material_safely()
        kwargs = {}
        kwargs['title'] = self._space_delimited_lowercase_name
        if self._session.is_in_score:
            title = self._session.current_score_package_manager.title
            string = '({})'.format(title)
            kwargs['subtitle'] = string
        illustration = self.illustration_builder(output_material, **kwargs)
        if illustration and self.stylesheet_file_path_in_memory:
            path = self.stylesheet_file_path_in_memory
            illustration.file_initial_user_includes.append(path)
        return illustration

    def _initialize_empty_user_input_wrapper(self):
        from scoremanager import editors
        user_input_wrapper = editors.UserInputWrapper()
        user_input_wrapper._user_input_module_import_statements = \
            getattr(self, 'user_input_module_import_statements', [])[:]
        for user_input_attribute_name in self.user_input_attribute_names:
            user_input_wrapper[user_input_attribute_name] = None
        return user_input_wrapper

    def _read_material_manager_class_name(self):
        return self._get_metadatum('material_manager_class_name')

    def _get_storage_format(self, expr):
        if hasattr(expr, '_make_storage_format_with_overrides'):
            return expr._make_storage_format_with_overrides()
        elif hasattr(expr, '_storage_format_specification'):
            return format(expr, 'storage')
        return repr(expr)

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif mathtools.is_integer_equivalent_expr(result):
            self._edit_user_input_wrapper_at_number(
                result, 
                include_newline=False,
                )
        elif result == 'user entered lone return':
            pass
        else:
            raise ValueError(result)

    def _initialize_user_input_wrapper_in_memory(self):
        from scoremanager import managers
        if not self._should_have_user_input_module:
            return
        user_input_module_path = self.user_input_module_path
        if os.path.exists(self.user_input_module_path):
            user_input_wrapper = self.read_user_input_wrapper_from_disk()
            if user_input_wrapper:
                user_input_wrapper._user_input_module_import_statements = \
                    getattr(self, 'user_input_module_import_statements', [])[:]
        else:
            user_input_wrapper = self._initialize_empty_user_input_wrapper()
        return user_input_wrapper

    def _make_stylesheet_menu_section(
        self,
        menu,
        ):
        name = 'stylesheets'
        section = menu.make_command_section(name=name)
        if os.path.isfile(self.output_material_module_path):
            section = menu.make_command_section(name=name)
            section.append(('stylesheet - edit', 'sse'))
            section.append(('stylesheet - select', 'sss'))

    def _make_illustration_builder_menu_section(
        self,
        main_menu,
        ):
        name = 'illustration builder'
        command_section = main_menu.make_command_section(name=name)
        if os.path.isfile(self.output_material_module_path):
            if os.path.isfile(self._illustration_builder_module_path):
                string = 'illustration builder - edit'
                command_section.append((string, 'ibe'))
                string = 'illustration builder - edit & execute'
                command_section.append((string, 'ibex'))
                string = 'illustration builder - execute'
                command_section.append((string, 'ibx'))
                string = 'illustration builder - remove'
                command_section.append((string, 'ibrm'))
                string = 'illustration builder - stub'
                command_section.append((string, 'ibs'))
            else:
                string = 'illustration builder - make'
                command_section.append((string, 'ibm'))

    def _make_illustration_ly_menu_section(self, menu):
        if os.path.isfile(self.output_material_module_path) or \
            os.path.isfile(self._illustration_ly_file_path):
            section = menu.make_command_section()
        if os.path.isfile(self.output_material_module_path):
            if os.path.isfile(self._illustration_builder_module_path) or \
                self._read_material_manager_class_name():
                section.append(('output ly - make', 'lym'))
        if os.path.isfile(self._illustration_ly_file_path):
            section.append(('output ly - remove', 'lyrm'))
            section.append(('output ly - view', 'ly'))

    def _make_illustration_pdf_menu_section(
        self,
        main_menu,
        ):
        name = 'illustration pdf'
        if os.path.isfile(self.output_material_module_path) or \
            os.path.isfile(self._illustration_pdf_file_path):
            command_section = main_menu.make_command_section(name=name)
        if os.path.isfile(self.output_material_module_path):
            if os.path.isfile(self._illustration_builder_module_path) or \
                (self._read_material_manager_class_name() and
                getattr(self, '__illustrate__', None)):
                command_section.append(('output pdf - make', 'pdfm'))
                has_illustration_pdf_section = True
        if os.path.isfile(self._illustration_pdf_file_path):
            if not has_illustration_pdf_section:
                command_section = main_menu.make_command_section(name=name)
            command_section.append(('output pdf - remove', 'pdfrm'))
            command_section.append(('output pdf - view', 'pdfv'))

    def _make_main_menu(self):
        superclass = super(MaterialManager, self)
        where = self._where
        menu, hidden_section = superclass._make_main_menu(where=where)
        self._make_illustration_builder_menu_section(menu)
        has_initializer = os.path.isfile(self._initializer_file_path)
        self._io_manager._make_initializer_menu_section(
            menu, 
            has_initializer=has_initializer,
            )
        self._make_material_definition_menu_section(menu)
        self._io_manager._make_metadata_menu_section(menu)
        self._io_manager._make_metadata_module_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_output_material_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_package_management_menu_section(menu)
        self._make_stylesheet_menu_section(menu)
        if self._should_have_user_input_module:
            if not self._output_material_editor:
                self._make_user_input_module_menu_section(menu)
        try:
            material_summary_section = menu['material summary']
            menu.menu_sections.remove(material_summary_section)
            menu.menu_sections.insert(0, material_summary_section)
        except KeyError:
            pass
        lilypond_section = menu['lilypond']
        index = menu.menu_sections.index(lilypond_section) + 1
        tour_menu_section = self._io_manager._make_material_tour_menu_section(
            menu)
        menu.menu_sections.insert(index, tour_menu_section)
        #print menu, 'MMM'
        #for x in menu.menu_sections:
        #    print x
        return menu

    def _make_main_menu_sections_with_user_input_wrapper(self, menu):
        if not self._output_material_editor:
            self._make_user_input_module_menu_section(menu)
        self._make_output_material_menu_section(menu)

    def _make_material_definition_menu_section(
        self,
        main_menu, 
        ):
        name = 'material definition'
        if not os.path.isfile(self._initializer_file_path):
            return
        if os.path.isfile(self._material_definition_module_path):
            command_section = main_menu.make_command_section(name=name)
            string = 'material definition - boilerplate'
            command_section.append((string, 'mdbp'))
            command_section.append(('material definition - edit', 'mde'))
            command_section.default_index = len(command_section) - 1
            command_section.append(('material definition - execute', 'mdx'))
            string = 'material definition - execute & edit'
            command_section.append((string, 'mdxe'))
            string = 'material definition - remove'
            command_section.append((string, 'mdrm'))
            command_section.append(('material definition - stub', 'mds'))
        elif self._read_material_manager_class_name() is None:
            command_section = main_menu.make_command_section(name=name)
            command_section.return_value_attribute = 'key'
            command_section.append(('material definition - stub', 'mds'))

    def _can_make_output_material(self):
        if os.path.isfile(self._material_definition_module_path):
            return True
        if bool(self.user_input_wrapper_in_memory) and \
            self.user_input_wrapper_in_memory.is_complete:
            return True
        return False

    def _make_output_material_menu_section(
        self,
        menu,
        ):
        if not os.path.isfile(self._initializer_file_path):
            return
        has_output_material_section = False
        name = 'output material'
        section = menu.make_command_section(name=name)
        string = 'output material - boilerplate'
        section.append((string, 'ombp'))
        if self._should_have_output_material_section():
            if self._can_make_output_material():
                section.append(('output material - make', 'omm'))
                has_output_material_section = True
            if self._output_material_editor:
                section.append(('output material - interact', 'omi'))
                if os.path.isfile(self.output_material_module_path):
                    editor = self._output_material_editor(
                        target=self.output_material,
                        session=self._session,
                        )
                    target_summary_lines = editor.target_summary_lines
                    if target_summary_lines:
                        contents_section = menu.make_command_section(
                            name='material summary',
                            )
                        contents_section.title = target_summary_lines
                has_output_material_section = True
            if os.path.isfile(self.output_material_module_path):
                section.append(('output material - remove', 'omrm'))
                section.append(('output material - view', 'omv'))

    def _should_have_output_material_section(self):
        if os.path.isfile(self._material_definition_module_path):
            return True
        if bool(self.user_input_wrapper_in_memory) and \
            self.user_input_wrapper_in_memory.is_complete:
            return True
        if self._output_material_editor:
            return True
        return False

    def _make_package_management_menu_section(self, main_menu):
        section = main_menu.make_command_section(
            is_secondary=True,
            name='package management',
            )
        section.append(('package - list', 'ls'))
        section.append(('package - list long', 'll'))
        section.append(('package - pwd', 'pwd'))
        section.append(('package - remove', 'rm'))
        section.append(('package - rename', 'ren'))

    def _make_user_input_module_menu_section(
        self,
        main_menu, 
        ):
        menu_entries = self.user_input_wrapper_in_memory.editable_lines
        numbered_section = main_menu.make_numbered_section(
            name='material summary')
        numbered_section.menu_entries = menu_entries
        command_section = main_menu.make_command_section(name='user input')
        command_section.append(('user input - clear', 'uic'))
        command_section.append(('user input - load demo values', 'uil'))
        command_section.append(('user input - populate', 'uip'))
        command_section.append(('user input - show demo values', 'uis'))
        command_section.append(('user input - toggle default mode', 'uit'))
        command_section = main_menu.make_command_section(
            name='user input module')
        command_section.append(('user input module - remove', 'uimrm'))
        command_section.append(('user input module - view', 'uimv'))

    def _run_first_time(self):
        self._run(pending_user_input='omi')

    def _write_stub_material_definition_module(self, prompt=True):
        self.write_stub_music_material_definition()
        message = 'stub material definition written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    ### PUBLIC PROPERTIES ###

    @property
    def generic_output_name(self):
        r'''Gets generic output name of material manager.

        Returns string.
        '''
        return self._generic_output_name

    @property
    def illustration_builder_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._illustration_builder_module_path,
            session=self._session,
            )

    @property
    def illustration_ly_file_manager(self):
        from scoremanager import managers
        file_path = os.path.join(self._filesystem_path, 'illustration.ly')
        manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        return manager

    @property
    def illustration_pdf_file_manager(self):
        from scoremanager import managers
        file_path = os.path.join(self._filesystem_path, 'illustration.pdf')
        manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        return manager

    @property
    def material_manager(self):
        if self._read_material_manager_class_name() is None:
            return
        directory_path = \
            self._configuration.abjad_material_managers_directory_path
        package_path = \
            self._configuration.path_to_package(
            directory_path)
        import_statement = 'from {} import {}'
        import_statement = import_statement.format(
            package_path,
            self._read_material_manager_class_name(),
            )
        try:
            exec(import_statement)
        except:
            return
        result = locals()[self._read_material_manager_class_name()]
        return result

    @property
    def material_package_name(self):
        return os.path.basename(self._filesystem_path)

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
        if self._should_have_material_definition_module:
            return self._output_material_module_import_statements_and_output_material_module_body_lines[1]

    @property
    def output_material_module_path(self):
        return os.path.join(self._filesystem_path, 'output_material.py')

    @property
    def output_material_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self.output_material_module_path,
            session=self._session,
            )

    @property
    def space_delimited_material_package_name(self):
        return self.material_package_name.replace('_', ' ')

    @property
    def stylesheet_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self.stylesheet_file_path_in_memory,
            session=self._session,
            )

    @property
    def stylesheet_file_path_on_disk(self):
        if os.path.isfile(self._illustration_ly_file_path):
            for line in self.illustration_ly_file_manager.read_lines():
                if line.startswith(r'\include') and 'stylesheets' in line:
                    file_name = line.split()[-1].replace('"', '')
                    return file_name

    @property
    def user_input_attribute_names(self):
        return tuple([x[0] for x in self.user_input_demo_values])

    @property
    def user_input_module_path(self):
        if self._should_have_user_input_module:
            return os.path.join(self._filesystem_path, 'user_input.py')

    @property
    def user_input_wrapper_in_memory(self):
        return self._user_input_wrapper_in_memory

    ### PUBLIC METHODS ###

    def edit_and_execute_illustration_builder_module(self):
        r'''Edits and then executes illustration builder module.

        Returns none.
        '''
        self.edit_illustration_builder_module()
        self.run_python_on_illustration_builder_module()

    def edit_illustration_builder_module(self):
        r'''Edits illustration builder module.

        Returns none.
        '''
        self.illustration_builder_module_manager.edit()

    def edit_material_definition_module(self):
        r'''Edits material definition module.

        Returns none.
        '''
        file_path = self._material_definition_module_path
        self._io_manager.edit(file_path)

    def edit_output_material(self):
        r'''Edits output material.

        Returns none.
        '''
        if not self._output_material_editor:
            return
        output_material = self.output_material
        if not hasattr(self, '_output_material_maker'):
            output_material_handler_callable = self._output_material_editor
        elif output_material is None and self._output_material_maker and \
            issubclass(self._output_material_maker, wizards.Wizard):
            output_material_handler_callable = self._output_material_maker
        else:
            output_material_handler_callable = self._output_material_editor
        output_material_handler = output_material_handler_callable(
            target=output_material, session=self._session)
        output_material_handler._run()
        if self._session._backtrack():
            return
        _output_material_module_import_statements = \
            self._output_material_module_import_statements
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = \
                self.make_output_material_module_body_lines(
                    output_material_handler.target)
        else:
            line = '{} = {}'
            target_repr = self._get_storage_format(
                output_material_handler.target)
            line = line.format(
                self.material_package_name,
                target_repr,
                )
            output_material_module_body_lines = [line]
        self.write_output_material(
            _output_material_module_import_statements=\
                _output_material_module_import_statements,
            output_material_module_body_lines=\
                output_material_module_body_lines,
            )

    def edit_stylesheet_file(self, prompt=True):
        r'''Edits stylesheet file.

        Returns none.
        '''
        if self.stylesheet_file_path_in_memory:
            self.stylesheet_file_manager.edit()
        elif prompt:
            message = 'select stylesheet first.'
            self._io_manager.proceed(message)

    def read_user_input_wrapper_from_disk(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.user_input_module_path,
            session=self._session,
            )
        result = manager._execute_file_lines(
            file_path=self.user_input_module_path,
            return_attribute_name='user_input_wrapper',
            )
        return result

    def remove_illustration_builder_module(self, prompt=True):
        if os.path.isfile(self._illustration_builder_module_path):
            self.illustration_builder_module_manager.remove(prompt=prompt)

    def remove_illustration_ly(self, prompt=True):
        if os.path.isfile(self._illustration_ly_file_path):
            self.illustration_ly_file_manager.remove(prompt=prompt)

    def remove_illustration_pdf(self, prompt=True):
        if os.path.isfile(self._illustration_pdf_file_path):
            self.illustration_pdf_file_manager.remove(prompt=prompt)

    def remove_material_definition_module(self, prompt=True):
        from scoremanager import managers
        if os.path.isfile(self._material_definition_module_path):
            manager = managers.FileManager(
                self._material_definition_module_path,
                session=self._session,
                )
            manager.remove(prompt=prompt)

    def remove_output_material_module(self, prompt=True):
        self.remove_illustration_builder_module(prompt=False)
        if os.path.isfile(self.output_material_module_path):
            self.output_material_module_manager._remove()

    def remove_user_input_module(self, prompt=True):
        from scoremanager import managers
        if os.path.isfile(self.user_input_module_path):
            manager = managers.FileManager(
                self.user_input_module_path,
                session=self._session,
                )
            manager._remove()

    def rename_package(self):
        base_name = os.path.basename(self._filesystem_path)
        line = 'current name: {}'.format(base_name)
        self._io_manager.display(line)
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self._session._backtrack():
            return
        lines = []
        lines.append('current name: {}'.format(base_name))
        lines.append('new name:     {}'.format(new_package_name))
        lines.append('')
        self._io_manager.display(lines)
        if not self._io_manager.confirm():
            return
        old_directory_path = self._filesystem_path
        new_directory_path = old_directory_path.replace(
            base_name,
            new_package_name,
            )
        is_git_versioned, is_svn_versioned = False, False
        if self._is_git_versioned():
            is_git_versioned = True
            command = 'git mv {} {}'
        elif self._is_svn_versioned():
            is_svn_versioend = True
            command = 'svn mv {} {}'
        elif self._is_svn_versioned():
            command = 'mv {} {}'
        command = command.format(self._filesystem_path, new_directory_path)
        self._io_manager.spawn_subprocess(command)
        self._path = new_directory_path
        for directory_entry in os.listdir(new_directory_path):
            if directory_entry.endswith('.py'):
                file_path = os.path.join(new_directory_path, directory_entry)
                result = os.path.splitext(base_name)
                old_package_name, extension = result
                self.replace_in_file(
                    file_path,
                    old_package_name,
                    new_package_name,
                    )
        commit_message = 'Renamed material package.\n\n'
        commit_message += 'OLD: {!r}.\n\n'.format(old_package_name)
        commit_message += 'NEW: {!r}.'.format(new_package_name)
        if is_git_versioned:
            command = 'git add -A {}'.format(new_directory_path)
            self._io_manager.spawn_subprocess(command)
            command = 'git commit -m "{}" {} {}'
            command = command.format(
                commit_message, 
                new_directory_path,
                old_directory_path,
                )
            self._io_manager.spawn_subprocess(command)
        elif is_svn_versioned:
            parent_directory_path = os.path.dirname(self._filesystem_path)
            command = 'svn commit -m "{}" {}'
            command = command.format(commit_message, parent_directory_path)
            self._io_manager.spawn_subprocess(command)
        self._session._is_backtracking_locally = True

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
            self._material_definition_module_path,
            session=self._session,
            )
        manager._run_abjad()

    def run_python_on_illustration_builder_module(self):
        self.illustration_builder_module_manager._run_python(prompt=True)

    def run_python_on_material_definition_module(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self._material_definition_module_path,
            session=self._session,
            )
        manager._run_python()

    def select_material_manager(self, prompt=True):
        from scoremanager import wranglers
        material_manager_wrangler = wranglers.MaterialManagerWrangler(
            session=self._session)
        with self._backtracking:
            material_manager = \
                material_manager_wrangler.select_material_manager_class_name_interactively()
        if self._session._backtrack():
            return
        self._add_metadatum(
            'material_manager',
            material_manager.class_name,
            )
        message = 'user input handler selected.'
        self._io_manager.proceed(message=message, prompt=prompt)

    def select_stylesheet(self, prompt=True):
        from scoremanager import wranglers
        stylesheet_file_wrangler = wranglers.StylesheetFileWrangler(
            session=self._session)
        with self._backtracking:
            stylesheet_file_path = \
                stylesheet_file_wrangler.select_asset_filesystem_path()
        if self._session._backtrack():
            return
        self.stylesheet_file_path_in_memory = stylesheet_file_path
        self._io_manager.proceed(
            'stylesheet selected.', 
            prompt=prompt,
            )

    def view_illustration_ly(self):
        self.illustration_ly_file_manager.view()

    def view_illustration_pdf(self):
        self.illustration_pdf_file_manager.view()

    def view_output_material_module(self):
        self.output_material_module_manager.view()

    def write_illustration_ly(self, prompt=True):
        illustration = self.illustration
        topleveltools.persist(illustration).as_pdf(
            self._illustration_ly_file_path,
            )
        self._io_manager.proceed(
            'LilyPond file written to disk.',
            prompt=prompt,
            )

    def write_illustration_ly_and_pdf(self, prompt=True):
        illustration = self._illustrate()
        topleveltools.persist(illustration).as_pdf(
            self._illustration_pdf_file_path,
            )
        self._io_manager.proceed(
            'PDF and LilyPond file written to disk.',
            prompt=prompt,
            )

    def write_illustration_pdf(self, prompt=True):
        illustration = self._illustrate()
        topleveltools.persist(illustration).as_pdf(
            self._illustration_pdf_file_path,
            )
        self._io_manager.proceed(
            'PDF written to disk.',
            prompt=prompt)

    def write_material_definition_module_boilerplate(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self._material_definition_module_path,
            session=self._session,
            )
        manager.write_boilerplate()

    def write_output_material(
        self,
        _output_material_module_import_statements=None,
        output_material_module_body_lines=None,
        prompt=True,
        ):
        if self._get_metadatum('is_static'):
            source_path = self._material_definition_module_path
            target_path = self.output_material_module_path
            shutil.copy(source_path, target_path)
            return
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        if _output_material_module_import_statements is None or \
            output_material_module_body_lines is None:
            pair = self._output_material_module_import_statements_and_output_material_module_body_lines
            _output_material_module_import_statements = pair[0]
            output_material_module_body_lines = pair[1]
        if _output_material_module_import_statements is None:
            _output_material_module_import_statements = []
        _output_material_module_import_statements = [
            x + '\n'
            for x in _output_material_module_import_statements
            ]
        lines.extend(_output_material_module_import_statements)
        lines.extend(['\n', '\n'])
        lines.extend(output_material_module_body_lines)
        lines = ''.join(lines)
        manager = self.output_material_module_manager
        with file(manager._filesystem_path, 'w') as file_pointer:
            file_pointer.write(lines)
        self._add_metadatum('is_material_package', True)
        if hasattr(self, 'generic_output_name'):
            self._add_metadatum('generic_output_name', self.generic_output_name)
        message = 'output material written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    def write_output_material_module_boilerplate(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.output_material_module_path,
            session=self._session,
            )
        manager.write_boilerplate()

    def write_stub_illustration_builder_module(self, prompt=True):
        material_package_path = self._package_path
        material_package_name = material_package_path.split('.')[-1]
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
        lines.append(line)
        line = 'illustration = lilypondfiletools.'
        line += 'make_basic_lilypond_file(score)\n'
        lines.append(line)
        file_path = os.path.join(
            self._filesystem_path,
            'illustration_builder.py',
            )
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(lines))
        message = 'stub illustration builder written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    def write_stub_music_material_definition(self):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        lines.append('_output_material_module_import_statements = []')
        lines.append('\n\n\n')
        line = '{} = None'.format(self.material_package_name)
        lines.append(line)
        lines = ''.join(lines)
        file_pointer = file(self._material_definition_module_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

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
        file_pointer = file(self.user_input_module_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt=False):
        r'''Clears user input wrapper.

        Returns none.
        '''
        if self.user_input_wrapper_in_memory.is_empty:
            message = 'user input already empty.'
            self._io_manager.proceed(message, prompt=prompt)
        else:
            self.user_input_wrapper_in_memory.clear()
            wrapper = self.user_input_wrapper_in_memory
            self.write_user_input_wrapper(wrapper)
            message = 'user input wrapper cleared and written to disk.'
            self._io_manager.proceed(message, prompt=prompt)

    def display_user_input_demo_values(self, prompt=True):
        r'''Displays user input demo values.

        Returns none.
        '''
        lines = []
        for i, (key, value) in enumerate(self.user_input_demo_values):
            line = '    {}: {!r}'.format(key.replace('_', ' '), value)
            lines.append(line)
        lines.append('')
        self._io_manager.display(lines)
        self._io_manager.proceed(prompt=prompt)

    def load_user_input_wrapper_demo_values(self, prompt=False):
        user_input_demo_values = copy.deepcopy(
            type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            self.user_input_wrapper_in_memory[key] = value
        wrapper = self.user_input_wrapper_in_memory
        self.write_user_input_wrapper(wrapper)
        self._io_manager.proceed(
            'demo values loaded and written to disk.',
            prompt=prompt,
            )

    def make_output_material_from_user_input_wrapper_in_memory(self):
        output_material = self._output_material_maker(
            *self.user_input_wrapper_in_memory.list_values())
        assert type(self)._output_material_checker(
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
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_integer_in_range(
            'start at element number', 1, total_elements, default_value=1)
        with self._backtracking:
            start_element_number = getter._run()
        if self._session._backtrack():
            return
        current_element_number = start_element_number
        current_element_index = current_element_number - 1
        while True:
            with self._backtracking:
                self._edit_user_input_wrapper_at_number(
                    current_element_number, include_newline=False)
            if self._session._backtrack():
                return
            current_element_index += 1
            current_element_index %= total_elements
            current_element_number = current_element_index + 1
            if current_element_number == start_element_number:
                break

    def toggle_user_input_values_default_status(self):
        self._session.toggle_user_input_values_default_status()

    def view_user_input_module(
        self,
        pending_user_input=None,
        ):
        from scoremanager import managers
        self._io_manager._assign_user_input(pending_user_input)
        file_path = self.user_input_module_path
        self._io_manager.view(file_path)

    def write_stub_user_input_module(self, prompt=False):
        wrapper = self._initialize_empty_user_input_wrapper()
        self.write_user_input_wrapper(wrapper)
        self._io_manager.proceed(
            'stub user input module written to disk.',
            prompt=prompt,
            )
