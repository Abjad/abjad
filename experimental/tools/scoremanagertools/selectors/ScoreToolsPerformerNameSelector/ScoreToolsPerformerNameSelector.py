from abjad.tools import scoretools
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ScoreToolsPerformerNameSelector(Selector):

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'performer'

    ### INITIALIZER ###

    def __init__(self, is_keyed=True, **kwargs):
        Selector.__init__(self, **kwargs)
        self.is_keyed = is_keyed

    ### PUBLIC METHODS ###

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(),
            is_keyed=self.is_keyed,
            is_numbered=self.is_numbered,
            is_parenthetically_numbered=self.is_parenthetically_numbered,
            is_ranged=self.is_ranged,
            )
        section.tokens = self.make_menu_tokens(head=head)
        section.return_value_attribute = 'body'
        return menu

    def make_menu_tokens(self, head=None):
        performer_names, performer_abbreviations = [], []
        performer_pairs = scoretools.list_primary_performer_names()
        performer_pairs = [(x[1].split()[-1].strip('.'), x[0]) for x in performer_pairs]
        performer_pairs.append(('perc', 'percussionist'))
        performer_pairs.sort(lambda x, y: cmp(x[1], y[1]))
        return performer_pairs
