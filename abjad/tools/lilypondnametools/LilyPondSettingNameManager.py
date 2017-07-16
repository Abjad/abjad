# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.lilypondnametools.LilyPondNameManager \
    import LilyPondNameManager


class LilyPondSettingNameManager(LilyPondNameManager):
    '''LilyPond setting name manager.

    ::

        >>> import abjad

    ..  container:: example

        Initializes with toplevel function:

        ::

            >>> note = abjad.Note("c'4")
            >>> abjad.setting(note)
            LilyPondSettingNameManager()

    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        r'''Gets arbitrary object keyed to `name`.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> abjad.setting(staff).instrument_name = abjad.Markup('Vn. I')
                >>> show(staff) # doctest: +SKIP

            ..  docs::

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

                >>> abjad.setting(staff).instrument_name
                Markup(contents=['Vn. I'])

        '''
        from abjad import ly
        from abjad.tools import lilypondnametools
        camel_name = datastructuretools.String(name).to_upper_camel_case()
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
