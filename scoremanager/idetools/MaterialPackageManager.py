# -*- encoding: utf-8 -*-
import collections
import copy
import os
from abjad.tools import systemtools
from scoremanager.idetools.ScoreInternalPackageManager import \
    ScoreInternalPackageManager


class MaterialPackageManager(ScoreInternalPackageManager):
    r'''Material package manager.


    ..  container:: example

        ::

            >>> import os
            >>> configuration = scoremanager.idetools.Configuration()
            >>> session = scoremanager.idetools.Session()
            >>> path = os.path.join(
            ...     configuration.abjad_material_packages_directory,
            ...     'example_numbers',
            ...     )
            >>> manager = scoremanager.idetools.MaterialPackageManager(
            ...     path=path,
            ...     session=session,
            ...     )
            >>> manager
            MaterialPackageManager('.../materials/example_numbers')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_output_py_import_statements',
        )

    ### INTIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(MaterialPackageManager, self)
        superclass.__init__(path=path, session=session)
        optional_files = list(self._optional_files)
        optional_files.extend([
            '__illustrate__.py',
            'illustration.ly',
            'illustration.pdf',
            'maker.py',
            'output.py',
            ])
        self._optional_files = tuple(optional_files)
        self._output_py_import_statements = [
            self._abjad_import_statement,
            ]

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        name = self._space_delimited_lowercase_name
        if self._session.is_in_score:
            return name
        configuration = self._configuration
        annotation = configuration._path_to_storehouse_annotation(self._path)
        string = '{} ({})'
        string = string.format(name, annotation)
        return string

    @property
    def _definition_py_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _handlertools_import_statement(self):
        return 'from experimental.tools import handlertools'

    @property
    def _illustrate_py_path(self):
        return os.path.join(self._path, '__illustrate__.py')

    @property
    def _illustration_ly_path(self):
        return os.path.join(self._path, 'illustration.ly')

    @property
    def _illustration_pdf_path(self):
        return os.path.join(self._path, 'illustration.pdf')

    @property
    def _input_to_method(self):
        superclass = super(MaterialPackageManager, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'da': self.autoedit_definition_py,
            'dc': self.check_definition_py,
            'do': self.open_definition_py,
            'dp': self.output_definition_py,
            'ds': self.write_stub_definition_py,
            #
            'ie': self.edit_illustrate_py,
            'iei': self.edit_and_interpret_illustrate_py,
            'ii': self.interpret_illustrate_py,
            'is': self.write_stub_illustrate_py,
            #
            'ili': self.interpret_illustration_ly,
            'ilo': self.open_illustration_ly,
            'ipo': self.open_illustration_pdf,
            #
            'oc': self.check_output_py,
            'oi': self.illustrate_output_py,
            'oo': self.open_output_py,
            #
            'vdo': self.open_versioned_definition_py,
            'vilo': self.open_versioned_illustration_ly,
            'vipo': self.open_versioned_illustration_pdf,
            'voo': self.open_versioned_output_py,
            })
        return result

    @property
    def _maker_py_path(self):
        return os.path.join(self._path, 'maker.py')

    @property
    def _output_py_path(self):
        return os.path.join(self._path, 'output.py')

    @property
    def _score_package_manager(self):
        from scoremanager import idetools
        score_path = self._configuration._path_to_score_path(self._path)
        return idetools.ScorePackageManager(
            path=score_path,
            session=self._session,
            )

    @property
    def _source_paths(self):
        return (
            self._definition_py_path,
            self._output_py_path,
            self._illustration_ly_path,
            self._illustration_pdf_path,
            )

    ### PRIVATE METHODS ###

    def _can_make_output_material(self):
        if os.path.isfile(self._definition_py_path):
            return True
        return False

    @staticmethod
    def _check_output_material(material):
        return True

    def _execute_definition_py(self):
        result = self._io_manager.execute_file(
            path = self._definition_py_path,
            attribute_names=(self._package_name,)
            )
        if result and len(result) == 1:
            target = result[0]
            return target

    def _execute_output_py(self):
        attribute_names = (self._package_name,)
        result = self._io_manager.execute_file(
            path = self._output_py_path,
            attribute_names=attribute_names,
            )
        if result and len(result) == 1:
            output_material = result[0]
            return output_material

    def _get_storage_format(self, expr):
        if hasattr(expr, '_make_storage_format_with_overrides'):
            return expr._make_storage_format_with_overrides()
        elif hasattr(expr, '_storage_format_specification'):
            return format(expr, 'storage')
        return repr(expr)

    def _has_output_material_editor(self):
        if not os.path.isfile(self._definition_py_path):
            return True
        return False

    # TODO: decide whether the keep this method or not
    def _make_autoeditor_summary_menu_section(self, menu):
        return
        output_material = self._execute_output_py()
        if output_material is None:
            return
        autoeditor = self._io_manager._make_autoeditor(target=output_material)
        lines = autoeditor._get_target_summary_lines()
        lines = lines or ['(empty)']
        return menu.make_material_summary_section(lines=lines)

    def _make_definition_py_menu_section(self, menu):
        name = 'definition.py'
        commands = []
        if os.path.isfile(self._definition_py_path):
            is_hidden = False
            commands.append(('definition.py - autoedit', 'da'))
            commands.append(('definition.py - check', 'dc'))
            commands.append(('definition.py - open', 'do'))
            commands.append(('definition.py - output', 'dp'))
        else:
            is_hidden = True
            commands.append(('definition.py - stub', 'ds'))
        if commands:
            menu.make_command_section(
                is_hidden=is_hidden,
                commands=commands,
                name='definition.py',
                )

    def _make_definition_target_lines(self, target):
        if hasattr(target, '_storage_format_specification'):
            lines = format(target, 'storage').splitlines()
        else:
            lines = [repr(target)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self._package_name, lines[0])
        if ' makers.' in lines[0]:
            module = target.__class__.__module__
            parts = module.split('.')
            index = parts.index('makers')
            storehouse = parts[index-1]
            line = lines[0]
            unqualified = ' makers.'
            qualified = ' {}.makers.'.format(storehouse)
            line = line.replace(unqualified, qualified)
            lines[0] = line
        return lines

    def _make_illustrate_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustrate_py_path):
            is_hidden = False
            string = '__illustrate__.py - edit'
            commands.append((string, 'ie'))
            string = '__illustrate__.py - edit & interpret'
            commands.append((string, 'iei'))
            string = '__illustrate__.py - interpret'
            commands.append((string, 'ii'))
            string = '__illustrate__.py - stub'
            commands.append((string, 'is'))
        else:
            is_hidden = True
            string = '__illustrate__.py - stub'
            commands.append((string, 'is'))
        menu.make_command_section(
            is_hidden=is_hidden,
            commands=commands,
            name='__illustrate__.py',
            )

    def _make_illustration_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_ly_path):
            commands.append(('illustration.ly - interpret', 'ili'))
            commands.append(('illustration.ly - open', 'ilo'))
        if os.path.isfile(self._illustration_pdf_path):
            commands.append(('illustration.pdf - open', 'ipo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='illustration.pdf',
                )

    def _make_main_menu(self):
        superclass = super(MaterialPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_autoeditor_summary_menu_section(menu)
        self._make_illustrate_py_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_definition_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_py_menu_section(menu)
        self._make_output_py_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        self._make_versions_directory_menu_section(menu)
        return menu

    def _make_output_material_lines(self, output_material):
        if hasattr(output_material, '_storage_format_specification'):
            lines = format(output_material, 'storage').splitlines()
        else:
            lines = [repr(output_material)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self._package_name, lines[0])
        return lines

    def _make_output_material_triple(self):
        result = self._retrieve_import_statements_and_output_material()
        import_statements, output_material = result
        body_string = '{} = {}'
        output_material_name = self._package_name
        storage_format = self._get_storage_format(output_material)
        body_string = body_string.format(
            output_material_name,
            storage_format,
            )
        return (import_statements, body_string, output_material)

    def _make_output_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._output_py_path):
            commands.append(('output.py - check', 'oc'))
            commands.append(('output.py - illustrate', 'oi'))
            commands.append(('output.py - open', 'oo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='output.py',
                )

    def _make_package(self, metadata=None):
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._make_silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )
            self.write_metadata_py(metadata=metadata)
            self.write_stub_definition_py()

    def _make_temporary_illustrate_py_lines(self):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append('import os')
        lines.append(self._abjad_import_statement)
        line = 'from output import {}'
        line = line.format(self._package_name)
        lines.append(line)
        if os.path.isfile(self._illustrate_py_path):
            lines.append('from illustrate import __illustrate__')
        lines.append('')
        lines.append('')
        if os.path.isfile(self._illustrate_py_path):
            line = 'lilypond_file = __illustrate__({})'
        else:
            line = 'lilypond_file = {}.__illustrate__()'
        line = line.format(self._package_name)
        lines.append(line)
        lines.append('path = os.path.abspath(__file__)')
        lines.append('directory = os.path.dirname(path)')
        line = "path = os.path.join(directory, 'illustration.pdf')"
        lines.append(line)
        lines.append("persist(lilypond_file).as_pdf(path)")
        return lines

    def _make_version_package_messages(self):
        path = self._versions_directory
        greatest_version = self._io_manager._get_greatest_version_number(path)
        new_version = greatest_version + 1
        next_version_string = '%04d' % new_version
        messages = []
        for source_path in self._source_paths:
            if not source_path:
                continue
            if not os.path.isfile(source_path):
                continue
            message = ' FROM: {}'.format(source_path)
            messages.append(message)
            versions_directory = self._versions_directory
            base_name = os.path.basename(source_path)
            file_name, extension = os.path.splitext(base_name)
            name = '{}_{}{}'.format(
                file_name,
                next_version_string,
                extension,
                )
            target_path = os.path.join(versions_directory, name)
            message = '   TO: {}'.format(target_path)
            messages.append(message)
        return messages

    def _make_versions_directory_menu_section(self, menu):
        commands = []
        commands.append(('versions - definition.py - open', 'vdo'))
        commands.append(('versions - illustration.ly - open', 'vilo'))
        commands.append(('versions - illustration.pdf - open', 'vipo'))
        commands.append(('versions - output.py - open', 'voo'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='versions directory',
            )

    def _object_to_import_statements(self, object_):
        import_statements = []
        module = object_.__class__.__module__
        assert isinstance(module, str)
        parts = module.split('.')
        if 'makers' in parts:
            index = parts.index('makers')
            storehouse = parts[index-1]
            import_statement = 'import {}'.format(storehouse)
            import_statements.append(import_statement)
        return import_statements

    def _rename_interactively(
        self,
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        getter = self._io_manager._make_getter()
        getter.append_snake_case_package_name('enter new package name')
        new_package_name = getter._run()
        if self._session.is_backtracking:
            return
        base_name = os.path.basename(self._path)
        new_directory = self._path.replace(
            base_name,
            new_package_name,
            )
        messages = []
        messages.append('will change ...')
        messages.append(' FROM: {}'.format(self._path))
        messages.append('   TO: {}'.format(new_directory))
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._rename(new_directory)
        for directory_entry in os.listdir(new_directory):
            if directory_entry.endswith('.py'):
                path = os.path.join(new_directory, directory_entry)
                result = os.path.splitext(base_name)
                old_package_name, extension = result
                self._replace_in_file(
                    path,
                    old_package_name,
                    new_package_name,
                    )

    def _retrieve_import_statements_and_output_material(self):
        attribute_names = (
            'output_py_import_statements',
            self._package_name,
            )
        result = self._io_manager.execute_file(
            path=self._definition_py_path,
            attribute_names=attribute_names,
            )
        return result

    def _run_first_time(self):
        if self._session.pending_input:
            pending_input = 'oae ' + self._session.pending_input
            self._session._pending_input = pending_input
        else:
            self._session._pending_input = 'oae'
        self._run()

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_materials = True

    ### PUBLIC METHODS ###

    def autoedit_definition_py(self):
        r'''Autoedits ``definition.py``.

        Returns none.
        '''
        target = self._execute_definition_py()
        if target is None:
            message = 'no autoedit target found;'
            message += ' would you like to create one?'
            result = self._io_manager._confirm(message=message)
            if self._session.is_backtracking or not result:
                return
            selector = self._io_manager.selector
            selector = selector.make_autoeditable_class_selector()
            class_ = selector._run()
            if self._session.is_backtracking or not class_:
                return
            target = class_()
        autoeditor = self._io_manager._make_autoeditor(target=target)
        autoeditor._run()
        if self._session.is_backtracking:
            return
        target = autoeditor.target
        import_statements = []
        import_statements.append(self._abjad_import_statement)
        import_statements.extend(self._object_to_import_statements(target))
        target_lines = self._make_definition_target_lines(target)
        self.write_definition_py(
            import_statements=import_statements,
            target=target,
            target_lines=target_lines,
            )
        self._session._pending_redraw = True

    def autoedit_output_py(self):
        r'''Autoedits ``output.py``.

        Returns none.
        '''
        output_material = self._execute_output_py()
        if output_material is None:
            return
        autoeditor = self._io_manager._make_autoeditor(target=output_material)
        autoeditor._run()
        if self._session.is_backtracking:
            return
        output_material = autoeditor.target
        import_statements = self._output_py_import_statements
        import_statements.extend(
            self._object_to_import_statements(output_material))
        output_material_lines = self._make_output_material_lines(
            output_material)
        self.output_definition_py(
            import_statements=import_statements,
            output_material_lines=output_material_lines,
            output_material=output_material,
            )

    def check_definition_py(self, dry_run=False):
        r'''Checks ``definition.py``.

        Display errors generated during interpretation.
        '''
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._definition_py_path)
            return inputs, outputs
        stderr_lines = self._io_manager.check_file(self._definition_py_path)
        if stderr_lines:
            messages = [self._definition_py_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(self._definition_py_path)
            self._io_manager._display(message)

    def check_output_py(self, dry_run=False):
        r'''Checks ``output.py``.

        Display errors generated during interpretation.
        '''
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._output_py_path)
            return inputs, outputs
        stderr_lines = self._io_manager.check_file(self._output_py_path)
        if stderr_lines:
            messages = [self._output_py_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(self._output_py_path)
            self._io_manager._display(message)

    def edit_and_interpret_illustrate_py(self):
        r'''Edits and then interprets ``__illustrate.py__``.

        Returns none.
        '''
        self.edit_illustrate_py()
        self.interpret_illustrate_py()

    def edit_illustrate_py(self):
        r'''Edits ``__illustrate.py__``.

        Returns none.
        '''
        self._io_manager.edit(self._illustrate_py_path)

    def illustrate_output_py(self):
        r'''Illustrates ``output.py``.

        Creates ``illustration.pdf`` and ``illustration.ly`` files.

        Returns none.
        '''
        file_name = 'temporary_illustrate.py'
        path = os.path.join(self._path, file_name)
        with systemtools.FilesystemState(remove=[path]):
            lines = self._make_temporary_illustrate_py_lines()
            contents = '\n'.join(lines)
            self._io_manager.write(path, contents)
            self._io_manager.interpret_file(path)

    def interpret_illustrate_py(self):
        r'''Interprets ``__illustrate.py__``.

        Returns none.
        '''
        result = self._io_manager.interpret_file(self._illustrate_py_path)

    def interpret_illustration_ly(self):
        r'''Interprets ``illustration.ly``.

        Returns none.
        '''
        from scoremanager import idetools
        path = self._illustration_ly_path
        if os.path.isfile(path):
            self._io_manager.run_lilypond(path)
        else:
            message = 'illustration.ly file does not exist.'
            self._io_manager._display(message)

    def open_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def open_illustration_ly(self):
        r'''Opens ``illustration.ly``.

        Returns none.
        '''
        self._io_manager.open_file(self._illustration_ly_path)

    def open_illustration_pdf(self):
        r'''Opens ``illustration.pdf``.

        Returns none.
        '''
        self._io_manager.open_file(self._illustration_pdf_path)

    def open_output_py(self):
        r'''Opens ``output.py``.

        Returns none.
        '''
        self._io_manager.open_file(self._output_py_path)

    def open_versioned_definition_py(self):
        r'''Opens versioned ``definition.py``.

        Returns none.
        '''
        self._open_versioned_file('definition.py')

    def open_versioned_illustration_ly(self):
        r'''Opens versioned ``illustration.ly``.

        Returns none.
        '''
        self._open_versioned_file('illustration.ly')

    def open_versioned_illustration_pdf(self):
        r'''Opens versioned ``illustration.pdf``.

        Returns none.
        '''
        self._open_versioned_file('illustration.pdf')

    def open_versioned_output_py(self):
        r'''Opens versioned ``output.py``.

        Returns none.
        '''
        self._open_versioned_file('output.py')

    def output_definition_py(
        self,
        import_statements=None,
        output_material=None,
        output_material_lines=None,
        ):
        r'''Outputs ``definition.py`` to ``output.py``.

        Returns none.
        '''
        message = 'will write output material to {}.'
        message = message.format(self._output_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        if import_statements is None:
            assert output_material_lines is None
        else:
            assert isinstance(import_statements, list), repr(import_statements)
        if output_material_lines is None:
            assert import_statements is None
            assert output_material is None
        else:
            assert isinstance(output_material_lines, list), repr(
                output_material_lines)
            assert output_material is not None
        lines = []
        lines.append(self._configuration.unicode_directive)
        if output_material_lines is None:
            triple = self._make_output_material_triple()
            import_statements = triple[0]
            output_py_body_string = triple[1]
            output_material = triple[2]
            output_material_lines = [output_py_body_string]
        import_statements = import_statements or []
        if self._abjad_import_statement not in import_statements:
            import_statements.append(self._abjad_import_statement)
        statements_ = self._object_to_import_statements(output_material)
        for statement_ in statements_:
            if statement_ not in import_statements:
                import_statements.append(statement_)
        if any('handlertools' in _ for _ in output_material_lines):
            import_statements.append(self._handlertools_import_statement)
        if ' makers.' in output_material_lines[0]:
            module = output_material.__class__.__module__
            parts = module.split('.')
            index = parts.index('makers')
            storehouse = parts[index-1]
            line = output_material_lines[0]
            unqualified = ' makers.'
            qualified = ' {}.makers.'.format(storehouse)
            line = line.replace(unqualified, qualified)
            output_material_lines[0] = line
        lines.extend(import_statements)
        lines.append('')
        lines.append('')
        lines.extend(output_material_lines)
        contents = '\n'.join(lines)
        clear = not os.path.isfile(self._output_py_path)
        self._io_manager.write(self._output_py_path, contents)
        output_material_class_name = type(output_material).__name__
        self._add_metadatum(
            'output_material_class_name', 
            output_material_class_name,
            )
        self._session._pending_redraw = clear

    def write_definition_py(
        self,
        import_statements=None,
        target=None,
        target_lines=None,
        ):
        r'''Writes ``definition.py``.

        Returns none.
        '''
        assert isinstance(import_statements, list), repr(import_statements)
        assert isinstance(target_lines, list), repr(target_lines)
        message = 'will write {} to {}.'
        name = type(target).__name__
        message = message.format(name, self._definition_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.extend(import_statements)
        lines.append('')
        lines.append('')
        lines.extend(target_lines)
        contents = '\n'.join(lines)
        clear = not os.path.isfile(self._definition_py_path)
        self._io_manager.write(self._definition_py_path, contents)
        self._session._pending_redraw = clear

    def write_stub_definition_py(self):
        r'''Writes stub ``definition.py``.

        Returns none.
        '''
        message = 'will write stub to {}.'
        message = message.format(self._definition_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('output_py_import_statements = []')
        lines.append('')
        lines.append('')
        line = '{} = None'.format(self._package_name)
        lines.append(line)
        contents = '\n'.join(lines)
        with open(self._definition_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        message = 'wrote stub to {}.'.format(self._definition_py_path)
        self._io_manager._display(message)

    def write_stub_illustrate_py(self):
        r'''Writes stub ``__illustrate.py__``.

        Returns none.
        '''
        message = 'will write stub to {}.'
        message = message.format(self._illustrate_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        lines = []
        lines.append(self._abjad_import_statement)
        line = 'from output import {}'
        line = line.format(self._package_name)
        lines.append(line)
        lines.append('')
        lines.append('')
        line = 'triple = scoretools.make_piano_score_from_leaves({})'
        line = line.format(self._package_name)
        lines.append(line)
        line = 'score, treble_staff, bass_staff = triple'
        lines.append(line)
        line = 'illustration = lilypondfiletools.'
        line += 'make_basic_lilypond_file(score)'
        lines.append(line)
        contents = '\n'.join(lines)
        with open(self._illustrate_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        message = 'wrote stub to {}.'
        message = message.format(self._illustrate_py_path)
        self._io_manager._display(message)