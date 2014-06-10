# -*- encoding: utf-8 -*-
import collections
import copy
import os
import shutil
import traceback
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools import topleveltools
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
        use_autoeditor = self._get_metadatum('use_autoeditor')
        if self._session.is_in_score:
            name = self._space_delimited_lowercase_name
            if use_autoeditor:
                return '{} (O)'.format(name)
            else:
                return name
        name = self._space_delimited_lowercase_name
        configuration = self._configuration
        annotation = configuration._path_to_storehouse_annotation(self._path)
        string = '{} ({})'
        string = string.format(name, annotation)
        return string

    @property
    def _definition_py_path(self):
        return os.path.join(self._path, 'definition.py')

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
            'oaes': self.set_output_py_autoeditor,
            'oaeu': self.unset_output_py_autoeditor,
            #
            'dae': self.autoopen_definition_py,
            'dc': self.check_definition_py,
            'do': self.open_definition_py,
            'ds': self.write_stub_definition_py,
            #
            'ie': self.edit_illustrate_py,
            'iei': self.edit_and_interpret_illustrate_py,
            'ii': self.interpret_illustrate_py,
            'is': self.write_stub_illustrate_py,
            #
            'ili': self.interpret_illustration_ly,
            'ilo': self.open_illustration_ly,
            #
            'oae': self.autoedit_output_py,
            'oi': self.illustrate_output_py,
            #
            'mae': self.autoedit_maker_py,
            'mc': self.check_maker_py,
            'mi': self.interpret_maker_py,
            'mo': self.open_maker_py,
            'ms': self.write_stub_maker_py,
            #
            'oc': self.check_output_py,
            'oo': self.open_output_py,
            'ow': self.write_output_py,
            #
            'ipo': self.open_illustration_pdf,
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
    def _material_package_name(self):
        return os.path.basename(self._path)

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

    def _execute_output_py(self):
        attribute_names = (self._material_package_name,)
        result = self._io_manager.execute_file(
            path = self._output_py_path,
            attribute_names=attribute_names,
            )
        if result and len(result) == 1:
            output_material = result[0]
            return output_material

    def _get_output_material_editor(self, target):
        if target is None:
            return
        from scoremanager import idetools
        prototype = (datastructuretools.TypedList, list)
        if isinstance(target, prototype):
            class_ = idetools.ListAutoeditor
        else:
            class_ = idetools.Autoeditor
        autoeditor = class_(session=self._session, target=target)
        return autoeditor

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

    def _make_autoeditor_summary_menu_section(self, menu):
        if not self._get_metadatum('use_autoeditor'):
            if os.path.isfile(self._definition_py_path):
                return
            if not os.path.isfile(self._output_py_path):
                return
        output_material = self._execute_output_py()
        autoeditor = self._get_output_material_editor(target=output_material)
        if not autoeditor:
            return
        lines = autoeditor._get_target_summary_lines()
        lines = lines or ['(empty)']
        return menu.make_material_summary_section(lines=lines)

    def _make_definition_py_menu_section(self, menu):
        name = 'definition.py'
        commands = []
        if os.path.isfile(self._definition_py_path):
            is_hidden = False
            commands.append(('definition.py - autoedit', 'dae'))
            commands.append(('definition.py - check', 'dc'))
            commands.append(('definition.py - edit', 'do'))
            commands.append(('definition.py - interpret', 'di'))
        else:
            is_hidden = True
            commands.append(('definition.py - stub', 'ds'))
        if commands:
            menu.make_command_section(
                is_hidden=is_hidden,
                commands=commands,
                name='definition.py',
                )

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

    def _make_illustration_ly_menu_section(self, menu):
        if not os.path.isfile(self._illustration_ly_path):
            return
        commands = []
        commands.append(('illustration.ly - interpret', 'ili'))
        commands.append(('illustration.ly - open', 'ilo'))
        menu.make_command_section(
            commands=commands,
            name='illustration.ly',
            )

    def _make_illustration_pdf_menu_section(self, menu):
        commands = []
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
        self._make_illustration_ly_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_maker_py_menu_section(menu)
        self._make_definition_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_py_menu_section(menu)
        self._make_output_py_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        self._make_versions_directory_menu_section(menu)
        try:
            section = menu['material summary']
            menu.menu_sections.remove(section)
            menu.menu_sections.insert(0, section)
        except KeyError:
            pass
        return menu

    def _make_maker_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._maker_py_path):
            commands.append(('maker.py - autoedit', 'mae'))
            commands.append(('maker.py - check', 'mc'))
            commands.append(('maker.py - interpret', 'mi'))
            commands.append(('maker.py - open', 'mo'))
            is_hidden = False
        else:
            commands.append(('maker.py - stub', 'ms'))
            is_hidden = True
        if commands:
            menu.make_command_section(
                is_hidden=is_hidden,
                commands=commands,
                name='maker.py',
                )

    def _make_output_material(self):
        return

    def _make_output_material_triple(self):
        result = self._retrieve_import_statements_and_output_material()
        import_statements, output_material = result
        body_string = '{} = {}'
        output_material_name = self._material_package_name
        output_material = self._get_storage_format(output_material)
        body_string = body_string.format(
            output_material_name,
            output_material,
            )
        return (import_statements, body_string, output_material)

    def _make_output_py_body_lines(self, output_material):
        if hasattr(output_material, '_storage_format_specification'):
            lines = format(output_material, 'storage').splitlines()
        else:
            lines = [repr(output_material)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self._material_package_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines

    def _make_output_py_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._output_py_path):
            commands.append(('output.py - check', 'oc'))
            commands.append(('output.py - illustrate', 'oi'))
            commands.append(('output.py - open', 'oo'))
        if self._get_metadatum('use_autoeditor'):
            commands.append(('output.py - autoedit', 'oae'))
            commands.append(('output.py - autoeditor - unset', 'oaeu'))
        else:
            commands.append(('output.py - autoeditor - set', 'oaes'))
        commands.append(('output.py - write', 'ow'))
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
        line = line.format(self._material_package_name)
        lines.append(line)
        if os.path.isfile(self._illustrate_py_path):
            lines.append('from illustrate import __illustrate__')
        lines.append('')
        lines.append('')
        if os.path.isfile(self._illustrate_py_path):
            line = 'lilypond_file = __illustrate__({})'
        else:
            line = 'lilypond_file = {}.__illustrate__()'
        line = line.format(self._material_package_name)
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
            self._material_package_name,
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

    def autoopen_definition_py(self):
        r'''Autoedits ``definition.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def autoedit_maker_py(self):
        r'''Autoedits ``maker.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def autoedit_output_py(self):
        r'''Autoedits ``output.py``.

        Returns none.
        '''
        output_material = self._execute_output_py()
        autoeditor = self._get_output_material_editor(target=output_material)
        if not autoeditor:
            return
        autoeditor._run()
        if self._session.is_backtracking:
            return
        output_py_import_statements = self._output_py_import_statements
        if hasattr(self, '_make_output_py_body_lines'):
            body_lines = self._make_output_py_body_lines(autoeditor.target)
        else:
            line = '{} = {}'
            target_repr = self._get_storage_format(
                autoeditor.target)
            line = line.format(
                self._material_package_name,
                target_repr,
                )
            body_lines = [line]
        self.write_output_py(
            import_statements=output_py_import_statements,
            body_lines=body_lines,
            output_material=autoeditor.target,
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

    def check_maker_py(self, dry_run=False):
        r'''Checks ``maker.py``.

        Display errors generated during interpretation.
        '''
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._maker_py_path)
            return inputs, outputs
        stderr_lines = self._io_manager.check_file(self._maker_py_path)
        if stderr_lines:
            messages = [self._maker_py_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(self._maker_py_path)
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

    def open_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

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

    def interpret_maker_py(self):
        r'''Interprets ``maker.py``.

        Writes ``output.py``.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

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

    def open_maker_py(self):
        r'''Opens ``maker.py``.

        Returns none.
        '''
        self._io_manager.open_file(self._maker_py_path)
    
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

    def set_output_py_autoeditor(self):
        r'''Sets autoeditor.

        Returns none.
        '''
        from scoremanager import idetools
        selector = self._io_manager.selector
        selector = selector.make_inventory_class_selector()
        class_ = selector._run()
        if not class_:
            return
        self._add_metadatum('use_autoeditor', True)
        self._add_metadatum('output_material_class_name', class_.__name__)
        output_material = self._execute_output_py()
        if type(output_material) is class_:
            return
        if output_material is not None:
            messages = []
            message = 'existing output.py file contains {}.'
            message = message.format(type(output_material).__name__)
            messages.append(message)
            message = 'overwrite existing output.py file?'
            messages.append(message)
            self._io_manager._display(messages)
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
        empty_target = class_()
        if type(empty_target) is list:
            storage_format = repr(empty_target)
        else:
            storage_format = format(empty_target, 'storage')
        body_lines = '{} = {}'.format(
            self._package_name,
            storage_format,
            )
        body_lines = body_lines.split('\n')
        body_lines = [_ + '\n' for _ in body_lines]
        import_statements = [self._abjad_import_statement]
        if 'handlertools.' in storage_format:
            statement = 'from experimental.tools import handlertools'
            import_statements.append(statement)
        with self._io_manager._make_silent():
            self.write_output_py(
                body_lines=body_lines,
                import_statements=import_statements,
                output_material=empty_target,
                )

    def unset_output_py_autoeditor(self):
        r'''Unsets autoeditor.

        Returns none.
        '''
        self._remove_metadatum('use_autoeditor')

    def write_output_py(
        self,
        import_statements=None,
        body_lines=None,
        output_material=None,
        ):
        r'''Writes ``output.py``.

        Returns none.
        '''
        message = 'will write output material to {}.'
        message = message.format(self._output_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        if import_statements is None:
            assert body_lines is None
        else:
            assert isinstance(import_statements, list), repr(import_statements)
        if body_lines is None:
            assert import_statements is None
            assert output_material is None
        else:
            assert isinstance(body_lines, list), repr(body_lines)
            assert output_material is not None
        lines = []
        lines.append(self._configuration.unicode_directive + '\n')
        if body_lines is None:
            triple = self._make_output_material_triple()
            import_statements = triple[0]
            output_py_body_string = triple[1]
            output_material = triple[2]
            body_lines = [output_py_body_string]
        import_statements = import_statements or []
        if any('handlertools' in _ for _ in body_lines):
            statement = 'from experimental.tools import handlertools'
            import_statements.append(statement)
        import_statements = [x + '\n' for x in import_statements]
        lines.extend(import_statements)
        lines.extend(['\n', '\n'])
        lines.extend(body_lines)
        contents = ''.join(lines)
        self._io_manager.write(self._output_py_path, contents)
        output_material_class_name = type(output_material).__name__
        self._add_metadatum(
            'output_material_class_name', 
            output_material_class_name,
            )

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
        line = '{} = None'.format(self._material_package_name)
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

    def write_stub_maker_py(self):
        r'''Writes stub ``maker.py``.

        Returns none.
        '''
        message = 'will write stub to {}.'
        message = message.format(self._maker_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('')
        lines.append('')
        lines.append('maker = None')
        contents = '\n'.join(lines)
        with open(self._maker_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        self._session._is_pending_output_removal = True