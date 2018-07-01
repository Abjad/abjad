import typing
from abjad.system.AbjadObject import AbjadObject
from .FormatSpecification import FormatSpecification


class Tag(AbjadObject):
    """
    Tag.

    ..  container:: example

        >>> abjad.Tag('YELLOW')
        Tag('YELLOW')

        >>> abjad.Tag('YELLOW:RED')
        Tag('YELLOW:RED')

        Removes duplicate words at initialization:

        >>> abjad.Tag('YELLOW:RED:RED')
        Tag('YELLOW:RED')

    ..  container:: example

        Initializes from other tag:

        >>> abjad.Tag(abjad.Tag('YELLOW'))
        Tag('YELLOW')

    ..  container:: example

        Raises exception on multiple only-edition tags:

        >>> abjad.Tag('+SEGMENT:+PARTS')
        Traceback (most recent call last):
            ...
        Exception: at most one only-edition tag: ['+SEGMENT', '+PARTS'].

    ..  container:: example

        Raises exception on mixed only-edition / not-edition tags:

        >>> abjad.Tag('+SEGMENT:-PARTS')
        Traceback (most recent call last):
            ...
        Exception: only-edition and not-edition forbidden in same tag:
        <BLANKLINE>
        ['+SEGMENT'] / ['-PARTS']

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_string',
        '_words',
        )

    ### INITIALIZER ###

    def __init__(self, string: typing.Union[str, 'Tag'] = None) -> None:
        if isinstance(string, Tag):
            string = str(string)
        if string is not None:
            assert not string.startswith(':'), repr(string)
            words = string.split(':')
        else:
            words = []
        assert isinstance(words, list), repr(words)
        words_: typing.List[str] = []
        for word in words:
            if word not in words_:
                words_.append(word)
        only_edition_tags, not_edition_tags = [], []
        for word_ in words_:
            if word_.startswith('+'):
                only_edition_tags.append(word_)
            if word_.startswith('-'):
                not_edition_tags.append(word_)
        if 1 < len(only_edition_tags):
            message = f'at most one only-edition tag: {only_edition_tags!r}.'
            raise Exception(message)
        if only_edition_tags and not_edition_tags:
            message = 'only-edition and not-edition forbidden in same tag:\n\n'
            message += f'  {only_edition_tags} / {not_edition_tags}'
            raise Exception(message)
        self._words = words_
        if bool(string):
            string = ':'.join(words_)
            assert not string.startswith(':'), repr(string)
        else:
            string = None
        self._string = string

    ### SPECIAL METHODS ###

    def __bool__(self):
        """
        Is true when tag has words.

        ..  container:: example

            >>> bool(abjad.Tag())
            False

            >>> bool(abjad.Tag('+PARTS'))
            True

        """
        return bool(str(self))

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` is word in tag.

        ..  container:: example

            >>> tag = abjad.Tag('-PARTS')
            >>> tag = tag.append(abjad.tags.DEFAULT_CLEF)

            >>> 'PARTS' in tag
            False

            >>> '-PARTS' in tag
            True

            >>> abjad.tags.DEFAULT_CLEF in tag
            True

        """
        return argument in self.words

    def __eq__(self, argument):
        """
        Is true when ``argument`` is tag with same string representation.

        ..  container:: example

            >>> tag_1 = abjad.Tag()
            >>> tag_2 = abjad.Tag()
            >>> tag_3 = abjad.Tag('+PARTS')

            >>> tag_1 == tag_1
            True
            >>> tag_1 == tag_2
            True
            >>> tag_1 == tag_3
            False

            >>> tag_2 == tag_1
            True
            >>> tag_2 == tag_2
            True
            >>> tag_2 == tag_3
            False

            >>> tag_3 == tag_1
            False
            >>> tag_3 == tag_2
            False
            >>> tag_3 == tag_3
            True

        """
        if isinstance(argument, Tag):
            return str(self) == str(argument)
        return False

    def __hash__(self):
        """
        Hashes tag.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates words in tag.

        ..  container:: example

            >>> tag = abjad.Tag('-PARTS:-SCORE:DEFAULT_CLEF')
            >>> for word  in tag:
            ...     word
            ...
            '-PARTS'
            '-SCORE'
            'DEFAULT_CLEF'

        """
        return iter(self.words)

    def __str__(self):
        """
        Changes tag to string.

        ..  container:: example

            >>> str(abjad.Tag())
            ''

            >>> str(abjad.Tag('-PARTS:-SCORE:DEFAULT_CLEF'))
            '-PARTS:-SCORE:DEFAULT_CLEF'

        """
        return self.string or ''

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = []
        if self.string is not None:
            values.append(self.string)
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def string(self) -> typing.Optional[str]:
        """
        Gets string.

        ..  container:: example

            >>> abjad.Tag().string is None
            True

            >>> abjad.Tag('-PARTS:DEFAULT_CLEF').string
            '-PARTS:DEFAULT_CLEF'

        """
        return self._string

    @property
    def words(self) -> typing.List[str]:
        """
        Gets words.

        ..  container:: example

            >>> abjad.Tag('-PARTS:DEFAULT_CLEF').words
            ['-PARTS', 'DEFAULT_CLEF']

        """
        return list(self._words)

    ### PUBLIC METHODS ###

    def append(self, word: str) -> 'Tag':
        """
        Appends ``word`` to tag.
        
        ..  container:: example

            >>> abjad.Tag('-PARTS').append(abjad.tags.DEFAULT_CLEF)
            Tag('-PARTS:DEFAULT_CLEF')

        """
        if not bool(word):
            return Tag(self)
        if isinstance(word, Tag):
            word = str(word)
        assert isinstance(word, str), repr(word)
        assert word != '', repr(word)
        words_ = self.words
        words_.append(word)
        return Tag.from_words(words_)

    def editions(self) -> typing.List['Tag']:
        """
        Gets edition tags in tag.

        ..  container:: example

            >>> abjad.Tag('FOO').editions()
            []

            >>> abjad.Tag('+SEGMENT').only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag('+SEGMENT:FOO').only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag('-SEGMENT').editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag('-SEGMENT:FOO').editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag('-SEGMENT:-PARTS').editions()
            [Tag('-SEGMENT'), Tag('-PARTS')]

        """
        result = []
        for word in self:
            if word.startswith('+') or word.startswith('-'):
                result.append(Tag(word))
        return result

    def extend(self, words: typing.List[str]) -> 'Tag':
        """
        Extends tag with ``words``.

        ..  container:: example

            >>> tag = abjad.Tag('-PARTS')
            >>> tag.extend(['-SCORE', abjad.tags.DEFAULT_CLEF])
            Tag('-PARTS:-SCORE:DEFAULT_CLEF')

        """
        assert isinstance(words, list), repr(words)
        tag = self
        for word in words:
            tag = tag.append(word)
        return tag

    @staticmethod
    def from_words(words: typing.List[str]) -> 'Tag':
        """
        Makes tag from ``words``.
        """
        assert isinstance(words, list), repr(words)
        words_ = []
        for word in words:
            if not bool(word):
                continue
            word = str(word)
            words_.append(word)
        string = ':'.join(words_)
        return Tag(string)

    def has_persistence_tag(self) -> bool:
        """
        Is true when tag has persistence tag.

        ..  container:: example

            >>> abjad.Tag('FOO').has_persistence_tag()
            False

            >>> abjad.Tag('FOO:DEFAULT_CLEF').has_persistence_tag()
            True

            >>> abjad.Tag('DEFAULT_CLEF').has_persistence_tag()
            True

        """
        from abjad.system.Tags import Tags
        tags = Tags().persistent_indicator_tags()
        for word in self:
            if word in tags:
                return True
        return False

    def invert_edition_tags(self) -> 'Tag':
        """
        Inverts edition tags in tag.

        ..  container:: example

            >>> abjad.Tag('FOO').invert_edition_tags()
            Tag('FOO')

            >>> abjad.Tag('FOO:-PARTS').invert_edition_tags()
            Tag('FOO:+PARTS')

            >>> abjad.Tag('FOO:+PARTS').invert_edition_tags()
            Tag('FOO:-PARTS')

        """
        words = []
        for word in self.words:
            if word.startswith('+'):
                word_ = '-' + word[1:]
            elif word.startswith('-'):
                word_ = '+' + word[1:]
            else:
                word_ = word
            words.append(word_)
        tag = Tag.from_words(words)
        return tag

    def not_editions(self) -> typing.List['Tag']:
        """
        Gets not-edition tags in tag.

        ..  container:: example

            >>> abjad.Tag('FOO').not_editions()
            []

            >>> abjad.Tag('-SEGMENT').not_editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag('-SEGMENT:FOO').not_editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag('-SEGMENT:-PARTS').not_editions()
            [Tag('-SEGMENT'), Tag('-PARTS')]

        """
        result = []
        for word in self:
            if word.startswith('-'):
                result.append(Tag(word))
        return result

    def only_edition(self) -> typing.Optional['Tag']:
        """
        Gets only-edition tag in tag.

        ..  container:: example

            >>> abjad.Tag('FOO').only_edition() is None
            True

            >>> abjad.Tag('+SEGMENT').only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag('+SEGMENT:FOO').only_edition()
            Tag('+SEGMENT')

        """
        for word in self:
            if word.startswith('+'):
                return Tag(word)
        else:
            return None

    def prepend(self, word: str) -> 'Tag':
        """
        Prepends ``word`` to tag.
        
        ..  container:: example

            >>> abjad.Tag('-PARTS').prepend(abjad.tags.DEFAULT_CLEF)
            Tag('DEFAULT_CLEF:-PARTS')

        """
        if not bool(word):
            return Tag(self)
        if isinstance(word, Tag):
            word = str(word)
        assert isinstance(word, str), repr(word)
        assert word != '', repr(word)
        words_ = self.words
        words_.insert(0, word)
        return Tag.from_words(words_)
