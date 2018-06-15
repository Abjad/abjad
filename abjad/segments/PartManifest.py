import typing
from abjad.system.AbjadObject import AbjadObject
from .Part import Part
from .PartAssignment import PartAssignment
from .Section import Section


class PartManifest(AbjadObject):
    """
    Part manifest.

    ..  container:: example

        Initializes from parts:

        >>> part_manifest = abjad.PartManifest(
        ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
        ...    abjad.Part(section='Violin', section_abbreviation='VN'),
        ...    abjad.Part(section='Viola', section_abbreviation='VA'),
        ...    abjad.Part(section='Cello', section_abbreviation='VC'),
        ...    )
        >>> len(part_manifest)
        4

    ..  container:: example

        Initializes from orchestra sections:

        >>> part_manifest = abjad.PartManifest(
        ...    abjad.Section(
        ...         abbreviation='FL',
        ...         count=4,
        ...         name='Flute',
        ...         ),
        ...    abjad.Section(
        ...         abbreviation='OB',
        ...         count=3,
        ...         name='Oboe',
        ...         ),
        ...    abjad.Part(
        ...         section_abbreviation='EH',
        ...         section='EnglishHorn',
        ...         ),
        ...    abjad.Section(
        ...         abbreviation='VN-1',
        ...         count=18,
        ...         instrument='Violin',
        ...         name='FirstViolin',
        ...         ),
        ...    abjad.Section(
        ...         abbreviation='VN-2',
        ...         count=18,
        ...         instrument='Violin',
        ...         name='SecondViolin',
        ...         ),
        ...    )
        >>> len(part_manifest)
        44

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_parts',
        '_sections',
        )

    ### INITIALIZER ###

    def __init__(self, *arguments):
        parts, sections = [], []
        for argument in arguments:
            if isinstance(argument, Part):
                parts.append(argument)
            elif isinstance(argument, Section):
                sections.append(argument)
                parts.extend(argument.parts)
            else:
                raise TypeError(f'must be part or section (not {argument}).')
        for i, part in enumerate(parts):
            number = i + 1
            part._number = number
        self._parts = parts
        self._sections = sections

    ### SPECIAL METHODS ###

    def __iter__(self) -> typing.Iterator:
        """
        Iterates parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL')
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')
            Part(instrument='EnglishHorn', number=8, section='EnglishHorn', section_abbreviation='EH')
            Part(instrument='Violin', member=1, number=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, number=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, number=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, number=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, number=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, number=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, number=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, number=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, number=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, number=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, number=19, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, number=20, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, number=21, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, number=22, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, number=23, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, number=24, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, number=25, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, number=26, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=1, number=27, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=2, number=28, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=3, number=29, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=4, number=30, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=5, number=31, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=6, number=32, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=7, number=33, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=8, number=34, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=9, number=35, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=10, number=36, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=11, number=37, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=12, number=38, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=13, number=39, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=14, number=40, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=15, number=41, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=16, number=42, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=17, number=43, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=18, number=44, section='SecondViolin', section_abbreviation='VN-2', zfill=2)

        """
        return iter(self.parts)

    def __len__(self) -> int:
        """
        Gets number of parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    abjad.Part(section='Violin', section_abbreviation='VN'),
            ...    abjad.Part(section='Viola', section_abbreviation='VA'),
            ...    abjad.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> len(part_manifest)
            4

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> len(part_manifest)
            44

        """
        return len(self.parts)

    ### PUBLIC PROPERTIES ###

    @property
    def parts(self) -> typing.List[Part]:
        """
        Gets parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    abjad.Part(section='Violin', section_abbreviation='VN'),
            ...    abjad.Part(section='Viola', section_abbreviation='VA'),
            ...    abjad.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='BassClarinet', number=1, section='BassClarinet', section_abbreviation='BCL')
            Part(instrument='Violin', number=2, section='Violin', section_abbreviation='VN')
            Part(instrument='Viola', number=3, section='Viola', section_abbreviation='VA')
            Part(instrument='Cello', number=4, section='Cello', section_abbreviation='VC')

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for part in part_manifest.parts:
            ...     part
            ...
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL')
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')
            Part(instrument='EnglishHorn', number=8, section='EnglishHorn', section_abbreviation='EH')
            Part(instrument='Violin', member=1, number=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, number=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, number=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, number=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, number=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, number=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, number=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, number=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, number=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, number=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, number=19, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, number=20, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, number=21, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, number=22, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, number=23, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, number=24, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, number=25, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, number=26, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=1, number=27, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=2, number=28, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=3, number=29, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=4, number=30, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=5, number=31, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=6, number=32, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=7, number=33, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=8, number=34, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=9, number=35, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=10, number=36, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=11, number=37, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=12, number=38, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=13, number=39, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=14, number=40, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=15, number=41, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=16, number=42, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=17, number=43, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=18, number=44, section='SecondViolin', section_abbreviation='VN-2', zfill=2)

        ..  container:: example

            >>> abjad.Part(section='FirstViolin', member=18) in part_manifest.parts
            True

            >>> abjad.Part(section='FirstViolin', member=19) in part_manifest.parts
            False

        """
        return list(self._parts)

    @property
    def sections(self) -> typing.List[Section]:
        """
        Gets sections in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    abjad.Part(section='Violin', section_abbreviation='VN'),
            ...    abjad.Part(section='Viola', section_abbreviation='VA'),
            ...    abjad.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> part_manifest.sections
            []

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for section in part_manifest.sections:
            ...     section
            ...
            Section(abbreviation='FL', count=4, instrument='Flute', name='Flute')
            Section(abbreviation='OB', count=3, instrument='Oboe', name='Oboe')
            Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')
            Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section in part_manifest.sections
            True

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=36,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section in part_manifest.sections
            False

        """
        return list(self._sections)

    ### PUBLIC METHODS ###

    def expand(self, part_assignment):
        """
        Expands ``part_assignment``.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> part_assignment = abjad.PartAssignment('Oboe')
            >>> for part in part_manifest.expand(part_assignment):
            ...     part
            ...
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')

        """
        assert isinstance(part_assignment, PartAssignment)
        parts = []
        for part in self.parts:
            if part.section == part_assignment.section:
                if part_assignment.token is None:
                    parts.append(part)
                elif part.member in part_assignment.members:
                    parts.append(part)
        return parts
