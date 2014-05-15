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
            'dpye': self.edit_definition_py,
            'dpyws': self.write_stub_definition_py,
            'mpyi': self.interpret_make_py,
            'mpyo': self.open_make_py,
            'mpyws': self.write_stub_make_py,
            'olyi': self.interpret_output_ly,
            'olyo': self.open_output_ly,
            'opdfo': self.open_output_pdf,
            'vdpyo': self.open_versioned_definition_py,
            'verls': self.list_versions_directory,
            'ver': self.version_package,
            'volyo': self.open_versioned_output_ly,
            'vopdfo': self.open_versioned_output_pdf,
            })
        return result

    @property
    def _make_py_path(self):
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

    def _make_output_ly_menu_section(self, menu):
        if os.path.isfile(self._output_lilypond_file_path):
            commands = []
            commands.append(('output.ly - interpret', 'olyi'))
            commands.append(('output.ly - open', 'olyo'))
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='output.ly',
                )

    def _make_output_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._output_pdf_file_path):
            commands.append(('output.pdf - open', 'opdfo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                is_hidden=True,
                name='output.pdf',
                )

    def _make_definition_py_menu_section(self, menu):
        if not os.path.isfile(self._definition_py_path):
            message = 'No definition.py found;'
            message += ' use (dpyws) to write stub.'
            menu.make_information_section(
                menu_entries=[message],
                )
        commands = []
        commands.append(('definition.py - edit', 'dpye'))
        commands.append(('definition.py - write stub', 'dpyws'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='definition py',
            )

    def _make_main_menu(self, name='segment package manager'):
        superclass = super(SegmentPackageManager, self)
        menu = superclass._make_main_menu(name=name)
        self._make_definition_py_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_py_menu_section(menu)
        self._make_make_py_menu_section(menu)
        self._make_output_ly_menu_section(menu)
        self._make_output_pdf_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        self._make_versions_directory_menu_section(menu)
        return menu

    def _make_make_py_menu_section(self, menu):
        commands = []
        commands.append(('__make__.py - interpret', 'mpyi'))
        commands.append(('__make__.py - open', 'mpyo'))
        commands.append(('__make__.py - write stub', 'mpyws'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='__make__.py',
            )

    def _make_version_package_messages(self):
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
        commands.append(('versions - definition.py - open', 'vdpyo'))
        commands.append(('versions - output.ly - open', 'volyo'))
        commands.append(('versions - output.pdf - open', 'vopdfo'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='versions directory',
            )

    ### PUBLIC METHODS ###

    def edit_definition_py(self):
        r'''Edits asset definition py.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def interpret_output_ly(self, confirm=True, display=True):
        r'''Reinterprets current LilyPond file.

        Returns none.
        '''
        if display:
            messages = []
            messages.append('will interpret ...')
            messages.append('')
            message = '  INPUT: {}'.format(self._output_lilypond_file_path)
            messages.append(message)
            message = ' OUTPUT: {}'.format(self._output_pdf_file_path)
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

    def interpret_make_py(self, confirm=True, display=True):
        r'''Interprets ``__make__.py``.

        Makes ``output.ly`` and ``output.pdf``.

        Returns none.
        '''
        with self._io_manager.make_interaction(display=display):
            if not os.path.isfile(self._make_py_path):
                message = 'no __make__.py found.'
                self._io_manager.display(message)
                return
            if display:
                messages = []
                messages.append('will interpret ...')
                message = '  INPUT: {}'.format(self._make_py_path)
                messages.append(message)
                message = ' OUTPUT: {}'.format(self._output_lilypond_file_path)
                messages.append(message)
                message = ' OUTPUT: {}'.format(self._output_pdf_file_path)
                messages.append(message)
                self._io_manager.display(messages)
            if confirm:
                result = self._io_manager.confirm()
                if self._should_backtrack():
                    return
                if not result:
                    return
            self._io_manager.interpret(
                self._make_py_path, 
                confirm=False, 
                display=False,
                )

    def list_versions_directory(self):
        r'''Lists versions directory.

        Returns none.
        '''
        self._list_versions_directory()

    def open_make_py(self):
        r'''Opens ``__make__.py``.

        Returns none.
        '''
        self._io_manager.open_file(self._make_py_path)

    def open_output_ly(self):
        r'''Opens ``output.ly``.

        Returns none.
        '''
        file_path = self._output_lilypond_file_path
        if os.path.isfile(file_path):
            self._io_manager.open_file(file_path)

    def open_output_pdf(self):
        r'''Opens ``output.pdf``.

        Returns none.
        '''
        file_path = self._output_pdf_file_path
        if os.path.isfile(file_path):
            self._io_manager.open_file(file_path)

    def open_versioned_definition_py(self):
        r'''Opens versioned ``definition py``.

        Returns none.
        '''
        self._open_versioned_file('definition.py')

    def open_versioned_output_ly(self):
        r'''Opens versioned ``output.ly``.

        Returns none.
        '''
        self._open_versioned_file('output.ly')

    def open_versioned_output_pdf(self):
        r'''Opens versioned ``output.pdf``.

        Returns none.
        '''
        self._open_versioned_file('output.pdf')

    def version_package(self, confirm=True, display=True):
        r'''Copies any of ``definition.py``, ``output.ly`` and ``output.pdf`` 
        to versions directory, if they exist.

        Returns none.
        '''
        self._version_package(confirm=confirm, display=display)

    # TODO: reimplement as boilerplate
    def write_stub_definition_py(self, confirm=True, display=True):
        r'''Writes stub ``definition.py``.

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
    def write_stub_make_py(self, confirm=True, display=True):
        r'''Writes stub ``__make__.py``.

        Returns none.
        '''
        if display:
            messages = []
            message = 'will write stub to {}.'.format(self._make_py_path)
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
        with file(self._make_py_path, 'w') as file_pointer:
            file_pointer.write(contents)
        if display:
            messages = []
            message = 'wrote stub to {}.'.format(self._make_py_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True