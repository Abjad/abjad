# -*- encoding: utf-8 -*-
import itertools
import os
from abjad.tools import systemtools
from scoremanager.managers.PackageManager import PackageManager


class SegmentPackageManager(PackageManager):
    r'''Segment package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        path=None,
        session=None,
        ):
        PackageManager.__init__(
            self,
            path=path,
            session=session,
            )

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
    def _definition_module_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _input_to_action(self):
        superclass = super(SegmentPackageManager, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'dme': self.edit_definition_module,
            'dmws': self.write_stub_definition_module,
            'lyi': self.interpret_lilypond_file,
            'lyo': self.open_output_ly,
            'mmi': self.interpret_make_module,
            'mmo': self.open_make_module,
            'mmws': self.write_stub_make_module,
            'pdfo': self.open_output_pdf,
            'uar': self.remove_unadded_assets,
            'vdmo': self.open_versioned_definition_module,
            'vdls': self.list_versions_directory,
            'ver': self.version_artifacts,
            'vlyo': self.open_versioned_output_ly,
            'vpdfo': self.open_versioned_output_pdf,
            'vpdfso': self.open_versioned_pdfs,
            })
        return result

    @property
    def _make_module_path(self):
        return os.path.join(self._path, '__make__.py')

    @property
    def _output_lilypond_file_path(self):
        return os.path.join(self._path, 'output.ly')

    @property
    def _output_pdf_file_path(self):
        return os.path.join(self._path, 'output.pdf')

    @property
    def _versions_directory_path(self):
        return os.path.join(self._path, 'versions')

    ### PRIVATE METHODS ###

    def _get_last_version_number(self):
        versions_directory_path = self._versions_directory_path
        if not os.path.exists(versions_directory_path):
            return
        file_names = sorted(os.listdir(versions_directory_path))
        if not file_names:
            return
        file_names.sort()
        last_file_name = file_names[-1]
        assert last_file_name[0].isdigit()
        version_string = last_file_name[:4]
        version_number = int(version_string)
        return version_number

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass

    def _make_current_lilypond_file_menu_section(self, menu):
        if os.path.isfile(self._output_lilypond_file_path):
            commands = []
            commands.append(('lilypond file - interpret', 'lyi'))
            commands.append(('lilypond file - open', 'lyo'))
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='lilypond file',
                )

    def _make_current_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._output_pdf_file_path):
            commands.append(('artifacts - version', 'ver'))
        if os.path.isfile(self._output_pdf_file_path):
            commands.append(('pdf - open', 'pdfo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                name='pdf',
                )

    def _make_definition_module_menu_section(self, menu):
        if not os.path.isfile(self._definition_module_path):
            message = 'No definition.py module found;'
            message += ' use (dmws) to write stub.'
            menu.make_informational_section(
                menu_entries=[message],
                )
        commands = []
        commands.append(('definition module - edit', 'dme'))
        commands.append(('definition module - write stub', 'dmws'))
        menu.make_command_section(
            commands=commands,
            name='definition module',
            )

    def _make_main_menu(self, name='segment package manager'):
        superclass = super(SegmentPackageManager, self)
        menu = superclass._make_main_menu(name=name)
        self._make_current_lilypond_file_menu_section(menu)
        self._make_current_pdf_menu_section(menu)
        self._make_definition_module_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_make_module_menu_section(menu)
        self._make_package_configuration_menu_section(menu)
        self._make_versions_directory_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    def _make_make_module_menu_section(self, menu):
        commands = []
        commands.append(('make module - interpret', 'mmi'))
        commands.append(('make module - open', 'mmo'))
        commands.append(('make module - write stub', 'mmws'))
        menu.make_command_section(
            commands=commands,
            name='make module',
            )

    def _make_package_configuration_menu_section(self, menu):
        commands = []
        commands.append(('package - initializer - open', 'ino'))
        commands.append(('package - initializer - write stub', 'inws'))
        commands.append(('package - unadded assets - remove', 'uar'))
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='package configuation',
                )

    def _make_version_artifacts_messages(self):
        paths = {}
        io_manager = systemtools.IOManager
        next_output_file_name = io_manager.get_next_output_file_name(
            output_directory_path=self._versions_directory_path,
            )
        result = os.path.splitext(next_output_file_name)
        next_output_file_name_root, extension = result
        messages = []
        source_paths = (
            self._definition_module_path,
            self._output_lilypond_file_path,
            self._output_pdf_file_path,
            )
        for source_path in source_paths:
            _, extension = os.path.splitext(source_path)
            message = ' FROM: {}'.format(source_path)
            messages.append(message)
            directory = self._versions_directory_path
            file_name = next_output_file_name_root + extension
            target_path = os.path.join(directory, file_name)
            message = '   TO: {}'.format(target_path)
            messages.append(message)
            messages.append('')
        return messages

    def _make_versions_directory_menu_section(self, menu):
        commands = []
        commands.append(('versions - definition.py - open', 'vdmo'))
        commands.append(('versions - output.ly - open', 'vlyo'))
        commands.append(('versions - output.pdf - open', 'vpdfo'))
        commands.append(('versions - all output.pdf - open', 'vpdfso'))
        commands.append(('versions directory - list', 'vdls'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='versions directory',
            )

    def _view_versioned_file(self, extension):
        assert extension in ('.ly', '.pdf', '.py')
        getter = self._io_manager.make_getter()
        last_version_number = self._get_last_version_number()
        if last_version_number is None:
            message = 'versions directory empty.'
            self._io_manager.proceed(message)
            return
        prompt = 'version number (0-{})'
        prompt = prompt.format(last_version_number)
        getter.append_integer(prompt)
        version_number = getter._run()
        if self._should_backtrack():
            return
        if last_version_number < version_number or \
            (version_number < 0 and last_version_number < abs(version_number)):
            message = "version {} doesn't exist yet."
            message = message.format(version_number)
            self._io_manager.proceed(['', message])
        if version_number < 0:
            version_number = last_version_number + version_number + 1
        version_string = str(version_number).zfill(4)
        file_name = '{}{}'.format(version_string, extension)
        file_path = os.path.join(
            self._path,
            'versions',
            file_name,
            )
        if os.path.isfile(file_path):
            self._io_manager.open_file(file_path)

    ### PUBLIC METHODS ###

    def edit_definition_module(self):
        r'''Edits asset definition module.

        Returns none.
        '''
        self._io_manager.edit(self._definition_module_path)

    def interpret_lilypond_file(self, confirm=True, notify=True):
        r'''Reinterprets current LilyPond file.

        Returns none.
        '''
        if notify:
            messages = []
            messages.append('will interpret ...')
            messages.append('')
            message = ' INPUT: {}'.format(self._output_lilypond_file_path)
            messages.append(message)
            message = 'OUTPUT: {}'.format(self._output_pdf_file_path)
            messages.append(message)
            messages.append('')
            self._io_manager.display(messages)
        if confirm:
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
            self._io_manager.display('')
        file_path = self._output_lilypond_file_path
        if not os.path.isfile(file_path):
            return
        result = self._io_manager.run_lilypond(file_path)
        if not result:
            return
        lilypond_file_path = self._output_lilypond_file_path
        if notify:
            messages = []
            message = 'interpreted {!r}.'
            message = message.format(lilypond_file_path)
            messages.append(message)
            message = 'wrote {!r}.'.format(self._output_pdf_file_path)
            messages.append(message)
            message = 'use (pdfo) to open {}.'
            message = message.format(self._output_pdf_file_path)
            messages.append(message)
            messages.append('')
            self._io_manager.display(messages)
            self._session._hide_next_redraw = True

    def interpret_make_module(self, confirm=True, notify=True):
        r'''Interprets ``__make__.py`` module.

        Creates ``output.ly`` and ``output.pdf`` files.

        Returns none.
        '''
        if not os.path.isfile(self._make_module_path):
            message = 'no __make__.py module found.'
            self._io_manager.proceed(message)
            return
        if notify:
            messages = []
            messages.append('will interpret ...')
            messages.append('')
            message = ' INPUT: {}'.format(self._make_module_path)
            messages.append(message)
            message = 'OUTPUT: {}'.format(self._output_lilypond_file_path)
            messages.append(message)
            message = 'OUTPUT: {}'.format(self._output_pdf_file_path)
            messages.append(message)
            messages.append('')
            self._io_manager.display(messages)
        if confirm:
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
            self._io_manager.display('')
        self._io_manager.interpret(self._make_module_path, prompt=False)
        if notify:
            messages = []
            message = 'Interpreted {!r}.'.format(self._make_module_path)
            messages.append(message)
            message = 'Wrote {!r}.'.format(self._output_lilypond_file_path)
            messages.append(message)
            message = 'Wrote {!r}.'.format(self._output_pdf_file_path)
            messages.append(message)
            messages.append('')
            self._io_manager.display(messages)
            self._session._hide_next_redraw = True

    def list_versions_directory(self):
        r'''Lists versions directory.

        Returns none.
        '''
        versions_directory_path = self._versions_directory_path
        if not os.path.exists(versions_directory_path):
            line = 'no versions found.'
            self._io_manager.display([line, ''])
            self._io_manager.proceed()
            return
        file_names = []
        for directory_entry in os.listdir(versions_directory_path):
            if directory_entry[0].isdigit():
                file_names.append(directory_entry)
        lines = []
        for x in itertools.groupby(file_names, key=lambda x: x[:4]):
            key, file_names = x
            line = ' '.join(file_names)
            lines.append(line)
        if lines:
            lines.append('')
        self._io_manager.display(lines)
        self._session._hide_next_redraw = True

    def open_make_module(self):
        r'''Opens ``__make__.py`` module.

        Returns none.
        '''
        self._io_manager.open_file(self._make_module_path)

    def open_output_ly(self):
        r'''Opens current output LilyPond file.

        Returns none.
        '''
        file_path = self._output_lilypond_file_path
        if os.path.isfile(file_path):
            self._io_manager.open_file(file_path)

    def open_output_pdf(self):
        r'''Opens output PDF.

        Returns none.
        '''
        file_path = self._output_pdf_file_path
        if os.path.isfile(file_path):
            self._io_manager.open_file(file_path)

    def open_versioned_definition_module(self):
        r'''Opens versioned definition module.

        Returns none.
        '''
        self._view_versioned_file('.py')

    def open_versioned_output_ly(self):
        r'''Opens output LilyPond file.

        Returns none.
        '''
        self._view_versioned_file('.ly')

    def open_versioned_output_pdf(self):
        r'''Opens output PDF.

        Returns none.
        '''
        self._view_versioned_file('.pdf')

    def open_versioned_pdfs(self):
        r'''Opens versioend PDFs.

        Returns none.
        '''
        versions_directory_path = self._versions_directory_path
        file_paths = []
        for directory_entry in os.listdir(versions_directory_path):
            if not directory_entry[0].isdigit():
                continue
            if not directory_entry.endswith('.pdf'):
                continue
            file_path = os.path.join(
                versions_directory_path,
                directory_entry,
                )
            file_paths.append(file_path)
        if not file_paths:
            message = 'version directory empty.'
            self._io_manager.proceed(message)
            return
        self._io_manager.open_file(file_paths)

    def version_artifacts(self, confirm=True, notify=True):
        r'''Saves definition.py, output.ly and output.pdf to versions
        directory.

        Returns version number or none.
        '''
        paths = {}
        if not os.path.isfile(self._definition_module_path):
            if notify:
                message = 'can not find {}.'
                message = message.format(self._definition_module_path)
                self._io_manager.display(message)
            return
        output_pdf_file_path = self._output_pdf_file_path
        if not os.path.isfile(self._output_pdf_file_path):
            if notify:
                message = 'can not find {}.'
                message = message.format(self._output_pdf_file_path)
                self._io_manager.display(message)
                return
        output_lilypond_file_path = self._output_lilypond_file_path
        if not os.path.isfile(output_lilypond_file_path):
            message = 'can not find output.ly file.'
            self._io_manager.proceed(
                message,
                prompt=prompt,
                )
            return
        if not os.path.isdir(self._versions_directory_path):
            os.mkdir(self._versions_directory_path)
        io_manager = systemtools.IOManager
        next_output_file_name = io_manager.get_next_output_file_name(
            output_directory_path=self._versions_directory_path,
            )
        result = os.path.splitext(next_output_file_name)
        next_output_file_name_root, extension = result
        if confirm:
            messages = []
            messages.append('will copy ...')
            messages.append('')
            messages.extend(self._make_version_artifacts_messages())
            self._io_manager.display(messages)
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
            self._io_manager.display('')
        result = os.path.splitext(next_output_file_name)
        next_output_file_name_root, extension = result
        target_file_name = next_output_file_name_root + '.py'
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
        target_file_name = next_output_file_name_root + '.pdf'
        target_file_path = os.path.join(
            self._versions_directory_path,
            target_file_name,
            )
        # TODO: replace with shutil.copyfile()
        command = 'cp {} {}'.format(
            output_pdf_file_path,
            target_file_path,
            )
        self._io_manager.spawn_subprocess(command)
        target_file_name = next_output_file_name_root + '.ly'
        target_file_path = os.path.join(
            self._versions_directory_path,
            target_file_name,
            )
        # TODO: replace with shutil.copyfile()
        command = 'cp {} {}'.format(
            output_lilypond_file_path,
            target_file_path,
            )
        self._io_manager.spawn_subprocess(command)
        version_number = int(next_output_file_name_root)
        message = 'copied definition.py, output.ly and output.pdf'
        message += ' to versions directory.'
        message = message.format(version_number)
        self._io_manager.display([message, ''])
        self._session._hide_next_redraw = True
        return version_number

    # TODO: reimplement as boilerplate
    def write_stub_definition_module(self, confirm=True, notify=True):
        r'''Writes stub definition module.

        Returns none.
        '''
        if notify:
            messages = []
            message = 'will write stub to {}.'
            message = message.format(self._definition_module_path)
            messages.append(message)
            self._io_manager.display(message)
        if confirm:
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
        lines = []
        lines.append(self._unicode_directive)
        lines.append(self._abjad_import_statement)
        lines.append('')
        lines.append('')
        contents = '\n'.join(lines)
        with file(self._definition_module_path, 'w') as file_pointer:
            file_pointer.write(contents)
        if notify:
            message = 'wrote stub to {}.'
            message = message.format(self._definition_module_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True

    # TODO: reimplement as boilerplate
    def write_stub_make_module(self, confirm=True, notify=True):
        r'''Writes stub __make__.py module.

        Returns none.
        '''
        if notify:
            messages = []
            message = 'will write stub to {}.'.format(self._make_module_path)
            self._io_manager.display(message)
        if confirm:
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
        lines = []
        lines.append(self._unicode_directive)
        lines.append('import os')
        lines.append(self._abjad_import_statement)
        lines.append('from definition import segment_maker')
        lines.append('')
        lines.append('')
        lines.append('lilypond_file = segment_maker()')
        lines.append('current_directory = os.path.dirname(__file__)')
        line = "ly_file_path = os.path.join(current_directory, 'output.ly')"
        lines.append(line)
        lines.append('persist(lilypond_file).as_ly(ly_file_path)')
        line = "pdf_file_path = os.path.join(current_directory, 'output.pdf')"
        lines.append(line)
        lines.append('persist(lilypond_file).as_pdf(pdf_file_path)')
        contents = '\n'.join(lines)
        with file(self._make_module_path, 'w') as file_pointer:
            file_pointer.write(contents)
        if notify:
            messages = []
            message = 'wrote stub to {}.'.format(self._make_module_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True