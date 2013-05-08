import os
from experimental.tools.scoremanagertools.proxies.SegmentPackageProxy import SegmentPackageProxy
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class SegmentPackageWrangler(PackageWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
        PackageWrangler.__init__(self,
            system_asset_container_package_paths= \
                [self.configuration.user_sketches_package_path],
            score_internal_asset_container_package_path_infix= \
                self.configuration._score_internal_segments_package_path_infix,
            session=session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return SegmentPackageProxy

    @property
    def breadcrumb(self):
        if self.session.is_in_score:
            return 'segments'
        else:
            return 'sketches'

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.make_asset_interactively()
        else:
            segment_package_proxy = self.get_asset_proxy(result)
            segment_package_proxy.run()

    def make_asset_interactively(self):
        segment_package_proxy = SegmentPackageProxy(session=self.session)
        segment_package_proxy.make_asset_interactively()

    def make_main_menu(self, head=None):
        menu, section = self.io.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_asset_space_delimited_lowercase_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new segment'))
        return menu
