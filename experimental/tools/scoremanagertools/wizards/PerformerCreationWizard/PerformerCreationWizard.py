# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from experimental.tools.scoremanagertools import io
from experimental.tools.scoremanagertools.wizards.InstrumentCreationWizard \
    import InstrumentCreationWizard
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class PerformerCreationWizard(Wizard):

    ### INITIALIZER ###

    def __init__(self, is_ranged=False, session=None, target=None):
        Wizard.__init__(self, session=session, target=target)
        self.is_ranged = is_ranged

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'performer creation wizard'

    ### PRIVATE METHODS ###

    def _run(
        self, 
        cache=False, 
        clear=True, 
        head=None, 
        pending_user_input=None,
        ):
        from experimental.tools.scoremanagertools.io import Selector
        self.session.io_manager.assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        try_again = False
        performers = []
        while True:
            self.session.push_breadcrumb(self._breadcrumb)
            selector = Selector.make_score_tools_performer_name_selector(
                session=self.session,
                )
            selector.is_ranged=self.is_ranged
            with self.backtracking:
                result = selector._run()
            if self.session.backtrack():
                break
            if isinstance(result, list):
                performer_names = result
            else:
                performer_names = [result]
            performers = []
            for performer_name in performer_names:
                self.session.push_breadcrumb(self._breadcrumb)
                with self.backtracking:
                    performer = scoretools.Performer(performer_name)
                    self.interactively_initialize_performer(performer)
                self.session.pop_breadcrumb()
                was_backtracking_locally = \
                    self.session.is_backtracking_locally
                if self.session.backtrack():
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
                self.session.pop_breadcrumb()
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
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        self.target = final_result
        return self.target

    ### PUBLIC METHODS ###

    def interactively_initialize_performer(
        self, 
        performer, 
        cache=False, 
        clear=True,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(pending_user_input)
        menu = self.make_performer_configuration_menu(performer)
        while True:
            self.session.push_breadcrumb(performer.name)
            result = menu._run(clear=clear)
            if self.session.backtrack():
                self.session.pop_breadcrumb()
                self.session.restore_breadcrumbs(cache=cache)
                return
            elif not result:
                self.session.pop_breadcrumb()
                continue
            if result in ('skip', ['skip']):
                break
            elif result in ('more', ['more']):
                with self.backtracking:
                    wizard = InstrumentCreationWizard(
                        session=self.session, is_ranged=True)
                    instruments = wizard._run()
                if self.session.backtrack():
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
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def make_performer_configuration_menu(self, performer):
        menu = self.session.io_manager.make_menu(where=self._where)
        numbered_list_section = menu.make_numbered_list_section()
        numbered_list_section.title = 'select instruments'
        command_section = menu.make_command_section()
        likely_instruments = \
            performer.likely_instruments_based_on_performer_name
        likely_instrument_names = [
            x().instrument_name for x in likely_instruments]
        likely_instrument_names.sort()
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
            numbered_list_section.menu_entries = likely_instrument_names
            command_section.append(('more instruments', 'more'))
        else:
            instrument_names = \
                instrumenttools.Instrument.list_instrument_names()
            numbered_list_section.menu_entries = instrument_names
        numbered_list_section.default_index = default_index
        command_section.append(('skip instruments', 'skip'))
        return menu
