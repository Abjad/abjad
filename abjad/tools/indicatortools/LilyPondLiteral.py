from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondLiteral(AbjadValueObject):
    r'''LilyPond literal.

    ..  container:: example

        Dotted slur:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> slur = abjad.Slur()
        >>> abjad.attach(slur, staff[:])
        >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
        >>> abjad.attach(literal, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \slurDotted
                c'8 (
                d'8
                e'8
                f'8 )
            }

    ..  container:: example

        Use the absolute before and absolute after format slots like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.attach(abjad.Slur(), staff[:])
        >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral('', format_slot='absolute_before')
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral(
        ...     '% before all formatting',
        ...     format_slot='absolute_before',
        ...     )
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral('', format_slot='absolute_after')
        >>> abjad.attach(literal, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
            <BLANKLINE>
                % before all formatting
                \slurDotted
                c'8 (
                d'8
                e'8
                f'8 )
            <BLANKLINE>
            }

    ..  container:: example

        LilyPond literals can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.attach(abjad.Slur(), staff[:])
        >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
        >>> abjad.attach(literal, staff[0], tag='RED')
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff {
            \slurDotted %! RED:1
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ..  container:: example

        Multiline input is allowed:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.attach(abjad.Slur(), staff[:])
        >>> lines = [
        ...     r'\stopStaff',
        ...     r'\startStaff',
        ...     r'\once \override Staff.StaffSymbol.color = #red',
        ...     ]
        >>> literal = abjad.LilyPondLiteral(lines)
        >>> abjad.attach(literal, staff[2], tag='RED')
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff {
            c'8 (
            d'8
            \stopStaff %! RED:1
            \startStaff %! RED:1
            \once \override Staff.StaffSymbol.color = #red %! RED:1
            e'8
            f'8 )
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_argument',
        '_format_slot',
        )

    _allowable_format_slots = (
        'absolute_after',
        'absolute_before',
        'after',
        'before',
        'closing',
        'opening',
        'right',
        )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(self, argument='', format_slot='opening'):
        self._argument = argument
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond literal.

        Returns string.
        '''
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self.argument
        return str(self)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        names = []
        if not self.format_slot == 'opening':
            names.append('format_slot')
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=[self.argument],
            storage_format_kwargs_names=names,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        if isinstance(self.argument, str):
            format_slot.commands.append(self.argument)
        elif isinstance(self.argument, list):
            format_slot.commands.extend(self.argument)
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots():
        r'''Lists allowable format slots.

        ..  container:: example

                >>> for slot in abjad.LilyPondLiteral.list_allowable_format_slots():
                ...     slot
                ...
                'absolute_after'
                'absolute_before'
                'after'
                'before'
                'closing'
                'opening'
                'right'

        Returns tuple.
        '''
        return LilyPondLiteral._allowable_format_slots

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self):
        r'''Gets argument of LilyPond literal.

        ..  container:: example

            >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
            >>> literal.argument
            '\\slurDotted'

        Returns string or list of string.
        '''
        return self._argument

    @property
    def format_slot(self):
        r'''Gets format slot of LilyPond literal.

        ..  container:: example

            >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
            >>> literal.format_slot
            'opening'

        Defaults to `'opening'`.

        Returns string.
        '''
        return self._format_slot
