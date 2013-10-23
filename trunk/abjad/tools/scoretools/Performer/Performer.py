# -*- encoding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Performer(AbjadObject):
    r'''A instrumental or vocal performer.

    ::

        >>> performer = scoretools.Performer(name='flutist')
        >>> performer.instruments.append(instrumenttools.Flute())
        >>> performer.instruments.append(instrumenttools.Piccolo())

    ::

        >>> print performer.storage_format
        scoretools.Performer(
            name='flutist',
            instruments=instrumenttools.InstrumentInventory([
                instrumenttools.Flute(),
                instrumenttools.Piccolo()
                ])
            )

    The purpose of the class is to model things like
    flute I doubling piccolo and flute.

    At present the class comprises an instrument inventory and name.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None, instruments=None):
        from abjad.tools import instrumenttools
        self._instruments = instrumenttools.InstrumentInventory()
        self.name = name
        self.instruments = instruments

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.name == expr.name:
                if self.instruments == expr.instruments:
                    return True
        return False

    def __hash__(self):
        return hash((self._class_name, self.name, tuple(self.instruments)))

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
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

    ### PUBLIC METHODS ###

    @staticmethod
    def list_performer_names():
        r'''Lists performer names.

        ::

            >>> for name in scoretools.Performer.list_performer_names():
            ...     name
            ...
            'accordionist'
            'baritone'
            'bass'
            'bassist'
            'bassoonist'
            'cellist'
            'clarinetist'
            'contralto'
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

    @staticmethod
    def list_primary_performer_names():
        r'''List performer names:

        ::

            >>> for pair in scoretools.Performer.list_primary_performer_names():
            ...     pair
            ...
            ('accordionist', 'acc.')
            ('baritone', 'bar.')
            ('bass', 'bass')
            ('bassist', 'vb.')
            ('bassoonist', 'bsn.')
            ('cellist', 'vc.')
            ('clarinetist', 'cl.')
            ('contralto', 'contr.')
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
            ('trombonist', 'trb.')
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
                    instrument, 'default_performer_abbreviation', None)
                performer_abbreviation = performer_abbreviation or \
                    instrument._default_short_instrument_name
                performer_names.add((performer_name, performer_abbreviation))
        return list(sorted(performer_names))

    @property
    def storage_format(self):
        r'''Storage format of performer.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Number of instruments to be played by performer:

            >>> performer.instrument_count
            2

        Returns nonnegative integer
        '''
        return len(self.instruments)

    @apply
    def instruments():
        def fget(self):
            r'''List of instruments to be played by performer:

            ::

                >>> performer.instruments
                InstrumentInventory([Flute(), Piccolo()])

            Returns instrument inventory.
            '''
            return self._instruments
        def fset(self, instruments):
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
        return property(**locals())

    @property
    def is_doubling(self):
        r'''Is performer to play more than one instrument?

        ::
            >>> performer.is_doubling
            True

        Returns boolean.
        '''
        return 1 < self.instrument_count

    @property
    def likely_instruments_based_on_performer_name(self):
        r'''Likely instruments based on performer name:

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

    @property
    def most_likely_instrument_based_on_performer_name(self):
        r'''Most likely instrument based on performer name:

        ::

            >>> performer.most_likely_instrument_based_on_performer_name
            <class 'abjad.tools.instrumenttools.Flute.Flute.Flute'>

        Returns instrument class.
        '''
        for likely_instrument_class in \
            self.likely_instruments_based_on_performer_name:
            likely_instrument = likely_instrument_class()
            if likely_instrument._is_primary_instrument:
                return likely_instrument_class

    @apply
    def name():
        def fget(self):
            r'''Score name of performer:

            ::

                >>> performer.name
                'flutist'

            Returns string.
            '''
            return self._name
        def fset(self, name):
            assert isinstance(name, (str, type(None)))
            self._name = name
        return property(**locals())

    ### PUBLIC METHODS ###

    def make_performer_name_instrument_dictionary(self):
        r'''Make performer name / instrument dictionary:

        ::

            >>> dictionary = \
            ...     performer.make_performer_name_instrument_dictionary()
            >>> for key, value in sorted(dictionary.iteritems()):
            ...     print key + ':'
            ...     for x in value:
            ...         print '\t{}'.format(x.__name__)
            accordionist:
                Accordion
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
                BFlatClarinet
                ClarinetInA
                ContrabassClarinet
                EFlatClarinet
            clarinettist:
                BassClarinet
                BFlatClarinet
                ClarinetInA
                ContrabassClarinet
                EFlatClarinet
            contrabassist:
                Contrabass
            contralto:
                ContraltoVoice
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
                BaritoneSaxophone
                BaritoneVoice
                BassClarinet
                BassFlute
                Bassoon
                BassSaxophone
                BassTrombone
                BassVoice
                BFlatClarinet
                Cello
                ClarinetInA
                Contrabass
                ContrabassClarinet
                ContrabassFlute
                Contrabassoon
                ContrabassSaxophone
                ContraltoVoice
                EFlatClarinet
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
                UntunedPercussion
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
                UntunedPercussion
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
                BFlatClarinet
                ClarinetInA
                ContrabassClarinet
                Contrabassoon
                ContrabassSaxophone
                EFlatClarinet
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
                BFlatClarinet
                ClarinetInA
                ContrabassClarinet
                ContrabassSaxophone
                EFlatClarinet
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
                BaritoneVoice
                BassVoice
                ContraltoVoice
                MezzoSopranoVoice
                SopranoVoice
                TenorVoice
            wind player:
                AltoFlute
                ...
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
        for instruments in result.itervalues():
            instruments.sort(key=lambda x: x.__name__.lower())
        return result
