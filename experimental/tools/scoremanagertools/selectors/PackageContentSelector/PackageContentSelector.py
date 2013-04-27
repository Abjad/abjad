from experimental.tools.scoremanagertools.selectors.DirectoryContentSelector import DirectoryContentSelector
import os


class PackageContentSelector(DirectoryContentSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_paths = []
    target_human_readable_name = 'item'

    ### PUBLIC METHODS ###

    def list_items(self):
        from experimental.tools.scoremanagertools.proxies.PackageProxy import PackageProxy
        result = []
        for package_path in self.asset_container_package_paths:
            package_proxy = PackageProxy(
                package_path=package_path, session=self.session)
            result.extend(package_proxy.public_names)
        return result
