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
            ...     configuration.abjad_material_packages_directory_path,
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
        '_output_module_import_statements',
        )

    ### INTIALIZER ###

    def __init__(self, path=None, session=None):
        if path is not None:
            assert os.path.sep in path
        PackageManager.__init__(
            self,
            path=path,
            session=session,
            )
        self._output_module_import_statements = [
            self._abjad_import_statement,
            ]

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return self._space_delimited_lowercase_name
        name = self._space_delimited_lowercase_name
        configuration = self._configuration
        annotation = configuration._path_to_storehouse_annotation(self._path)
        string = '{} ({})'
        string = string.format(name, annotation)
        return string

    @property
    def _definition_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            path=self._definition_module_path,
            session=self._session,
            )

    @property
    def _definition_module_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _illustrate_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            path=self._illustrate_module_path,
            session=self._session,
            )

    @property
    def _illustrate_module_path(self):
        return os.path.join(self._path, '__illustrate__.py')

    @property
    def _illustration_ly_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            path=self._illustration_ly_file_path,
            session=self._session,
            )

    @property
    def _illustration_ly_file_path(self):
        return os.path.join(self._path, 'illustration.ly')

    @property
    def _illustration_pdf_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            path=self._illustration_pdf_file_path,
            session=self._session,
            )

    @property
    def _illustration_pdf_file_path(self):
        return os.path.join(self._path, 'illustration.pdf')

    @property
    def _material_package_name(self):
        return os.path.basename(self._path)

    @property
    def _output_module_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            path=self._output_module_path,
            session=self._session,
            )

    @property
    def _output_module_path(self):
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
    def _user_input_to_action(self):
        superclass = super(MaterialPackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'dme': self.edit_definition_module,
            'dmrm': self.remove_definition_module,
            'dms': self.write_definition_module_stub,
            'dmi': self.interpret_definition_module,
            'ime': self.edit_illustrate_module,
            'imei': self.edit_and_interpret_illustrate_module,
            'imrm': self.remove_illustrate_module,
            'ims': self.write_illustrate_module_stub,
            'imi': self.interpret_illustrate_module,
            'lyi': self.interpret_illustration_ly,
            'lyrm': self.remove_illustration_ly,
            'lyo': self.open_illustration_ly,
            'mae': self.autoedit_output_material,
            'mi': self.illustrate_material,
            'omw': self.write_output_material,
            'omrm': self.remove_output_module,
            'omro': self.view_output_module,
            'pca': self.configure_autoeditor,
            'pdfrm': self.remove_illustration_pdf,
            'pdfo': self.open_illustration_pdf,
            'pra': self.remove_autoeditor,
            'ren': self.rename,
            'uit': self.toggle_user_input_values_default_status,
            'ver': self.version_artifacts,
            })
        return result

    @property
    def _versions_directory_path(self):
        return os.path.join(self._path, 'versions')

    ### PRIVATE METHODS ###

    def _can_make_output_material(self):
        if os.path.isfile(self._definition_module_path):
            return True
        return False

    @staticmethod
    def _check_output_material(material):
        return True

    def _execute_output_module(self):
        attribute_names = (self._material_package_name,)
        result = self._output_module_manager._execute(
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
            class_ = iotools.ListEditor
        else:
            class_ = iotools.Editor
        editor = class_(session=self._session, target=target)
        return editor

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
        elif result == 'user entered lone return':
            pass
        else:
            raise ValueError(result)

    def _has_output_material_editor(self):
        if not os.path.isfile(self._definition_module_path):
            return True
        return False

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

    def _make_autoeditor_summary_menu_section(self, menu):
        if not self._get_metadatum('use_autoeditor'):
            if os.path.isfile(self._definition_module_path):
                return
            if not os.path.isfile(self._output_module_path):
                return
        output_material = self._execute_output_module()
        editor = self._get_output_material_editor(target=output_material)
        if not editor:
            return
        lines = editor._get_target_summary_lines()
        lines = lines or ['(empty)']
        return menu.make_material_summary_section(lines=lines)

    def _make_illustrate_module_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustrate_module_path):
            is_hidden = False
            string = 'illustrate module - edit'
            commands.append((string, 'ime'))
            string = 'illustrate module - edit & interpret'
            commands.append((string, 'imei'))
            string = 'illustrate module - interpret'
            commands.append((string, 'imi'))
            string = 'illustrate module - remove'
            commands.append((string, 'imrm'))
            string = 'illustrate module - stub'
            commands.append((string, 'ims'))
        else:
            is_hidden = True
            string = 'illustrate module - stub'
            commands.append((string, 'ims'))
        menu.make_command_section(
            is_hidden=is_hidden,
            commands=commands,
            name='illustrate module',
            )

    def _make_illustration_ly_menu_section(self, menu):
        if not os.path.isfile(self._illustration_ly_file_path):
            return
        commands = []
        commands.append(('illustration ly - interpret', 'lyi'))
        commands.append(('illustration ly - remove', 'lyrm'))
        commands.append(('illustration ly - read only', 'lyo'))
        menu.make_command_section(
            commands=commands,
            name='illustration ly',
            )

    def _make_illustration_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_pdf_file_path):
            commands.append(('illustration pdf - remove', 'pdfrm'))
            commands.append(('illustration pdf - open', 'pdfo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='illustration pdf',
                )

    def _make_main_menu(self, name='material manager'):
        superclass = super(MaterialPackageManager, self)
        menu = superclass._make_main_menu(name=name)
        self._make_autoeditor_summary_menu_section(menu)
        self._make_illustrate_module_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_illustration_pdf_menu_section(menu)
        self._make_material_definition_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_material_menu_section(menu)
        self._make_output_module_menu_section(menu)
        self._make_package_configuration_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        try:
            section = menu['material summary']
            menu.menu_sections.remove(section)
            menu.menu_sections.insert(0, section)
        except KeyError:
            pass
        return menu

    def _make_material_definition_menu_section(self, menu):
        name = 'definition module'
        commands = []
        if os.path.isfile(self._definition_module_path):
            commands.append(('definition module - edit', 'dme'))
            commands.append(('definition module - interpret', 'dmi'))
            commands.append(('definition module - remove', 'dmrm'))
        else:
            commands.append(('definition module - stub', 'dms'))
        if commands:
            use_autoeditor = self._get_metadatum('use_autoeditor')
            menu.make_command_section(
                is_hidden=use_autoeditor,
                commands=commands,
                name='definition module',
                )

    def _make_material_menu_section(self, menu):
        commands = []         
        if os.path.isfile(self._output_module_path):
            commands.append(('material - autoedit', 'mae'))
        if os.path.isfile(self._output_module_path):
            commands.append(('material - illustrate', 'mi'))
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

    def _make_output_module_body_lines(self, output_material):
        if hasattr(output_material, '_storage_format_specification'):
            lines = format(output_material, 'storage').splitlines()
        else:
            lines = [repr(output_material)]
        lines = list(lines)
        lines[0] = '{} = {}'.format(self._material_package_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines

    def _make_output_module_menu_section(self, menu):
        if not os.path.isfile(self._initializer_file_path):
            return
        commands = []
        if os.path.isfile(self._output_module_path):
            commands.append(('output module - remove', 'omrm'))
            commands.append(('output module - read only', 'omro'))
        if self._can_make_output_material():
            commands.append(('output module - write', 'omw'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='output module',
                )

    def _make_package_configuration_menu_section(self, menu):
        commands = []
        use_autoeditor = self._get_metadatum('use_autoeditor')
        if use_autoeditor:
            commands.append(('package - remove autoeditor', 'pra'))
        else:
            commands.append(('package - configure autoeditor', 'pca'))
        commands.append(('package - initializer - open', 'ino'))
        commands.append(('package - version artifacts', 'ver'))
        if commands:
            path = self._definition_module_path
            has_definition_module = os.path.isfile(path)
            menu.make_command_section(
                is_hidden=has_definition_module,
                commands=commands,
                name='package configuration',
                )

    def _make_temporary_illustrate_module_lines(self):
        lines = []
        lines.append(self._unicode_directive)
        lines.append('import os')
        lines.append(self._abjad_import_statement)
        line = 'from output import {}'
        line = line.format(self._material_package_name)
        lines.append(line)
        if os.path.isfile(self._illustrate_module_path):
            lines.append('from illustrate import __illustrate__')
        lines.append('')
        lines.append('')
        if os.path.isfile(self._illustrate_module_path):
            line = 'lilypond_file = __illustrate__({})'
        else:
            line = 'lilypond_file = {}.__illustrate__()'
        line = line.format(self._material_package_name)
        lines.append(line)
        lines.append('file_path = os.path.abspath(__file__)')
        lines.append('directory_path = os.path.dirname(file_path)')
        line = "file_path = os.path.join(directory_path, 'illustration.pdf')"
        lines.append(line)
        lines.append("persist(lilypond_file).as_pdf(file_path)")
        return lines

    def _make_version_artifacts_messages(self):
        #io_manager = systemtools.IOManager
        #next_output_file_name = io_manager.get_next_output_file_name(
        #    output_directory_path=self._versions_directory_path,
        #    )
        #result = os.path.splitext(next_output_file_name)
        #next_output_file_name_root, extension = result
        path = self._versions_directory_path
        greatest_version = self._io_manager.get_greatest_version_number(path)
        new_version = greatest_version + 1
        new_version_string = '%04d' % new_version
        messages = []
        source_paths = (
            self._definition_module_path,
            self._illustration_ly_file_path,
            self._illustration_pdf_file_path,
            self._output_module_path,
            )
        for source_path in source_paths:
            if not source_path:
                continue
            if not os.path.isfile(source_path):
                continue
            message = ' FROM: {}'.format(source_path)
            messages.append(message)
            versions_directory = self._versions_directory_path
            base_name = os.path.basename(source_path)
            file_name, extension = os.path.splitext(base_name)
            name = '{}_{}{}'.format(
                file_name,
                #next_output_file_name_root,
                new_version_string,
                extension,
                )
            target_path = os.path.join(versions_directory, name)
            message = '   TO: {}'.format(target_path)
            messages.append(message)
            messages.append('')
        return messages

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
        if self._session.pending_user_input:
            pending_user_input = 'mae ' + self._session.pending_user_input
            self._session._pending_user_input = pending_user_input
        else:
            self._session._pending_user_input = 'mae'
        self._run()

    def _write_definition_module_stub(self, prompt=True):
        self.write_definition_module_stub()
        message = 'stub material definition written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    ### PUBLIC METHODS ###

    def autoedit_output_material(self):
        r'''Autoedits output material.

        Returns none.
        '''
        output_material = self._execute_output_module()
        if (hasattr(self, '_make_output_material') and
            output_material is None and
            self._make_output_material() and
            isinstance(self._make_output_material(), wizards.Wizard)
            ):
            editor = self._make_output_material(target=output_material)
        else:
            editor = self._get_output_material_editor(target=output_material)
        if not editor:
            return
        editor._run()
        if self._should_backtrack():
            return
        output_module_import_statements = self._output_module_import_statements
        if hasattr(self, '_make_output_module_body_lines'):
            body_lines = self._make_output_module_body_lines(editor.target)
        else:
            line = '{} = {}'
            target_repr = self._get_storage_format(
                editor.target)
            line = line.format(
                self._material_package_name,
                target_repr,
                )
            body_lines = [line]
        self.write_output_material(
            import_statements=output_module_import_statements,
            body_lines=body_lines,
            output_material=editor.target,
            )

    def configure_autoeditor(self, prompt=True):
        r'''Configures autoeditor.

        Returns none.
        '''
        from scoremanager import iotools
        from scoremanager import managers
        selector = iotools.Selector(session=self._session)
        selector = selector.make_inventory_class_selector()
        class_ = selector._run()
        if not class_:
            return
        self._add_metadatum('use_autoeditor', True)
        self._add_metadatum('output_material_class_name', class_.__name__)
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
        self.write_output_material(
            body_lines=body_lines,
            import_statements=import_statements,
            output_material=empty_target,
            prompt=False,
            )
        message = 'package configured for {} autoeditor.'
        message = message.format(class_.__name__)
        self._io_manager.proceed(message, prompt=prompt)

    def edit_and_interpret_illustrate_module(self):
        r'''Edits and then interprets illustrate module module.

        Returns none.
        '''
        self.edit_illustrate_module()
        self.interpret_illustrate_module()

    def edit_definition_module(self):
        r'''Edits material definition module.

        Returns none.
        '''
        file_path = self._definition_module_path
        self._io_manager.edit(file_path)

    def edit_illustrate_module(self):
        r'''Edits illustrate module module.

        Returns none.
        '''
        self._illustrate_module_manager.edit()

    def illustrate_material(self, prompt=True):
        r'''Illustrates material.

        Creates illustration.pdf and illustration.ly files.

        Returns none.
        '''
        from scoremanager import managers
        lines = self._make_temporary_illustrate_module_lines()
        contents = '\n'.join(lines)
        file_name = 'temporary_illustrate.py'
        path = os.path.join(self._path, file_name)
        manager = managers.FileManager(path=path, session=self._session)
        manager._write(contents)
        result = manager.interpret(prompt=False)
        manager._remove()
        if result:
            message = 'created illustration.pdf and illustration.ly files.'
            self._io_manager.proceed(message, prompt=prompt)

    def interpret_definition_module(self):
        r'''Calls Python on material definition module.

        Returns none.
        '''
        self._definition_module_manager.interpret()

    def interpret_illustrate_module(self, prompt=True):
        r'''Calls Python on illustrate module module.

        Returns none.
        '''
        self._illustrate_module_manager.interpret(prompt=prompt)

    def interpret_illustration_ly(self, prompt=True):
        r'''Calls LilyPond on illustration.ly file.

        Returns none.
        '''
        from scoremanager import managers
        path = self._illustration_ly_file_path
        if os.path.isfile(path):
            manager = managers.FileManager(path=path, session=self._session)
            manager.call_lilypond(prompt=prompt)
        else:
            message = 'illustration.ly file does not exist.'
            self._io_manager.proceed(message)

    def remove_autoeditor(self, prompt=True):
        r'''Removes autoeditor.

        Returns none.
        '''
        self._remove_metadatum('use_autoeditor')
        message = 'Removed autoeditor from package.'
        self._io_manager.proceed(message, prompt=prompt)

    def remove_definition_module(self, prompt=True):
        r'''Removes material definition module.

        Returns none.
        '''
        self._definition_module_manager._remove(prompt=prompt)
        self._session._is_backtracking_locally = False

    def remove_illustrate_module(self, prompt=True):
        r'''Removes illustrate module module.

        Returns none.
        '''
        self._illustrate_module_manager._remove(prompt=prompt)
        self._session._is_backtracking_locally = False

    def remove_illustration_ly(self, prompt=True):
        r'''Removes illustration ly.

        Returns none.
        '''
        self._illustration_ly_file_manager._remove(prompt=prompt)
        self._session._is_backtracking_locally = False

    def remove_illustration_pdf(self, prompt=True):
        r'''Removes illustration PDF.

        Returns none.
        '''
        self._illustration_pdf_file_manager._remove(prompt=prompt)
        self._session._is_backtracking_locally = False

    def remove_output_module(self, prompt=True):
        r'''Removes output module.

        Returns none.
        '''
        self._output_module_manager._remove(prompt=prompt)
        self._session._is_backtracking_locally = False

    def rename(
        self,
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        r'''Renames material package.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_snake_case_package_name('enter new package name')
        new_package_name = getter._run()
        if self._should_backtrack():
            return
        base_name = os.path.basename(self._path)
        new_directory_path = self._path.replace(
            base_name,
            new_package_name,
            )
        messages = []
        messages.append('')
        messages.append('will change ...')
        messages.append('')
        messages.append(' FROM: {}'.format(self._path))
        messages.append('   TO: {}'.format(new_directory_path))
        messages.append('')
        self._io_manager.display(messages)
        if not self._io_manager.confirm():
            return
        self._rename(new_directory_path)
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

    def toggle_user_input_values_default_status(self):
        r'''Toggles user input values default status.

        Returns none.
        '''
        self._session.toggle_user_input_values_default_status()

    def open_illustration_ly(self):
        r'''Views illustration LilyPond file.

        Returns none.
        '''
        self._illustration_ly_file_manager.view()

    def open_illustration_pdf(self):
        r'''Views illustration PDF.

        Returns none.
        '''
        self._illustration_pdf_file_manager.view()

    def version_artifacts(self, prompt=True):
        r'''Copies any of ``definition.py``, ``output.py``, 
        ``illustration.ly`` and ``illustration.pdf`` to versions directory,
        if they exist.

        Returns none.
        '''
        if not os.path.isdir(self._versions_directory_path):
            os.mkdir(self._versions_directory_path)
        path = self._versions_directory_path
        greatest_version = self._io_manager.get_greatest_version_number(path)
        new_version = greatest_version + 1
        new_version_string = '%04d' % new_version
        if prompt:
            messages = []
            messages.append('will copy ...')
            messages.append('')
            messages.extend(self._make_version_artifacts_messages())
            self._io_manager.display(messages)
            result = self._io_manager.confirm()
            self._io_manager.display('')
            if self._should_backtrack():
                return
            if not result:
                return
        if os.path.isfile(self._definition_module_path):
            target_file_name = 'definition_{}.py'.format(new_version_string)
            target_file_path = os.path.join(
                self._versions_directory_path,
                target_file_name,
                )
            # TODO: replace with shutil.copyfile()
            command = 'cp {} {}'.format(
                self._definition_module_path,
                target_file_path,
                )
            self._io_manager.spawn_subprocess(command)
        if os.path.isfile(self._output_module_path):
            target_file_name = 'output_{}.py'.format(new_version_string)
            target_file_path = os.path.join(
                self._versions_directory_path,
                target_file_name,
                )
            # TODO: replace with shutil.copyfile()
            command = 'cp {} {}'.format(
                self._output_module_path,
                target_file_path,
                )
            self._io_manager.spawn_subprocess(command)
        if os.path.isfile(self._illustration_ly_file_path):
            target_file_name = 'illustration_{}.ly'.format(new_version_string)
            target_file_path = os.path.join(
                self._versions_directory_path,
                target_file_name,
                )
            # TODO: replace with shutil.copyfile()
            command = 'cp {} {}'.format(
                self._illustration_ly_file_path,
                target_file_path,
                )
            self._io_manager.spawn_subprocess(command)
        if os.path.isfile(self._illustration_pdf_file_path):
            target_file_name = 'illustration_{}.pdf'.format(new_version_string)
            target_file_path = os.path.join(
                self._versions_directory_path,
                target_file_name,
                )
            # TODO: replace with shutil.copyfile()
            command = 'cp {} {}'.format(
                self._illustration_pdf_file_path,
                target_file_path,
                )
            self._io_manager.spawn_subprocess(command)
        self._io_manager.display('')
        self._session._hide_next_redraw = True

    def view_output_module(self):
        r'''Views output module.

        Returns none.
        '''
        self._output_module_manager.view()

    def write_definition_module_stub(self):
        r'''Writes stub material definition module.

        Returns none.
        '''
        lines = []
        lines.append(self._unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('output_module_import_statements = []')
        lines.append('')
        lines.append('')
        line = '{} = None'.format(self._material_package_name)
        lines.append(line)
        contents = '\n'.join(lines)
        with file(self._definition_module_path, 'w') as file_pointer:
            file_pointer.write(contents)

    def write_illustrate_module_stub(self, prompt=True):
        r'''Writes stub illustrate module module.

        Returns none.
        '''
        material_package_name = self._package_name
        lines = []
        lines.append(self._abjad_import_statement)
        line = 'from {}.output import {}'
        line = line.format(material_package_path, material_package_name)
        lines.append(line)
        lines.append('')
        lines.append('')
        line = 'score, treble_staff, bass_staff ='
        line += ' scoretools.make_piano_score_from_leaves({})'
        line = line.format(material_package_name)
        lines.append(line)
        line = 'illustration = lilypondfiletools.'
        line += 'make_basic_lilypond_file(score)'
        lines.append(line)
        contents = '\n'.join(lines)
        file_path = os.path.join(
            self._path,
            '__illustrate__.py',
            )
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(contents)
        message = 'stub illustrate module written to disk.'
        self._io_manager.proceed(message, prompt=prompt)

    def write_output_material(
        self,
        import_statements=None,
        body_lines=None,
        output_material=None,
        prompt=True,
        ):
        r'''Writes output material.

        Returns none.
        '''
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
        lines.append(self._unicode_directive + '\n')
        if body_lines is None:
            triple = self._make_output_material_triple()
            import_statements = triple[0]
            output_module_body_string = triple[1]
            output_material = triple[2]
            body_lines = [output_module_body_string]
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
        self._output_module_manager._write(contents)
        output_material_class_name = type(output_material).__name__
        self._add_metadatum(
            'output_material_class_name', 
            output_material_class_name,
            )
        message = 'output module written to disk.'
        self._io_manager.proceed(message, prompt=prompt)