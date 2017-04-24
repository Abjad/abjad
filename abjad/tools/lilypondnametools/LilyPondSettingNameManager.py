# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondnametools.LilyPondNameManager \
    import LilyPondNameManager


class LilyPondSettingNameManager(LilyPondNameManager):
    '''LilyPond setting name manager.

    ..  container:: example

        Initializes with toplevel function:

        ::

            >>> note = Note("c'4")
            >>> set_(note)
            LilyPondSettingNameManager()

    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        r'''Gets arbitrary object keyed to `name`.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> set_(staff).instrument_name = Markup('Vn. I')
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    instrumentName = \markup { "Vn. I" }
                } {
                    c'4
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Returns arbitrary object keyed to `name`:

            ::

                >>> set_(staff).instrument_name
                Markup(contents=['Vn. I'])

        '''
        from abjad import ly
        from abjad.tools import lilypondnametools
        camel_name = stringtools.to_upper_camel_case(name)
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)
        elif camel_name in ly.contexts:
            try:
                return vars(self)['_' + name]
            except KeyError:
                context = lilypondnametools.LilyPondNameManager()
                vars(self)['_' + name] = context
                return context
        else:
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        from abjad.tools import lilypondnametools
        result = []
        for name, value in vars(self).items():
            if type(value) is lilypondnametools.LilyPondNameManager:
                prefixed_context_name = name
                context_name = prefixed_context_name.strip('_')
                context_proxy = value
                attribute_pairs = context_proxy._get_attribute_pairs()
                for attribute_name, attribute_value in attribute_pairs:
                    triple = (context_name, attribute_name, attribute_value)
                    result.append(triple)
            else:
                attribute_name, attribute_value = name, value
                result.append((attribute_name, attribute_value))
        return result
