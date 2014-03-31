# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import getters
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