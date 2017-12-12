from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondCommand(AbjadValueObject):
    r'''LilyPond command.

    ..  container:: example

        Dotted slur:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> slur = abjad.Slur()
        >>> abjad.attach(slur, staff[:])
        >>> command = abjad.LilyPondCommand('slurDotted')
        >>> abjad.attach(command, staff[0])
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_format_slot',
        '_name',
        '_prefix',
        )

    _allowable_format_slots = (
        'after',
        'before',
        'closing',
        'opening',
        'right',
        )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(self, name=None, format_slot='opening', prefix='\\'):
        name = name or 'slurDotted'
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        assert isinstance(name, str), repr(name)
        self._name = name
        self._format_slot = format_slot
        assert isinstance(prefix, str), repr(prefix)
        self._prefix = prefix

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond command.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._get_lilypond_format()
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.name)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        names = []
        if not self.format_slot == 'opening':
            names.append('format_slot')
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=[self.name],
            storage_format_kwargs_names=names,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        import abjad
        command = self._name
        if command.startswith('#'):
            return command
        elif ' ' not in command:
            return self.prefix + abjad.String(command).to_lower_camel_case()
        else:
            return self.prefix + command

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        format_slot.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots():
        r'''Lists allowable format slots.

        ..  container:: example

            Default:

                >>> commands = abjad.LilyPondCommand.list_allowable_format_slots()
                >>> for command in commands:
                ...     command
                'after'
                'before'
                'closing'
                'opening'
                'right'

        Returns tuple of strings.
        '''
        return LilyPondCommand._allowable_format_slots

    ### PUBLIC PROPERTIES ###

    @property
    def format_slot(self):
        r'''Gets format slot of LilyPond command.

        ..  container:: example

            Dotted slur:

            >>> command = abjad.LilyPondCommand('slurDotted')
            >>> command.format_slot
            'opening'

        Defaults to `'opening'`.

        Returns string.
        '''
        return self._format_slot

    @property
    def name(self):
        r'''Gets name of LilyPond command.

        ..  container:: example

            Dotted slur:

            >>> command = abjad.LilyPondCommand('slurDotted')
            >>> command.name
            'slurDotted'

        Returns string.
        '''
        return self._name

    @property
    def prefix(self):
        r'''Gets prefix.

        Defaults to `'\\'`.

        Set to string.

        Returns string.
        '''
        return self._prefix
