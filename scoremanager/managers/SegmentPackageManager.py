# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import systemtools
from scoremanager.managers.PackageManager import PackageManager


class SegmentPackageManager(PackageManager):
    r'''Segment package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(SegmentPackageManager, self)
        superclass.__init__(path=path, session=session)

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
    def _definition_py_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _input_to_action(self):
        superclass = super(SegmentPackageManager, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'dme': self.edit_definition_py,
            'dmws': self.write_stub_definition_py,
            'lyi': self.interpret_lilypond_file,
            'lyo': self.open_output_ly,
            'mmi': self.interpret_make_module,
            'mmo': self.open_make_module,
            'mmws': self.write_stub_make_module,
            'pdfo': self.open_output_pdf,
            'uar': self.remove_unadded_assets,
            'vdmo': self.open_versioned_definition_py,
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
    def _source_paths(self):
        return (
            self._definition_py_path,
            self._output_lilypond_file_path,
            self._output_pdf_file_path,
            )

    @property
    def _versions_directory_path(self):
        return os.path.join(self._path, 'versions')

    ### PRIVATE METHODS ###

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

    def _make_definition_py_menu_section(self, menu):
        if not os.path.isfile(self._definition_py_path):
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
        self._make_definition_py_menu_section(menu)
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
        last_version_number = self._get_last_version_number()
        next_version_number = last_version_number + 1
        next_version_string = '%04d' % next_version_number
        messages = []
        for source_path in self._source_paths:
            root, extension = os.path.splitext(source_path)
            message = ' FROM: {}'.format(source_path)
            messages.append(message)
            directory = self._versions_directory_path
            file_name = '{}_{}{}'.format(root, next_version_string, extension)
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

    ### PUBLIC METHODS ###

    def edit_definition_py(self):
        r'''Edits asset definition module.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def interpret_lilypond_file(self, confirm=True, display=True):
        r'''Reinterprets current LilyPond file.

        Returns none.
        '''
        if display:
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
        if display:
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

    def interpret_make_module(self, confirm=True, display=True):
        r'''Interprets ``__make__.py`` module.

        Creates ``output.ly`` and ``output.pdf`` files.

        Returns none.
        '''
        if not os.path.isfile(self._make_module_path):
            message = 'no __make__.py module found.'
            self._io_manager.display(message)
            return
        if display:
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
        self._io_manager.interpret(
            self._make_module_path, 
            confirm=False, 
            display=False,
            )
        if display:
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
        self._list_versions_directory()

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

    def open_versioned_definition_py(self):
        r'''Opens versioned definition module.

        Returns none.
        '''
        self._open_versioned_file('definition.py')

    def open_versioned_output_ly(self):
        r'''Opens output LilyPond file.

        Returns none.
        '''
        self._open_versioned_file('output.ly')

    def open_versioned_output_pdf(self):
        r'''Opens output PDF.

        Returns none.
        '''
        self._open_versioned_file('output.pdf')

    def open_versioned_pdfs(self):
        r'''Opens versioned PDFs.

        Returns none.
        '''
        versions_directory_path = self._versions_directory_path
        file_paths = []
        for directory_entry in os.listdir(versions_directory_path):
            if not directory_entry.startswith('output'):
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
            self._io_manager.display(message)
            return
        self._io_manager.open_file(file_paths)

    def version_artifacts(self, confirm=True, display=True):
        r'''Copies any of ``definition.py``, ``output.ly`` and ``output.pdf`` 
        to versions directory, if they exist.

        Returns none.
        '''
        self._version_artifacts(confirm=confirm, display=display)

    # TODO: reimplement as boilerplate
    def write_stub_definition_py(self, confirm=True, display=True):
        r'''Writes stub definition module.

        Returns none.
        '''
        if display:
            messages = []
            message = 'will write stub to {}.'
            message = message.format(self._definition_py_path)
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
        with file(self._definition_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        if display:
            message = 'wrote stub to {}.'
            message = message.format(self._definition_py_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True

    # TODO: reimplement as boilerplate
    def write_stub_make_module(self, confirm=True, display=True):
        r'''Writes stub __make__.py module.

        Returns none.
        '''
        if display:
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
        if display:
            messages = []
            message = 'wrote stub to {}.'.format(self._make_module_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True