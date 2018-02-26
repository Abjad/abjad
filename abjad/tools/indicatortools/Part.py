from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.String import String
from abjad.tools.systemtools.FormatSpecification import FormatSpecification


class Part(AbjadValueObject):
    r'''Part.

    ..  container:: example

        >>> abjad.Part('Horn')
        Part('Horn')

        >>> abjad.Part('Horn', 1)
        Part('Horn', 1)

        >>> abjad.Part('Horn', 2)
        Part('Horn', 2)

        >>> abjad.Part('Horn', (3, 4))
        Part('Horn', (3, 4))

        >>> abjad.Part('Horn', [1, 3])
        Part('Horn', [1, 3])

    ..  container:: example

        >>> part = abjad.Part('Horn', [1, 3])

        >>> abjad.f(part)
        Part('Horn', [1, 3])

        >>> print(format(part))
        abjad.Part('Horn', [1, 3])
        
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_members',
        '_section',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        section: str = None,
        members: Union[int, Tuple[int, int], List[int]] = None,
        ) -> None:
        self._members: Union[int, Tuple[int, int], List[int]] = members
        self._section: str = section

    ### SPECIAL METHODS ###

    def __contains__(self, argument: str) -> bool:
        r'''Is true when part contains ``argument``.

        ..  container:: example

            >>> part_names = ['Horn1', 'Horn2', 'Horn3', 'Horn4']

            >>> part = abjad.Part('Horn')
            >>> for part_name in part_names:
            ...     part_name, part_name in part
            ...
            ('Horn1', True)
            ('Horn2', True)
            ('Horn3', True)
            ('Horn4', True)

            >>> part = abjad.Part('Horn', 1)
            >>> for part_name in part_names:
            ...     part_name, part_name in part
            ...
            ('Horn1', True)
            ('Horn2', False)
            ('Horn3', False)
            ('Horn4', False)

            >>> part = abjad.Part('Horn', 2)
            >>> for part_name in part_names:
            ...     part_name, part_name in part
            ...
            ('Horn1', False)
            ('Horn2', True)
            ('Horn3', False)
            ('Horn4', False)

            >>> part = abjad.Part('Horn', (3, 4))
            >>> for part_name in part_names:
            ...     part_name, part_name in part
            ...
            ('Horn1', False)
            ('Horn2', False)
            ('Horn3', True)
            ('Horn4', True)

            >>> part = abjad.Part('Horn', [1, 3])
            >>> for part_name in part_names:
            ...     part_name, part_name in part
            ...
            ('Horn1', True)
            ('Horn2', False)
            ('Horn3', True)
            ('Horn4', False)

        ..  container:: example

            REGRESSION. Removes zfill:

            >>> part = abjad.Part('Horn', 1)
            >>> 'Horn1' in part
            True

            >>> 'Horn01' in part
            True


        '''
        if not isinstance(argument, str):
            return False
        argument = String(argument).remove_zfill()
        if self.members is None:
            if argument.startswith(self.section):
                return True
            else:
                return False
        part_names = self._expand()
        if argument in part_names:
            return True
        return False

    ### PRIVATE METHODS ###

    def _expand(self) -> List[str]:
        if self.members is None:
            return []
        if isinstance(self.members, int):
            members = [self.members]
        elif isinstance(self.members, tuple):
            assert len(self.members) == 2
            members = list(range(self.members[0], self.members[1] + 1))
        else:
            assert isinstance(self.members, list)
            members = self.members
        part_names_ = []
        for member in members:
            member_number = int(member)
            part_name = f'{self.section}{member_number}'
            part_names_.append(part_name)
        return part_names_

    def _get_format_specification(self):
        repr_args_values = [self.section]
        if self.members is not None:
            repr_args_values.append(self.members)
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

    ### PUBLIC PROPERTIES ###

    @property
    def members(self) -> Optional[Union[int, Tuple[int, int], List[int]]]:
        r'''Gets members.

        ..  container:: example

            >>> abjad.Part('Horn', [1, 3]).members
            [1, 3]

        '''
        return self._members

    @property
    def section(self) -> str:
        r'''Gets section.

        ..  container:: example

            >>> abjad.Part('Horn', [1, 3]).section
            'Horn'

        '''
        return self._section
