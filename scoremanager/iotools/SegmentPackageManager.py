# -*- encoding: utf-8 -*-
import collections
import os
import shutil
from abjad.tools import systemtools
from scoremanager.iotools.ScoreInternalPackageManager import \
    ScoreInternalPackageManager


class SegmentPackageManager(ScoreInternalPackageManager):
    r'''Segment package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(SegmentPackageManager, self)
        superclass.__init__(path=path, session=session)
        optional_files = list(self._optional_files)
        optional_files.extend([
            '__make__.py',
            'output.ly',
            'output.pdf',
            ])
        self._optional_files = tuple(optional_files)
        required_files = list(self._required_files)
        required_files.extend([
            '__make__.py',
            'definition.py',
            ])
        self._required_files = tuple(required_files)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            name = self._get_metadatum('name')
            name = name or self._space_delimited_lowercase_name
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
    def _input_to_method(self):
        superclass = super(SegmentPackageManager, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'de': self.edit_definition_py,
            'ds': self.write_stub_definition_py,
            #
            'ki': self.interpret_make_py,
            'ko': self.open_make_py,
            'ks': self.write_stub_make_py,
            #
            'oli': self.interpret_output_ly,
            'olo': self.open_output_ly,
            'opo': self.open_output_pdf,
            #
            'vdo': self.open_versioned_definition_py,
            'volo': self.open_versioned_output_ly,
            'vopo': self.open_versioned_output_pdf,
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

    ### PRIVATE METHODS ###

    def _make_definition_py_menu_section(self, menu):
        if not os.path.isfile(self._definition_py_path):
            message = 'No definition.py found;'
            message += ' use (ds) to write stub.'
            menu.make_information_section(
                menu_entries=[message],
                )
        commands = []
        commands.append(('definition.py - edit', 'de'))
        commands.append(('definition.py - stub', 'ds'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='definition py',
            )

    def _make_main_menu(self):
        superclass = super(SegmentPackageManager, self)
        menu = superclass._make_main_menu()
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
        commands.append(('__make__.py - interpret', 'ki'))
        commands.append(('__make__.py - open', 'ko'))
        commands.append(('__make__.py - stub', 'ks'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='__make__.py',
            )

    def _make_output_ly_menu_section(self, menu):
        if os.path.isfile(self._output_lilypond_file_path):
            commands = []
            commands.append(('output.ly - interpret', 'oli'))
            commands.append(('output.ly - open', 'olo'))
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='output.ly',
                )

    def _make_output_pdf_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._output_pdf_file_path):
            commands.append(('output.pdf - open', 'opo'))
        if commands:
            menu.make_command_section(
                commands=commands,
                is_hidden=True,
                name='output.pdf',
                )

    def _make_package(self):
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._make_silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
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
            directory = self._versions_directory
            file_name = '{}_{}{}'.format(root, next_version_string, extension)
            target_path = os.path.join(directory, file_name)
            message = '   TO: {}'.format(target_path)
            messages.append(message)
        return messages

    def _make_versions_directory_menu_section(self, menu):
        commands = []
        commands.append(('versions - definition.py - open', 'vdo'))
        commands.append(('versions - output.ly - open', 'volo'))
        commands.append(('versions - output.pdf - open', 'vopo'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='versions directory',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_segments = True

    ### PUBLIC METHODS ###

    def edit_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def interpret_make_py(self, dry_run=False):
        r'''Interprets ``__make__.py``.

        Makes ``output.ly`` and ``output.pdf``.

        Returns none.
        '''
        inputs = [self._make_py_path]
        outputs = [(
            self._output_lilypond_file_path, self._output_pdf_file_path)]
        if dry_run:
            return inputs, outputs
        if not os.path.isfile(self._make_py_path):
            message = 'no __make__.py found.'
            self._io_manager._display(message)
            return
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._make_silent():
            self._io_manager.interpret_file(self._make_py_path)

    def interpret_output_ly(self, dry_run=False):
        r'''Interprets ``output.ly``.

        Makes ``output.pdf``.

        Returns none.
        '''
        inputs = [self._output_lilypond_file_path]
        outputs = [self._output_pdf_file_path]
        if dry_run:
            return inputs, outputs
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        file_path = self._output_lilypond_file_path
        if not os.path.isfile(file_path):
            return
        self._io_manager.run_lilypond(file_path)

    def open_make_py(self):
        r'''Opens ``__make__.py``.

        Returns none.
        '''
        self._open_file(self._make_py_path)

    def open_output_ly(self):
        r'''Opens ``output.ly``.

        Returns none.
        '''
        self._open_file(self._output_lilypond_file_path)

    def open_output_pdf(self):
        r'''Opens ``output.pdf``.

        Returns none.
        '''
        self._open_file(self._output_pdf_file_path)

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

    def write_stub_definition_py(self):
        r'''Writes stub ``definition.py``.

        Returns none.
        '''
        messages = []
        message = 'will write stub to {}.'
        message = message.format(self._definition_py_path)
        messages.append(message)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        source_path = os.path.join(
            self._configuration.score_manager_directory,
            'boilerplate',
            'definition.py',
            )
        destination_path = self._definition_py_path
        shutil.copyfile(source_path, destination_path)

    def write_stub_make_py(self):
        r'''Writes stub ``__make__.py``.

        Returns none.
        '''
        messages = []
        message = 'will write stub to {}.'.format(self._make_py_path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        source_path = os.path.join(
            self._configuration.score_manager_directory,
            'boilerplate',
            '__make__.py',
            )
        destination_path = self._make_py_path
        shutil.copyfile(source_path, destination_path)