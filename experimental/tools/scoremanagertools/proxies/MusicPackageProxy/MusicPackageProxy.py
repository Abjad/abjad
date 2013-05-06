from experimental.tools.scoremanagertools.proxies.PackageProxy import PackageProxy


class MusicPackageProxy(PackageProxy):

    def __init__(self, score_package_name=None, session=None):
        package_path = '{}.music'.format(score_package_name)
        PackageProxy.__init__(self, package_path=package_path, session=session)
