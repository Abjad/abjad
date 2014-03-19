# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class SegmentPackageWrangler(PackageWrangler):
    r'''Segment package wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> wrangler = score_manager._segment_package_wrangler
            >>> wrangler
            SegmentPackageWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(SegmentPackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.SegmentPackageManager
        self._score_storehouse_path_infix_parts = ('segments',)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'segments'

    @property
    def _user_input_to_action(self):
        superclass = super(SegmentPackageWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'lyi': self.interpret_current_lilypond_files,
            'pdfs': self.version_segment_packages,
            'pdfv': self.view_segment_pdfs,
            'dmi': self.interpret_definition_modules,
            })
        return result

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            segment_package_manager = self._initialize_asset_manager(result)
            segment_package_manager._run()

    def _make_asset(
        self, 
        path, 
        prompt=False, 
        metadata=None,
        ):
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._asset_manager_class(
            path=path,
            session=self._session,
            )
        manager.write_initializer()
        manager.write_definition_module()
        manager.make_versions_directory()
        message = 'segment created: {!r}.'.format(path)
        self._io_manager.proceed(message=message, prompt=prompt)

    def _make_asset_menu_section(self, menu):
        section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries()
        for menu_entry in asset_menu_entries:
            section.append(menu_entry)
        section = menu.make_command_section(
            name='assets',
            match_on_display_string=False,
            )
        return section

    def _make_current_definition_modules_menu_section(self, menu):
        name = 'definition modules'
        section = menu.make_command_section(name=name)
        string = 'all segments - definition module - interpret'
        section.append((string, 'dmi'))
        return section

    def _make_current_lilypond_files_menu_section(self, menu):
        section = menu.make_command_section(name='lilypond files')
        string = 'all segments - lilypond file - interpret'
        section.append((string, 'lyi'))
        return section

    def _make_current_pdfs_menu_section(self, menu):
        section = menu.make_command_section(name='pdfs')
        section.append(('all segments - pdf - version', 'pdfs'))
        section.append(('all segments - pdf - view', 'pdfv'))
        return section

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        self._make_asset_menu_section(menu)
        self._make_current_definition_modules_menu_section(menu)
        self._make_current_lilypond_files_menu_section(menu)
        self._make_current_pdfs_menu_section(menu)
        self._make_segments_menu_section(menu)
        self._make_directory_menu_section(menu, is_permanent=True)
        self._make_initializer_menu_section(menu, has_initializer=True)
        self._make_metadata_menu_section(menu)
        self._make_metadata_module_menu_section(menu)
        self._make_views_menu_section(menu)
        self._make_views_module_menu_section(menu)
        return menu

    def _make_segments_menu_section(self, menu):
        section = menu.make_command_section(name='segments')
        section.append(('segments - new', 'new'))
        return section

    ### PUBLIC METHODS ###

    def interpret_definition_modules(
        self,
        pending_user_input=None,
        ):
        r'''Makes asset PDFs.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            segment_package_directory_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                )
            manager = self._asset_manager_class(
                path=segment_package_directory_path,
                session=self._session,
                )
            manager.interpret_definition_module(
                prompt=False,
                view_asset_pdf=False,
                )
            output_pdf_file_path = manager._output_pdf_file_path
            if os.path.isfile(output_pdf_file_path):
                message = 'segment {} PDF created.'
                message = message.format(segment_package_name)
                self._io_manager.display(message)
        self._io_manager.display('')
        self._io_manager.proceed()

    def interpret_current_lilypond_files(
        self,
        pending_user_input=None,
        prompt=True,
        view_output_pdfs=True,
        ):
        r'''Reinterprets all current LilyPond files.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            segment_package_directory_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                )
            segment_package_path = \
                self._configuration.path_to_package_path(
                segment_package_directory_path)
            manager = self._asset_manager_class(
                segment_package_path,
                session=self._session,
                )
            manager.interpret_current_lilypond_file(
                prompt=False,
                view_output_pdf=False,
                )
        message = 'press return to view PDF(s).'
        self._io_manager.proceed(message=message, prompt=prompt)
        if view_output_pdfs:
            self.view_segment_pdfs()

    def version_segment_packages(
        self,
        pending_user_input=None,
        ):
        r'''Versions all assets.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            segment_package_directory_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                )
            segment_package_path = \
                self._configuration.path_to_package_path(
                segment_package_directory_path)
            manager = self._asset_manager_class(
                segment_package_path,
                session=self._session,
                )
            version_number = manager.save_to_versions_directory(
                prompt=False,
                )
            if version_number is not None:
                message = 'segment {} version {} written to disk.'
                message = message.format(segment_package_name, version_number)
                self._io_manager.display(message)
        self._io_manager.display('')
        self._io_manager.proceed()

    def view_segment_pdfs(
        self,
        pending_user_input=None,
        ):
        r'''Views all asset PDFs.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self._score_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        output_pdf_file_paths = []
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            if not directory_entry[0].isalpha():
                continue
            segment_package_name = directory_entry
            output_pdf_file_path = os.path.join(
                segments_directory_path,
                segment_package_name,
                'output.pdf',
                )
            if os.path.isfile(output_pdf_file_path):
                output_pdf_file_paths.append(output_pdf_file_path)
        self._io_manager.view(output_pdf_file_paths)
