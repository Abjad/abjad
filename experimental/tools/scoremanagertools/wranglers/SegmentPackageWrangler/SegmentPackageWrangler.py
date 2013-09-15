# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import iotools
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import \
    PackageWrangler


class SegmentPackageWrangler(PackageWrangler):
    r'''Segment package wrangler.

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.segment_package_wrangler
        >>> wrangler
        SegmentPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    asset_storehouse_packagesystem_path_in_built_in_asset_library = None

    score_package_asset_storehouse_path_infix_parts = ('music', 'segments')

    asset_storehouse_packagesystem_path_in_user_asset_library = None

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'segments'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            segment_package_proxy = self._initialize_asset_proxy(result)
            segment_package_proxy._run()

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = main_menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        asset_section.menu_entries = asset_menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('new segment', 'new'))
        command_section = main_menu.make_command_section()
        command_section.append(('view segment pdfs', 'pdfv'))
        command_section.append(('write segment pdfs', 'pdfw'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        r'''Asset proxy class of segment package wrangler.

        ::

            >>> wrangler.asset_proxy_class.__name__
            'SegmentPackageProxy'

        Returns class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.SegmentPackageProxy

    @property
    def storage_format(self):
        r'''Storage format of segment package wrangler.

        ::

            >>> wrangler.storage_format
            'wranglers.SegmentPackageWrangler()'

        Returns string.
        '''
        return super(SegmentPackageWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def interactively_view_asset_pdfs(
        self,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        parts = (self.session.current_score_directory_path,)
        parts += self.score_package_asset_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)
        pdf_file_paths = []
        for directory_entry in os.listdir(segments_directory_path):
            if not directory_entry[0].isalpha():
                continue
            history_directory_path = os.path.join(
                segments_directory_path,
                directory_entry,
                'history',
                )
            if not os.path.isdir(history_directory_path):
                continue
            last_output_file_name = \
                iotools.get_last_output_file_name(history_directory_path)
            if last_output_file_name is None:
                continue
            result = os.path.splitext(last_output_file_name)
            last_output_file_name_root, extension = result
            last_output_pdf_name = last_output_file_name_root + '.pdf'
            last_output_pdf_file_path = os.path.join(
                history_directory_path,
                last_output_pdf_name,
                )
            if not os.path.isfile(last_output_pdf_file_path):
                continue
            pdf_file_paths.append(last_output_pdf_file_path)
        if not pdf_file_paths:
            message = 'no PDFs to view.'
            self.session.io_manager.proceed(message)
        command = ' '.join(pdf_file_paths)
        command = 'open ' + command
        iotools.spawn_subprocess(command)

    def interactively_write_asset_pdfs(
        self,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        parts = (self.session.current_score_directory_path,)
        parts += self.score_package_asset_storehouse_path_infix_parts
        segments_directory_path = os.path.join(*parts)


    def list_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Example. List built-in segment package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            '.../blue_example_score/music/segments/segment_01'
            '.../blue_example_score/music/segments/segment_02'
            '.../red_example_score/music/segments/segment_01'
            '.../red_example_score/music/segments/segment_02'
            '.../red_example_score/music/segments/segment_03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_names(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Example 1. List built-in segment package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            'segment 01'
            'segment 02'
            'segment 01'
            'segment 02'
            'segment 03'

        Example 2. List red example score segment package names:

            >>> head = 'experimental.tools.scoremanagertools.scorepackages.red_example_score'
            >>> for x in wrangler.list_asset_names(head=head):
            ...     x
            'segment 01'
            'segment 02'
            'segment 03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Example. List built-in segment package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '....blue_example_score.music.segments.segment_01'
            '....blue_example_score.music.segments.segment_02'
            '....red_example_score.music.segments.segment_01'
            '....red_example_score.music.segments.segment_02'
            '....red_example_score.music.segments.segment_03'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_proxies(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset proxies.

        Example 1. List built-in segment package proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            SegmentPackageProxy('.../blue_example_score/music/segments/segment_01')
            SegmentPackageProxy('.../blue_example_score/music/segments/segment_02')
            SegmentPackageProxy('.../red_example_score/music/segments/segment_01')
            SegmentPackageProxy('.../red_example_score/music/segments/segment_02')
            SegmentPackageProxy('.../red_example_score/music/segments/segment_03')

        Example 2. List red example score segment package proxies:

        ::

            >>> head = 'experimental.tools.scoremanagertools.scorepackages.red_example_score'
            >>> for x in wrangler.list_asset_proxies(head=head):
            ...     x
            SegmentPackageProxy('.../red_example_score/music/segments/segment_01')
            SegmentPackageProxy('.../red_example_score/music/segments/segment_02')
            SegmentPackageProxy('.../red_example_score/music/segments/segment_03')

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_storehouse_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Example. List built-in segment package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            '.../blue_example_score/music/segments'
            '.../green_example_score/music/segments'
            '.../red_example_score/music/segments'

        Returns list.
        '''
        superclass = super(SegmentPackageWrangler, self)
        return superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    def make_asset(
        self, 
        package_path, 
        is_interactive=False, 
        tags=None,
        ):
        r'''Makes package.

        Returns none.
        '''
        tags = collections.OrderedDict(tags or {})
        directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        proxy = self.asset_proxy_class(
            packagesystem_path=package_path,
            session=self.session,
            )
        proxy.write_initializer_to_disk()
        proxy.write_segment_definition_module_to_disk()
        proxy.make_history_directory()
        line = 'package {!r} created.'.format(package_path)
        self.session.io_manager.proceed(line, is_interactive=is_interactive)

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'pdfv': interactively_view_asset_pdfs,
        'pdfw': interactively_write_asset_pdfs,
        })
