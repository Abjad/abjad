import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.String import String
from abjad.tools.systemtools.FormatSpecification import FormatSpecification
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.tools.systemtools.StorageFormatManager import StorageFormatManager


class LilyPondCommand(AbjadValueObject):
    r'''
    LilyPond command.

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
            \new Staff
            {
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
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

    def __init__(
        self,
        name: str = None,
        format_slot: str = 'opening',
        *,
        prefix: str = '\\',
        ) -> None:
        name = name or 'slurDotted'
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        assert isinstance(name, str), repr(name)
        self._name = name
        self._format_slot = format_slot
        assert isinstance(prefix, str), repr(prefix)
        self._prefix = prefix

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        r'''Formats LilyPond command.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.
        '''
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        assert format_specification == 'lilypond', repr(format_specification)
        return self._get_lilypond_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.name)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        names = []
        if not self.format_slot == 'opening':
            names.append('format_slot')
        return FormatSpecification(
            client=self,
            storage_format_args_values=[self.name],
            storage_format_kwargs_names=names,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        command = self._name
        if command.startswith('#'):
            return command
        elif ' ' not in command:
            return self.prefix + String(command).to_lower_camel_case()
        else:
            return self.prefix + command

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        format_slot.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def format_slot(self) -> str:
        '''
        Gets format slot of LilyPond command.

        ..  container:: example

            Dotted slur:

            >>> command = abjad.LilyPondCommand('slurDotted')
            >>> command.format_slot
            'opening'

        '''
        return self._format_slot

    @property
    def name(self) -> str:
        '''
        Gets name of LilyPond command.

        ..  container:: example

            Dotted slur:

            >>> command = abjad.LilyPondCommand('slurDotted')
            >>> command.name
            'slurDotted'

        '''
        return self._name

    @property
    def prefix(self) -> str:
        '''
        Gets prefix.
        '''
        return self._prefix

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots() -> typing.Tuple[str, ...]:
        '''
        Lists allowable format slots.

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

        '''
        return LilyPondCommand._allowable_format_slots
