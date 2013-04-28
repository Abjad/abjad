from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.PackageProxy import PackageProxy


class ChunkPackageProxy(PackageProxy):

    ### INITIALIZER ###

    def __init__(self, package_path=None, score_template=None, session=None):
        PackageProxy.__init__(self, package_path=package_path, session=session)
        self.score_template = score_template

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return self.human_readable_name

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def score_template():
        def fget(self):
            return self._score_template
        def fset(self, score_template):
            from abjad.tools import scoretools
            assert isinstance(score_template, (scoretools.Score, type(None)))
            self._score_template = score_template
        return property(**locals())

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.remove()
            return False
        elif result == 'n':
            self.initializer_file_proxy.view()

    def make_asset(self):
        self.print_not_yet_implemented()

    def make_asset_interactively(self, prompt=True):
        self.print_not_yet_implemented()

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where())
        section.append(('n', 'initializer'))
        section = menu.make_section()
        section.append(('d', 'delete'))
        return menu

    def set_score_template_interactively(self):
        self.print_not_yet_implemented()
