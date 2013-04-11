from experimental.tools.scftools.proxies.PackageProxy import PackageProxy


class MusPackageProxy(PackageProxy):

    def __init__(self, score_package_short_name=None, session=None):
        package_importable_name = '{}.mus'.format(score_package_short_name)
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
