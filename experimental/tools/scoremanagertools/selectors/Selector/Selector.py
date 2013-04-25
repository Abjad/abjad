from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject


class Selector(ScoreManagerObject):

    def __init__(self, is_keyed=False, is_numbered=False,
        is_parenthetically_numbered=True, is_ranged=False, items=None, session=None):
        ScoreManagerObject.__init__(self, session=session)
        self.is_keyed = is_keyed
        self.is_numbered = is_numbered
        self.is_parenthetically_numbered = is_parenthetically_numbered
        self.is_ranged = is_ranged
        self.items = items or []

    ### READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        if getattr(self, 'explicit_breadcrumb', None):
            return self.explicit_breadcrumb
        elif hasattr(self, 'target_human_readable_name'):
            return 'select {}:'.format(self.target_human_readable_name)
        else:
            return 'select:'

    ### READ / WRITE PROPERTIES ###

    @apply
    def items():
        def fget(self):
            if self._items:
                return self._items
            else:
                return self.list_items()
        def fset(self, items):
            self._items = items
        return property(**locals())

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        return result

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(),
            is_keyed=self.is_keyed,
            is_numbered=self.is_numbered,
            is_parenthetically_numbered=self.is_parenthetically_numbered,
            is_ranged=self.is_ranged,
            )
        section.tokens = self.make_menu_tokens(head=head)
        section.return_value_attribute = 'prepopulated'
        return menu

    def make_menu_tokens(self, head=None):
        return [self.change_expr_to_menu_token(item) for item in self.items]

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result
