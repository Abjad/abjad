from scf import getters
from scf import selectors
from scf import wizards
from abjad.tools.instrumenttools.Instrument import Instrument
from abjad.tools import instrumenttools
from scf.editors.ClefMarkInventoryEditor import ClefMarkInventoryEditor
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest


class InstrumentEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(Instrument,
        ('instrument_name', 'in', getters.get_string),
        ('instrument_name_markup', 'im', getters.get_markup),
        ('short_instrument_name',  'sn', getters.get_string),
        ('short_instrument_name_markup', 'sm', getters.get_markup),
        ('pitch_range', 'range', 'rg', getters.get_symbolic_pitch_range_string),
        ('all_clefs', 'clefs', 'cf', ClefMarkInventoryEditor),
        is_keyed=True,
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.instrument_name

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is None:
            self.push_backtrack()
            wizard = wizards.InstrumentCreationWizard(is_ranged=True, session=self.session)
            instruments = wizard.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            if instruments:
                self.target = instruments[0]
            else:
                self.target = None

    def handle_main_menu_result(self, result):
        if result == 'tprd':
            if self.session.display_pitch_ranges_with_numbered_pitches:
                self.session.display_pitch_ranges_with_numbered_pitches = False
            else:
                self.session.display_pitch_ranges_with_numbered_pitches = True
        else:
            InteractiveEditor.handle_main_menu_result(self, result)

    def make_main_menu(self):
        menu = InteractiveEditor.make_main_menu(self)
        hidden_section = menu.hidden_section
        hidden_section.append(('tprd', 'toggle pitch range display'))
        return menu
