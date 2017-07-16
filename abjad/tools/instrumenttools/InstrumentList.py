# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.topleveltools import new


class InstrumentList(TypedList):
    r'''Instrument list.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> instruments = abjad.instrumenttools.InstrumentList([
            ...     abjad.instrumenttools.Flute(),
            ...     abjad.instrumenttools.Guitar()
            ...     ])

        ::

            >>> f(instruments)
            instrumenttools.InstrumentList(
                [
                    instrumenttools.Flute(
                        instrument_name='flute',
                        short_instrument_name='fl.',
                        instrument_name_markup=abjad.Markup(
                            contents=['Flute'],
                            ),
                        short_instrument_name_markup=abjad.Markup(
                            contents=['Fl.'],
                            ),
                        allowable_clefs=instrumenttools.ClefList(
                            [
                                abjad.Clef(
                                    name='treble',
                                    ),
                                ]
                            ),
                        pitch_range=abjad.PitchRange('[C4, D7]'),
                        sounding_pitch_of_written_middle_c=abjad.NamedPitch("c'"),
                        ),
                    instrumenttools.Guitar(
                        instrument_name='guitar',
                        short_instrument_name='gt.',
                        instrument_name_markup=abjad.Markup(
                            contents=['Guitar'],
                            ),
                        short_instrument_name_markup=abjad.Markup(
                            contents=['Gt.'],
                            ),
                        allowable_clefs=instrumenttools.ClefList(
                            [
                                abjad.Clef(
                                    name='treble',
                                    ),
                                ]
                            ),
                        default_tuning=abjad.Tuning(
                            pitches=abjad.PitchSegment(
                                (
                                    abjad.NamedPitch('e,'),
                                    abjad.NamedPitch('a,'),
                                    abjad.NamedPitch('d'),
                                    abjad.NamedPitch('g'),
                                    abjad.NamedPitch('b'),
                                    abjad.NamedPitch("e'"),
                                    ),
                                item_class=abjad.NamedPitch,
                                ),
                            ),
                        pitch_range=abjad.PitchRange('[E2, E5]'),
                        sounding_pitch_of_written_middle_c=abjad.NamedPitch('c'),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats instruments.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        superclass = super(InstrumentList, self)
        return superclass.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Gets interpreter representation of instrument list.

        ..  container:: example

            ::

                >>> instruments
                InstrumentList([Flute(), Guitar()])

        Returns string.
        '''
        contents = [repr(x) for x in self]
        contents = ', '.join(contents)
        return '{}([{}])'.format(type(self).__name__, contents)

    ### PRIVATE METHODS ###

    @staticmethod
    def _change_instrument_name_to_instrument(instrument_name):
        from abjad.tools import instrumenttools
        if instrument_name in (
            'alto',
            'baritone',
            'bass',
            'soprano',
            'tenor',
            ):
            instrument_name = instrument_name + ' Voice'
        instrument_name = instrument_name.title()
        instrument_name = instrument_name.replace(' ', '')
        instrument_name = instrument_name.replace('-', '')
        instrument_class = instrumenttools.__dict__[instrument_name]
        instrument = instrument_class()
        return instrument

    @staticmethod
    def _name_percussion(instrument, session):
        from abjad.tools import instrumenttools
        from ide import idetools
        if isinstance(instrument, instrumenttools.Percussion):
            Percussion = abjad.instrumenttools.Percussion
            items = Percussion.known_percussion[:]
            selector = idetools.Selector(session=session, items=items)
            instrument_name = selector._run()
            if selector._session.is_backtracking or instrument_name is None:
                return
            instrument = new(
                instrument,
                instrument_name=instrument_name,
                short_instrument_name=instrument_name,
                )
        return instrument

    ### ITEM CREATOR ###

    @staticmethod
    def _make_item_creator_class():
        from ide.idetools.Controller import Controller
        class ItemCreator(Controller):
            ### CLASS VARIABLES ###
            __slots__ = ('_is_ranged', '_target',)
            ### INITIALIZER ###
            def __init__(self, is_ranged=False, session=None, target=None):
                Controller.__init__(self, session=session)
                self._is_ranged = is_ranged
                self._target = target
            ### PRIVATE METHODS ###
            def _run(self):
                from abjad.tools import instrumenttools
                from ide import idetools
                controller = idetools.ControllerContext(controller=self)
                with controller:
                    items = abjad.instrumenttools.Instrument._list_instrument_names()
                    selector = idetools.Selector(
                        session=self._session,
                        items=items,
                        is_ranged=self._is_ranged,
                        )
                    result = selector._run()
                    if self._session.is_backtracking or not result:
                        return
                    if isinstance(result, list):
                        instrument_names = result
                    else:
                        instrument_names = [result]
                    instruments = []
                    class_ = InstrumentList
                    to_instrument = \
                        class_._change_instrument_name_to_instrument
                    name_percussion = class_._name_percussion
                    for instrument_name in instrument_names:
                        instrument = to_instrument(instrument_name)
                        instrument = name_percussion(instrument, self._session)
                        if instrument is not None:
                            instruments.append(instrument)
                    if self._is_ranged:
                        result = instruments[:]
                    else:
                        result = instruments[0]
                    self._target = result
                    return self.target
            @property
            def target(self):
                return self._target
        return ItemCreator

    ### PRIVATE PROPERTIES ###

    @property
    def _item_creator_class(self):
        item_creator_class = self._make_item_creator_class()
        return item_creator_class

    @property
    def _item_creator_class_kwargs(self):
        return {'is_ranged': True}
