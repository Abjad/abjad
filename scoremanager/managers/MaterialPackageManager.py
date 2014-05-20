# -*- encoding: utf-8 -*-
import copy
import os
import shutil
import traceback
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools import topleveltools
from scoremanager import wizards
from scoremanager.managers.PackageManager import PackageManager


class MaterialPackageManager(PackageManager):
    r'''Material package manager.


    ..  container:: example

        ::

            >>> import os
            >>> configuration = scoremanager.core.ScoreManagerConfiguration()
            >>> session = scoremanager.core.Session()
            >>> path = os.path.join(
            ...     configuration.abjad_material_packages_directory,
            ...     'example_numbers',
            ...     )
            >>> manager = scoremanager.managers.MaterialPackageManager(
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
        if path is not None:
            assert os.path.sep in path
        superclass = super(MaterialPackageManager, self)
        superclass.__init__(path=path, session=session)
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
                return '{} (AE)'.format(name)
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
    def _illustration_ly_file_path(self):
        return os.path.join(self._path, 'illustration.ly')

    @property
    def _illustration_pdf_file_path(self):
        return os.path.join(self._path, 'illustration.pdf')

    @property
    def _input_to_method(self):
        superclass = super(MaterialPackageManager, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'aes': self.set_autoeditor,
            'aeu': self.unset_autoeditor,
            #
            'de': self.edit_definition_py,
            'di': self.interpret_definition_py,
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
            'ae': self.autoedit,
            'i': self.illustrate_material,
            #
            'oo': self.open_output_py,
            'ow': self.write_output_py,
            #
            'ipo': self.open_illustration_pdf,
            #
            'vdo': self.open_versioned_definition_py,
            'vilo': self.open_versioned_illustration_ly,
            'vipo': self.open_versioned_illustration_pdf,
            'voo': self.open_versioned_output_py,
            #
            'vr': self.version_package,
            'vrls': self.list_versions_directory,
            })
        return result

    @property
    def _material_package_name(self):
        return os.path.basename(self._path)

    @property
    def _output_py_path(self):
        return os.path.join(self._path, 'output.py')

    @property
    def _score_package_manager(self):
        from scoremanager import managers
        score_path = self._configuration._path_to_score_path(self._path)
        return managers.ScorePackageManager(
            path=score_path,
            session=self._session,
            )

    @property
    def _source_paths(self):
        return (
            self._definition_py_path,
            self._output_py_path,
            self._illustration_ly_file_path,
            self._illustration_pdf_file_path,
            )

    @property
    def _versions_directory(self):
        return os.path.join(self._path, 'versions')

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
        from scoremanager import iotools
        prototype = (datastructuretools.TypedList, list)
        if isinstance(target, prototype):
            class_ = iotools.ListAutoeditor
        else:
            class_ = iotools.Autoeditor
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

    def _interpret_definition_py(self):
        if not os.path.isfile(self._definition_py_path):
            return
        result = self._io_manager.execute_file(
            path=self._definition_py_path,
            attribute_names=(self._material_package_name,),
            )
        if result:
            assert len(result) == 1
            result = result[0]
            return result

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
            string = '__illustrate__.py - write stub'
            commands.append((string, 'is'))
        else:
            is_hidden = True
            string = '__illustrate__.py - write stub'
            commands.append((string, 'is'))
        menu.make_command_section(
            is_hidden=is_hidden,
            commands=commands,
            name='__illustrate__.py',
            )

    def _make_illustration_ly_menu_section(self, menu):
        if not os.path.isfile(self._illustration_ly_file_path):
            return
        commands = []
        commands.append(('illustration ly - interpret', 'ili'))
        commands.append(('illustration ly - open', 'ilo'))
        menu.make_command_section(
            commands=commands,
            name='illustration ly',
            )

    def _make_illustration_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_pdf_file_path):
            commands.append(('illustration pdf - open', 'ipo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='illustration pdf',
                )

    def _make_main_menu(self):
        superclass = super(MaterialPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_autoeditor_summary_menu_section(menu)
        self._make_illustrate_py_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_material_definition_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_py_menu_section(menu)
        self._make_material_menu_section(menu)
        self._make_output_py_menu_section(menu)
        self._make_package_configuration_menu_section(menu)
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

    def _make_material_definition_menu_section(self, menu):
        name = 'definition.py'
        commands = []
        commands.append(('definition.py - edit', 'de'))
        commands.append(('definition.py - interpret', 'di'))
        commands.append(('definition.py - write stub', 'ds'))
        if commands:
            use_autoeditor = self._get_metadatum('use_autoeditor')
            menu.make_command_section(
                is_hidden=use_autoeditor,
                commands=commands,
                name='definition.py',
                )

    def _make_material_menu_section(self, menu):
        commands = []         
        if os.path.isfile(self._output_py_path):
            if self._get_metadatum('use_autoeditor'):
                commands.append(('material - autoedit', 'ae'))
            commands.append(('material - illustrate', 'i'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='material',
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
        if not os.path.isfile(self._init_py_file_path):
            return
        commands = []
        commands.append(('output.py - write', 'ow'))
        if os.path.isfile(self._output_py_path):
            commands.append(('output.py - open', 'oo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='output.py',
                )

    def _make_package_configuration_menu_section(self, menu):
        commands = []
        use_autoeditor = self._get_metadatum('use_autoeditor')
        if use_autoeditor:
            commands.append(('package - autoeditor - unset', 'aeu'))
        else:
            commands.append(('package - autoeditor - set', 'aes'))
        if commands:
            path = self._definition_py_path
            has_definition_py = os.path.isfile(path)
            menu.make_command_section(
                is_hidden=has_definition_py,
                commands=commands,
                name='package configuration',
                )

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
        lines.append('file_path = os.path.abspath(__file__)')
        lines.append('directory = os.path.dirname(file_path)')
        line = "file_path = os.path.join(directory, 'illustration.pdf')"
        lines.append(line)
        lines.append("persist(lilypond_file).as_pdf(file_path)")
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
            messages.append('')
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
        messages.append('')
        messages.append('will change ...')
        messages.append('')
        messages.append(' FROM: {}'.format(self._path))
        messages.append('   TO: {}'.format(new_directory))
        messages.append('')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        self._rename(new_directory)
        for directory_entry in os.listdir(new_directory):
            if directory_entry.endswith('.py'):
                file_path = os.path.join(new_directory, directory_entry)
                result = os.path.splitext(base_name)
                old_package_name, extension = result
                self._replace_in_file(
                    file_path,
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
            pending_input = 'ae ' + self._session.pending_input
            self._session._pending_input = pending_input
        else:
            self._session._pending_input = 'ae'
        self._run()

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_materials = True

    ### PUBLIC METHODS ###

    def autoedit(self):
        r'''Autoedits.

        Returns none.
        '''
        output_material = self._execute_output_py()
        if (hasattr(self, '_make_output_material') and
            output_material is None and
            self._make_output_material() and
            isinstance(self._make_output_material(), wizards.Wizard)
            ):
            autoeditor = self._make_output_material(target=output_material)
        else:
            autoeditor = self._get_output_material_editor(
                target=output_material)
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

    def edit_and_interpret_illustrate_py(self):
        r'''Edits and then interprets ``__illustrate.py__``.

        Returns none.
        '''
        self.edit_illustrate_py()
        self.interpret_illustrate_py()

    def edit_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def edit_illustrate_py(self):
        r'''Edits ``__illustrate.py__``.

        Returns none.
        '''
        self._io_manager.edit(self._illustrate_py_path)

    def illustrate_material(self, confirm=True, display=True):
        r'''Illustrates material.

        Creates ``illustration.pdf`` and ``illustration.ly`` files.

        Returns none.
        '''
        with self._io_manager._make_interaction(display=display):
            lines = self._make_temporary_illustrate_py_lines()
            contents = '\n'.join(lines)
            file_name = 'temporary_illustrate.py'
            path = os.path.join(self._path, file_name)
            self._io_manager.write(path, contents)
            self._io_manager.interpret_file(
                path, 
                confirm=confirm, 
                display=display,
                )

    def interpret_definition_py(self):
        r'''Interprets ``definition.py``.

        Returns none.
        '''
        result = self._io_manager.interpret_file(self._definition_py_path)
        message = 'no exceptions raised; use (oo) to write output py.'
        self._io_manager._display([message, ''])
        self._session._hide_next_redraw = True

    def interpret_illustrate_py(self, confirm=True, display=True):
        r'''Interprets ``__illustrate.py__``.

        Returns none.
        '''
        result = self._io_manager.interpret_file(
            self._illustrate_py_path,
            confirm=confirm,
            display=display,
            )
        if result == 0:
            self._io_manager._display('')
        self._session._hide_next_redraw = True

    def interpret_illustration_ly(self, confirm=True, display=True):
        r'''Interprets ``illustration.ly``.

        Returns none.
        '''
        from scoremanager import managers
        path = self._illustration_ly_file_path
        if os.path.isfile(path):
            self._io_manager.run_lilypond(
                path, 
                confirm=confirm, 
                display=display,
                )
        else:
            message = 'illustration.ly file does not exist.'
            self._io_manager._display([message, ''])
        self._session._hide_next_redraw = True

    def list_versions_directory(self):
        r'''Lists ``versions/`` directory.

        Returns none.
        '''
        self._list_versions_directory()

    def open_illustration_ly(self):
        r'''Opens ``illustration.ly``.

        Returns none.
        '''
        self._io_manager.open_file(self._illustration_ly_file_path)

    def open_illustration_pdf(self):
        r'''Opens `illustration.pdf``.

        Returns none.
        '''
        self._io_manager.open_file(self._illustration_pdf_file_path)

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

    def set_autoeditor(self, confirm=True, display=True):
        r'''Sets autoeditor.

        Returns none.
        '''
        from scoremanager import iotools
        # not wrapped in interaction because redraw is important afterwards
        #with self._io_manager._make_interaction(display=display):
        if True:
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
            if confirm:
                if output_material is not None:
                    self._session._hide_next_redraw = False
                    messages = []
                    message = 'existing output.py file contains {}.'
                    message = message.format(type(output_material).__name__)
                    messages.append(message)
                    message = 'overwrite existing output.py file?'
                    messages.append(message)
                    self._io_manager._display(messages)
                    result = self._io_manager._confirm()
                    if self._session.is_backtracking:
                        return
                    if not result:
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
            if ' makers.' in storage_format:
                statement = 'from scoremanager import makers'
                import_statements.append(statement)
            self.write_output_py(
                body_lines=body_lines,
                import_statements=import_statements,
                output_material=empty_target,
                confirm=False,
                display=False,
                )
            self._session._hide_next_redraw = False

    def unset_autoeditor(self, confirm=True, display=True):
        r'''Unsets autoeditor.

        Returns none.
        '''
        #with self._io_manager._make_interaction(display=display):
        # no interaction because redraw is important
        if True:
            self._remove_metadatum('use_autoeditor')
            self._session._hide_next_redraw = False

    def version_package(self, confirm=True, display=True):
        r'''Versions package.
        
        Copies any of ``definition.py``, ``output.py``, 
        ``illustration.ly`` and ``illustration.pdf`` to versions directory,
        if they exist.

        Returns none.
        '''
        self._version_package(confirm=confirm, display=display)

    def write_output_py(
        self,
        import_statements=None,
        body_lines=None,
        output_material=None,
        confirm=True,
        display=True,
        ):
        r'''Writes ``output.py``.

        Returns none.
        '''
        if confirm:
            message = 'will write output material to {}.'
            message = message.format(self._output_py_path)
            self._io_manager._display(message)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            if not result:
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
        if any(' makers.' in _ for _ in body_lines):
            statement = 'from scoremanager import makers'
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

    def write_stub_definition_py(self, confirm=True, display=True):
        r'''Writes stub ``definition.py``.

        Returns none.
        '''
        if confirm:
            message = 'will write stub to {}.'
            message = message.format(self._definition_py_path)
            self._io_manager._display(message)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            if not result:
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
        with file(self._definition_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        if display:
            message = 'wrote stub to {}.'.format(self._definition_py_path)
            self._io_manager._display([message, ''])
            self._session._hide_next_redraw = True

    def write_stub_illustrate_py(self, confirm=True, display=True):
        r'''Writes stub ``__illustrate.py__``.

        Returns none.
        '''
        if confirm:
            message = 'will write stub to {}.'
            message = message.format(self._illustrate_py_path)
            self._io_manager._display(message)
            result = self._io_manager._confirm()
            if self._session.is_backtracking:
                return
            if not result:
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
        with file(self._illustrate_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        if display:
            message = 'wrote stub to {}.'
            message = message.format(self._illustrate_py_path)
            self._io_manager._display([message, ''])
            self._session._hide_next_redraw = True