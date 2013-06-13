from abjad.tools import iotools
from experimental.tools.scoremanagertools.proxies.PackageProxy \
    import PackageProxy


class SegmentPackageProxy(PackageProxy):

    ### INITIALIZER ###

    def __init__(self, 
        packagesystem_path=None, score_template=None, session=None):
        PackageProxy.__init__(self, 
            packagesystem_path=packagesystem_path, 
            session=session)
        self.score_template = score_template

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)

    def _make_main_menu(self):
        menu, menu_section = self._io.make_menu(
            where=self._where,
            return_value_attribute='key',
            menu_tokens=menu_tokens,
            )
        menu_section.append(('initializer', 'n'))
        menu_section = menu.make_section(
            menu_tokens=menu_tokens,
            return_value_attribute='key',
            )
        menu_section.append(('remove', 'rm'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._space_delimited_lowercase_name

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

    def interactively_make_asset(self, prompt=True):
        self._io.print_not_yet_implemented()

    def interactively_set_score_template(self):
        self._io.print_not_yet_implemented()

    def make_asset(self):
        self._io.print_not_yet_implemented()

    def remove_segment_package(self):
        self.remove()
        return False

    ### UI MANIFEST ###

    user_input_to_action = PackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'd': remove_segment_package,
        })
