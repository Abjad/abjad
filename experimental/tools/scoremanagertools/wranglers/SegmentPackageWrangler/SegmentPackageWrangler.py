import os
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


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
    
    built_in_external_storehouse_packagesystem_path = None

    storehouse_path_infix_parts = ('music', 'segments')

    user_external_storehouse_packagesystem_path = None

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'segments'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.make_asset_interactively()
        else:
            segment_package_proxy = self._initialize_asset_proxy(result)
            segment_package_proxy._run()

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(where=self._where, is_numbered=True)
        section.tokens = self.list_asset_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new segment'))
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
        return super(type(self), self).storage_format

    ### PUBLIC METHODS ###

    def list_asset_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List asset filesystem paths.

        Example. List built-in segment package filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x

        Return list.
        '''
        return super(type(self), self).list_asset_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def list_asset_packagesystem_paths(self, head=None):
        '''List asset packagesystem paths.

        ::

            >>> for x in wrangler.list_asset_packagesystem_paths():
            ...     x
            'betoerung.music.segments.BetoerungChunk'
            'gebiete.music.segments.segment_01'
            'manos.music.segments.test_chunk'

        .. note:: TODO: supply with four keyword filters.

        Return list.
        '''
        return super(type(self), self).list_asset_packagesystem_paths(head=head)

    def list_storehouse_filesystem_paths(self,
        built_in_external=True, user_external=True,
        built_in_score=True, user_score=True, head=None):
        '''List storehouse filesystem paths.

        Example. List built-in segment package storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_storehouse_filesystem_paths(
            ...     user_external=False, user_score=False):
            ...     x
            '.../tools/scoremanagertools/built_in_scores/blue_example_score/music/segments'
            '.../tools/scoremanagertools/built_in_scores/green_example_score/music/segments'
            '.../tools/scoremanagertools/built_in_scores/red_example_score/music/segments'

        Return list.
        '''
        return super(type(self), self).list_storehouse_filesystem_paths(
            built_in_external=built_in_external,
            user_external=user_external,
            built_in_score=built_in_score,
            user_score=user_score,
            head=head)

    def make_asset_interactively(self):
        segment_package_proxy = SegmentPackageProxy(session=self._session)
        segment_package_proxy.make_asset_interactively()
