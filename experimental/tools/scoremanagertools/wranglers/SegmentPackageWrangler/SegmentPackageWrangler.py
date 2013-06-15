import os
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import \
    PackageWrangler


class SegmentPackageWrangler(PackageWrangler):
    '''Segment package wrangler.

    ::

        >>> score_manager = scoremanagertools.scoremanager.ScoreManager()
        >>> wrangler = score_manager.segment_package_wrangler
        >>> wrangler
        SegmentPackageWrangler()

    Return segment package wrangler.
    '''

    ### CLASS VARIABLES ###

    asset_storehouse_packagesystem_path_in_built_in_asset_library = None

    score_package_asset_storehouse_path_infix_parts = ('music', 'segments')

    asset_storehouse_packagesystem_path_in_user_asset_library = None

    ### READ-ONLY PRIVATE PROPERTIES ###

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
        menu_entries = self.list_asset_names(head=head)
        menu, menu_section = self._io.make_menu(
            where=self._where,
            menu_entries=menu_entries,
            is_numbered=True,
            )
        menu_section = menu.make_section(return_value_attribute='key')
        menu_section.append(('new segment', 'new'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        '''Segment package wrangler asset proxy class:

        ::

            >>> wrangler.asset_proxy_class.__name__
            'SegmentPackageProxy'

        Return class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.SegmentPackageProxy

    @property
    def storage_format(self):
        '''Segment package wrangler storage format:

        ::

            >>> wrangler.storage_format
            'wranglers.SegmentPackageWrangler()'

        Return string.
        '''
        return super(SegmentPackageWrangler, self).storage_format

    ### PUBLIC METHODS ###

    def interactively_make_asset(self):
        segment_package_proxy = self.asset_proxy_class(session=self._session)
        segment_package_proxy.interactively_make_asset()

    def list_asset_filesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset filesystem paths.

        Example. List built-in segment package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/scorepackages/blue_example_score/music/segments/segment_01.py'
            '.../tools/scoremanagertools/scorepackages/blue_example_score/music/segments/segment_02.py'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_01.py'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_02.py'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_03.py'

        Return list.
        '''
        return super(SegmentPackageWrangler, self).list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_names(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset names.

        Example. List built-in segment package names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
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

        Return list.
        '''
        return super(SegmentPackageWrangler, self).list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_packagesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset packagesystem paths.

        Example. List built-in segment package paths:

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            'experimental.tools.scoremanagertools.scorepackages.blue_example_score.music.segments.segment_01'
            'experimental.tools.scoremanagertools.scorepackages.blue_example_score.music.segments.segment_02'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments.segment_01'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments.segment_02'
            'experimental.tools.scoremanagertools.scorepackages.red_example_score.music.segments.segment_03'

        Return list.
        '''
        return super(SegmentPackageWrangler, self).list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_proxies(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None):
        '''List asset proxies.

        Example. List built-in segment package proxies:

        ::

            >>> for x in wrangler.list_asset_proxies(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/blue_example_score/music/segments/segment_01')
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/blue_example_score/music/segments/segment_02')
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_01')
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_02')
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_03')

        Example 2. List red example score segment package proxies:

            >>> head = 'experimental.tools.scoremanagertools.scorepackages.red_example_score'
            >>> for x in wrangler.list_asset_proxies(head=head):
            ...     x
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_01')
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_02')
            SegmentPackageProxy('.../tools/scoremanagertools/scorepackages/red_example_score/music/segments/segment_03')

        Return list.
        '''
        return super(SegmentPackageWrangler, self).list_asset_proxies(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head)

    def list_asset_storehouse_filesystem_paths(self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True):
        '''List asset storehouse filesystem paths.

        Example. List built-in segment package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False):
            ...     x
            '.../tools/scoremanagertools/scorepackages/blue_example_score/music/segments'
            '.../tools/scoremanagertools/scorepackages/green_example_score/music/segments'
            '.../tools/scoremanagertools/scorepackages/red_example_score/music/segments'

        Return list.
        '''
        return super(SegmentPackageWrangler, self).list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages)

    ### UI MANIFEST ###

    user_input_to_action = PackageWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'new': interactively_make_asset,
        })
