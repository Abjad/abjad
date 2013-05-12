import os
from experimental.tools.scoremanagertools.proxies.SegmentPackageProxy import SegmentPackageProxy
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class SegmentPackageWrangler(PackageWrangler):

    ### CLASS ATTRIBUTES ###
    
    asset_container_path_infix_parts = ('music', 'segments')

    ### INITIALIZER ###

    def __init__(self, session=None):
        PackageWrangler.__init__(self,
            built_in_asset_container_package_paths= [self.configuration.user_sketches_package_path],
            session=session)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'segments'
        else:
            return 'sketches'

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.make_asset_interactively()
        else:
            segment_package_proxy = self._get_asset_proxy(result)
            segment_package_proxy._run()

    def _make_main_menu(self, head=None):
        menu, section = self._io.make_menu(where=self._where, is_numbered=True)
        section.tokens = self.list_space_delimited_lowercase_visible_asset_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new segment'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        return SegmentPackageProxy

    ### PUBLIC METHODS ###

    def make_asset_interactively(self):
        segment_package_proxy = SegmentPackageProxy(session=self._session)
        segment_package_proxy.make_asset_interactively()
