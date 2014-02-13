# -*- encoding: utf-8 -*-
import itertools
import os
from abjad.tools import systemtools
from scoremanager.managers.PackageManager import PackageManager


class SegmentPackageManager(PackageManager):

    ### INITIALIZER ###

    def __init__(
        self, 
        packagesystem_path=None, 
        score_template=None, 
        session=None,
        ):
        PackageManager.__init__(
            self, 
            packagesystem_path=packagesystem_path, 
            session=session,
            )
        self.score_template = score_template

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

    ### PRIVATE METHODS ###

    def _get_asset_definition_module_file_path(self):
        return os.path.join(self.filesystem_path, 'definition.py')

    def _get_last_version_number(self):
        versions_directory_path = self._get_versions_directory_path()
        file_names = sorted(os.listdir(versions_directory_path))
        if not file_names:
            return
        file_names.sort()
        last_file_name = file_names[-1]
        assert last_file_name[0].isdigit()
        version_string = last_file_name[:4]
        version_number = int(version_string)
        return version_number

    def _get_output_lilypond_file_path(self):
        return os.path.join(self.filesystem_path, 'output.ly')
        
    def _get_output_pdf_file_path(self):
        return os.path.join(self.filesystem_path, 'output.pdf')

    def _get_versions_directory_path(self):
        return os.path.join(self.filesystem_path, 'versions')
        
    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif result == 'user entered lone return':
            self.interactively_edit_asset_definition_module()

    def _interactively_view_versioned_file(self, extension):
        assert extension in ('.ly', '.pdf', '.py')
        getter = self.session.io_manager.make_getter(where=self._where)
        last_version_number = self._get_last_version_number()
        if last_version_number is None:
            message = 'versions directory empty.'
            self.session.io_manager.proceed(message)
            return
        prompt = 'version number (0-{})'
        prompt = prompt.format(last_version_number)
        getter.append_integer(prompt)
        version_number = getter._run(clear_terminal=False)
        if self.session.backtrack():
            return
        if last_version_number < version_number or \
            (version_number < 0 and last_version_number < abs(version_number)):
            message = "version {} doesn't exist yet."
            message = message.format(version_number)
            self.session.io_manager.proceed(['', message])
        if version_number < 0:
            version_number = last_version_number + version_number + 1
        version_string = str(version_number).zfill(4)
        file_name = '{}{}'.format(version_string, extension)
        file_path = os.path.join(
            self.filesystem_path,
            'versions',
            file_name,
            )
        if os.path.isfile(file_path):
            if extension in ('.ly', '.py'):
                command = 'vim -R {}'.format(file_path)
            elif extension == '.pdf':
                command = 'open {}'.format(file_path)
            systemtools.IOManager.spawn_subprocess(command)
        
    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('remove package', 'rm'))
        hidden_section.append(('list package', 'ls'))
        hidden_section.append(('rename package', 'ren'))
        hidden_section.append(('manage tags', 'tags'))
        command_section = main_menu.make_command_section()
        command_section.append(('segment definition module - edit', 'e'))
        command_section = main_menu.make_command_section()
        command_section.append(('output pdf - make', 'pdfm'))
        if os.path.isfile(self._get_output_pdf_file_path()):
            command_section.append(('output pdf - save', 'pdfs'))
        if os.path.isfile(self._get_output_pdf_file_path()):
            command_section.append(('output pdf - view', 'pdfv'))
            command_section.default_index = len(command_section) - 1
        command_section = main_menu.make_command_section()
        versions_directory_path = self._get_versions_directory_path()
        if self._is_populated_directory(versions_directory_path):
            command_section.append(('versioned pdfs - view', 'vv'))
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('segment definition module - edit at top', 'E'))
        if os.path.isfile(self._get_output_lilypond_file_path()):
            hidden_section.append(('current output ly - view', 'ly'))
            hidden_section.append(('versioned output ly - view', 'lyver'))
        hidden_section.append(('versioned output pdf - view', 'pdfv'))
        display_string = 'versioned segment definition module - view'
        hidden_section.append((display_string, 'pyver'))
        hidden_section.append(('list versions directory', 'vrl'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @apply
    def score_template():
        def fget(self):
            return self._score_template
        def fset(self, score_template):
            from abjad.tools import scoretools
            assert isinstance(score_template, (scoretools.Score, type(None)))
            self._score_template = score_template
        return property(**locals())

    @property
    def segment_definition_module_file_path(self):
        return os.path.join(self.filesystem_path, 'definition.py')

    @property
    def segment_definition_module_manager(self):
        from scoremanager import managers
        manager = managers.FileManager(
            self.segment_definition_module_file_path,
            session=self.session,
            )
        return manager

    @property
    def segment_definition_module_packagesystem_path(self):
        return '.'.join([
            self.package_path,
            'definition',
            ])

    ### PUBLIC METHODS ###

    def interactively_edit_asset_definition_module(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits asset definition module.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        self.segment_definition_module_manager.interactively_edit()

    def interactively_edit_asset_definition_module_from_top(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits asset definition module.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        self.segment_definition_module_manager.interactively_edit(
            line_number=1)

    def interactively_list_versions_directory(self):
        r'''Interactively lists versions directory.

        Returns none.
        '''
        versions_directory_path = self._get_versions_directory_path()
        file_names = []
        for directory_entry in os.listdir(versions_directory_path):
            if directory_entry[0].isdigit():
                file_names.append(directory_entry)
        for x in itertools.groupby(file_names, key=lambda x: x[:4]):
            key, file_names = x
            string = ' '.join(file_names)
            print string
        self.session.io_manager.proceed('')

    def interactively_make_asset_pdf(
        self,
        view_asset_pdf=True,
        ):
        r'''Interactively makes asset PDF.

        Returns none.
        '''
        output_pdf_file_path = self._get_output_pdf_file_path()
        modification_time = 0
        if os.path.isfile(output_pdf_file_path):
            modification_time = os.path.getmtime(output_pdf_file_path)
        manager = self.segment_definition_module_manager
        manager._interpret_in_external_process()
        new_modification_time = 0
        if os.path.isfile(output_pdf_file_path):
            new_modification_time = os.path.getmtime(output_pdf_file_path)
        if modification_time < new_modification_time and view_asset_pdf:
            self.view_output_pdf()

    def interactively_save_to_versions_directory(
        self,
        is_interactive=True
        ):
        r'''Interactively saves asset definition module,
        output PDF and output LilyPond file to versions directory.

        Returns none.
        '''
        paths = {}
        asset_definition_module_file_path = \
            self._get_asset_definition_module_file_path()
        if not os.path.isfile(asset_definition_module_file_path):
            message = 'can not find asset definition module.'
            self.session.io_manager.proceed(
                message,
                is_interactive=is_interactive,
                )
            return
        output_pdf_file_path = self._get_output_pdf_file_path()
        if not os.path.isfile(output_pdf_file_path):
            message = 'can not find output PDF.'
            self.session.io_manager.proceed(
                message,
                is_interactive=is_interactive,
                )
            return
        output_lilypond_file_path = self._get_output_lilypond_file_path()
        if not os.path.isfile(output_lilypond_file_path):
            message = 'can not find output LilyPond file.'
            self.session.io_manager.proceed(
                message,
                is_interactive=is_interactive,
                )
            return
        next_output_file_name = systemtools.IOManager.get_next_output_file_name(
            output_directory_path=self._get_versions_directory_path(),
            )
        result = os.path.splitext(next_output_file_name)
        next_output_file_name_root, extension = result
        target_file_name = next_output_file_name_root + '.py'
        target_file_path = os.path.join(
            self._get_versions_directory_path(),
            target_file_name,
            )
        command = 'cp {} {}'.format(
            asset_definition_module_file_path,
            target_file_path,
            )
        systemtools.IOManager.spawn_subprocess(command)
        target_file_name = next_output_file_name_root + '.pdf'
        target_file_path = os.path.join(
            self._get_versions_directory_path(),
            target_file_name,
            )
        command = 'cp {} {}'.format(
            output_pdf_file_path,
            target_file_path,
            )
        systemtools.IOManager.spawn_subprocess(command)
        target_file_name = next_output_file_name_root + '.ly'
        target_file_path = os.path.join(
            self._get_versions_directory_path(),
            target_file_name,
            )
        command = 'cp {} {}'.format(
            output_lilypond_file_path,
            target_file_path,
            )
        systemtools.IOManager.spawn_subprocess(command)
        version_number = int(next_output_file_name_root)
        message = 'version {} written to disk.'
        message = message.format(version_number)
        self.session.io_manager.proceed(
            message,
            is_interactive=is_interactive,
            )
        return version_number

    def interactively_view_all_versioned_pdfs(self):
        r'''Interactively views all versioend PDFs.

        Returns none.
        '''
        versions_directory_path = self._get_versions_directory_path()
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
            self.session.io_manager.proceed(message)
            return
        file_paths = ' '.join(file_paths)
        command = 'open {}'.format(file_paths)
        systemtools.IOManager.spawn_subprocess(command)

    def interactively_view_current_output_ly(self):
        r'''Interactively views current output LilyPond file.

        Returns none.
        '''
        output_lilypond_file_path = self._get_output_lilypond_file_path()
        if os.path.isfile(output_lilypond_file_path):
            command = 'vim -R {}'.format(output_lilypond_file_path)
            systemtools.IOManager.spawn_subprocess(command)

    def interactively_view_versioned_output_ly(self):
        r'''Interactively views output LilyPond file.

        Returns none.
        '''
        self._interactively_view_versioned_file('.ly')

    def interactively_view_versioned_output_pdf(self):
        r'''Interactively views output PDF.

        Returns none.
        '''
        self._interactively_view_versioned_file('.pdf')

    def interactively_view_versioned_segment_definition_module(self):
        r'''Interactively views versioned segment definition module.

        Returns none.
        '''
        self._interactively_view_versioned_file('.py')

    def make_versions_directory(self):
        r'''Makes versions directory.

        Returns none.
        '''
        if not os.path.exists(self._get_versions_directory_path()):
            os.mkdir(self._get_versions_directory_path())

    def view_output_pdf(self):
        r'''Views output PDF.

        Returns none.
        '''
        output_pdf_file_path = self._get_output_pdf_file_path()
        if os.path.isfile(output_pdf_file_path):
            command = 'open {}'.format(output_pdf_file_path)
            systemtools.IOManager.spawn_subprocess(command)

    def write_initializer_to_disk(self):
        r'''Writes initializer to disk.

        Returns none.
        '''
        if not os.path.exists(self.initializer_file_name):
            file_pointer = file(self.initializer_file_name, 'w')
            file_pointer.write('')
            file_pointer.close()

    def write_segment_definition_module_to_disk(self):
        r'''Write segment definition module to disk.

        Returns none.
        '''
        if not os.path.exists(self.segment_definition_module_file_path):
            file_pointer = file(self.segment_definition_module_file_path, 'w')
            file_pointer.write('# -*- encoding: utf-8 -*-\n')
            file_pointer.write('from abjad import *\n')
            file_pointer.write('\n\n')
            file_pointer.close()

    ### UI MANIFEST ###

    user_input_to_action = PackageManager.user_input_to_action.copy()
    user_input_to_action.update({
        'E': interactively_edit_asset_definition_module_from_top,
        'e': interactively_edit_asset_definition_module,
        'ly': interactively_view_current_output_ly,
        'lyver': interactively_view_versioned_output_ly,
        'pdfv': view_output_pdf,
        'pdfm': interactively_make_asset_pdf,
        'vv': interactively_view_all_versioned_pdfs,
        'pdfver': interactively_view_versioned_output_pdf,
        'pyver': interactively_view_versioned_segment_definition_module,
        'pdfs': interactively_save_to_versions_directory,
        'vrl': interactively_list_versions_directory,
        })
