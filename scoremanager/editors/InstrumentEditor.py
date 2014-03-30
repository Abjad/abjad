# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import getters
from scoremanager import iotools
from scoremanager import wizards
from scoremanager.editors.Editor import Editor


class InstrumentEditor(Editor):
    r'''Instrument editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )
    
    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import editors
        return systemtools.TargetManifest(
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

    def _make_main_menu(self, name='instrument editor'):
        superclass = super(InstrumentEditor, self)
        menu = superclass._make_main_menu(name=name)
        self._make_pitch_range_menu_section(menu)
        return menu

    def _make_pitch_range_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            name='pitch range',
            )
        section.append(('pitch range - toggle display', 'tprd'))
        return section
        
    ### PUBLIC PROPERTIES ###

    @property
    def _target_name(self):
        if self.target is not None:
            return self.target.instrument_name

    ### PUBLIC METHODS ###

    def _initialize_target(self):
        if self.target is None:
            wizard = wizards.InstrumentCreationWizard(
                is_ranged=True, 
                session=self._session,
                )
            instruments = wizard._run()
            if self._should_backtrack():
                return
            if instruments:
                self._target = instruments[0]
            else:
                self._target = None

    def toggle_pitch_range_display(self):
        r'''Toggle pitch range display.

        Between numbered pitches and lettered pitches.

        Returns none.
        '''
        if self._session.display_pitch_ranges_with_numbered_pitches:
            self._session._display_pitch_ranges_with_numbered_pitches = False
        else:
            self._session._display_pitch_ranges_with_numbered_pitches = True