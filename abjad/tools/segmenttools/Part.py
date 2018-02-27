import typing
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.datastructuretools.String import String


class Part(AbjadObject):
    r'''Part.

    ..  container:: example

        >>> part = abjad.Part('FirstViolin01', 'VN-1-1', 'Violin')
        
        >>> abjad.f(part)
        abjad.Part(
            name='FirstViolin01',
            abbreviation='VN-1-1',
            instrument_name='Violin',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abbreviation',
        '_instrument_name',
        '_name',
        '_number',
        '_section',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        name: str = None,
        abbreviation: str = None,
        instrument_name: str = None,
        ) -> None:
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
        if abbreviation is not None:
            assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation
        if instrument_name is not None:
            assert isinstance(instrument_name, str), repr(instrument_name)
        self._instrument_name = instrument_name
        words = String(name).delimit_words()
        try:
            number = int(words[-1])
        except ValueError:
            number = None
        self._number = number
        if name is not None:
            section = name.strip('0123456789')
        else:
            section = None
        self._section = section

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        r'''Is true when ``argument`` is a part with same name as this part.

        ..  container:: example

            >>> part_1 = abjad.Part('FirstViolin01')
            >>> part_2 = abjad.Part('FirstViolin01', 'VN-1-1')
            >>> part_3 = abjad.Part('Piccolo')

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

        '''
        if isinstance(argument, type(self)):
            return argument.name == self.name
        return False

    def __hash__(self):
        r'''Hashes part.
        '''
        return super(Part, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self) -> typing.Optional[str]:
        r'''Gets abbreviation.

        ..  container:: example

            >>> abjad.Part('FirstViolin01', 'VN-1-1', 'Violin').abbreviation
            'VN-1-1'

        '''
        return self._abbreviation

    @property
    def instrument_name(self) -> typing.Optional[str]:
        r'''Gets instrument name.

        ..  container:: example

            >>> abjad.Part('FirstViolin01', 'VN-1-1', 'Violin').instrument_name
            'Violin'

        '''
        return self._instrument_name

    @property
    def name(self) -> str:
        r'''Gets name.

        ..  container:: example

            >>> abjad.Part('FirstViolin01', 'VN-1-1', 'Violin').name
            'FirstViolin01'

        '''
        return self._name

    @property
    def number(self) -> typing.Optional[int]:
        r'''Gets number.

        ..  container:: example

            >>> abjad.Part('FirstViolin01', 'VN-1-1', 'Violin').number
            1

        '''
        return self._number

    @property
    def section(self) -> str:
        r'''Gets section.

        ..  container:: example

            >>> abjad.Part('FirstViolin01', 'VN-1-1', 'Violin').section
            'FirstViolin'

        '''
        return self._section
