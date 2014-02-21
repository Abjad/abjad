# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class SegmentPackageWrangler(PackageWrangler):
    r'''Segment package wrangler.

    ::

        >>> score_manager = scoremanager.core.ScoreManager()
        >>> wrangler = score_manager._segment_package_wrangler
        >>> wrangler
        SegmentPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    storehouse_packagesystem_path_in_built_in_library = None

    score_package_storehouse_path_infix_parts = ('segments',)

    storehouse_packagesystem_path_in_user_library = None

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(SegmentPackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.SegmentPackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'segments'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif result == 'user entered lone return':
            pass
        else:
            segment_package_manager = self._initialize_asset_manager(result)
            segment_package_manager._run()

    def _make_main_menu(self, head=None):
        main_menu = self._session.io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section(
            match_on_display_string=False,
            )
        string = 'all segments - current lilypond file - reinterpret'
        command_section.append((string, 'lyri'))
        command_section = main_menu.make_command_section(
            match_on_display_string=False,
            )
        string = 'all segments - current pdf - make'
        command_section.append((string, 'pdfm'))
        string = 'all segments - current pdf - version'
        command_section.append((string, 'pdfs'))
        string = 'all segments - current pdf - view'
        command_section.append((string, 'pdfv'))
        command_section = main_menu.make_command_section()
        command_section.append(('new segment', 'new'))
        hidden_section = main_menu.make_command_section(is_secondary=True)
        hidden_section.append(('list', 'ls'))
        self._session.io_manager._make_initializer_menu_section(
            main_menu,
            has_initializer=True,
            )
        self._session.io_manager._make_metadata_menu_section(main_menu)
        self._session.io_manager._make_metadata_module_menu_section(main_menu)
        self._session.io_manager._make_views_menu_section(main_menu)
        self._session.io_manager._make_views_module_menu_section(main_menu)
        return main_menu

    ### PUBLIC METHODS ###

    def interactively_make_asset_pdfs(
        self,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_package_storehouse_path_infix_parts
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
                self.configuration.filesystem_path_to_packagesystem_path(
                segment_package_directory_path)
            manager = self._asset_manager_class(
                segment_package_path,
                session=self._session,
                )
            manager.interactively_make_asset_pdf(
                view_asset_pdf=False,
                )
            output_pdf_file_path = manager._get_output_pdf_file_path()
            if os.path.isfile(output_pdf_file_path):
                message = 'segment {} PDF created.'
                message = message.format(segment_package_name)
                self._session.io_manager.display(message)
        self._session.io_manager.display('')
        self.interactively_view_asset_pdfs()
        self._session.io_manager.proceed()

    def interactively_reinterpret_all_current_lilypond_files(
        self,
        pending_user_input=None,
        prompt=True,
        view_output_pdfs=True,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_package_storehouse_path_infix_parts
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
                self.configuration.filesystem_path_to_packagesystem_path(
                segment_package_directory_path)
            manager = self._asset_manager_class(
                segment_package_path,
                session=self._session,
                )
            manager.interactively_reinterpret_current_lilypond_file(
                prompt=False,
                view_output_pdf=False,
                )
        message = 'press return to view PDF(s).'
        self._session.io_manager.proceed(message=message, prompt=prompt)
        if view_output_pdfs:
            self.interactively_view_asset_pdfs()

    def interactively_version_all_assets(
        self,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_package_storehouse_path_infix_parts
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
                self.configuration.filesystem_path_to_packagesystem_path(
                segment_package_directory_path)
            manager = self._asset_manager_class(
                segment_package_path,
                session=self._session,
                )
            version_number = manager.interactively_save_to_versions_directory(
                prompt=False,
                )
            if version_number is not None:
                message = 'segment {} version {} written to disk.'
                message = message.format(segment_package_name, version_number)
                self._session.io_manager.display(message)
        self._session.io_manager.display('')
        self._session.io_manager.proceed()

    def interactively_view_asset_pdfs(
        self,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        parts = (self._session.current_score_directory_path,)
        parts += self.score_package_storehouse_path_infix_parts
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
        self._session.io_manager.spawn_subprocess(command)

    def list_asset_filesystem_paths(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Example. List built-in segment package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_library=False, 
            ...     in_user_score_packages=False,
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
        return superclass.list_asset_filesystem_paths(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_managers(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Example 1. List built-in segment package managers:

        ::

            >>> for x in wrangler.list_asset_managers(
            ...     in_user_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            SegmentPackageManager('.../blue_example_score/segments/segment_01')
            SegmentPackageManager('.../blue_example_score/segments/segment_02')
            SegmentPackageManager('.../red_example_score/segments/segment_01')
            SegmentPackageManager('.../red_example_score/segments/segment_02')
            SegmentPackageManager('.../red_example_score/segments/segment_03')

        Example 2. List red example score segment package managers:

        ::

            >>> head = 'scoremanager.scorepackages.red_example_score'
            >>> for x in wrangler.list_asset_managers(head=head):
            ...     x
            SegmentPackageManager('.../red_example_score/segments/segment_01')
            SegmentPackageManager('.../red_example_score/segments/segment_02')
            SegmentPackageManager('.../red_example_score/segments/segment_03')

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_managers(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_names(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Example 1. List built-in segment package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            'segment 01'
            'segment 02'
            'segment 01'
            'segment 02'
            'segment 03'

        Example 2. List red example score segment package names:

            >>> head = 'scoremanager.scorepackages.red_example_score'
            >>> for x in wrangler.list_asset_names(head=head):
            ...     x
            'segment 01'
            'segment 02'
            'segment 03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_names(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_packagesystem_paths(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Example. List built-in segment package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '....blue_example_score.segments.segment_01'
            '....blue_example_score.segments.segment_02'
            '....red_example_score.segments.segment_01'
            '....red_example_score.segments.segment_02'
            '....red_example_score.segments.segment_03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_packagesystem_paths(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_storehouse_filesystem_paths(
        self,
        in_built_in_library=True, 
        in_user_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Example. List built-in segment package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     in_user_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            '.../blue_example_score/segments'
            '.../green_example_score/segments'
            '.../red_example_score/segments'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_storehouse_filesystem_paths(
            in_built_in_library=in_built_in_library,
            in_user_library=in_user_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    def make_asset(
        self, 
        package_path, 
        prompt=False, 
        metadata=None,
        ):
        r'''Makes package.

        Returns none.
        '''
        metadata = collections.OrderedDict(metadata or {})
        directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        manager = self._asset_manager_class(
            packagesystem_path=package_path,
            session=self._session,
            )
        manager.write_initializer()
        manager.write_segment_definition_module()
        manager.make_versions_directory()
        message = 'package {!r} created.'.format(package_path)
        self._session.io_manager.proceed(message=message, prompt=prompt)

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'lyri': interactively_reinterpret_all_current_lilypond_files,
        'pdfm': interactively_make_asset_pdfs,
        'pdfs': interactively_version_all_assets,
        'pdfv': interactively_view_asset_pdfs,
        })
