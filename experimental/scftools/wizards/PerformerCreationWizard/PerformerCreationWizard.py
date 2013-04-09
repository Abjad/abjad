from abjad.tools import instrumenttools
from abjad.tools import scoretools
from scftools import selectors
from scftools.wizards.InstrumentCreationWizard import InstrumentCreationWizard
from scftools.wizards.Wizard import Wizard


class PerformerCreationWizard(Wizard):

    def __init__(self, is_ranged=False, session=None, target=None):
        Wizard.__init__(self, session=session, target=target)
        self.is_ranged = is_ranged

    ### READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'instrument creation wizard'

    ### PUBLIC METHODS ###

    def initialize_performer_interactively(self, performer, cache=False, clear=True):
        menu = self.make_performer_configuration_menu(performer)
        while True:
            self.push_breadcrumb(performer.name)
            result = menu.run(clear=clear)
            if self.backtrack():
                self.pop_breadcrumb()
                self.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.pop_breadcrumb()
                continue
            if result in ('skip', ['skip']):
                break
            elif result in ('more', ['more']):
                self.push_backtrack()
                wizard = InstrumentCreationWizard(session=self.session, is_ranged=True)
                instruments = wizard.run()
                self.pop_backtrack()
                if self.backtrack():
                    break
                if instruments is not None:
                    for instrument in instruments:
                        performer.instruments.append(instrument)
                break
            elif isinstance(result, list):
                for instrument_name in result:
                    instrument_class = instrumenttools.default_instrument_name_to_instrument_class(
                        instrument_name)
                    instrument = instrument_class()
                    performer.instruments.append(instrument)
                break
            else:
                raise ValueError("how'd we get here?")
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def make_performer_configuration_menu(self, performer):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True, is_ranged=True)
        section.title = 'select instruments'
        likely_instruments = performer.likely_instruments_based_on_performer_name
        likely_instrument_names = [x().instrument_name for x in likely_instruments]
        most_likely_instrument = performer.most_likely_instrument_based_on_performer_name
        default_index = None
        if most_likely_instrument is not None:
            most_likely_instrument_name = most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = '{} (default)'.format(most_likely_instrument_name)
            most_likely_number = most_likely_index + 1
            default_index = most_likely_index
        if likely_instruments:
            section.tokens = likely_instrument_names
            section.default_index = default_index
            section = menu.make_section(is_keyed=False)
            section.append(('more', 'more instruments'))
        else:
            section.tokens = instrumenttools.list_instrument_names()
            section.default_index = default_index
            section = menu.make_section(is_keyed=False)
        section.append(('skip', 'skip instruments'))
        return menu

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        try_again = False
        performers = []
        while True:
            self.push_breadcrumb()
            kwargs = {'session': self.session, 'is_ranged': self.is_ranged}
            selector = selectors.ScoreToolsPerformerNameSelector(**kwargs)
            self.push_backtrack()
            result = selector.run()
            self.pop_backtrack()
            if self.backtrack():
                break
            if isinstance(result, list):
                performer_names = result
            else:
                performer_names = [result]
            performers = []
            for performer_name in performer_names:
                self.push_breadcrumb()
                self.push_backtrack()
                performer = scoretools.Performer(performer_name)
                self.initialize_performer_interactively(performer)
                self.pop_backtrack()
                self.pop_breadcrumb()
                was_backtracking_locally = self.session.is_backtracking_locally
                if self.backtrack():
                    if was_backtracking_locally:
                        try_again = True
                    else:
                        try_again = False
                        performers = []
                    break
                performers.append(performer)
            if not try_again:
                break
            else:
                try_again = False
                self.pop_breadcrumb()
        if self.is_ranged and performers:
            final_result = performers[:]
        elif self.is_ranged and not performers:
            final_result = []
        elif not self.is_ranged and performers:
            final_result = performers[0]
        elif not self.is_ranged and not performers:
            final_result = None
        else:
            raise ValueError
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        self.target = final_result
        return self.target
