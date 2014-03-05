# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class SegmentPackageWrangler(PackageWrangler):
    r'''Segment package wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
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
        self.score_storehouse_path_infix_parts = ('segments',)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'segments'

    @property
    def _user_input_to_action(self):
        superclass = super(SegmentPackageWrangler, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'lyri': self.reinterpret_all_current_lilypond_files,
            'pdfm': self.make_asset_pdfs,
            'pdfs': self.version_all_assets,
            'pdfv': self.view_asset_pdfs,
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            segment_package_manager = self._initialize_asset_manager(result)
            segment_package_manager._run()

    def _list_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad segment package filesystem paths:

        ::

            >>> for x in wrangler._list_asset_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../blue_example_score/segments/segment_01'
            '.../blue_example_score/segments/segment_02'
            '.../red_example_score/segments/segment_01'
            '.../red_example_score/segments/segment_02'
            '.../red_example_score/segments/segment_03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_managers(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        ..  container:: example

            List abjad segment package managers:

            ::

                >>> for x in wrangler._list_asset_managers(
                ...     user_library=False, 
                ...     user_score_packages=False):
                ...     x
                SegmentPackageManager('.../blue_example_score/segments/segment_01')
                SegmentPackageManager('.../blue_example_score/segments/segment_02')
                SegmentPackageManager('.../red_example_score/segments/segment_01')
                SegmentPackageManager('.../red_example_score/segments/segment_02')
                SegmentPackageManager('.../red_example_score/segments/segment_03')

        ..  container:: example

            List red example score segment package managers:

            ::

                >>> head = 'red_example_score'
                >>> for x in wrangler._list_asset_managers(head=head):
                ...     x
                SegmentPackageManager('.../red_example_score/segments/segment_01')
                SegmentPackageManager('.../red_example_score/segments/segment_02')
                SegmentPackageManager('.../red_example_score/segments/segment_03')

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass._list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_names(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        ..  container:: example

            List abjad segment package names:

            ::

                >>> for x in wrangler._list_asset_names(
                ...     user_library=False, 
                ...     user_score_packages=False,
                ...     ):
                ...     x
                'segment 01'
                'segment 02'
                'segment 01'
                'segment 02'
                'segment 03'

        ..  container:: example

            List red example score segment package names:

            ::

                >>> head = 'red_example_score'
                >>> for x in wrangler._list_asset_names(head=head):
                ...     x
                'segment 01'
                'segment 02'
                'segment 03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass._list_asset_names(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad segment package storehouse filesystem paths:

        ::

            >>> for x in wrangler._list_storehouse_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../blue_example_score/segments'
            '.../green_example_score/segments'
            '.../red_example_score/segments'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass._list_storehouse_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

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
        manager.write_segment_definition_module()
        manager.make_versions_directory()
        message = 'segment created: {!r}.'.format(path)
        self._io_manager.proceed(message=message, prompt=prompt)

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries()
        asset_section.menu_entries = asset_menu_entries
        section = menu.make_command_section(
            match_on_display_string=False,
            )
        string = 'all segments - current lilypond file - reinterpret'
        section.append((string, 'lyri'))
        section = menu.make_command_section(
            match_on_display_string=False,
            )
        section.append(('all segments - current pdf - make', 'pdfm'))
        section.append(('all segments - current pdf - version', 'pdfs'))
        section.append(('all segments - current pdf - view', 'pdfv'))
        section = menu.make_command_section()
        section.append(('segments - new', 'new'))
        section = menu.make_command_section(is_secondary=True)
        section.append(('package - list', 'ls'))
        self._io_manager._make_initializer_menu_section(
            menu,
            has_initializer=True,
            )
        self._io_manager._make_metadata_menu_section(menu)
        self._io_manager._make_metadata_module_menu_section(menu)
        self._io_manager._make_views_menu_section(menu)
        self._io_manager._make_views_module_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

    def make_asset_pdfs(
        self,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_storehouse_path_infix_parts
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
            manager.make_asset_pdf(
                view_asset_pdf=False,
                )
            output_pdf_file_path = manager._get_output_pdf_file_path()
            if os.path.isfile(output_pdf_file_path):
                message = 'segment {} PDF created.'
                message = message.format(segment_package_name)
                self._io_manager.display(message)
        self._io_manager.display('')
        self.view_asset_pdfs()
        self._io_manager.proceed()

    def reinterpret_all_current_lilypond_files(
        self,
        pending_user_input=None,
        prompt=True,
        view_output_pdfs=True,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_storehouse_path_infix_parts
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
            manager.reinterpret_current_lilypond_file(
                prompt=False,
                view_output_pdf=False,
                )
        message = 'press return to view PDF(s).'
        self._io_manager.proceed(message=message, prompt=prompt)
        if view_output_pdfs:
            self.view_asset_pdfs()

    def version_all_assets(
        self,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_storehouse_path_infix_parts
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

    def view_asset_pdfs(
        self,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_storehouse_path_infix_parts
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
        command = ' '.join(output_pdf_file_paths)
        command = 'open ' + command
        self._io_manager.spawn_subprocess(command)
