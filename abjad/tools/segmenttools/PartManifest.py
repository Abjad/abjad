import typing
from abjad.tools.abctools.AbjadObject import AbjadObject
from .Part import Part
from .PartAssignment import PartAssignment


class PartManifest(AbjadObject):
    r'''Part manifest.

    ..  container:: example

        >>> part_manifest = abjad.PartManifest(
        ...    ('Piccolo', 'PICC'),
        ...    ('Flute1', 'FL-1'),
        ...    ('Flute2', 'FL-2'),
        ...    ('Flute3', 'FL-3'),
        ...    ('Oboe1', 'OB-1'),
        ...    ('Oboe2', 'OB-2'),
        ...    ('Oboe3', 'OB-3'),
        ...    ('EnglishHorn', 'EH'),
        ...    ('FirstViolin01', 'VN-1-1', 'Violin'),
        ...    ('FirstViolin02', 'VN-1-2', 'Violin'),
        ...    ('FirstViolin03', 'VN-1-3', 'Violin'),
        ...    ('FirstViolin04', 'VN-1-4', 'Violin'),
        ...    ('FirstViolin05', 'VN-1-5', 'Violin'),
        ...    ('FirstViolin06', 'VN-1-6', 'Violin'),
        ...    ('FirstViolin07', 'VN-1-7', 'Violin'),
        ...    ('FirstViolin08', 'VN-1-8', 'Violin'),
        ...    ('FirstViolin09', 'VN-1-9', 'Violin'),
        ...    ('FirstViolin10', 'VN-1-10', 'Violin'),
        ...    ('FirstViolin11', 'VN-1-11', 'Violin'),
        ...    ('FirstViolin12', 'VN-1-12', 'Violin'),
        ...    ('FirstViolin13', 'VN-1-13', 'Violin'),
        ...    ('FirstViolin14', 'VN-1-14', 'Violin'),
        ...    ('FirstViolin15', 'VN-1-15', 'Violin'),
        ...    ('FirstViolin16', 'VN-1-16', 'Violin'),
        ...    ('FirstViolin17', 'VN-1-17', 'Violin'),
        ...    ('FirstViolin18', 'VN-1-18', 'Violin'),
        ...    )

        >>> part_manifest
        PartManifest()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_parts',
        )

    ### INITIALIZER ###

    def __init__(self, *arguments):
        parts = []
        for argument in arguments:
            assert isinstance(argument, tuple), repr(argument)
            part = Part(*argument)
            parts.append(part)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __len__(self) -> int:
        r'''Gets number of parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    ('Piccolo', 'PICC'),
            ...    ('Flute1', 'FL-1'),
            ...    ('Flute2', 'FL-2'),
            ...    ('Flute3', 'FL-3'),
            ...    ('Oboe1', 'OB-1'),
            ...    ('Oboe2', 'OB-2'),
            ...    ('Oboe3', 'OB-3'),
            ...    ('EnglishHorn', 'EH'),
            ...    ('FirstViolin01', 'VN-1-1', 'Violin'),
            ...    ('FirstViolin02', 'VN-1-2', 'Violin'),
            ...    ('FirstViolin03', 'VN-1-3', 'Violin'),
            ...    ('FirstViolin04', 'VN-1-4', 'Violin'),
            ...    ('FirstViolin05', 'VN-1-5', 'Violin'),
            ...    ('FirstViolin06', 'VN-1-6', 'Violin'),
            ...    ('FirstViolin07', 'VN-1-7', 'Violin'),
            ...    ('FirstViolin08', 'VN-1-8', 'Violin'),
            ...    ('FirstViolin09', 'VN-1-9', 'Violin'),
            ...    ('FirstViolin10', 'VN-1-10', 'Violin'),
            ...    ('FirstViolin11', 'VN-1-11', 'Violin'),
            ...    ('FirstViolin12', 'VN-1-12', 'Violin'),
            ...    ('FirstViolin13', 'VN-1-13', 'Violin'),
            ...    ('FirstViolin14', 'VN-1-14', 'Violin'),
            ...    ('FirstViolin15', 'VN-1-15', 'Violin'),
            ...    ('FirstViolin16', 'VN-1-16', 'Violin'),
            ...    ('FirstViolin17', 'VN-1-17', 'Violin'),
            ...    ('FirstViolin18', 'VN-1-18', 'Violin'),
            ...    )

            >>> len(part_manifest)
            26

        '''
        return len(self.parts)

    ### PUBLIC PROPERTIES ###

    @property
    def names(self) -> typing.List[str]:
        r'''Gets part names.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    ('Piccolo', 'PICC'),
            ...    ('Flute1', 'FL-1'),
            ...    ('Flute2', 'FL-2'),
            ...    ('Flute3', 'FL-3'),
            ...    ('Oboe1', 'OB-1'),
            ...    ('Oboe2', 'OB-2'),
            ...    ('Oboe3', 'OB-3'),
            ...    ('EnglishHorn', 'EH'),
            ...    ('FirstViolin01', 'VN-1-1', 'Violin'),
            ...    ('FirstViolin02', 'VN-1-2', 'Violin'),
            ...    ('FirstViolin03', 'VN-1-3', 'Violin'),
            ...    ('FirstViolin04', 'VN-1-4', 'Violin'),
            ...    ('FirstViolin05', 'VN-1-5', 'Violin'),
            ...    ('FirstViolin06', 'VN-1-6', 'Violin'),
            ...    ('FirstViolin07', 'VN-1-7', 'Violin'),
            ...    ('FirstViolin08', 'VN-1-8', 'Violin'),
            ...    ('FirstViolin09', 'VN-1-9', 'Violin'),
            ...    ('FirstViolin10', 'VN-1-10', 'Violin'),
            ...    ('FirstViolin11', 'VN-1-11', 'Violin'),
            ...    ('FirstViolin12', 'VN-1-12', 'Violin'),
            ...    ('FirstViolin13', 'VN-1-13', 'Violin'),
            ...    ('FirstViolin14', 'VN-1-14', 'Violin'),
            ...    ('FirstViolin15', 'VN-1-15', 'Violin'),
            ...    ('FirstViolin16', 'VN-1-16', 'Violin'),
            ...    ('FirstViolin17', 'VN-1-17', 'Violin'),
            ...    ('FirstViolin18', 'VN-1-18', 'Violin'),
            ...    )

            >>> for name in part_manifest.names:
            ...     name
            ...
            'Piccolo'
            'Flute1'
            'Flute2'
            'Flute3'
            'Oboe1'
            'Oboe2'
            'Oboe3'
            'EnglishHorn'
            'FirstViolin01'
            'FirstViolin02'
            'FirstViolin03'
            'FirstViolin04'
            'FirstViolin05'
            'FirstViolin06'
            'FirstViolin07'
            'FirstViolin08'
            'FirstViolin09'
            'FirstViolin10'
            'FirstViolin11'
            'FirstViolin12'
            'FirstViolin13'
            'FirstViolin14'
            'FirstViolin15'
            'FirstViolin16'
            'FirstViolin17'
            'FirstViolin18'

        '''
        names = []
        for part in self.parts:
            names.append(part.name)
        return names

    @property
    def parts(self) -> typing.List[Part]:
        r'''Gets parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    ('Piccolo', 'PICC'),
            ...    ('Flute1', 'FL-1'),
            ...    ('Flute2', 'FL-2'),
            ...    ('Flute3', 'FL-3'),
            ...    ('Oboe1', 'OB-1'),
            ...    ('Oboe2', 'OB-2'),
            ...    ('Oboe3', 'OB-3'),
            ...    ('EnglishHorn', 'EH'),
            ...    ('FirstViolin01', 'VN-1-1', 'Violin'),
            ...    ('FirstViolin02', 'VN-1-2', 'Violin'),
            ...    ('FirstViolin03', 'VN-1-3', 'Violin'),
            ...    ('FirstViolin04', 'VN-1-4', 'Violin'),
            ...    ('FirstViolin05', 'VN-1-5', 'Violin'),
            ...    ('FirstViolin06', 'VN-1-6', 'Violin'),
            ...    ('FirstViolin07', 'VN-1-7', 'Violin'),
            ...    ('FirstViolin08', 'VN-1-8', 'Violin'),
            ...    ('FirstViolin09', 'VN-1-9', 'Violin'),
            ...    ('FirstViolin10', 'VN-1-10', 'Violin'),
            ...    ('FirstViolin11', 'VN-1-11', 'Violin'),
            ...    ('FirstViolin12', 'VN-1-12', 'Violin'),
            ...    ('FirstViolin13', 'VN-1-13', 'Violin'),
            ...    ('FirstViolin14', 'VN-1-14', 'Violin'),
            ...    ('FirstViolin15', 'VN-1-15', 'Violin'),
            ...    ('FirstViolin16', 'VN-1-16', 'Violin'),
            ...    ('FirstViolin17', 'VN-1-17', 'Violin'),
            ...    ('FirstViolin18', 'VN-1-18', 'Violin'),
            ...    )

            >>> for part in part_manifest.parts:
            ...     part
            ...
            Part(name='Piccolo', abbreviation='PICC')
            Part(name='Flute1', abbreviation='FL-1')
            Part(name='Flute2', abbreviation='FL-2')
            Part(name='Flute3', abbreviation='FL-3')
            Part(name='Oboe1', abbreviation='OB-1')
            Part(name='Oboe2', abbreviation='OB-2')
            Part(name='Oboe3', abbreviation='OB-3')
            Part(name='EnglishHorn', abbreviation='EH')
            Part(name='FirstViolin01', abbreviation='VN-1-1', instrument_name='Violin')
            Part(name='FirstViolin02', abbreviation='VN-1-2', instrument_name='Violin')
            Part(name='FirstViolin03', abbreviation='VN-1-3', instrument_name='Violin')
            Part(name='FirstViolin04', abbreviation='VN-1-4', instrument_name='Violin')
            Part(name='FirstViolin05', abbreviation='VN-1-5', instrument_name='Violin')
            Part(name='FirstViolin06', abbreviation='VN-1-6', instrument_name='Violin')
            Part(name='FirstViolin07', abbreviation='VN-1-7', instrument_name='Violin')
            Part(name='FirstViolin08', abbreviation='VN-1-8', instrument_name='Violin')
            Part(name='FirstViolin09', abbreviation='VN-1-9', instrument_name='Violin')
            Part(name='FirstViolin10', abbreviation='VN-1-10', instrument_name='Violin')
            Part(name='FirstViolin11', abbreviation='VN-1-11', instrument_name='Violin')
            Part(name='FirstViolin12', abbreviation='VN-1-12', instrument_name='Violin')
            Part(name='FirstViolin13', abbreviation='VN-1-13', instrument_name='Violin')
            Part(name='FirstViolin14', abbreviation='VN-1-14', instrument_name='Violin')
            Part(name='FirstViolin15', abbreviation='VN-1-15', instrument_name='Violin')
            Part(name='FirstViolin16', abbreviation='VN-1-16', instrument_name='Violin')
            Part(name='FirstViolin17', abbreviation='VN-1-17', instrument_name='Violin')
            Part(name='FirstViolin18', abbreviation='VN-1-18', instrument_name='Violin')

        '''
        return list(self._parts)

    ### PUBLIC METHODS ###

    def expand(self, part_assignment: PartAssignment) -> typing.List[Part]:
        r'''Expands ``part_assignment``.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    ('Piccolo', 'PICC'),
            ...    ('Flute1', 'FL-1'),
            ...    ('Flute2', 'FL-2'),
            ...    ('Flute3', 'FL-3'),
            ...    ('Oboe1', 'OB-1'),
            ...    ('Oboe2', 'OB-2'),
            ...    ('Oboe3', 'OB-3'),
            ...    ('EnglishHorn', 'EH'),
            ...    ('FirstViolin01', 'VN-1-1', 'Violin'),
            ...    ('FirstViolin02', 'VN-1-2', 'Violin'),
            ...    ('FirstViolin03', 'VN-1-3', 'Violin'),
            ...    ('FirstViolin04', 'VN-1-4', 'Violin'),
            ...    ('FirstViolin05', 'VN-1-5', 'Violin'),
            ...    ('FirstViolin06', 'VN-1-6', 'Violin'),
            ...    ('FirstViolin07', 'VN-1-7', 'Violin'),
            ...    ('FirstViolin08', 'VN-1-8', 'Violin'),
            ...    ('FirstViolin09', 'VN-1-9', 'Violin'),
            ...    ('FirstViolin10', 'VN-1-10', 'Violin'),
            ...    ('FirstViolin11', 'VN-1-11', 'Violin'),
            ...    ('FirstViolin12', 'VN-1-12', 'Violin'),
            ...    ('FirstViolin13', 'VN-1-13', 'Violin'),
            ...    ('FirstViolin14', 'VN-1-14', 'Violin'),
            ...    ('FirstViolin15', 'VN-1-15', 'Violin'),
            ...    ('FirstViolin16', 'VN-1-16', 'Violin'),
            ...    ('FirstViolin17', 'VN-1-17', 'Violin'),
            ...    ('FirstViolin18', 'VN-1-18', 'Violin'),
            ...    )

            >>> part_assignment = abjad.PartAssignment('Oboe')
            >>> for part in part_manifest.expand(part_assignment):
            ...     part
            ...
            Part(name='Oboe1', abbreviation='OB-1')
            Part(name='Oboe2', abbreviation='OB-2')
            Part(name='Oboe3', abbreviation='OB-3')

            >>> part_assignment = abjad.PartAssignment('FirstViolin', (10, 18))
            >>> for part in part_manifest.expand(part_assignment):
            ...     part
            ...
            Part(name='FirstViolin10', abbreviation='VN-1-10', instrument_name='Violin')
            Part(name='FirstViolin11', abbreviation='VN-1-11', instrument_name='Violin')
            Part(name='FirstViolin12', abbreviation='VN-1-12', instrument_name='Violin')
            Part(name='FirstViolin13', abbreviation='VN-1-13', instrument_name='Violin')
            Part(name='FirstViolin14', abbreviation='VN-1-14', instrument_name='Violin')
            Part(name='FirstViolin15', abbreviation='VN-1-15', instrument_name='Violin')
            Part(name='FirstViolin16', abbreviation='VN-1-16', instrument_name='Violin')
            Part(name='FirstViolin17', abbreviation='VN-1-17', instrument_name='Violin')
            Part(name='FirstViolin18', abbreviation='VN-1-18', instrument_name='Violin')

        '''
        section = self.section(part_assignment.section)
        if not section:
            message = f'Section {part_assignment.section} not found'
            message += ' in manifest.'
            raise Exception(message)
        parts = []
        for part in section:
            if part.name in part_assignment:
                parts.append(part)
        return parts

    def section(self, section: str) -> typing.List[Part]:
        r'''Gets parts in section

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    ('Piccolo', 'PICC'),
            ...    ('Flute1', 'FL-1'),
            ...    ('Flute2', 'FL-2'),
            ...    ('Flute3', 'FL-3'),
            ...    ('Oboe1', 'OB-1'),
            ...    ('Oboe2', 'OB-2'),
            ...    ('Oboe3', 'OB-3'),
            ...    ('EnglishHorn', 'EH'),
            ...    ('FirstViolin01', 'VN-1-1', 'Violin'),
            ...    ('FirstViolin02', 'VN-1-2', 'Violin'),
            ...    ('FirstViolin03', 'VN-1-3', 'Violin'),
            ...    ('FirstViolin04', 'VN-1-4', 'Violin'),
            ...    ('FirstViolin05', 'VN-1-5', 'Violin'),
            ...    ('FirstViolin06', 'VN-1-6', 'Violin'),
            ...    ('FirstViolin07', 'VN-1-7', 'Violin'),
            ...    ('FirstViolin08', 'VN-1-8', 'Violin'),
            ...    ('FirstViolin09', 'VN-1-9', 'Violin'),
            ...    ('FirstViolin10', 'VN-1-10', 'Violin'),
            ...    ('FirstViolin11', 'VN-1-11', 'Violin'),
            ...    ('FirstViolin12', 'VN-1-12', 'Violin'),
            ...    ('FirstViolin13', 'VN-1-13', 'Violin'),
            ...    ('FirstViolin14', 'VN-1-14', 'Violin'),
            ...    ('FirstViolin15', 'VN-1-15', 'Violin'),
            ...    ('FirstViolin16', 'VN-1-16', 'Violin'),
            ...    ('FirstViolin17', 'VN-1-17', 'Violin'),
            ...    ('FirstViolin18', 'VN-1-18', 'Violin'),
            ...    )

            >>> for part in part_manifest.section('Oboe'):
            ...     part
            ...
            Part(name='Oboe1', abbreviation='OB-1')
            Part(name='Oboe2', abbreviation='OB-2')
            Part(name='Oboe3', abbreviation='OB-3')

            >>> for part in part_manifest.section('FirstViolin'):
            ...     part
            ...
            Part(name='FirstViolin01', abbreviation='VN-1-1', instrument_name='Violin')
            Part(name='FirstViolin02', abbreviation='VN-1-2', instrument_name='Violin')
            Part(name='FirstViolin03', abbreviation='VN-1-3', instrument_name='Violin')
            Part(name='FirstViolin04', abbreviation='VN-1-4', instrument_name='Violin')
            Part(name='FirstViolin05', abbreviation='VN-1-5', instrument_name='Violin')
            Part(name='FirstViolin06', abbreviation='VN-1-6', instrument_name='Violin')
            Part(name='FirstViolin07', abbreviation='VN-1-7', instrument_name='Violin')
            Part(name='FirstViolin08', abbreviation='VN-1-8', instrument_name='Violin')
            Part(name='FirstViolin09', abbreviation='VN-1-9', instrument_name='Violin')
            Part(name='FirstViolin10', abbreviation='VN-1-10', instrument_name='Violin')
            Part(name='FirstViolin11', abbreviation='VN-1-11', instrument_name='Violin')
            Part(name='FirstViolin12', abbreviation='VN-1-12', instrument_name='Violin')
            Part(name='FirstViolin13', abbreviation='VN-1-13', instrument_name='Violin')
            Part(name='FirstViolin14', abbreviation='VN-1-14', instrument_name='Violin')
            Part(name='FirstViolin15', abbreviation='VN-1-15', instrument_name='Violin')
            Part(name='FirstViolin16', abbreviation='VN-1-16', instrument_name='Violin')
            Part(name='FirstViolin17', abbreviation='VN-1-17', instrument_name='Violin')
            Part(name='FirstViolin18', abbreviation='VN-1-18', instrument_name='Violin')

            >>> part_manifest.section('Contrabass')
            []

        '''
        parts = []
        for part in self.parts:
            if part.section == section:
                parts.append(part)
        return parts
