# -*- encoding: utf-8 -*-
import collections
import os
import shutil
from abjad.tools import systemtools
from scoremanager.idetools.ScoreInternalPackageManager import \
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
            'illustration.ly',
            'illustration.pdf',
            ])
        self._optional_files = tuple(optional_files)
        required_files = list(self._required_files)
        required_files.extend([
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
    def _command_to_method(self):
        superclass = super(SegmentPackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'di': self.illustrate_definition_py,
            #
            'ii': self.interpret_illustration_ly,
            'ie': self.edit_illustration_ly,
            'io': self.open_illustration_pdf,
            #
            'vde': self.edit_versioned_definition_py,
            'vie': self.edit_versioned_illustration_ly,
            'vio': self.open_versioned_illustration_pdf,
            })
        return result

    @property
    def _definition_py_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _illustration_ly_path(self):
        return os.path.join(self._path, 'illustration.ly')

    @property
    def _illustration_pdf_path(self):
        return os.path.join(self._path, 'illustration.pdf')

    @property
    def _source_paths(self):
        return (
            self._definition_py_path,
            self._illustration_ly_path,
            self._illustration_pdf_path,
            )

    ### PRIVATE METHODS ###

    def _execute_definition_py(self):
        result = self._io_manager.execute_file(
            path = self._definition_py_path,
            attribute_names=('segment_maker',)
            )
        if result and len(result) == 1:
            target = result[0]
            return target

    def _make_definition_py_menu_section(self, menu):
        if not os.path.isfile(self._definition_py_path):
            message = 'No definition.py found;'
            message += ' use (ds) to write stub.'
            menu.make_information_section(
                menu_entries=[message],
                )
        commands = []
        commands.append(('definition.py - check', 'dc'))
        commands.append(('definition.py - edit', 'de'))
        commands.append(('definition.py - illustrate', 'di'))
        commands.append(('definition.py - stub', 'ds'))
        menu.make_command_section(
            commands=commands,
            is_hidden=False,
            name='definition py',
            )

    def _make_illustration_ly_menu_section(self, menu):
        commands = []
        if os.path.isfile(self._illustration_ly_path):
            commands.append(('illustration.ly - edit', 'ie'))
            commands.append(('illustration.ly - interpret', 'ii'))
        if os.path.isfile(self._illustration_pdf_path):
            commands.append(('illustration.pdf - open', 'io'))
        if commands:
            menu.make_command_section(
                is_hidden=False,
                commands=commands,
                name='illustration',
                )

    def _make_main_menu(self):
        superclass = super(SegmentPackageManager, self)
        menu = superclass._make_main_menu()
        self._make_definition_py_menu_section(menu)
        self._make_init_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_illustration_ly_menu_section(menu)
        self._make_package_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        self._make_versions_directory_menu_section(menu)
        return menu

    def _make_package(self):
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_segments = True

    ### PUBLIC METHODS ###

    def edit_definition_py(self):
        r'''Edits ``definition.py``.

        Returns none.
        '''
        self._io_manager.edit(self._definition_py_path)

    def edit_illustration_ly(self):
        r'''Opens ``illustration.ly``.

        Returns none.
        '''
        self._open_file(self._illustration_ly_path)

    def edit_versioned_definition_py(self):
        r'''Opens versioned ``definition py``.

        Returns none.
        '''
        self._open_versioned_file('definition.py')

    def edit_versioned_illustration_ly(self):
        r'''Opens versioned ``illustration.ly``.

        Returns none.
        '''
        self._open_versioned_file('illustration.ly')

    # TODO: refactor with MaterialPackageManager.illustrate_output_py()
    def illustrate_definition_py(self, dry_run=False):
        r'''Illustrates ``definition.py``.

        Makes ``illustration.ly`` and ``illustration.pdf``.

        Returns none.
        '''
        boilerplate_path = os.path.join(
            self._configuration.score_manager_directory,
            'boilerplate',
            '__illustrate_segment__.py',
            )
        illustrate_path = os.path.join(
            self._path,
            '__illustrate_segment__.py',
            )
        candidate_ly_path = os.path.join(
            self._path, 
            'illustration.candidate.ly'
            )
        candidate_pdf_path = os.path.join(
            self._path, 
            'illustration.candidate.pdf'
            )
        temporary_files = (
            illustrate_path, 
            candidate_ly_path,
            candidate_pdf_path,
            )
        for path in temporary_files:
            if os.path.exists(path):
                os.remove(path)
        illustration_ly_path = os.path.join(
            self._path,
            'illustration.ly',
            )
        illustration_pdf_path = os.path.join(
            self._path,
            'illustration.pdf',
            )
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._definition_py_path)
            outputs.append((illustration_ly_path, illustration_pdf_path))
            return inputs, outputs
        with systemtools.FilesystemState(remove=temporary_files):
            shutil.copyfile(boilerplate_path, illustrate_path)
            with self._io_manager._silent():
                result = self._io_manager.interpret_file(illustrate_path)
            stdout_lines, stderr_lines = result
            if stderr_lines:
                self._io_manager._display_errors(stderr_lines)
                return
            if not os.path.exists(illustration_pdf_path):
                messages = []
                messages.append('Wrote ...')
                tab = self._io_manager._tab
                if os.path.exists(candidate_ly_path):
                    shutil.move(candidate_ly_path, illustration_ly_path)
                    messages.append(tab + illustration_ly_path)
                if os.path.exists(candidate_pdf_path):
                    shutil.move(candidate_pdf_path, illustration_pdf_path)
                    messages.append(tab + illustration_pdf_path)
                self._io_manager._display(messages)
            else:
                result = systemtools.TestManager.compare_files(
                candidate_pdf_path,
                illustration_pdf_path,
                )
                messages = self._make_candidate_messages(
                    result, candidate_pdf_path, illustration_pdf_path)
                self._io_manager._display(messages)
                if result:
                    message = 'preserved {}.'.format(illustration_pdf_path)
                    self._io_manager._display(message)
                    return
                else:
                    message = 'overwrite existing PDF with candidate PDF?'
                    result = self._io_manager._confirm(message=message)
                    if self._session.is_backtracking or not result:
                        return
                    try:
                        shutil.move(candidate_ly_path, illustration_ly_path)
                    except IOError:
                        pass
                    try:
                        shutil.move(candidate_pdf_path, illustration_pdf_path)
                    except IOError:
                        pass

    def open_illustration_pdf(self):
        r'''Opens ``illustration.pdf``.

        Returns none.
        '''
        self._open_file(self._illustration_pdf_path)

    def open_versioned_illustration_pdf(self):
        r'''Opens versioned ``illustration.pdf``.

        Returns none.
        '''
        self._open_versioned_file('illustration.pdf')

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