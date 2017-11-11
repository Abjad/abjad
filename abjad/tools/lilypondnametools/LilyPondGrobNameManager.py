from abjad.tools.lilypondnametools.LilyPondNameManager \
    import LilyPondNameManager


class LilyPondGrobNameManager(LilyPondNameManager):
    '''LilyPond grob name manager.

    ..  container:: example

        Initializes with toplevel override function:

        >>> note = abjad.Note("c'4")
        >>> abjad.override(note)
        LilyPondGrobNameManager()

    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        r'''Gets LilyPond name manager keyed to `name`.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff).note_head.color = 'red'
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override NoteHead.color = #red
                } {
                    c'4
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Returns LilyPond name manager:

            >>> abjad.override(staff).note_head
            LilyPondNameManager(('color', 'red'))

        '''
        import abjad
        from abjad import ly
        from abjad.tools import lilypondnametools
        camel_name = abjad.String(name).to_upper_camel_case()
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
                context = lilypondnametools.LilyPondGrobNameManager()
                vars(self)['_' + name] = context
                return context
        elif camel_name in ly.grob_interfaces:
            try:
                return vars(self)[name]
            except KeyError:
                vars(self)[name] = lilypondnametools.LilyPondNameManager()
                return vars(self)[name]
        else:
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)

    def __setattr__(self, attribute, value):
        r'''Sets attribute `attribute` of grob name manager to `value`.

        Returns none.
        '''
        # make sure attribute name is valid grob name before setting value
        object.__setattr__(self, attribute, value)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        import abjad
        result = []
        for name, value in vars(self).items():
            if type(value) is abjad.LilyPondNameManager:
                grob, grob_proxy = name, value
                pairs = iter(vars(grob_proxy).items())
                for attribute, value in pairs:
                    triple = (grob, attribute, value)
                    result.append(triple)
            else:
                context, context_proxy = name.strip('_'), value
                for grob, grob_proxy in vars(context_proxy).items():
                    pairs = iter(vars(grob_proxy).items())
                    for attribute, value in pairs:
                        quadruple = (
                            context,
                            grob,
                            attribute,
                            value,
                            )
                        result.append(quadruple)
        return tuple(result)

    def _list_format_contributions(self, contribution_type, once=False):
        from abjad.tools import systemtools
        manager = systemtools.LilyPondFormatManager
        assert contribution_type in ('override', 'revert')
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 3:
                context = None
                grob = attribute_tuple[0]
                attribute = attribute_tuple[1]
                value = attribute_tuple[2]
            elif len(attribute_tuple) == 4:
                context = attribute_tuple[0]
                grob = attribute_tuple[1]
                attribute = attribute_tuple[2]
                value = attribute_tuple[3]
            else:
                message = 'invalid attribute tuple: {!r}.'
                message = message.format(attribute_tuple)
                raise ValueError(message)
            if contribution_type == 'override':
                override_string = manager.make_lilypond_override_string(
                    grob,
                    attribute,
                    value,
                    context=context,
                    once=once,
                    )
                result.append(override_string)
            else:
                revert_string = manager.make_lilypond_revert_string(
                    grob,
                    attribute,
                    context=context,
                    )
                result.append(revert_string)
        result.sort()
        return result

    def _make_override_dictionary(self):
        result = {}
        grob_override_tuples = self._get_attribute_tuples()
        for grob_override_tuple in grob_override_tuples:
            most = '__'.join(grob_override_tuple[:-1])
            value = grob_override_tuple[-1]
            attribute = '_tools_package_qualified_repr'
            value = getattr(value, attribute, repr(value))
            result[most] = value
        return result
