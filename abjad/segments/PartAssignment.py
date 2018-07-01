import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.utilities.String import String
from abjad.system.FormatSpecification import FormatSpecification
from .Part import Part


class PartAssignment(AbjadValueObject):
    """
    Part assignment.

    ..  container:: example

        >>> abjad.PartAssignment('Horn')
        PartAssignment('Horn')

        >>> abjad.PartAssignment('Horn', 1)
        PartAssignment('Horn', 1)

        >>> abjad.PartAssignment('Horn', 2)
        PartAssignment('Horn', 2)

        >>> abjad.PartAssignment('Horn', (3, 4))
        PartAssignment('Horn', (3, 4))

        >>> abjad.PartAssignment('Horn', [1, 3])
        PartAssignment('Horn', [1, 3])

    ..  container:: example

        >>> part_assignment = abjad.PartAssignment('Horn', [1, 3])

        >>> abjad.f(part_assignment)
        PartAssignment('Horn', [1, 3])

        >>> print(format(part_assignment))
        abjad.PartAssignment('Horn', [1, 3])
        
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_members',
        '_parts',
        '_section',
        '_token',
        )

    ### INITIALIZER ###

    token_type = typing.Union[
        None,
        int,
        typing.Tuple[int, int],
        typing.List[int],
        ]

    def __init__(
        self,
        section: str = None,
        token: token_type = None,
        ) -> None:
        self._section = section
        if token is not None:
            assert self._is_token(token), repr(token)
        self._token = token
        members = self._expand_members(token)
        self._members = members
        parts = self._expand_parts()
        assert isinstance(parts, list), repr(parts)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __contains__(self, part: Part) -> bool:
        """
        Is true when part assignment contains ``part``.

        ..  container:: example

            >>> parts = [
            ...     abjad.Part(section='Horn', member= 1),
            ...     abjad.Part(section='Horn', member= 2),
            ...     abjad.Part(section='Horn', member= 3),
            ...     abjad.Part(section='Horn', member= 4),
            ...     ]

            >>> part_assignment = abjad.PartAssignment('Horn')
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = abjad.PartAssignment('Horn', 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = abjad.PartAssignment('Horn', 2)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = abjad.PartAssignment('Horn', (3, 4))
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = abjad.PartAssignment('Horn', [1, 3])
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), False)

        ..  container:: example

            Raises exception when input is not part:

            >>> part_assignment = abjad.PartAssignment('Horn')
            >>> 'Horn' in part_assignment
            Traceback (most recent call last):
                ...
            TypeError: must be part (not 'Horn').

        """
        if not isinstance(part, Part):
            raise TypeError(f'must be part (not {part!r}).')
        if part.section == self.section:
            if (part.member is None or
                self.members is None or
                part.member in self.members or []):
                return True
            return False
        return False

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a part assignment with section and
        members equal to this part assignment.

        ..  container:: example

            >>> part_assignment_1 = abjad.PartAssignment('Horn', (1, 2))
            >>> part_assignment_2 = abjad.PartAssignment('Horn', [1, 2])
            >>> part_assignment_3 = abjad.PartAssignment('Horn')

            >>> part_assignment_1 == part_assignment_1
            True
            >>> part_assignment_1 == part_assignment_2
            True
            >>> part_assignment_1 == part_assignment_3
            False

            >>> part_assignment_2 == part_assignment_1
            True
            >>> part_assignment_2 == part_assignment_2
            True
            >>> part_assignment_2 == part_assignment_3
            False

            >>> part_assignment_3 == part_assignment_1
            False
            >>> part_assignment_3 == part_assignment_2
            False
            >>> part_assignment_3 == part_assignment_3
            True

        """
        if isinstance(argument, type(self)):
            if argument.section == self.section:
                return argument.members == self.members
        return False

    def __hash__(self) -> int:
        """
        Hashes part assignment.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates parts in assignment.
        
        ..  container:: example

            >>> part_assignment = abjad.PartAssignment('Horn', [1, 3])
            >>> for part in part_assignment:
            ...     part
            ... 
            Part(instrument='Horn', member=1, section='Horn')
            Part(instrument='Horn', member=3, section='Horn')

        """
        return iter(self.parts)

    ### PRIVATE METHODS ###

    @staticmethod
    def _expand_members(token):
        if token is None:
            return
        members = []
        if isinstance(token, int):
            members.append(token)
        elif isinstance(token, tuple):
            assert len(token) == 2, repr(token)
            for member in range(token[0], token[1] + 1):
                members.append(member)
        else:
            assert isinstance(token, list), repr(token)
            members.extend(token)
        return members

    def _expand_parts(self):
        parts = []
        if self.members is None:
            parts.append(Part(section=self.section))
        else:
            for member in self.members:
                part = Part(member=member, section=self.section)
                parts.append(part)
        return parts

    def _get_format_specification(self):
        repr_args_values = [self.section]
        if self.token is not None:
            repr_args_values.append(self.token)
        repr_is_indented = False
        repr_kwargs_names = []
        return FormatSpecification(
            self,
            repr_args_values=repr_args_values,
            repr_is_indented=repr_is_indented,
            repr_kwargs_names=repr_kwargs_names,
            storage_format_args_values=repr_args_values,
            storage_format_is_indented=repr_is_indented,
            storage_format_kwargs_names=repr_kwargs_names,
            )

    @staticmethod
    def _is_token(argument):
        if isinstance(argument, int) and 1 <= argument:
            return True
        if (isinstance(argument, tuple) and
            len(argument) == 2 and
            isinstance(argument[0], int) and
            isinstance(argument[1], int)):
            return True
        if isinstance(argument, list):
            for item in argument:
                if not isinstance(item, int):
                    return False
                if not 1 <= item:
                    return False
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def members(self) -> typing.Optional[typing.List[int]]:
        """
        Gets members.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').members is None
            True

            >>> abjad.PartAssignment('Horn', 1).members
            [1]

            >>> abjad.PartAssignment('Horn', 2).members
            [2]

            >>> abjad.PartAssignment('Horn', (3, 4)).members
            [3, 4]

            >>> abjad.PartAssignment('Horn', [1, 3]).members
            [1, 3]

        """
        return self._members

    @property
    def parts(self) -> typing.List[Part]:
        """
        Gets parts.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').parts
            [Part(instrument='Horn', section='Horn')]

            >>> abjad.PartAssignment('Horn', 1).parts
            [Part(instrument='Horn', member=1, section='Horn')]

            >>> abjad.PartAssignment('Horn', 2).parts
            [Part(instrument='Horn', member=2, section='Horn')]

            >>> abjad.PartAssignment('Horn', (3, 4)).parts
            [Part(instrument='Horn', member=3, section='Horn'), Part(instrument='Horn', member=4, section='Horn')]

            >>> abjad.PartAssignment('Horn', [1, 3]).parts
            [Part(instrument='Horn', member=1, section='Horn'), Part(instrument='Horn', member=3, section='Horn')]

        """
        return self._parts

    @property
    def section(self) -> typing.Optional[str]:
        """
        Gets section.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').section
            'Horn'

            >>> abjad.PartAssignment('Horn', 1).section
            'Horn'

            >>> abjad.PartAssignment('Horn', 2).section
            'Horn'

            >>> abjad.PartAssignment('Horn', (3, 4)).section
            'Horn'

            >>> abjad.PartAssignment('Horn', [1, 3]).section
            'Horn'

        """
        return self._section

    @property
    def token(self) -> token_type:
        """
        Gets token.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').token is None
            True

            >>> abjad.PartAssignment('Horn', 1).token
            1

            >>> abjad.PartAssignment('Horn', 2).token
            2

            >>> abjad.PartAssignment('Horn', (3, 4)).token
            (3, 4)

            >>> abjad.PartAssignment('Horn', [1, 3]).token
            [1, 3]

        """
        return self._token
