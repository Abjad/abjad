from experimental.tools.scoremanagertools.proxies.PackageProxy import PackageProxy


class MusPackageProxy(PackageProxy):

    def __init__(self, score_package_short_name=None, session=None):
        package_path = '{}.mus'.format(score_package_short_name)
        PackageProxy.__init__(self, package_path=package_path, session=session)
