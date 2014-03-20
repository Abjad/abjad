# -*- encoding: utf-8 -*-
import itertools
import os
from abjad.tools import systemtools
from scoremanager.managers.PackageManager import PackageManager


class SegmentPackageManager(PackageManager):
    r'''Segment package manager.
    '''

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
        return self._space_delimited_lowercase_name

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
    def _definition_module_manager(self):
        from scoremanager import managers
        if not os.path.exists(self._definition_module_path):
            message = 'no definition.py module found.'
            self._io_manager.confirm(message)
            return
        manager = managers.FileManager(
            self._definition_module_path,
            session=self._session,
            )
        return manager

    @property
    def _definition_module_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _user_input_to_action(self):
        superclass = super(SegmentPackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'dmi': self.interpret_definition_module,
            'E': self.edit_definition_module_from_top,
            'e': self.edit_definition_module,
            'lyi': self.interpret_current_lilypond_file,
            'lyv': self.view_current_output_ly,
            'lyver': self.view_versioned_output_ly,
            'mmi': self.interpret_make_module,
            'mms': self.write_make_module_stub,
            'mmv': self.view_make_module,
            'pdfv': self.view_output_pdf,
            'vv': self.view_all_versioned_pdfs,
            'pdfver': self.view_versioned_output_pdf,
            'pyver': self.view_versioned_definition_module,
            'pdfs': self.save_to_versions_directory,
            'vrl': self.list_versions_directory,
            })
        return result

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
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            self.edit_definition_module()

    def _make_current_lilypond_file_menu_section(self, menu):
        if os.path.isfile(self._output_lilypond_file_path):
            section = menu.make_command_section(
                name='lilypond file',
                is_hidden=True,
                )
            string = 'lilypond file - interpret'
            section.append((string, 'lyi'))
            string = 'lilypond file - view'
            section.append((string, 'lyv'))
            return section

    def _make_current_pdf_menu_section(self, menu):
        section = menu.make_command_section(name='pdf')
        if os.path.isfile(self._output_pdf_file_path):
            section.append(('pdf - version', 'pdfs'))
        if os.path.isfile(self._output_pdf_file_path):
            section.append(('pdf - view', 'pdfv'))
        return section

    def _make_main_menu(self):
        superclass = super(SegmentPackageManager, self)
        where = self._where
        menu = superclass._make_main_menu(where=where)
        self._make_current_lilypond_file_menu_section(menu)
        self._make_current_pdf_menu_section(menu)
        self._make_definition_module_menu_section(menu)
        self._make_directory_menu_section(menu)
        self._make_make_module_menu_section(menu)
        self._make_versioned_pdfs_menu_section(menu)
        self._make_versions_directory_menu_section(menu)
        return menu

    def _make_definition_module_menu_section(self, menu):
        section = menu.make_command_section(name='definition module')
        section.append(('definition module - edit', 'e'))
        section.append(('definition module - edit at top', 'E'))
        section.append(('definition module - interpret', 'dmi'))
        return section

    def _make_make_module_menu_section(self, menu):
        section = menu.make_command_section(name='make module')
        if os.path.isfile(self._make_module_path):
            section.append(('make module - interpret', 'mmi'))
            section.append(('make module - view', 'mmv'))
        section.append(('make module - stub', 'mms'))
        return section

    def _make_versioned_pdfs_menu_section(self, menu):
        section = menu.make_command_section(name='versioned pdfs')
        versions_directory_path = self._versions_directory_path
        if self._is_populated_directory(versions_directory_path):
            section.append(('versioned pdfs - view', 'vv'))
        return section

    def _make_versions_directory_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            name='versions directory',
            )
        section.append(('versioned output ly - view', 'lyver'))
        section.append(('versioned output pdf - view', 'pdfv'))
        string = 'versioned definition module - view'
        section.append((string, 'pyver'))
        section.append(('versions directory - list', 'vrl'))
        return section

    def _view_versioned_file(self, extension):
        assert extension in ('.ly', '.pdf', '.py')
        getter = self._io_manager.make_getter(where=self._where)
        last_version_number = self._get_last_version_number()
        if last_version_number is None:
            message = 'versions directory empty.'
            self._io_manager.proceed(message)
            return
        prompt = 'version number (0-{})'
        prompt = prompt.format(last_version_number)
        getter.append_integer(prompt)
        version_number = getter._run(clear_terminal=False)
        if self._session._backtrack():
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
            self._io_manager.view(file_path)
        
    ### PUBLIC METHODS ###

    def edit_definition_module(
        self,
        pending_user_input=None,
        ):
        r'''Edits asset definition module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        manager = self._definition_module_manager
        if not manager:
            return
        manager.edit()

    def edit_definition_module_from_top(
        self,
        pending_user_input=None,
        ):
        r'''Edits asset definition module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        manager = self._definition_module_manager
        if not manager:
            return
        manager.edit(line_number=1)

    def interpret_definition_module(
        self,
        prompt=True,
        view_asset_pdf=True,
        ):
        r'''Makes asset PDF.

        Returns none.
        '''
        output_pdf_file_path = self._output_pdf_file_path
        modification_time = 0
        if os.path.isfile(output_pdf_file_path):
            modification_time = os.path.getmtime(output_pdf_file_path)
        manager = self._definition_module_manager
        if not manager:
            return
        manager._interpret(prompt=prompt)
        if not view_asset_pdf:
            return
        new_modification_time = 0
        if os.path.isfile(output_pdf_file_path):
            new_modification_time = os.path.getmtime(output_pdf_file_path)
        if modification_time < new_modification_time and view_asset_pdf:
            self.view_output_pdf()

    def interpret_make_module(self, prompt=True):
        r'''Interprets __make__ module.

        Creates output.pdf and output.ly files.

        Returns none.
        '''
        from scoremanager import managers
        if not os.path.isfile(self._make_module_path):
            message = 'no __make__ module found.'
            self._io_manager.proceed(message, prompt=prompt)
            return
        manager = managers.FileManager(
            path=self._make_module_path,
            session=self._session,
            )
        manager._interpret(prompt=False)
        message = 'created output.pdf and output.ly files.'
        self._io_manager.proceed(message, prompt=prompt)

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
        self._io_manager.display(lines)
        self._io_manager.proceed('')

    def make_versions_directory(self):
        r'''Makes versions directory.

        Returns none.
        '''
        if not os.path.exists(self._versions_directory_path):
            os.mkdir(self._versions_directory_path)

    def interpret_current_lilypond_file(
        self, 
        view_output_pdf=True,
        prompt=True,
        ):
        r'''Reinterprets current LilyPond file.

        Opens resulting PDF when `view_output_pdf` is true.

        Returns none.
        '''
        file_path = self._output_lilypond_file_path
        if not os.path.isfile(file_path):
            return
        result = self._io_manager.run_lilypond(file_path)
        if not result:
            return
        lines = []
        lilypond_file_path = self._output_lilypond_file_path
        message = 'interpreted {!r}.'
        message = message.format(lilypond_file_path)
        lines.append(message)
        pdf_file_path = self._output_pdf_file_path
        message = 'wrote {!r}.'
        message = message.format(pdf_file_path)
        lines.append(message)
        lines.append('')
        self._io_manager.display(lines)
        lines = []
        message = None
        if view_output_pdf:
            message = 'press return to view PDF.'
        self._io_manager.proceed(message=message, prompt=prompt)
        if view_output_pdf:
            self.view_output_pdf()

    def save_to_versions_directory(
        self,
        prompt=True
        ):
        r'''Saves asset definition module,
        output PDF and output LilyPond file to versions directory.

        Returns none.
        '''
        paths = {}
        definition_module_path = \
            self._get_definition_module_path()
        if not os.path.isfile(definition_module_path):
            message = 'can not find asset definition module.'
            self._io_manager.proceed(
                message,
                prompt=prompt,
                )
            return
        output_pdf_file_path = self._output_pdf_file_path
        if not os.path.isfile(output_pdf_file_path):
            message = 'can not find output PDF.'
            self._io_manager.proceed(
                message,
                prompt=prompt,
                )
            return
        output_lilypond_file_path = self._output_lilypond_file_path
        if not os.path.isfile(output_lilypond_file_path):
            message = 'can not find output LilyPond file.'
            self._io_manager.proceed(
                message,
                prompt=prompt,
                )
            return
        next_output_file_name = systemtools.IOManager.get_next_output_file_name(
            output_directory_path=self._versions_directory_path,
            )
        result = os.path.splitext(next_output_file_name)
        next_output_file_name_root, extension = result
        target_file_name = next_output_file_name_root + '.py'
        target_file_path = os.path.join(
            self._versions_directory_path,
            target_file_name,
            )
        command = 'cp {} {}'.format(
            definition_module_path,
            target_file_path,
            )
        self._io_manager.spawn_subprocess(command)
        target_file_name = next_output_file_name_root + '.pdf'
        target_file_path = os.path.join(
            self._versions_directory_path,
            target_file_name,
            )
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
        command = 'cp {} {}'.format(
            output_lilypond_file_path,
            target_file_path,
            )
        self._io_manager.spawn_subprocess(command)
        version_number = int(next_output_file_name_root)
        message = 'version {} written to disk.'
        message = message.format(version_number)
        self._io_manager.proceed(
            message,
            prompt=prompt,
            )
        return version_number

    def view_all_versioned_pdfs(self):
        r'''Views all versioend PDFs.

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
        self._io_manager.view(file_paths)

    def view_current_output_ly(self):
        r'''Views current output LilyPond file.

        Returns none.
        '''
        file_path = self._output_lilypond_file_path
        if os.path.isfile(file_path):
            self._io_manager.view(file_path)

    def view_make_module(self):
        r'''Views __make__ module.

        Returns none.
        '''
        self._io_manager.view(self._make_module_path)

    def view_output_pdf(self):
        r'''Views output PDF.

        Returns none.
        '''
        file_path = self._output_pdf_file_path
        if os.path.isfile(file_path):
            self._io_manager.view(file_path)

    def view_versioned_output_ly(self):
        r'''Views output LilyPond file.

        Returns none.
        '''
        self._view_versioned_file('.ly')

    def view_versioned_output_pdf(self):
        r'''Views output PDF.

        Returns none.
        '''
        self._view_versioned_file('.pdf')

    def view_versioned_definition_module(self):
        r'''Views versioned definition module.

        Returns none.
        '''
        self._view_versioned_file('.py')

    def write_definition_module(self):
        r'''Write definition module to disk.

        Returns none.
        '''
        if not os.path.exists(self._definition_module_path):
            with file(self._definition_module_path, 'w') as file_pointer:
                file_pointer.write(self._unicode_directive + '\n')
                file_pointer.write('from abjad import *\n')
                file_pointer.write('\n\n')

    def write_initializer(self):
        r'''Writes initializer to disk.

        Returns none.
        '''
        if not os.path.exists(self._initializer_file_path):
            with file(self._initializer_file_path, 'w') as file_pointer:
                file_pointer.write('')

    def write_make_module_stub(self):
        r'''Writes __make__ module stub to disk.

        Returns none.
        '''
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