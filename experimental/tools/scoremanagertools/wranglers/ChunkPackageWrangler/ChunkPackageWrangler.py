import os
from experimental.tools.scoremanagertools.proxies.ChunkPackageProxy import ChunkPackageProxy
from experimental.tools.scoremanagertools.wranglers.PackageWrangler import PackageWrangler


class ChunkPackageWrangler(PackageWrangler):

    ### INITIALIZER ###

    def __init__(self, session=None):
#        PackageWrangler.__init__(self,
#            score_external_asset_container_importable_names= \
#                [self.configuration.score_external_chunks_package_importable_name],
#            score_internal_asset_container_importable_name_infix= \
#                self.configuration.score_internal_chunks_package_importable_name_infix,
#            session=session)
        PackageWrangler.__init__(self, session=session)
        self._score_external_asset_container_importable_names = [
            self.configuration.score_external_chunks_package_importable_name]
        self._score_internal_asset_container_importable_name_infix = \
            self.configuration.score_internal_chunks_package_importable_name_infix

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return ChunkPackageProxy

    @property
    def breadcrumb(self):
        if self.session.is_in_score:
            return 'chunks'
        else:
            return 'sketches'

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'new':
            self.make_asset_interactively()
        else:
            chunk_package_proxy = self.get_asset_proxy(result)
            chunk_package_proxy.run()

    def make_asset_interactively(self):
        chunk_package_proxy = ChunkPackageProxy(session=self.session)
        chunk_package_proxy.make_asset_interactively()

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_asset_human_readable_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new chunk'))
        return menu
