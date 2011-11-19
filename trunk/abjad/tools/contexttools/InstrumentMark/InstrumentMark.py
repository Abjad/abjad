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

    def __init__(self, instrument_name_markup, short_instrument_name_markup, target_context = None):
        from abjad.tools.stafftools.Staff import Staff
        from abjad.tools.markuptools import Markup
        ContextMark.__init__(self, target_context = target_context)
        if self.target_context is None:
            self._target_context = Staff
        self._default_instrument_name_markup = None
        self._default_short_instrument_name_markup = None
        self.instrument_name_markup = instrument_name_markup
        self.short_instrument_name_markup = short_instrument_name_markup

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._instrument_name_markup, self._short_instrument_name_markup,
            target_context = self.target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.instrument_name_markup == arg.instrument_name_markup:
                if self.short_instrument_name_markup == arg.short_instrument_name_markup:
                    return True
        return False

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        markups = []
        if self.instrument_name_markup != self.default_instrument_name_markup:
            markups.append(self.instrument_name_markup)
        if self.short_instrument_name_markup != self.default_short_instrument_name_markup:
            markups.append(self.short_instrument_name_markup)
        if not markups:
            contents_string = ''
        else:
            contents_string = ', '.join([repr(markup._contents_string) for markup in markups])
        return contents_string

    # will probably need to change definition at some point #
    @property
    def _target_context_name(self):
        return self.target_context.__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def default_instrument_name_markup(self):
        r'''Read-only default instrument name.

        Return markup.
        '''
        return self._default_instrument_name_markup

    @property
    def default_short_instrument_name_markup(self):
        r'''Read-only default short instrument name.

        Return markup.
        '''
        return self._default_short_instrument_name_markup

    @property
    def format(self):
        '''Read-only LilyPond input format of instrument mark:

        ::

            abjad> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
            abjad> instrument.format
            ['\\set Staff.instrumentName = \\markup { Flute }', '\\set Staff.shortInstrumentName = \\markup { Fl. }']

        Return list.
        '''
        result = []
        result.append(r'\set %s.instrumentName = %s' % (self._target_context_name, self.instrument_name_markup))
        result.append(r'\set %s.shortInstrumentName = %s' % (self._target_context_name, self.short_instrument_name_markup))
        return result

    @apply
    def instrument_name_markup():
        def fget(self):
            r'''Get instrument name::

                abjad> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                abjad> instrument.instrument_name_markup
                Markup('Flute')

            Set instrument name::

                abjad> instrument.instrument_name_markup = 'Alto Flute'
                abjad> instrument.instrument_name_markup
                Markup('Alto Flute')

            Return markup.
            '''
            if self._instrument_name_markup is None:
                return self.default_instrument_name_markup
            else:
                return self._instrument_name_markup
        def fset(self, instrument_name_markup):
            from abjad.tools.markuptools import Markup
            assert isinstance(instrument_name_markup, (str, type(None)))
            if instrument_name_markup is None:
                self._instrument_name_markup = instrument_name_markup
            else:
                self._instrument_name_markup = Markup(instrument_name_markup)
        return property(**locals())

    @apply
    def short_instrument_name_markup():
        def fget(self):
            r'''Get short instrument name::

                abjad> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                abjad> instrument.short_instrument_name_markup
                Markup('Fl.')

            Set short instrument name::

                abjad> instrument.short_instrument_name_markup = 'Alto Fl.'
                abjad> instrument.short_instrument_name_markup
                Markup('Alto Fl.')

            Return markup.
            '''
            if self._short_instrument_name_markup is None:
                return self.default_short_instrument_name_markup
            else:
                return self._short_instrument_name_markup
        def fset(self, short_instrument_name_markup):
            from abjad.tools.markuptools import Markup
            assert isinstance(short_instrument_name_markup, (str, type(None)))
            if short_instrument_name_markup is None:
                self._short_instrument_name_markup = short_instrument_name_markup
            else:
                self._short_instrument_name_markup = Markup(short_instrument_name_markup)
        return property(**locals())
