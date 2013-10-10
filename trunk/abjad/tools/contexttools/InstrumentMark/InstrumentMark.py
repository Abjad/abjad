# -*- encoding: utf-8 -*-
import copy
from abjad.tools import markuptools
from abjad.tools import stringtools
from abjad.tools.contexttools.ContextMark import ContextMark


# Note that instruments are the classes in the system that 
# implement default attribute values.
#
# That means that three things are true.
#
# First, all instruments come supplied with a default name and 
# a default short instrument name.
#
# Second, all instruments allow users to override both instrument name 
# and short instrument name.
#
# Third, all instruments 'remember' default values 
# when such values are overridden.
#
# When all three of these things are the case we talk about a class 
# implementing default attribute values.
#
# This is the meaning of the '_has_default_attribute_values' class attribute.
# The impact this currently has in the system concerns the 
# storage format of such objects.
class InstrumentMark(ContextMark):
    r'''An instrument mark.

    Instrument marks target staff context by default.
    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

    _has_default_attribute_values = True

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        target_context=None,
        ):
        from abjad.tools.stafftools.Staff import Staff
        target_context = target_context or Staff
        ContextMark.__init__(self, target_context=target_context)

#        self._default_instrument_name = None
#        self._default_instrument_name_markup = None
#        self._default_short_instrument_name = None
#        self._default_short_instrument_name_markup = None

        self._default_instrument_name = instrument_name
        self._default_instrument_name_markup = instrument_name_markup
        self._default_short_instrument_name = short_instrument_name
        self._default_short_instrument_name_markup = \
            short_instrument_name_markup

        self.instrument_name = instrument_name
        self.instrument_name_markup = instrument_name_markup
        self.short_instrument_name = short_instrument_name
        self.short_instrument_name_markup = short_instrument_name_markup

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies instrument mark.

        Returns new instrument mark.
        '''
        return type(self)(
            instrument_name_markup=self._instrument_name_markup, 
            short_instrument_name_markup=self._short_instrument_name_markup,
            target_context=self.target_context,
            )

    def __eq__(self, arg):
        r'''True when instrument mark equals `arg`.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.instrument_name == arg.instrument_name:
                if self.short_instrument_name == arg.short_instrument_name:
                    return True
        return False

    def __hash__(self):
        '''Hash value of instrument mark.

        Returns integer.
        '''
        return hash((
            self._class_name, 
            self.instrument_name, 
            self.short_instrument_name,
            ))

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        result = []
        for keyword_argument_name in self._keyword_argument_names:
            private_keyword_argument_name = '_{}'.format(
                keyword_argument_name)
            private_keyword_argument_value = \
                getattr(self, private_keyword_argument_name, None)
            if private_keyword_argument_value is not None:
                string = '{}={!r}'.format(
                    keyword_argument_name, private_keyword_argument_value)
                result.append(string)
        result = ', '.join(result)
        return result

    # TODO: remove in favor of all subclass inits implementing only keywords
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

    # will probably need to change definition at some point
    @property
    def _target_context_name(self):
        return self.target_context.__name__

    ### PRIVATE METHODS ###

    def _make_default_name_markups(self):
        string = self._default_instrument_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        self._default_instrument_name_markup = markup
        string = self._default_short_instrument_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        self._default_short_instrument_name_markup = markup

    ### PUBLIC PROPERTIES ###

    @apply
    def instrument_name():
        def fget(self):
            r'''Gets and sets instrument name.

            Returns string.
            '''
            if self._instrument_name is None:
                return self._default_instrument_name
            else:
                return self._instrument_name
        def fset(self, instrument_name):
            assert isinstance(instrument_name, (str, type(None)))
            self._instrument_name = instrument_name
        return property(**locals())

    @apply
    def instrument_name_markup():
        def fget(self):
            r'''Gets and sets instrument name markup.

            Returns markup.
            '''
            if self._instrument_name_markup is None:
                if self._default_instrument_name_markup is None:
                    self._make_default_name_markups()
                markup = self._default_instrument_name_markup
                markup = copy.copy(markup)
                self._instrument_name_markup = markup
            return self._instrument_name_markup
        def fset(self, instrument_name_markup):
            from abjad.tools.markuptools import Markup
            assert isinstance(
                instrument_name_markup, (str, type(Markup('')), type(None)))
            if instrument_name_markup is None:
                self._instrument_name_markup = instrument_name_markup
            else:
                self._instrument_name_markup = Markup(instrument_name_markup)
        return property(**locals())

    @property
    def lilypond_format(self):
        r'''LilyPond format of instrument mark.

        Returns string.
        '''
        result = []
        line = r'\set {}.instrumentName = {}'
        line = line.format(
            self._target_context_name, 
            self.instrument_name_markup,
            )
        result.append(line)
        line = r'\set {}.shortInstrumentName = {}'
        line = line.format(
            self._target_context_name, 
            self.short_instrument_name_markup,
            )
        result.append(line)
        return result

    @apply
    def short_instrument_name():
        def fget(self):
            r'''Gets and sets short instrument name.

            Returns string.
            '''
            if self._short_instrument_name is None:
                return self._default_short_instrument_name
            else:
                return self._short_instrument_name
        def fset(self, short_instrument_name):
            assert isinstance(short_instrument_name, (str, type(None)))
            self._short_instrument_name = short_instrument_name
        return property(**locals())

    @apply
    def short_instrument_name_markup():
        def fget(self):
            r'''Gets and sets short instrument name markup.

            Returns markup.
            '''
            if self._short_instrument_name_markup is None:
                if self._default_instrument_name_markup is None:
                    self._make_default_name_markups()
                markup = self._default_short_instrument_name_markup
                markup = copy.copy(markup)
                self._short_instrument_name_markup = markup
            return self._short_instrument_name_markup
        def fset(self, short_instrument_name_markup):
            from abjad.tools.markuptools import Markup
            assert isinstance(short_instrument_name_markup, 
                (str, type(Markup('')), type(None)))
            if short_instrument_name_markup is None:
                self._short_instrument_name_markup = \
                    short_instrument_name_markup
            else:
                self._short_instrument_name_markup = \
                    Markup(short_instrument_name_markup)
        return property(**locals())
