# -*- coding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Performer(AbjadObject):
    r'''A performer.

    ..  container:: example

        ::

            >>> performer = instrumenttools.Performer(name='flutist')
            >>> performer.instruments.append(instrumenttools.Flute())
            >>> performer.instruments.append(instrumenttools.Piccolo())

        ::

            >>> print(format(performer))
            instrumenttools.Performer(
                name='flutist',
                instruments=instrumenttools.InstrumentInventory(
                    [
                        instrumenttools.Flute(
                            instrument_name='flute',
                            short_instrument_name='fl.',
                            instrument_name_markup=markuptools.Markup(
                                contents=('Flute',),
                                ),
                            short_instrument_name_markup=markuptools.Markup(
                                contents=('Fl.',),
                                ),
                            allowable_clefs=indicatortools.ClefInventory(
                                [
                                    indicatortools.Clef(
                                        name='treble',
                                        ),
                                    ]
                                ),
                            pitch_range=pitchtools.PitchRange(
                                range_string='[C4, D7]',
                                ),
                            sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                            ),
                        instrumenttools.Piccolo(
                            instrument_name='piccolo',
                            short_instrument_name='picc.',
                            instrument_name_markup=markuptools.Markup(
                                contents=('Piccolo',),
                                ),
                            short_instrument_name_markup=markuptools.Markup(
                                contents=('Picc.',),
                                ),
                            allowable_clefs=indicatortools.ClefInventory(
                                [
                                    indicatortools.Clef(
                                        name='treble',
                                        ),
                                    ]
                                ),
                            pitch_range=pitchtools.PitchRange(
                                range_string='[D5, C8]',
                                ),
                            sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c''"),
                            ),
                        ]
                    ),
                )

    Performer models instrument doublings.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None, instruments=None):
        from abjad.tools import instrumenttools
        self._instruments = instrumenttools.InstrumentInventory()
        self.name = name
        self.instruments = instruments

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a performer with name and instruments equal to
        those of this performer. Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            if self.name == expr.name:
                if self.instruments == expr.instruments:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats performer.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __hash__(self):
        r'''Hashes performer.

        Returns string.
        '''
        return hash((type(self).__name__, self.name, tuple(self.instruments)))

    ### PUBLIC METHODS ###

    def get_instrument(self, instrument_name):
        r'''Gets instrument in performer with `instrument_name`.

        ..  container:: example

            For examples:

            ::

                >>> flutist = instrumenttools.Performer(name='flutist')
                >>> flutist.instruments.append(instrumenttools.Flute())
                >>> flutist.instruments.append(instrumenttools.Piccolo())

        ..  container:: example

            **Example 1.** Gets instrument with instrument name:

            ::

                >>> flutist.get_instrument('piccolo')
                Piccolo()

        ..  container:: example

            **Example 2.** Gets instrument with short instrument name:

            ::

                >>> flutist.get_instrument('picc.')
                Piccolo()

        ..  container:: example

            **Example 3.** Gets instrument regardless of case:

            ::

                >>> flutist.get_instrument('PICCOLO')
                Piccolo()

        ..  container:: example

            **Example 4.** Returns none when no match is found:

            ::

                >>> flutist.get_instrument('xyl.') is None
                True

        Returns instrument or none.
        '''
        for instrument in self.instruments:
            if instrument.instrument_name.lower() == instrument_name.lower():
                return instrument
            if instrument.short_instrument_name.lower() == \
                instrument_name.lower():
                return instrument

    # TODO: make private
    @staticmethod
    def list_performer_names():
        r'''Lists performer names.

        ..  container:: example

            ::

                >>> for name in instrumenttools.Performer.list_performer_names():
                ...     name
                ...
                'accordionist'
                'alto'
                'baritone'
                'bass'
                'bassist'
                'bassoonist'
                'cellist'
                'clarinetist'
                'flutist'
                'guitarist'
                'harpist'
                'harpsichordist'
                'hornist'
                'mezzo-soprano'
                'oboist'
                'percussionist'
                'pianist'
                'saxophonist'
                'soprano'
                'tenor'
                'trombonist'
                'trumpeter'
                'tubist'
                'vibraphonist'
                'violinist'
                'violist'
                'xylophonist'

        Returns list.
        '''
        from abjad.tools import instrumenttools
        performer_names = set([])
        for instrument_class in instrumenttools.Instrument._list_instruments():
            instrument = instrument_class()
            performer_name = instrument._get_default_performer_name()
            performer_names.add(performer_name)
        return list(sorted(performer_names))

    # TODO: make private
    @staticmethod
    def list_primary_performer_names():
        r'''Lists primary performer names.

        ..  container:: example

            ::

                >>> for pair in instrumenttools.Performer.list_primary_performer_names():
                ...     pair
                ...
                ('accordionist', 'acc.')
                ('alto', 'alto')
                ('baritone', 'bar.')
                ('bass', 'bass')
                ('bassist', 'cb.')
                ('bassoonist', 'bsn.')
                ('cellist', 'vc.')
                ('clarinetist', 'cl.')
                ('flutist', 'fl.')
                ('guitarist', 'gt.')
                ('harpist', 'hp.')
                ('harpsichordist', 'hpschd.')
                ('hornist', 'hn.')
                ('mezzo-soprano', 'ms.')
                ('oboist', 'ob.')
                ('pianist', 'pf.')
                ('saxophonist', 'alt. sax.')
                ('soprano', 'sop.')
                ('tenor', 'ten.')
                ('trombonist', 'ten. trb.')
                ('trumpeter', 'tp.')
                ('tubist', 'tb.')
                ('violinist', 'vn.')
                ('violist', 'va.')

        Returns list.
        '''
        from abjad.tools import instrumenttools
        performer_names = set([])
        for instrument_class in instrumenttools.Instrument._list_instruments():
            instrument = instrument_class()
            if instrument._is_primary_instrument:
                performer_name = instrument._get_default_performer_name()
                performer_abbreviation = getattr(
                    instrument, 'performer_abbreviation', None)
                performer_abbreviation = performer_abbreviation or \
                    instrument.short_instrument_name
                performer_names.add((performer_name, performer_abbreviation))
        return list(sorted(performer_names))

    # TODO: make private
    @staticmethod
    def make_performer_name_instrument_dictionary():
        r'''Makes performer name / instrument dictionary.

        ..  container:: example

            ::

                >>> dictionary = \
                ...     performer.make_performer_name_instrument_dictionary()
                >>> for key, value in sorted(dictionary.items()):
                ...     print(key + ':')
                ...     for x in value:
                ...         print('\t{}'.format(x.__name__))
                accordionist:
                    Accordion
                alto:
                    AltoVoice
                baritone:
                    BaritoneVoice
                bass:
                    BassVoice
                bassist:
                    Contrabass
                bassoonist:
                    Bassoon
                    Contrabassoon
                brass player:
                    AltoTrombone
                    BassTrombone
                    FrenchHorn
                    TenorTrombone
                    Trumpet
                    Tuba
                cellist:
                    Cello
                clarinetist:
                    BassClarinet
                    ClarinetInA
                    ClarinetInBFlat
                    ClarinetInEFlat
                    ContrabassClarinet
                clarinettist:
                    BassClarinet
                    ClarinetInA
                    ClarinetInBFlat
                    ClarinetInEFlat
                    ContrabassClarinet
                contrabassist:
                    Contrabass
                double reed player:
                    Bassoon
                    Contrabassoon
                    EnglishHorn
                    Oboe
                flautist:
                    AltoFlute
                    BassFlute
                    ContrabassFlute
                    Flute
                    Piccolo
                flutist:
                    AltoFlute
                    BassFlute
                    ContrabassFlute
                    Flute
                    Piccolo
                guitarist:
                    Guitar
                harpist:
                    Harp
                harpsichordist:
                    Harpsichord
                hornist:
                    FrenchHorn
                instrumentalist:
                    Accordion
                    AltoFlute
                    AltoSaxophone
                    AltoTrombone
                    AltoVoice
                    BaritoneSaxophone
                    BaritoneVoice
                    BassClarinet
                    BassFlute
                    Bassoon
                    BassSaxophone
                    BassTrombone
                    BassVoice
                    Cello
                    ClarinetInA
                    ClarinetInBFlat
                    ClarinetInEFlat
                    Contrabass
                    ContrabassClarinet
                    ContrabassFlute
                    Contrabassoon
                    ContrabassSaxophone
                    EnglishHorn
                    Flute
                    FrenchHorn
                    Glockenspiel
                    Guitar
                    Harp
                    Harpsichord
                    Marimba
                    MezzoSopranoVoice
                    Oboe
                    Percussion
                    Piano
                    Piccolo
                    SopraninoSaxophone
                    SopranoSaxophone
                    SopranoVoice
                    TenorSaxophone
                    TenorTrombone
                    TenorVoice
                    Trumpet
                    Tuba
                    Vibraphone
                    Viola
                    Violin
                    Xylophone
                keyboardist:
                    Accordion
                    Harpsichord
                    Piano
                mezzo-soprano:
                    MezzoSopranoVoice
                oboist:
                    EnglishHorn
                    Oboe
                percussionist:
                    Glockenspiel
                    Marimba
                    Percussion
                    Vibraphone
                    Xylophone
                pianist:
                    Piano
                reed player:
                    AltoSaxophone
                    BaritoneSaxophone
                    BassClarinet
                    Bassoon
                    BassSaxophone
                    ClarinetInA
                    ClarinetInBFlat
                    ClarinetInEFlat
                    ContrabassClarinet
                    Contrabassoon
                    ContrabassSaxophone
                    EnglishHorn
                    Oboe
                    SopraninoSaxophone
                    SopranoSaxophone
                    TenorSaxophone
                saxophonist:
                    AltoSaxophone
                    BaritoneSaxophone
                    BassSaxophone
                    ContrabassSaxophone
                    SopraninoSaxophone
                    SopranoSaxophone
                    TenorSaxophone
                single reed player:
                    AltoSaxophone
                    BaritoneSaxophone
                    BassClarinet
                    BassSaxophone
                    ClarinetInA
                    ClarinetInBFlat
                    ClarinetInEFlat
                    ContrabassClarinet
                    ContrabassSaxophone
                    SopraninoSaxophone
                    SopranoSaxophone
                    TenorSaxophone
                soprano:
                    SopranoVoice
                string player:
                    Cello
                    Contrabass
                    Guitar
                    Harp
                    Viola
                    Violin
                tenor:
                    TenorVoice
                trombonist:
                    AltoTrombone
                    BassTrombone
                    TenorTrombone
                trumpeter:
                    Trumpet
                tubist:
                    Tuba
                vibraphonist:
                    Vibraphone
                violinist:
                    Violin
                violist:
                    Viola
                vocalist:
                    AltoVoice
                    BaritoneVoice
                    BassVoice
                    MezzoSopranoVoice
                    SopranoVoice
                    TenorVoice
                wind player:
                    AltoFlute
                    AltoSaxophone
                    BaritoneSaxophone
                    BassClarinet
                    BassFlute
                    Bassoon
                    BassSaxophone
                    ClarinetInA
                    ClarinetInBFlat
                    ClarinetInEFlat
                    ContrabassClarinet
                    ContrabassFlute
                    Contrabassoon
                    ContrabassSaxophone
                    EnglishHorn
                    Flute
                    FrenchHorn
                    Oboe
                    Piccolo
                    SopraninoSaxophone
                    SopranoSaxophone
                    TenorSaxophone
                xylophonist:
                    Xylophone

        Returns ordered dictionary.
        '''
        from abjad.tools import instrumenttools
        result = collections.OrderedDict()
        for instrument_class in instrumenttools.Instrument._list_instruments():
            instrument = instrument_class()
            for performer_name in instrument._get_performer_names():
                if performer_name in result:
                    result[performer_name].append(instrument_class)
                else:
                    result[performer_name] = [instrument_class]
        for instruments in result.values():
            instruments.sort(key=lambda x: x.__name__.lower())
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menu_summary(self):
        if not self.instruments:
            result = '{}: no instruments'.format(self.name)
        elif len(self.instruments) == 1 and self.name == \
            self.instruments[0].instrument_name:
            result = '{}'.format(self.name)
        else:
            instruments = ([x.instrument_name for x in self.instruments])
            instruments = ', '.join(instruments)
            result = '{}: {}'.format(self.name, instruments)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Gets count of instruments to be played by performer.

        ..  container:: example

            ::

                >>> performer = instrumenttools.Performer(name='flutist')
                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> performer.instrument_count
                2

        Returns nonnegative integer
        '''
        return len(self.instruments)

    @property
    def instruments(self):
        r'''Gets and sets instruments to be played by performer.

        ..  container:: example

            ::

                >>> performer = instrumenttools.Performer(name='flutist')
                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> for instrument in performer.instruments:
                ...     instrument
                Flute()
                Piccolo()

        Returns instrument inventory.
        '''
        return self._instruments

    @instruments.setter
    def instruments(self, instruments):
        from abjad.tools.instrumenttools.Instrument import Instrument
        if instruments is None:
            self._instruments[:] = []
        elif isinstance(instruments,
            (list, datastructuretools.TypedList)):
            assert all(isinstance(x, Instrument) for x in instruments)
            self._instruments[:] = instruments[:]
        else:
            message = 'instruments {!r} must be list or none.'
            message = message.format(instruments)
            raise TypeError(message)

    @property
    def is_doubling(self):
        r'''Is true when performer is to play more than one instrument.
        Otherwise false.

        ..  container:: example

            ::

                >>> performer = instrumenttools.Performer(name='flutist')
                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> performer.is_doubling
                True

        Returns true or false.
        '''
        return 1 < self.instrument_count

    # TODO: make private
    @property
    def likely_instruments_based_on_performer_name(self):
        r'''Gets likely instruments based on performer name.

        ..  container:: example

            ::

                >>> performer = instrumenttools.Performer(name='flutist')
                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> for likely_instrument in \
                ...     performer.likely_instruments_based_on_performer_name:
                ...     likely_instrument.__name__
                ...
                'AltoFlute'
                'BassFlute'
                'ContrabassFlute'
                'Flute'
                'Piccolo'

        Returns list.
        '''
        dictionary = self.make_performer_name_instrument_dictionary()
        try:
            result = dictionary[self.name]
        except KeyError:
            result = []
        return result

    # TODO: make private
    @property
    def most_likely_instrument_based_on_performer_name(self):
        r'''Gets most likely instrument based on performer name.

        ..  container:: example

            ::

                >>> performer = instrumenttools.Performer(name='flutist')
                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> performer.most_likely_instrument_based_on_performer_name
                <class 'abjad.tools.instrumenttools.Flute.Flute'>

        Returns instrument class.
        '''
        for likely_instrument_class in \
            self.likely_instruments_based_on_performer_name:
            likely_instrument = likely_instrument_class()
            if likely_instrument._is_primary_instrument:
                return likely_instrument_class

    @property
    def name(self):
        r'''Gets and sets score name of performer.

        ..  container:: example

            ::

                >>> performer = instrumenttools.Performer(name='flutist')
                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> performer.name
                'flutist'

        Returns string.
        '''
        return self._name

    @name.setter
    def name(self, name):
        assert isinstance(name, (str, type(None)))
        self._name = name
