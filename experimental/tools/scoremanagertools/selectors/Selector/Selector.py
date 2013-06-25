import os
from experimental.tools.scoremanagertools.scoremanager.ScoreManagerObject \
    import ScoreManagerObject


class Selector(ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, 
        is_numbered=True,
        is_ranged=False, 
        items=None, 
        session=None):
        ScoreManagerObject.__init__(self, session=session)
        self.is_numbered = is_numbered
        self.is_ranged = is_ranged
        self.items = items or []

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if getattr(self, 'explicit_breadcrumb', None):
            return self.explicit_breadcrumb
        elif hasattr(self, 'space_delimited_lowercase_target_name'):
            return 'select {}:'.format(
                self.space_delimited_lowercase_target_name)
        else:
            return 'select:'

    ### PRIVATE METHODS ###

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        menu_section = main_menu._make_section(
            return_value_attribute='explicit',
            is_numbered=self.is_numbered,
            is_ranged=self.is_ranged,
            )
        menu_entries = self.make_menu_entries(head=head)
        menu_section.menu_entries = menu_entries
        return main_menu

    def _run(self, 
        cache=False, clear=True, head=None, pending_user_input=None):
        self.session.io_manager.assign_user_input(pending_user_input=pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu(head=head)
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            else:
                break
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        return result

    ### PUBLIC PROPERTIES ###

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

    def change_expr_to_menu_entry(self, expr):
        return (self.session.io_manager.get_one_line_menuing_summary(expr), None, None, expr)

    def get_tag_from_directory_path(self, directory_path, tag_name):
        tags_file_name = os.path.join(directory_path, 'tags.py')
        if os.path.isfile(tags_file_name):
            tags_file = open(tags_file_name, 'r')
            tags_file_string = tags_file.read()
            tags_file.close()
            exec(tags_file_string)
            result = locals().get('tags') or OrderedDict([])
            return result.get(tag_name)

    def list_items(self):
        result = []
        return result

    def make_menu_entries(self, head=None):
        return [self.change_expr_to_menu_entry(item) for item in self.items]
