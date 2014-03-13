# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import getters
from scoremanager import iotools
from scoremanager import wizards
from scoremanager.editors.Editor import Editor


class InstrumentEditor(Editor):
    r'''Instrument editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from editors import TargetManifest
        from scoremanager import editors
        return TargetManifest(
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

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        result = {
            'tprd': self.toggle_pitch_range_display,
        }
        return result

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        else:
            super(InstrumentEditor, self)._handle_main_menu_result(result)

    def _make_pitch_range_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            name='pitch range',
            )
        section.append(('toggle pitch range display', 'tprd'))
        return section
        
    def _make_main_menu(self):
        menu = super(InstrumentEditor, self)._make_main_menu()
        self._make_pitch_range_menu_section(menu)
        return menu

    ### PUBLIC PROPERTIES ###

    @property
    def _target_name(self):
        if self.target is not None:
            return self.target.instrument_name

    ### PUBLIC METHODS ###

    def _initialize_target(self):
        if self.target is None:
            with self._backtracking:
                wizard = wizards.InstrumentCreationWizard(
                    is_ranged=True, 
                    session=self._session)
                instruments = wizard._run()
            if self._session._backtrack():
                return
            if instruments:
                self.target = instruments[0]
            else:
                self.target = None

    def toggle_pitch_range_display(self):
        r'''Toggle pitch range display.

        Between numbered pitches and lettered pitches.

        Returns none.
        '''
        if self._session.display_pitch_ranges_with_numbered_pitches:
            self._session._display_pitch_ranges_with_numbered_pitches = False
        else:
            self._session._display_pitch_ranges_with_numbered_pitches = True
