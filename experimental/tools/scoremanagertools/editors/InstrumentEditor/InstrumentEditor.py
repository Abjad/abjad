from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools import wizards
from abjad.tools.instrumenttools.Instrument import Instrument
from abjad.tools import instrumenttools
from experimental.tools.scoremanagertools.editors.ClefMarkInventoryEditor \
    import ClefMarkInventoryEditor
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class InstrumentEditor(InteractiveEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(Instrument,
        ('instrument_name', 'in', getters.get_string),
        ('instrument_name_markup', 'im', getters.get_markup),
        ('short_instrument_name',  'sn', getters.get_string),
        ('short_instrument_name_markup', 'sm', getters.get_markup),
        ('pitch_range', 'range', 'rg', getters.get_symbolic_pitch_range_string),
        ('all_clefs', 'clefs', 'cf', ClefMarkInventoryEditor),
        )

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            super(InstrumentEditor, self)._handle_main_menu_result(result)

    def _make_main_menu(self):
        menu = super(InstrumentEditor, self)._make_main_menu()
        menu.hidden_section.append(
            ('toggle pitch range display', 'tprd'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.instrument_name

    ### PUBLIC METHODS ###

    def initialize_target(self):
        if self.target is None:
            with self.backtracking:
                wizard = wizards.InstrumentCreationWizard(
                    is_ranged=True, 
                    session=self._session)
                instruments = wizard._run()
            if self._session.backtrack():
                return
            if instruments:
                self.target = instruments[0]
            else:
                self.target = None

    def toggle_pitch_range_display(self):
        if self._session.display_pitch_ranges_with_numbered_pitches:
            self._session.display_pitch_ranges_with_numbered_pitches = False
        else:
            self._session.display_pitch_ranges_with_numbered_pitches = True

    ### UI MANIFEST ###

    user_input_to_action = {
        'tprd':     toggle_pitch_range_display,
        }
