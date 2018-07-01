import typing
from abjad.system.AbjadObject import AbjadObject
from abjad.utilities.String import String
from abjad.system.FormatSpecification import FormatSpecification
from .Part import Part


class Section(AbjadObject):
    """
    Section.

    ..  container:: example

        >>> abjad.Section(
        ...     abbreviation='VN-1',
        ...     count=18,
        ...     instrument='Violin',
        ...     name='FirstViolin',
        ...     )
        Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')

        >>> abjad.Section(
        ...     abbreviation='VN-2',
        ...     count=18,
        ...     instrument='Violin',
        ...     name='SecondViolin',
        ...     )
        Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        >>> abjad.Section(
        ...     abbreviation='VA',
        ...     count=18,
        ...     name='Viola',
        ...     )
        Section(abbreviation='VA', count=18, instrument='Viola', name='Viola')

        >>> abjad.Section(
        ...     abbreviation='VC',
        ...     count=14,
        ...     name='Cello',
        ...     )
        Section(abbreviation='VC', count=14, instrument='Cello', name='Cello')

        >>> abjad.Section(
        ...     abbreviation='CB',
        ...     count=6,
        ...     name='Contrabass',
        ...     )
        Section(abbreviation='CB', count=6, instrument='Contrabass', name='Contrabass')

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abbreviation',
        '_count',
        '_instrument',
        '_name',
        '_parts',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        abbreviation: str = None,
        count: int = 1,
        instrument: str = None,
        name: str = None,
        ) -> None:
        if abbreviation is not None:
            assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation
        if not isinstance(count, int):
            raise Exception(f'Count must be integer (not {count!r}).')
        if not 1 <= count:
            raise Exception(f'Count must be positive (not {count!r}).')
        self._count = count
        if instrument is not None:
            assert isinstance(instrument, str), repr(instrument)
        else:
            instrument = name
        self._instrument = instrument
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
        parts = []
        if self.count is None:
            part = Part(self.name)
            parts.append(part)
        else:
            if 1 < len(str(self.count)):
                zfill: typing.Optional[int] = len(str(self.count))
            else:
                zfill = None
            for member in range(1, self.count + 1):
                part = Part(
                    member=member,
                    instrument=self.instrument,
                    section=self.name,
                    section_abbreviation=self.abbreviation,
                    zfill=zfill,
                    )
                parts.append(part)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a section with the same name,
        abbreviation and count as this section.

        ..  container:: example

            >>> section_1 = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section_2 = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section_3 = abjad.Section(
            ...     abbreviation='VN-2',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='SecondViolin',
            ...     )

            >>> section_1 == section_1
            True
            >>> section_1 == section_2
            True
            >>> section_1 == section_3
            False

            >>> section_2 == section_1
            True
            >>> section_2 == section_2
            True
            >>> section_2 == section_3
            False

            >>> section_3 == section_1
            False
            >>> section_3 == section_2
            False
            >>> section_3 == section_3
            True

        """
        if (isinstance(argument, type(self)) and
            argument.name == self.name and
            argument.abbreviation == self.abbreviation and
            argument.count == self.count):
            return True
        return False

    def __hash__(self):
        """
        Hashes section.
        """
        return super().__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self) -> typing.Optional[str]:
        """
        Gets abbreviation.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.abbreviation
            'VN-1'

        """
        return self._abbreviation

    @property
    def count(self) -> typing.Optional[int]:
        """
        Gets section count.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.count
            18

        """
        return self._count

    @property
    def instrument(self) -> typing.Optional[str]:
        """
        Gets section instrument.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.instrument
            'Violin'

        """
        return self._instrument

    @property
    def name(self) -> typing.Optional[str]:
        """
        Gets section name.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.name
            'FirstViolin'

        """
        return self._name

    @property
    def parts(self) -> typing.List[Part]:
        """
        Gets parts.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> for part in section.parts:
            ...     part
            ...
            Part(instrument='Violin', member=1, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)

        """
        return list(self._parts)
