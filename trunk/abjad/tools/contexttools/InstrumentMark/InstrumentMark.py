from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools import stringtools


# Note that instruments are the classes in the system that implement default attribute values.
# That means that three things are true.
# First, all instruments come supplied with a default name and a default short instrument name.
# Second, all instruments allow users to override both instrument name and short instrument name.
# Third, all instruments 'remember' default values when such values are overridden.
# When all three of these things are the case we talk about a class implementing default attribute values.
# This is the meaning of the '_has_default_attribute_values' class attribute.
# The impact this currently has in the system concerns the _storage_format of such objects.
class InstrumentMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of an instrument change::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> contexttools.InstrumentMark('Flute', 'Fl.')(staff)
        InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4})

    ::

        >>> f(staff)
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

    ### CLASS ATTRIBUTES ###

    _format_slot = 'opening'

    _has_default_attribute_values = True

    ### INITIALIZER ###

    def __init__(self, 
        instrument_name, 
        short_instrument_name, 
        instrument_name_markup=None, 
        short_instrument_name_markup=None, 
        target_context=None):
        from abjad.tools.stafftools.Staff import Staff
        ContextMark.__init__(self, target_context=target_context)
        if self.target_context is None:
            self._target_context = Staff
        self._default_instrument_name = None
        self._default_instrument_name_markup = None
        self._default_short_instrument_name = None
        self._default_short_instrument_name_markup = None
        self._instrument_name = instrument_name
        self._instrument_name_markup = instrument_name_markup
        self._short_instrument_name = short_instrument_name
        self._short_instrument_name_markup = short_instrument_name_markup

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self._instrument_name_markup, self._short_instrument_name_markup,
            target_context = self.target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.instrument_name_markup == arg.instrument_name_markup:
                if self.short_instrument_name_markup == arg.short_instrument_name_markup:
                    return True
        return False

    def __hash__(self):
        return hash((type(self).__name__, self.instrument_name_markup, self.short_instrument_name_markup))

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        result = []
        for keyword_argument_name in self._keyword_argument_names:
            private_keyword_argument_name = '_{}'.format(keyword_argument_name)
            private_keyword_argument_value = getattr(self, private_keyword_argument_name, None)
            if private_keyword_argument_value is not None:
                string = '{}={!r}'.format(keyword_argument_name, private_keyword_argument_value)
                result.append(string)
        result = ', '.join(result)
        return result

    @property
    def _keyword_argument_names(self):
        return (
            'instrument_name',
            'instrument_name_markup',
            'short_instrument_name',
            'short_instrument_name_markup',
            )

    @property
    def _one_line_menuing_summary(self):
        return self.instrument_name

    # will probably need to change definition at some point #
    @property
    def _target_context_name(self):
        return self.target_context.__name__

    ### PUBLIC PROPERTIES ###

    @property
    def default_instrument_name(self):
        r'''Read-only default instrument name.

        Return string.
        '''
        return self._default_instrument_name

    @property
    def default_short_instrument_name(self):
        r'''Read-only default short instrument name.

        Return string.
        '''
        return self._default_short_instrument_name

    @property
    def lilypond_format(self):
        '''Read-only LilyPond input format of instrument mark:

        ::

            >>> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
            >>> instrument.lilypond_format
            ['\\set Staff.instrumentName = \\markup { Flute }', 
                '\\set Staff.shortInstrumentName = \\markup { Fl. }']

        Return list.
        '''
        result = []
        result.append(r'\set %s.instrumentName = %s' % (self._target_context_name, self.instrument_name_markup))
        result.append(r'\set %s.shortInstrumentName = %s' % (self._target_context_name, self.short_instrument_name_markup))
        return result

    @apply
    def instrument_name():
        def fget(self):
            r'''Get instrument name::

                >>> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                >>> instrument.instrument_name
                'Flute'

            Set instrument name::

                >>> instrument.instrument_name = 'Alto Flute'
                >>> instrument.instrument_name
                'Alto Flute'

            Return string.
            '''
            if self._instrument_name is None:
                return self.default_instrument_name
            else:
                return self._instrument_name
        def fset(self, instrument_name):
            assert isinstance(instrument_name, (str, type(None)))
            self._instrument_name = instrument_name
        return property(**locals())

    @apply
    def instrument_name_markup():
        def fget(self):
            r'''Get instrument name::

                >>> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                >>> instrument.instrument_name_markup
                Markup(('Flute',))

            Set instrument name::

                >>> instrument.instrument_name_markup = 'Alto Flute'
                >>> instrument.instrument_name_markup
                Markup(('Alto Flute',))

            Return markup.
            '''
            from abjad.tools.markuptools import Markup
            if self._instrument_name_markup is None:
                return Markup(stringtools.capitalize_string_start(self.instrument_name))
            else:
                return self._instrument_name_markup
        def fset(self, instrument_name_markup):
            from abjad.tools.markuptools import Markup
            assert isinstance(instrument_name_markup, (str, type(Markup('')), type(None)))
            if instrument_name_markup is None:
                self._instrument_name_markup = instrument_name_markup
            else:
                self._instrument_name_markup = Markup(instrument_name_markup)
        return property(**locals())

    @apply
    def short_instrument_name():
        def fget(self):
            r'''Get short instrument name::

                >>> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                >>> instrument.short_instrument_name
                'Fl.'

            Set short instrument name::

                >>> instrument.short_instrument_name = 'Alto Fl.'
                >>> instrument.short_instrument_name
                'Alto Fl.'

            Return string.
            '''
            if self._short_instrument_name is None:
                return self.default_short_instrument_name
            else:
                return self._short_instrument_name
        def fset(self, short_instrument_name):
            assert isinstance(short_instrument_name, (str, type(None)))
            self._short_instrument_name = short_instrument_name
        return property(**locals())

    @apply
    def short_instrument_name_markup():
        def fget(self):
            r'''Get short instrument name::

                >>> instrument = contexttools.InstrumentMark('Flute', 'Fl.')
                >>> instrument.short_instrument_name_markup
                Markup(('Fl.',))

            Set short instrument name::

                >>> instrument.short_instrument_name_markup = 'Alto Fl.'
                >>> instrument.short_instrument_name_markup
                Markup(('Alto Fl.',))

            Return markup.
            '''
            from abjad.tools.markuptools import Markup
            if self._short_instrument_name_markup is None:
                return Markup(stringtools.capitalize_string_start(self.short_instrument_name))
            else:
                return self._short_instrument_name_markup
        def fset(self, short_instrument_name_markup):
            from abjad.tools.markuptools import Markup
            assert isinstance(short_instrument_name_markup, (str, type(Markup('')), type(None)))
            if short_instrument_name_markup is None:
                self._short_instrument_name_markup = short_instrument_name_markup
            else:
                self._short_instrument_name_markup = Markup(short_instrument_name_markup)
        return property(**locals())
