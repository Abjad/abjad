# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor


class InstrumentEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanagertools import editors
        return self.TargetManifest(
            instrumenttools.Instrument,
            (
                'instrument_name', 
                'instrument name', 
                'in', 
                getters.get_string, 
                False,
                ),
            (
                'instrument_name_markup', 
                'instrument name markup',
                'im', 
                getters.get_markup,
                False,
                ),
            (
                'short_instrument_name', 
                'short instrument name',
                'sn', 
                getters.get_string,
                False,
                ),
            (
                'short_instrument_name_markup', 
                'short instrument name markup',
                'sm', 
                getters.get_markup,
                False,
                ),
            (
                'pitch_range', 
                'pitch range',
                'range', 
                'rg', 
                getters.get_symbolic_pitch_range_string,
                False,
                ),
            (
                'allowable_clefs', 
                'allowable clefs',
                'clefs', 
                'cf', 
                editors.ClefInventoryEditor,
                False,
                ),
            )

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            super(InstrumentEditor, self)._handle_main_menu_result(result)

    def _make_main_menu(self):
        menu = super(InstrumentEditor, self)._make_main_menu()
        pair = ('toggle pitch range display', 'tprd')
        menu.hidden_section.append(pair)
        return menu

    ### PUBLIC PROPERTIES ###

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
                    session=self.session)
                instruments = wizard._run()
            if self.session.backtrack():
                return
            if instruments:
                self.target = instruments[0]
            else:
                self.target = None

    def toggle_pitch_range_display(self):
        if self.session.display_pitch_ranges_with_numbered_pitches:
            self.session.display_pitch_ranges_with_numbered_pitches = False
        else:
            self.session.display_pitch_ranges_with_numbered_pitches = True

    ### UI MANIFEST ###

    user_input_to_action = {
        'tprd':     toggle_pitch_range_display,
        }
