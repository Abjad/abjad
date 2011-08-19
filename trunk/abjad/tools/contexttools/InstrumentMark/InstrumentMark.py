from abjad.tools.contexttools.ContextMark import ContextMark


class InstrumentMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of an instrument change::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> contexttools.InstrumentMark('Flute', 'Fl.')(staff)
        InstrumentMark('Flute', 'Fl.')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    Instrument marks target staff context by default.
    '''

    _format_slot = 'opening'

    def __init__(self, instrument_name, short_instrument_name, target_context = None):
        from abjad.tools.stafftools.Staff import Staff
        from abjad.tools.markuptools import Markup
        ContextMark.__init__(self, target_context = target_context)
        if self.target_context is None:
            self._target_context = Staff
        self._instrument_name = Markup(instrument_name)
        self._short_instrument_name = Markup(short_instrument_name)

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._instrument_name, self._short_instrument_name,
            target_context = self.target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.instrument_name == arg.instrument_name:
                if self.short_instrument_name == arg.short_instrument_name:
                    return True
        return False

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        markups = (self.instrument_name, self.short_instrument_name)
        contents_string = ', '.join([repr(markup._contents_string) for markup in markups])
        return contents_string

    ### will probably need to change definition at some point ###
    @property
    def _target_context_name(self):
        return self.target_context.__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''Read-only LilyPond input format of instrument mark:

        ::

            abjad> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
            abjad> instrument.format
            ['\\set Staff.instrumentName = \\markup { Flute }', '\\set Staff.shortInstrumentName = \\markup { Fl. }']

        Return list.
        '''
        result = [ ]
        result.append(r'\set %s.instrumentName = %s' % (self._target_context_name, self.instrument_name))
        result.append(r'\set %s.shortInstrumentName = %s' % (self._target_context_name, self.short_instrument_name))
        return result

    @apply
    def instrument_name():
        def fget(self):
            r'''Get instrument name::

                abjad> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                abjad> instrument.instrument_name
                Markup('Flute')

            Set instrument name::

                abjad> instrument.instrument_name = 'Alto Flute'
                abjad> instrument.instrument_name
                Markup('Alto Flute')

            Return markup.
            '''
            return self._instrument_name
        def fset(self, instrument_name):
            from abjad.tools.markuptools import Markup
            assert isinstance(instrument_name, str)
            self._instrument_name = Markup(instrument_name)
        return property(**locals())

    @apply
    def short_instrument_name():
        def fget(self):
            r'''Get short instrument name::

                abjad> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                abjad> instrument.short_instrument_name
                Markup('Fl.')

            Set short instrument name::

                abjad> instrument.short_instrument_name = 'Alto Fl.'
                abjad> instrument.short_instrument_name
                Markup('Alto Fl.')

            Return markup.
            '''
            return self._short_instrument_name
        def fset(self, short_instrument_name):
            from abjad.tools.markuptools import Markup
            assert isinstance(short_instrument_name, str)
            self._short_instrument_name = Markup(short_instrument_name)
        return property(**locals())


