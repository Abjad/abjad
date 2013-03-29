from scf.selectors.DirectoryContentSelector import DirectoryContentSelector
import os


class PackageContentSelector(DirectoryContentSelector):

    ### CLASS ATTRIBUTES ###

    asset_container_package_importable_names = []
    target_human_readable_name = 'item'

    ### PUBLIC METHODS ###

    def list_items(self):
        from scf.proxies.PackageProxy import PackageProxy
        result = []
        for package_importable_name in self.asset_container_package_importable_names:
            package_proxy = PackageProxy(
                package_importable_name=package_importable_name, session=self.session)
            result.extend(package_proxy.public_names)
        return result
