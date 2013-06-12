from abjad.tools import instrumenttools
from abjad.tools import scoretools
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.InstrumentCreationWizard \
    import InstrumentCreationWizard
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class PerformerCreationWizard(Wizard):

    ### INITIALIZER ###

    def __init__(self, is_ranged=False, session=None, target=None):
        Wizard.__init__(self, session=session, target=target)
        self.is_ranged = is_ranged

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'performer creation wizard'

    ### PRIVATE METHODS ###

    def _run(self, cache=False, clear=True, head=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        try_again = False
        performers = []
        while True:
            self._session.push_breadcrumb(self._breadcrumb)
            kwargs = {'session': self._session, 'is_ranged': self.is_ranged}
            selector = selectors.ScoreToolsPerformerNameSelector(**kwargs)
            with self.backtracking:
                result = selector._run()
            if self._session.backtrack():
                break
            if isinstance(result, list):
                performer_names = result
            else:
                performer_names = [result]
            performers = []
            for performer_name in performer_names:
                self._session.push_breadcrumb(self._breadcrumb)
                with self.backtracking:
                    performer = scoretools.Performer(performer_name)
                    self.interactively_initialize_performer(performer)
                self._session.pop_breadcrumb()
                was_backtracking_locally = \
                    self._session.is_backtracking_locally
                if self._session.backtrack():
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
                self._session.pop_breadcrumb()
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
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        self.target = final_result
        return self.target

    ### PUBLIC METHODS ###

    def interactively_initialize_performer(self, 
        performer, 
        cache=False, 
        clear=True):
        menu = self.make_performer_configuration_menu(performer)
        while True:
            self._session.push_breadcrumb(performer.name)
            result = menu._run(clear=clear)
            if self._session.backtrack():
                self._session.pop_breadcrumb()
                self._session.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self._session.pop_breadcrumb()
                continue
            if result in ('skip', ['skip']):
                break
            elif result in ('more', ['more']):
                with self.backtracking:
                    wizard = InstrumentCreationWizard(
                        session=self._session, is_ranged=True)
                    instruments = wizard._run()
                if self._session.backtrack():
                    break
                if instruments is not None:
                    for instrument in instruments:
                        performer.instruments.append(instrument)
                break
            elif isinstance(result, list):
                for instrument_name in result:
                    instrument_class = \
                        instrumenttools.default_instrument_name_to_instrument_class(
                        instrument_name)
                    instrument = instrument_class()
                    performer.instruments.append(instrument)
                break
            else:
                raise ValueError("how'd we get here?")
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)

    def make_performer_configuration_menu(self, performer):
        menu, menu_section = self._io.make_menu(
            where=self._where,
            is_numbered=True,
            is_ranged=True,
            #is_modern=True,
            )
        menu_section.title = 'select instruments'
        likely_instruments = \
            performer.likely_instruments_based_on_performer_name
        likely_instrument_names = [
            x().instrument_name for x in likely_instruments]
        most_likely_instrument = \
            performer.most_likely_instrument_based_on_performer_name
        default_index = None
        if most_likely_instrument is not None:
            most_likely_instrument_name = \
                most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(
                most_likely_instrument_name)
            string = '{} (default)'.format(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = string
            most_likely_number = most_likely_index + 1
            default_index = most_likely_index
        if likely_instruments:
            menu_section.menu_tokens = likely_instrument_names
            menu_section.default_index = default_index
            menu_section = menu.make_section(
                return_value_attribute='key',
                is_modern=True,
                )
            menu_section.append(('more instruments', 'more'))
        else:
            menu_tokens = instrumenttools.list_instrument_names()
            menu_section.default_index = default_index
            menu_section = menu.make_section(
                return_value_attribute='key',
                is_modern=True,
                )
        menu_section.append(('skip instruments', 'skip'))
        return menu
