# -*- encoding: utf-8 -*-
import copy
import os
import shutil
import traceback
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools import topleveltools
from scoremanager import wizards
from scoremanager.managers.PackageManager import PackageManager


class MaterialManager(PackageManager):
    r'''Material manager.

    ..  container:: example

        ::

            >>> import os
            >>> configuration = scoremanager.core.ScoreManagerConfiguration()
            >>> session = scoremanager.core.Session()
            >>> path = os.path.join(
            ...     configuration.abjad_material_packages_directory_path,
            ...     'example_numbers',
            ...     )
            >>> manager = scoremanager.managers.MaterialManager(
            ...     path=path,
            ...     session=session,
            ...     )
            >>> manager
            MaterialManager('.../materials/example_numbers')

    '''

    ### INTIALIZER ###

    def __init__(self, path=None, session=None):
        if path is not None:
            assert os.path.sep in path
        PackageManager.__init__(
            self,
            path=path,
            session=session,
            )
        self._generic_output_name = None
        self._generic_class_name = 'material manager'
        self._output_module_import_statements = []
        self._stylesheet_file_path_in_memory = None
        self._user_input_wrapper_in_memory = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

    @property
    def _illustration_builder_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._illustration_builder_module_path,
            session=self._session,
            )

    @property
    def _illustration_builder_module_path(self):
        return os.path.join(
            self._path, 
            'illustration_builder.py',
            )

    @property
    def _illustration_ly_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._illustration_ly_file_path,
            session=self._session,
            )

    @property
    def _illustration_ly_file_path(self):
        return os.path.join(
            self._path, 
            'illustration.ly',
            )

    @property
    def _illustration_pdf_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._illustration_pdf_file_path,
            session=self._session,
            )

    @property
    def _illustration_pdf_file_path(self):
        return os.path.join(
            self._path, 
            'illustration.pdf',
            )

    @property
    def _definition_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._definition_module_path,
            session=self._session,
            )

    @property
    def _definition_module_path(self):
        path = os.path.join(
            self._path, 
            'material_definition.py',
            )
        return path

    @property
    def _material_package_name(self):
        return os.path.basename(self._path)

    @property
    def _output_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._output_module_path,
            session=self._session,
            )

    @property
    def _output_module_path(self):
        return os.path.join(self._path, 'output_material.py')

    @property
    def _stylesheet_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._stylesheet_file_path_in_memory,
            session=self._session,
            )

    @property
    def _user_input_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._user_input_module_path,
            session=self._session,
            )

    @property
    def _user_input_module_path(self):
        return os.path.join(self._path, 'user_input.py')

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'ibe': self.edit_illustration_builder_module,
            'ibei': self.edit_and_interpret_illustration_builder_module,
            'ibm': self.write_illustration_builder_module_stub,
            'ibrm': self.remove_illustration_builder_module,
            'ibs': self.write_illustration_builder_module_stub,
            'ibi': self.interpret_illustration_builder_module,
            'lym': self.write_illustration_ly,
            'lyrm': self.remove_illustration_ly,
            'lyv': self.view_illustration_ly,
            'dmbp': self.write_definition_module_boilerplate,
            'dme': self.edit_definition_module,
            'dmrm': self.remove_definition_module,
            'dms': self.write_definition_module_stub,
            'dmi': self.interpret_definition_module,
            'ommbp': self.write_output_module_boilerplate,
            'ommm': self.write_output_material,
            'omi': self.edit_output_material,
            'ommmrm': self.remove_output_module,
            'ommv': self.view_output_module,
            'pdfm': self.write_illustration_ly_and_pdf,
            'pdfrm': self.remove_illustration_pdf,
            'pdfv': self.view_illustration_pdf,
            'ren': self.rename,
            'sse': self.edit_stylesheet,
            'sss': self.select_stylesheet,
            'uid': self.remove_user_input_module,
            'uic': self.clear_user_input_wrapper,
            'uil': self.load_user_input_wrapper_demo_values,
            'uip': self.populate_user_input_wrapper,
            'uis': self.display_user_input_demo_values,
            'uit': self.toggle_user_input_values_default_status,
            'uimv': self.view_user_input_module,
            })
        return result

    ### PRIVATE METHODS ###

    def _can_make_output_material(self):
        if os.path.isfile(self._definition_module_path):
            return True
        if bool(self._user_input_wrapper_in_memory) and \
            self._user_input_wrapper_in_memory.is_complete:
            return True
        return False

    @staticmethod
    def _check_output_material(material):
        return True

    def _edit_user_input_wrapper_at_number(
        self,
        number,
        include_newline=True,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        number = int(number)
        if self._user_input_wrapper_in_memory is None:
            return
        if len(self._user_input_wrapper_in_memory) < number:
            return
        index = number - 1
        key, current_value = \
            self._user_input_wrapper_in_memory.list_items()[index]
        test_tuple = type(self).user_input_tests.fget(self)[index]
        test = test_tuple[1]
        if len(test_tuple) == 3:
            setup_statement = test_tuple[2]
        else:
            setup_statement = 'evaluated_user_input = {}'
        if self._session.use_current_user_input_values_as_default:
            default_value = current_value
        else:
            default_value = None
        getter = self._io_manager.make_getter(
            allow_none=True,
            include_newlines=include_newline,
            )
        spaced_attribute_name = key.replace('_', ' ')
        message = "value for '{}' must satisfy " + test.__name__ + '().'
        getter._make_prompt(
            spaced_attribute_name,
            help_template=message,
            validation_function=test,
            setup_statements=['from abjad import *', setup_statement],
            default_value=default_value,
            )
        new_value = getter._run()
        if self._session._backtrack():
            return
        self._user_input_wrapper_in_memory[key] = new_value
        wrapper = self._user_input_wrapper_in_memory
        self._write_user_input_wrapper(wrapper)

    def _execute_output_module(self):
        attribute_names = (self._material_package_name,)
        result = self._output_module_manager._execute(
            attribute_names=attribute_names,
            )
        if result:
            assert len(result) == 1
            output_material = result[0]
            return output_material

    @staticmethod
    def _get_output_material_editor(target=None, session=None):
        return

    def _get_output_module_import_statements_and_body_lines(self):
        if os.path.isfile(self._definition_module_path):
            result = self._retrieve_import_statements_and_output_material()
            output_module_import_statements, output_material = result
        else:
            output_module_import_statements = \
                self._output_module_import_statements
            output_material = \
                self._make_output_material_from_user_input_wrapper_in_memory()
        line = '{} = {}'
        output_material_storage_format = \
            self._get_storage_format(output_material)
        line = line.format(
            self._material_package_name,
            output_material_storage_format,
            )
        body_lines = [line]
        return (
            output_module_import_statements,
            body_lines,
            )

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

    # TODO: change property to method
    # TODO: make illustration work the same way as for segment PDF rendering;
    #       use something like _interpret_in_external_process()
    def _illustrate(self):
        # TODO: replace old and dangerous import_output_material_safely()
        output_material = \
            self._output_module_manager.import_output_material_safely()
        kwargs = {}
        kwargs['title'] = self._space_delimited_lowercase_name
        if self._session.is_in_score:
            title = self._session.current_score_package_manager.title
            string = '({})'.format(title)
            kwargs['subtitle'] = string
        illustration = self.illustration_builder(output_material, **kwargs)
        if illustration and self._stylesheet_file_path_in_memory:
            path = self._stylesheet_file_path_in_memory
            illustration.file_initial_user_includes.append(path)
        return illustration

    def _initialize_empty_user_input_wrapper(self):
        from scoremanager import editors
        user_input_wrapper = editors.UserInputWrapper()
        user_input_wrapper._user_input_module_import_statements = \
            getattr(self, 'user_input_module_import_statements', [])[:]
        names = tuple([x[0] for x in self.user_input_demo_values])
        for user_input_attribute_name in names:
            user_input_wrapper[user_input_attribute_name] = None
        return user_input_wrapper

    def _initialize_user_input_wrapper_in_memory(self):
        from scoremanager import managers
        user_input_module_path = self._user_input_module_path
        if os.path.exists(self._user_input_module_path):
            user_input_wrapper = self._read_user_input_wrapper_from_disk()
            if user_input_wrapper:
                user_input_wrapper._user_input_module_import_statements = \
                    getattr(self, 'user_input_module_import_statements', [])[:]
        else:
            user_input_wrapper = self._initialize_empty_user_input_wrapper()
        self._user_input_wrapper_in_memory = user_input_wrapper

    def _interpret_definition_module(self):
        if not os.path.isfile(self._definition_module_path):
            return
        result = self._definition_module_manager._execute(
            attribute_names=(self._material_package_name,),
            )
        if result:
            assert len(result) == 1
            result = result[0]
            return result

    def _make_illustration_builder_menu_section(
        self,
        menu,
        ):
        name = 'illustration builder'
        section = menu.make_command_section(name=name)
        if os.path.isfile(self._output_module_path):
            if os.path.isfile(self._illustration_builder_module_path):
                string = 'illustration builder - edit'
                section.append((string, 'ibe'))
                string = 'illustration builder - edit & interpret'
                section.append((string, 'ibei'))
                string = 'illustration builder - interpret'
                section.append((string, 'ibi'))
                string = 'illustration builder - remove'
                section.append((string, 'ibrm'))
                string = 'illustration builder - stub'
                section.append((string, 'ibs'))
            else:
                string = 'illustration builder - make'
                section.append((string, 'ibm'))

    def _make_illustration_ly_menu_section(self, menu):
        if os.path.isfile(self._output_module_path) or \
            os.path.isfile(self._illustration_ly_file_path):
            section = menu.make_command_section(name='output ly')
        if os.path.isfile(self._output_module_path):
            if os.path.isfile(self._illustration_builder_module_path) or \
                self._read_material_manager_class_name():
                section.append(('output ly - make', 'lym'))
        if os.path.isfile(self._illustration_ly_file_path):
            section.append(('output ly - remove', 'lyrm'))
            section.append(('output ly - view', 'lyv'))

    def _make_illustration_pdf_menu_section(
        self,
        menu,
        ):
        name = 'illustration pdf'
        has_illustration_pdf_section = False
        if os.path.isfile(self._output_module_path) or \
            os.path.isfile(self._illustration_pdf_file_path):
            section = menu.make_command_section(name=name)
        if os.path.isfile(self._output_module_path):
            if os.path.isfile(self._illustration_builder_module_path) or \
                (self._read_material_manager_class_name() and
                getattr(self, '__illustrate__', None)):
                section.append(('output pdf - make', 'pdfm'))
                has_illustration_pdf_section = True
        if os.path.isfile(self._illustration_pdf_file_path):
            if not has_illustration_pdf_section:
                section = menu.make_command_section(name=name)
            section.append(('output pdf - remove', 'pdfrm'))
            section.append(('output pdf - view', 'pdfv'))

    def _make_main_menu(self):
        superclass = super(MaterialManager, self)
        where = self._where
        menu = superclass._make_main_menu(where=where)
        self._make_illustration_builder_menu_section(menu)
        has_initializer = os.path.isfile(self._initializer_file_path)
        self._make_initializer_menu_section(
            menu, 
            has_initializer=has_initializer,
            )
        self._make_material_definition_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_module_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_output_material_menu_section(menu)
        self._make_output_module_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_directory_menu_section(menu)
        self._make_stylesheet_menu_section(menu)
        if self._user_input_wrapper_in_memory:
            editor = self._get_output_material_editor(session=self._session)
            if not editor:
                self._make_user_input_module_menu_section(menu)
        try:
            material_summary_section = menu['material summary']
            menu.menu_sections.remove(material_summary_section)
            menu.menu_sections.insert(0, material_summary_section)
        except KeyError:
            pass
        self._make_material_tour_menu_section(menu)
        return menu

    def _make_main_menu_sections_with_user_input_wrapper(self, menu):
        editor = self._get_output_material_editor(session=self._session)
        if not editor:
            self._make_user_input_module_menu_section(menu)
        self._make_output_material_menu_section(menu)

    def _make_material_definition_menu_section(
        self,
        menu, 
        ):
        name = 'definition module'
        if not os.path.isfile(self._initializer_file_path):
            return
        if os.path.isfile(self._definition_module_path):
            section = menu.make_command_section(
                name=name,
                default_index=1
                )
            string = 'definition module - boilerplate'
            section.append((string, 'dmbp'))
            section.append(('definition module - edit', 'dme'))
            section.append(('definition module - interpret', 'dmi'))
            string = 'definition module - remove'
            section.append((string, 'dmrm'))
            section.append(('definition module - stub', 'dms'))
        elif self._read_material_manager_class_name() is None:
            section = menu.make_command_section(name=name)
            section.append(('definition module - stub', 'dms'))

    @staticmethod
    def _make_output_material():
        return

    def _make_output_material_from_user_input_wrapper_in_memory(self):
        output_material = self._make_output_material(
            *self._user_input_wrapper_in_memory.list_values())
        assert type(self)._check_output_material(
            output_material), repr(output_material)
        return output_material

    def _make_output_material_menu_section(self, menu):
        section = menu.make_command_section(name='output material')
        if self._should_have_output_material_section():
            editor = self._get_output_material_editor(session=self._session)
            if editor:
                section.append(('output material - interact', 'omi'))
                # TODO: encapsulate the following in an independent section
                if os.path.isfile(self._output_module_path):
                    output_material = self._execute_output_module()
                    editor = self._get_output_material_editor(
                        target=output_material,
                        session=self._session,
                        )
                    _target_summary_lines = editor._target_summary_lines
                    if _target_summary_lines:
                        contents_section = menu.make_attribute_section(
                            name='material summary',
                            title=_target_summary_lines,
                            )

    def _make_output_module_body_lines(self, output_material):
        if hasattr(output_material, '_storage_format_specification'):
            lines = format(output_material, 'storage').splitlines()
        else:
            lines = [repr(output_material)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self._material_package_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines

    def _make_output_module_menu_section(
        self,
        menu,
        ):
        if not os.path.isfile(self._initializer_file_path):
            return
        section = menu.make_command_section(name='output material module')
        string = 'output material module - boilerplate'
        section.append((string, 'ommbp'))
        if self._should_have_output_material_section():
            if self._can_make_output_material():
                section.append(('output material module - make', 'ommm'))
            if os.path.isfile(self._output_module_path):
                section.append(('output material module - remove', 'ommmrm'))
                section.append(('output material module - view', 'ommv'))

    def _make_stylesheet_menu_section(
        self,
        menu,
        ):
        name = 'stylesheets'
        section = menu.make_command_section(name=name)
        if os.path.isfile(self._output_module_path):
            section = menu.make_command_section(name=name)
            section.append(('stylesheet - edit', 'sse'))
            section.append(('stylesheet - select', 'sss'))

    def _make_user_input_module_menu_section(
        self,
        menu, 
        ):
        menu_entries = self._user_input_wrapper_in_memory.editable_lines
        numbered_section = menu.make_numbered_section(name='material summary')
        for menu_entry in menu_entries:
            numbered_section.append(menu_entry)
        section = menu.make_command_section(name='user input')
        section.append(('user input - clear', 'uic'))
        section.append(('user input - load demo values', 'uil'))
        section.append(('user input - populate', 'uip'))
        section.append(('user input - show demo values', 'uis'))
        section.append(('user input - toggle default mode', 'uit'))
        section = menu.make_command_section(name='user input module')
        section.append(('user input module - remove', 'uimrm'))
        section.append(('user input module - view', 'uimv'))

    def _read_material_manager_class_name(self):
        return self._get_metadatum('material_manager_class_name')

    def _read_user_input_wrapper_from_disk(self):
        result = self._user_input_module_manager._execute(
            path=self._user_input_module_path,
            attribute_names=('user_input_wrapper',),
            )
        assert len(result) == 1
        result = result[0]
        return result

    @staticmethod
    def _replace_in_file(file_path, old, new):
        with file(file_path, 'r') as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(new_file_lines))

    def _retrieve_import_statements_and_output_material(self):
        attribute_names = (
            'output_module_import_statements',
            self._material_package_name,
            )
        result = self._definition_module_manager._execute(
            attribute_names=attribute_names,
            )
        return result

    def _run_first_time(self):
        self._run(pending_user_input='omi')

    def _should_have_output_material_section(self):
        if os.path.isfile(self._definition_module_path):
            return True
        if bool(self._user_input_wrapper_in_memory) and \
            self._user_input_wrapper_in_memory.is_complete:
            return True
        editor = self._get_output_material_editor(session=self._session)
        if editor:
            return True
        return False

    def _write_definition_module_stub(self, prompt=True):
        self.write_definition_module_stub()
        message = 'stub material definition written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    def _write_user_input_module_stub(self, prompt=False):
        wrapper = self._initialize_empty_user_input_wrapper()
        self._write_user_input_wrapper(wrapper)
        self._io_manager.proceed(
            'stub user input module written to disk.',
            prompt=prompt,
            )

    def _write_user_input_wrapper(self, wrapper):
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
        file_pointer = file(self._user_input_module_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt=False):
        r'''Clears user input wrapper.

        Returns none.
        '''
        if self._user_input_wrapper_in_memory.is_empty:
            message = 'user input already empty.'
            self._io_manager.proceed(message, prompt=prompt)
        else:
            self._user_input_wrapper_in_memory.clear()
            wrapper = self._user_input_wrapper_in_memory
            self._write_user_input_wrapper(wrapper)
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

    def edit_and_interpret_illustration_builder_module(self):
        r'''Edits and then interprets illustration builder module.

        Returns none.
        '''
        self.edit_illustration_builder_module()
        self.interpret_illustration_builder_module()

    def edit_illustration_builder_module(self):
        r'''Edits illustration builder module.

        Returns none.
        '''
        self._illustration_builder_module_manager.edit()

    def edit_definition_module(self):
        r'''Edits material definition module.

        Returns none.
        '''
        file_path = self._definition_module_path
        self._io_manager.edit(file_path)

    def edit_output_material(self):
        r'''Edits output material.

        Returns none.
        '''
        editor = self._get_output_material_editor(session=self._session)
        if not editor:
            return
        output_material = self._execute_output_module()
        if not hasattr(self, '_make_output_material'):
            output_material_handler = self._get_output_material_editor(
                target=output_material,
                session=self._session,
                )
        elif output_material is None and self._make_output_material() and \
            isinstance(self._make_output_material(), wizards.Wizard):
            output_material_handler = self._make_output_material(
                target=output_material,
                session=self._session,
                )
        else:
            output_material_handler = self._get_output_material_editor(
                target=output_material,
                session=self._session,
                )
        output_material_handler._run()
        if self._session._backtrack():
            return
        output_module_import_statements = \
            self._output_module_import_statements
        if hasattr(self, '_make_output_module_body_lines'):
            output_module_body_lines = \
                self._make_output_module_body_lines(
                    output_material_handler.target)
        else:
            line = '{} = {}'
            target_repr = self._get_storage_format(
                output_material_handler.target)
            line = line.format(
                self._material_package_name,
                target_repr,
                )
            output_module_body_lines = [line]
        self.write_output_material(
            output_module_import_statements=\
                output_module_import_statements,
            output_module_body_lines=\
                output_module_body_lines,
            )

    def edit_stylesheet(self, prompt=True):
        r'''Edits stylesheet.

        Returns none.
        '''
        if self._stylesheet_file_path_in_memory:
            self._stylesheet_manager.edit()
        elif prompt:
            message = 'select stylesheet first.'
            self._io_manager.proceed(message)

    def interpret_illustration_builder_module(self):
        r'''Runs Python on illustration builder module.

        Returns none.
        '''
        self._illustration_builder_module_manager._interpret(prompt=True)

    def interpret_definition_module(self):
        r'''Runs Python on material definition module.

        Returns none.
        '''
        self._definition_module_manager._interpret()

    def load_user_input_wrapper_demo_values(self, prompt=False):
        r'''Loads user input wrapper demo values.

        Returns none.
        '''
        user_input_demo_values = type(self).user_input_demo_values.fget(self)
        user_input_demo_values = copy.deepcopy(user_input_demo_values)
        for key, value in user_input_demo_values:
            self._user_input_wrapper_in_memory[key] = value
        wrapper = self._user_input_wrapper_in_memory
        self._write_user_input_wrapper(wrapper)
        self._io_manager.proceed(
            'demo values loaded and written to disk.',
            prompt=prompt,
            )

    def populate_user_input_wrapper(self, prompt=False):
        r'''Populates user input wrapper.

        Returns none.
        '''
        total_elements = len(self._user_input_wrapper_in_memory)
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_integer_in_range(
            'start at element number', 
            1, 
            total_elements, 
            default_value=1,
            )
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

    def remove_illustration_builder_module(self, prompt=True):
        r'''Removes illustration builder module.

        Returns none.
        '''
        self._illustration_builder_module_manager.remove(prompt=prompt)

    def remove_illustration_ly(self, prompt=True):
        r'''Removes illustration ly.

        Returns none.
        '''
        self._illustration_ly_file_manager.remove(prompt=prompt)

    def remove_illustration_pdf(self, prompt=True):
        r'''Removes illustration PDF.

        Returns none.
        '''
        self._illustration_pdf_file_manager.remove(prompt=prompt)

    def remove_definition_module(self, prompt=True):
        r'''Removes material definition module.

        Returns none.
        '''
        self._definition_module_manager.remove(prompt=prompt)

    def remove_output_module(self, prompt=True):
        r'''Removes output material module.

        Returns none.
        '''
        self._output_module_manager.remove(prompt=prompt)

    def remove_user_input_module(self, prompt=True):
        r'''Removes user input module.

        Returns none.
        '''
        self._user_input_module_manager.remove(prompt=prompt)

    def rename(self):
        r'''Renames material package.

        Returns none.
        '''
        base_name = os.path.basename(self._path)
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
        old_directory_path = self._path
        new_directory_path = old_directory_path.replace(
            base_name,
            new_package_name,
            )
        is_in_git_repository, is_svn_versioned = False, False
        if self._is_in_git_repository():
            is_in_git_repository = True
            command = 'git mv {} {}'
        elif self._is_svn_versioned():
            is_svn_versioned = True
            command = 'svn mv {} {}'
        else:
            command = 'mv {} {}'
        command = command.format(self._path, new_directory_path)
        self._io_manager.spawn_subprocess(command)
        self._path = new_directory_path
        for directory_entry in os.listdir(new_directory_path):
            if directory_entry.endswith('.py'):
                file_path = os.path.join(new_directory_path, directory_entry)
                result = os.path.splitext(base_name)
                old_package_name, extension = result
                self._replace_in_file(
                    file_path,
                    old_package_name,
                    new_package_name,
                    )
        commit_message = 'Renamed material package.\n\n'
        commit_message += 'OLD: {!r}.\n\n'.format(old_package_name)
        commit_message += 'NEW: {!r}.'.format(new_package_name)
        if is_in_git_repository:
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
            parent_directory_path = os.path.dirname(self._path)
            command = 'svn commit -m "{}" {}'
            command = command.format(commit_message, parent_directory_path)
            self._io_manager.spawn_subprocess(command)
        self._session._is_backtracking_locally = True

    def select_stylesheet(self, prompt=True):
        r'''Selects stylesheet.

        Returns none.
        '''
        from scoremanager import wranglers
        wrangler = wranglers.StylesheetWrangler(session=self._session)
        with self._backtracking:
            stylesheet_file_path = wrangler.select_asset_path()
        if self._session._backtrack():
            return
        self._stylesheet_file_path_in_memory = stylesheet_file_path
        self._io_manager.proceed(
            'stylesheet selected.', 
            prompt=prompt,
            )

    def toggle_user_input_values_default_status(self):
        r'''Toggles user input values default status.

        Returns none.
        '''
        self._session.toggle_user_input_values_default_status()

    def view_illustration_ly(self):
        r'''Views illustration LilyPond file.

        Returns none.
        '''
        self._illustration_ly_file_manager.view()

    def view_illustration_pdf(self):
        r'''Views illustration PDF.

        Returns none.
        '''
        self._illustration_pdf_file_manager.view()

    def view_output_module(self):
        r'''Views output material module.

        Returns none.
        '''
        self._output_module_manager.view()

    def view_user_input_module(
        self,
        pending_user_input=None,
        ):
        r'''Views user input module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        file_path = self._user_input_module_path
        self._io_manager.view(file_path)

    def write_illustration_builder_module_stub(self, prompt=True):
        r'''Writes stub illustration builder module.

        Returns none.
        '''
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
            self._path,
            'illustration_builder.py',
            )
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(lines))
        message = 'stub illustration builder written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    def write_illustration_ly(self, prompt=True):
        r'''Writes illustration LilyPond file.

        Returns none.
        '''
        illustration = self.illustration
        topleveltools.persist(illustration).as_pdf(
            self._illustration_ly_file_path,
            )
        self._io_manager.proceed(
            'LilyPond file written to disk.',
            prompt=prompt,
            )

    def write_illustration_ly_and_pdf(self, prompt=True):
        r'''Writes illustration LilyPond file and PDF.

        Returns none.
        '''
        illustration = self._illustrate()
        topleveltools.persist(illustration).as_pdf(
            self._illustration_pdf_file_path,
            )
        self._io_manager.proceed(
            'PDF and LilyPond file written to disk.',
            prompt=prompt,
            )

    def write_definition_module_boilerplate(self):
        r'''Writes material definition module boilerplate.

        Returns none.
        '''
        self._definition_module_manager.write_boilerplate()

    def write_definition_module_stub(self):
        r'''Writes stub material definition module.

        Returns none.
        '''
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        lines.append('output_module_import_statements = []')
        lines.append('\n\n\n')
        line = '{} = None'.format(self._material_package_name)
        lines.append(line)
        lines = ''.join(lines)
        file_pointer = file(self._definition_module_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    def write_output_material(
        self,
        output_module_import_statements=None,
        output_module_body_lines=None,
        prompt=True,
        ):
        r'''Writes output material.

        Returns none.
        '''
        if self._get_metadatum('is_static'):
            source_path = self._definition_module_path
            target_path = self._output_module_path
            shutil.copy(source_path, target_path)
            return
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        if output_module_import_statements is None or \
            output_module_body_lines is None:
            pair = self._get_output_module_import_statements_and_body_lines()
            output_module_import_statements = pair[0]
            output_module_body_lines = pair[1]
        if output_module_import_statements is None:
            output_module_import_statements = []
        output_module_import_statements = [
            x + '\n'
            for x in output_module_import_statements
            ]
        lines.extend(output_module_import_statements)
        lines.extend(['\n', '\n'])
        lines.extend(output_module_body_lines)
        lines = ''.join(lines)
        manager = self._output_module_manager
        with file(manager._path, 'w') as file_pointer:
            file_pointer.write(lines)
        self._add_metadatum('is_material_package', True)
        if hasattr(self, '_generic_output_name'):
            generic_output_name = self._generic_output_name
            self._add_metadatum('generic_output_name', generic_output_name)
        message = 'output material written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    def write_output_module_boilerplate(self):
        r'''Writes output material module boilerplate.

        Returns none.
        '''
        self._output_module_manager.write_boilerplate()
