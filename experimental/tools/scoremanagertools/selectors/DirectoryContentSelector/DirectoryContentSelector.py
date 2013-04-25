from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class DirectoryContentSelector(Selector):

    ### CLASS ATTRIBUTES ###

    asset_container_paths = []
    target_human_readable_name = 'file'

    ### PUBLIC METHODS ###

    def list_items(self):
        from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy
        result = []
        for path in self.asset_container_paths:
            directory_proxy = DirectoryProxy(path=path, session=self.session)
            result.extend(directory_proxy.public_content_short_names)
            if hasattr(self, 'forbidden_names'):
                for forbidden_name in self.forbidden_names:
                    if forbidden_name in result:
                        result.remove(forbidden_name)
        return result
