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
    def _output_lilypond_file_path(self):
        return os.path.join(self._path, 'output.ly')
        
    @property
    def _output_pdf_file_path(self):
        return os.path.join(self._path, 'output.pdf')

    @property
    def _segment_definition_module_manager(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self._segment_definition_module_path,
            session=self._session,
            )
        return manager

    @property
    def _segment_definition_module_path(self):
        return os.path.join(self._path, 'definition.py')

    @property
    def _user_input_to_action(self):
        superclass = super(SegmentPackageManager, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'E': self.edit_segment_definition_module_from_top,
            'e': self.edit_segment_definition_module,
            'lyri': self.reinterpret_current_lilypond_file,
            'lyv': self.view_current_output_ly,
            'lyver': self.view_versioned_output_ly,
            'pdfv': self.view_output_pdf,
            'pdfm': self.make_asset_pdf,
            'vv': self.view_all_versioned_pdfs,
            'pdfver': self.view_versioned_output_pdf,
            'pyver': self.view_versioned_segment_definition_module,
            'pdfs': self.save_to_versions_directory,
            'vrl': self.list_versions_directory,
            })
        return _user_input_to_action

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
            self.edit_segment_definition_module()

    def _make_main_menu(self):
        superclass = super(SegmentPackageManager, self)
        where = self._where
        menu, section = superclass._make_main_menu(where=where)
        section.append(('package - remove', 'rm'))
        section.append(('package - list ', 'ls'))
        section.append(('package - rename', 'ren'))
        section = menu.make_command_section()
        section.append(('segment definition module - edit', 'e'))
        section = menu.make_command_section()
        section.append(('current pdf - make', 'pdfm'))
        if os.path.isfile(self._output_pdf_file_path):
            section.append(('current pdf - version', 'pdfs'))
        if os.path.isfile(self._output_pdf_file_path):
            section.append(('current pdf - view', 'pdfv'))
            section.default_index = len(section) - 1
        section = menu.make_command_section()
        versions_directory_path = self._versions_directory_path
        if self._is_populated_directory(versions_directory_path):
            section.append(('versioned pdfs - view', 'vv'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('segment definition module - edit at top', 'E'))
        if os.path.isfile(self._output_lilypond_file_path):
            section = menu.make_command_section(is_secondary=True)
            string = 'current lilypond file - reinterpret'
            section.append((string, 'lyri'))
            string = 'current lilypond file - view'
            section.append((string, 'lyv'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('versioned output ly - view', 'lyver'))
        section.append(('versioned output pdf - view', 'pdfv'))
        string = 'versioned segment definition module - view'
        section.append((string, 'pyver'))
        section.append(('versions directory - list', 'vrl'))
        return menu

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
            if extension in ('.ly', '.py'):
                command = 'vim -R {}'.format(file_path)
            elif extension == '.pdf':
                command = 'open {}'.format(file_path)
            self._io_manager.spawn_subprocess(command)
        
    ### PUBLIC METHODS ###

    def edit_segment_definition_module(
        self,
        pending_user_input=None,
        ):
        r'''Edits asset definition module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        self._segment_definition_module_manager.edit()

    def edit_segment_definition_module_from_top(
        self,
        pending_user_input=None,
        ):
        r'''Edits asset definition module.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        self._segment_definition_module_manager.edit(
            line_number=1)

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

    def make_asset_pdf(
        self,
        view_asset_pdf=True,
        ):
        r'''Makes asset PDF.

        Returns none.
        '''
        output_pdf_file_path = self._output_pdf_file_path
        modification_time = 0
        if os.path.isfile(output_pdf_file_path):
            modification_time = os.path.getmtime(output_pdf_file_path)
        manager = self._segment_definition_module_manager
        manager._interpret_in_external_process()
        new_modification_time = 0
        if os.path.isfile(output_pdf_file_path):
            new_modification_time = os.path.getmtime(output_pdf_file_path)
        if modification_time < new_modification_time and view_asset_pdf:
            self.view_output_pdf()

    def make_versions_directory(self):
        r'''Makes versions directory.

        Returns none.
        '''
        if not os.path.exists(self._versions_directory_path):
            os.mkdir(self._versions_directory_path)

    def reinterpret_current_lilypond_file(
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
        message = 'reinterpreted {!r}.'
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
        segment_definition_module_path = \
            self._get_segment_definition_module_path()
        if not os.path.isfile(segment_definition_module_path):
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
            segment_definition_module_path,
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
        file_paths = ' '.join(file_paths)
        command = 'open {}'.format(file_paths)
        self._io_manager.spawn_subprocess(command)

    def view_current_output_ly(self):
        r'''Views current output LilyPond file.

        Returns none.
        '''
        output_lilypond_file_path = self._output_lilypond_file_path
        if os.path.isfile(output_lilypond_file_path):
            command = 'vim -R {}'.format(output_lilypond_file_path)
            self._io_manager.spawn_subprocess(command)

    def view_output_pdf(self):
        r'''Views output PDF.

        Returns none.
        '''
        output_pdf_file_path = self._output_pdf_file_path
        if os.path.isfile(output_pdf_file_path):
            command = 'open {}'.format(output_pdf_file_path)
            self._io_manager.spawn_subprocess(command)

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

    def view_versioned_segment_definition_module(self):
        r'''Views versioned segment definition module.

        Returns none.
        '''
        self._view_versioned_file('.py')

    def write_initializer(self):
        r'''Writes initializer to disk.

        Returns none.
        '''
        if not os.path.exists(self._initializer_file_path):
            file_pointer = file(self._initializer_file_path, 'w')
            file_pointer.write('')
            file_pointer.close()

    def write_segment_definition_module(self):
        r'''Write segment definition module to disk.

        Returns none.
        '''
        if not os.path.exists(self.segment_definition_module_path):
            file_pointer = file(self.segment_definition_module_path, 'w')
            file_pointer.write('# -*- encoding: utf-8 -*-\n')
            file_pointer.write('from abjad import *\n')
            file_pointer.write('\n\n')
            file_pointer.close()
