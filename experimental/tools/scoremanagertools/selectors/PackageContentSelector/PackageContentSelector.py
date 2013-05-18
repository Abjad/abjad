from experimental.tools.scoremanagertools.selectors.DirectoryContentSelector import DirectoryContentSelector
import os


class PackageContentSelector(DirectoryContentSelector):

    ### CLASS ATTRIBUTES ###

    storehouse_package_paths = []
    space_delimited_lowercase_target_name = 'item'

    ### PUBLIC METHODS ###

    def list_items(self):
        from experimental.tools.scoremanagertools.proxies.PackageProxy import PackageProxy
        result = []
        for package_path in self.storehouse_package_paths:
            package_proxy = PackageProxy(
                packagesystem_path=package_path, session=self._session)
            result.extend(package_proxy.public_names)
        return result
