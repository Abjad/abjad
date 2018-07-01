import typing
from abjad.system.AbjadObject import AbjadObject
from abjad.utilities.String import String
from abjad.system.FormatSpecification import FormatSpecification


class Part(AbjadObject):
    """
    Part.

    ..  container:: example

        >>> part = abjad.Part(
        ...     member=18,
        ...     section='FirstViolin',
        ...     section_abbreviation='VN-1',
        ...     )
        
        >>> abjad.f(part)
        abjad.Part(
            instrument='FirstViolin',
            member=18,
            section='FirstViolin',
            section_abbreviation='VN-1',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_section_abbreviation',
        '_instrument',
        '_member',
        '_name',
        '_number',
        '_section',
        '_zfill',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        instrument: str = None,
        member: int = None,
        number: int = None,
        section: str = None,
        section_abbreviation: str = None,
        zfill: int = None,
        ) -> None:
        instrument = instrument or section
        if instrument is not None:
            if not isinstance(instrument, str):
                message = 'instrument must be string'
                message += f' (not {instrument!r}).'
                raise Exception(message)
        self._instrument = instrument
        if member is not None:
            if not isinstance(member, int):
                message = 'member must be integer'
                message += f' (not {member!r}).'
                raise Exception(message)
        self._member = member
        if number is not None:
            assert isinstance(number, int), repr(number)
            assert 1 <= number, repr(number)
        self._number = number
        if section is not None:
            if not isinstance(section, str):
                raise Exception(f'section must be string (not {section!r}).')
        self._section = section
        if section_abbreviation is not None:
            if not isinstance(section_abbreviation, str):
                message = 'section_abbreviation must be string'
                message += f' (not {section_abbreviation!r}).'
                raise Exception(message)
        self._section_abbreviation = section_abbreviation
        if zfill is not None:
            assert isinstance(zfill, int), repr(zfill)
            assert 1 <= zfill, repr(zfill)
        self._zfill = zfill
        if member is not None:
            member_ = str(member)
            if self.zfill is not None:
                member_ = member_.zfill(self.zfill)
            name: typing.Optional[str] = f'{section}{member_}'
        else:
            name = section
        self._name = name

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a part with the same section and
        member as this part.

        ..  container:: example

            >>> part_1 = abjad.Part(
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            >>> part_2 = abjad.Part(
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            >>> part_3 = abjad.Part(
            ...     member=18,
            ...     section='SecondViolin',
            ...     section_abbreviation='VN-2',
            ...     )

            >>> part_1 == part_1
            True
            >>> part_1 == part_2
            True
            >>> part_1 == part_3
            False

            >>> part_2 == part_1
            True
            >>> part_2 == part_2
            True
            >>> part_2 == part_3
            False

            >>> part_3 == part_1
            False
            >>> part_3 == part_2
            False
            >>> part_3 == part_3
            True

        """
        if isinstance(argument, type(self)):
            if argument.section == self.section:
                return argument.member == self.member
        return False

    def __hash__(self):
        """
        Hashes part.
        """
        return super().__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self) -> str:
        """
        Gets identifier.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.identifier
            'VN-1-18'

        """
        assert isinstance(self.section_abbreviation, str)
        if self.member is None:
            return self.section_abbreviation
        else:
            assert isinstance(self.member, int)
            return f'{self.section_abbreviation}-{self.member}'

    @property
    def instrument(self) -> typing.Optional[str]:
        """
        Gets instrument.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.instrument
            'Violin'

        """
        return self._instrument

    @property
    def member(self) -> typing.Optional[int]:
        """
        Gets member.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.member
            18

        """
        return self._member

    @property
    def name(self) -> typing.Optional[str]:
        """
        Gets name.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=1,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.name
            'FirstViolin1'

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=1,
            ...     zfill=2,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.name
            'FirstViolin01'

        """
        return self._name

    @property
    def number(self) -> typing.Optional[int]:
        """
        Gets number.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     number=107,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            
            >>> part.number
            107

        """
        return self._number

    @property
    def section(self) -> typing.Optional[str]:
        """
        Gets section.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.section
            'FirstViolin'

        """
        return self._section

    @property
    def section_abbreviation(self) -> typing.Optional[str]:
        """
        Gets section_abbreviation.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.section_abbreviation
            'VN-1'

        """
        return self._section_abbreviation

    @property
    def zfill(self) -> typing.Optional[int]:
        """
        Gets zfill.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=9,
            ...     number=99,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     zfill=2,
            ...     )
            
            >>> part.zfill
            2

            >>> str(part.member).zfill(part.zfill)
            '09'

        """
        return self._zfill
