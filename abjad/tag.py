import typing

from .storage import FormatSpecification, StorageFormatManager


class Tag:
    """
    Tag.

    ..  container:: example

        >>> abjad.Tag("YELLOW")
        Tag('YELLOW')

        >>> abjad.Tag("YELLOW:RED")
        Tag('YELLOW:RED')

        Removes duplicate words at initialization:

        >>> abjad.Tag("YELLOW:RED:RED")
        Tag('YELLOW:RED')

    ..  container:: example

        Initializes from other tag:

        >>> abjad.Tag(abjad.Tag("YELLOW"))
        Tag('YELLOW')

    ..  container:: example

        Raises exception on multiple only-edition tags:

        >>> abjad.Tag("+SEGMENT:+PARTS")
        Traceback (most recent call last):
            ...
        Exception: at most one only-edition tag: ['+SEGMENT', '+PARTS'].

    ..  container:: example

        Raises exception on mixed only-edition / not-edition tags:

        >>> abjad.Tag("+SEGMENT:-PARTS")
        Traceback (most recent call last):
            ...
        Exception: only-edition and not-edition forbidden in same tag:
        <BLANKLINE>
        ['+SEGMENT'] / ['-PARTS']

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_string", "_words")

    ### INITIALIZER ###

    def __init__(self, string: typing.Union[str, "Tag"] = None) -> None:
        if isinstance(string, Tag):
            string = str(string)
        if string is not None:
            assert not string.startswith(":"), repr(string)
            words = string.split(":")
        else:
            words = []
        assert isinstance(words, list), repr(words)
        words_: typing.List[str] = []
        for word in words:
            if word not in words_:
                words_.append(word)
        only_edition_tags, not_edition_tags = [], []
        for word_ in words_:
            if word_.startswith("+"):
                only_edition_tags.append(word_)
            if word_.startswith("-"):
                not_edition_tags.append(word_)
        if 1 < len(only_edition_tags):
            raise Exception(f"at most one only-edition tag: {only_edition_tags!r}.")
        if only_edition_tags and not_edition_tags:
            message = "only-edition and not-edition forbidden in same tag:\n\n"
            message += f"  {only_edition_tags} / {not_edition_tags}"
            raise Exception(message)
        self._words = words_
        if bool(string):
            string = ":".join(words_)
            assert not string.startswith(":"), repr(string)
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

            >>> bool(abjad.Tag("+PARTS"))
            True

        """
        return bool(str(self))

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` is word in tag.

        ..  container:: example

            >>> tag = abjad.Tag("-PARTS")
            >>> tag = tag.append(abjad.Tag("DEFAULT_CLEF"))

            >>> "PARTS" in tag
            False

            >>> "-PARTS" in tag
            True

            >>> abjad.Tag("DEFAULT_CLEF") in tag
            True

        """
        return str(argument) in self.words

    def __eq__(self, argument):
        """
        Is true when ``argument`` is tag with same string representation.

        ..  container:: example

            >>> tag_1 = abjad.Tag()
            >>> tag_2 = abjad.Tag()
            >>> tag_3 = abjad.Tag("+PARTS")

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

        ..  container:: example

            REGRESSION. Tags compare equal when strings compare equal:

            >>> tag_1 = abjad.Tag("MEASURE_1")
            >>> tag_2 = abjad.Tag("MEASURE_1")
            >>> hash(tag_1) == hash(tag_2)
            True

        """
        return hash(str(self))

    def __iter__(self):
        """
        Iterates words in tag.

        ..  container:: example

            >>> tag = abjad.Tag("-PARTS:-SCORE:DEFAULT_CLEF")
            >>> for word  in tag:
            ...     word
            ...
            '-PARTS'
            '-SCORE'
            'DEFAULT_CLEF'

        """
        return iter(self.words)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Changes tag to string.

        ..  container:: example

            >>> str(abjad.Tag())
            ''

            >>> str(abjad.Tag("-PARTS:-SCORE:DEFAULT_CLEF"))
            '-PARTS:-SCORE:DEFAULT_CLEF'

        """
        return self.string or ""

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

            >>> abjad.Tag("-PARTS:DEFAULT_CLEF").string
            '-PARTS:DEFAULT_CLEF'

        """
        return self._string

    @property
    def words(self) -> typing.List[str]:
        """
        Gets words.

        ..  container:: example

            >>> abjad.Tag("-PARTS:DEFAULT_CLEF").words
            ['-PARTS', 'DEFAULT_CLEF']

        """
        return list(self._words)

    ### PUBLIC METHODS ###

    def append(self, word: typing.Optional["Tag"]) -> "Tag":
        """
        Appends ``word`` to tag.

        ..  container:: example

            >>> abjad.Tag("-PARTS").append(abjad.Tag("DEFAULT_CLEF"))
            Tag('-PARTS:DEFAULT_CLEF')

        """
        if not bool(word):
            return Tag(self)
        assert isinstance(word, Tag), repr(word)
        words = []
        if str(self) != "":
            words.append(str(self))
        words.append(str(word))
        string = ":".join(words)
        return Tag(string)

    def editions(self) -> typing.List["Tag"]:
        """
        Gets edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").editions()
            []

            >>> abjad.Tag("+SEGMENT").only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag("+SEGMENT:FOO").only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag("-SEGMENT").editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:FOO").editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:-PARTS").editions()
            [Tag('-SEGMENT'), Tag('-PARTS')]

        """
        result = []
        for word in self:
            if word.startswith("+") or word.startswith("-"):
                result.append(Tag(word))
        return result

    def invert_edition_tags(self) -> "Tag":
        """
        Inverts edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").invert_edition_tags()
            Tag('FOO')

            >>> abjad.Tag("FOO:-PARTS").invert_edition_tags()
            Tag('FOO:+PARTS')

            >>> abjad.Tag("FOO:+PARTS").invert_edition_tags()
            Tag('FOO:-PARTS')

        """
        words = []
        for word in self.words:
            if word.startswith("+"):
                word_ = "-" + word[1:]
            elif word.startswith("-"):
                word_ = "+" + word[1:]
            else:
                word_ = word
            words.append(word_)
        string = ":".join(words)
        tag = Tag(string)
        return tag

    def not_editions(self) -> typing.List["Tag"]:
        """
        Gets not-edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").not_editions()
            []

            >>> abjad.Tag("-SEGMENT").not_editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:FOO").not_editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:-PARTS").not_editions()
            [Tag('-SEGMENT'), Tag('-PARTS')]

        """
        result = []
        for word in self:
            if word.startswith("-"):
                result.append(Tag(word))
        return result

    def only_edition(self) -> typing.Optional["Tag"]:
        """
        Gets only-edition tag in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").only_edition() is None
            True

            >>> abjad.Tag("+SEGMENT").only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag("+SEGMENT:FOO").only_edition()
            Tag('+SEGMENT')

        """
        for word in self:
            if word.startswith("+"):
                return Tag(word)
        else:
            return None


class Line:
    r"""
    Line in a LilyPond file.

    ..  container:: example

        >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
        >>> abjad.Line(string)
        Line(string='    %@%  \\with-color %! MEASURE_NUMBER:SM31')

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Segment-makers"

    __slots__ = ("_string",)

    ### INITIALIZER ###

    def __init__(self, string=""):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        r"""
        Gets string representation of line.

        ..  container:: example

            >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
            >>> str(abjad.Line(string))
            '    %@%  \\with-color %! MEASURE_NUMBER:SM31'

        Returns string.
        """
        return self.string

    ### PUBLIC PROPERTIES ###

    @property
    def string(self):
        r"""
        Gets string.

        ..  container:: example

            >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
            >>> abjad.Line(string).string
            '    %@%  \\with-color %! MEASURE_NUMBER:SM31'

        Returns string.
        """
        return self._string

    ### PUBLIC METHODS ###

    def get_tags(self):
        r"""
        Gets tags.

        ..  container:: example

            >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
            >>> abjad.Line(string).get_tags()
            [Tag('MEASURE_NUMBER'), Tag('SM31')]

        ..  container:: example

            REGRESSION. Works with multiple ``%!`` prefixes:

            >>> string = r"    %@%  \with-color %! SM31 %! SM32"
            >>> line = abjad.Line(string)
            >>> line.get_tags()
            [Tag('SM31'), Tag('SM32')]

        Returns list of zero or more strings.
        """
        tags = []
        if " %! " in self.string:
            for chunk in self.string.split(" %! ")[1:]:
                parts = chunk.split()
                parts = parts[0].split(":")
                tags_ = [Tag(_) for _ in parts]
                tags.extend(tags_)
        return tags

    def is_active(self):
        r"""
        Is true when line is active.

        ..  container:: example

            >>> string = '              \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_active()
            True

            >>> string = '          %@% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_active()
            False

            >>> string = '          %%% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_active()
            False

        Returns true or false.
        """
        return not self.is_deactivated()

    def is_deactivated(self):
        r"""
        Is true when line is deactivated.

        ..  container:: example

            >>> string = '              \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_deactivated()
            False

            >>> string = '          %@% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_deactivated()
            True

            >>> string = '          %%% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_deactivated()
            True

        Returns true or false.
        """
        string = self.string.strip()
        if string.startswith("%@%"):
            return True
        if string.startswith("%%%"):
            return True
        return False

    def match(self, predicate):
        r"""
        Is true when ``predicate`` matches tags.

        ..  container:: example

            >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
            >>> line = abjad.Line(string)

        ..  container:: example

            Tags:

            >>> line.match(abjad.Tag("MEASURE_NUMBER"))
            True

            >>> line.match(abjad.Tag("SM31"))
            True

            >>> line.match(abjad.Tag("%@%"))
            False

            >>> line.match(abjad.Tag("with-color"))
            False

            >>> line.match(abjad.Tag("%!"))
            False

        ..  container:: example

            Lambdas:

            >>> line.match(lambda x: any(_ for _ in x if str(_).startswith("M")))
            True

            >>> line.match(lambda x: any(_ for _ in x if str(_).startswith("S")))
            True

            >>> line.match(lambda x: any(_ for _ in x if str(_)[0] in "SM"))
            True

        ..  container:: example

            Functions:

            >>> def predicate(tags):
            ...     if abjad.Tag("SM31") in tags and abjad.Tag("MEASURE_NUMBER") in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            True

            >>> def predicate(tags):
            ...     if abjad.Tag("SM31") in tags and abjad.Tag("MEASURE_NUMBER") not in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            False

        ..  container:: example

            REGRESSION. Works with multiple ``%!`` prefixes:

            >>> string = r"    %@%  \with-color %! SM31 %! SM32"
            >>> line = abjad.Line(string)

            >>> line.match(abjad.Tag("SM31"))
            True

            >>> line.match(abjad.Tag("SM32"))
            True

        Returns true or false.
        """
        if not callable(predicate) and not isinstance(predicate, Tag):
            raise Exception(f"must be callable or tag: {predicate!r}")
        tags = self.get_tags()
        if not tags:
            return False
        if predicate in tags:
            return True
        if not callable(predicate):
            return False
        return predicate(tags)


### FUNCTIONS ###


def activate(text, tag, skipped=False):
    r"""
    Activates ``tag`` in ``text``.

    ..  container:: example

        Writes (deactivated) tag with ``"%@%"`` prefix into LilyPond
        input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> string = r"\markup { \with-color #red Allegro }"
        >>> markup = abjad.Markup(string, literal=True)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("RED_MARKUP"),
        ...     )

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> print(text)
        \new Staff {
            c'4
        %@% - \markup { \with-color #red Allegro }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Activates tag:

        >>> text, count = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff {
            c'4
            - \markup { \with-color #red Allegro }               %! RED_MARKUP %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile(items=[string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff {
            c'4
            %@% - \markup { \with-color #red Allegro }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile(items=[string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff {
            c'4
            - \markup { \with-color #red Allegro }               %! RED_MARKUP %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile(items=[string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns text, count pair.

    Count gives number of activated tags.
    """
    assert isinstance(tag, Tag) or callable(tag), repr(tag)
    lines, count, skipped_count = [], 0, 0
    treated_last_line = False
    found_already_active_on_last_line = False
    text_lines = text.split("\n")
    text_lines = [_ + "\n" for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    for line in text_lines:
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if not Line(line).match(tag):
            lines.append(line)
            treated_last_line = False
            found_already_active_on_last_line = False
            continue
        if line[index : index + 4] in ("%%% ", "%@% "):
            if "%@% " in line:
                line = line.replace("%@%", "   ")
                suffix = " %@%"
            else:
                line = line.replace("%%%", "   ")
                suffix = None
            assert line.endswith("\n"), repr(line)
            if suffix:
                line = line.strip("\n") + suffix + "\n"
            if not treated_last_line:
                count += 1
            treated_last_line = True
            found_already_active_on_last_line = False
        else:
            if not found_already_active_on_last_line:
                skipped_count += 1
            found_already_active_on_last_line = True
            treated_last_line = False
        lines.append(line)
    text = "".join(lines)
    if skipped is True:
        return text, count, skipped_count
    else:
        return text, count


def deactivate(text, tag, prepend_empty_chord=False, skipped=False):
    r"""
    Deactivates ``tag`` in ``text``.

    ..  container:: example

        Writes (active) tag into LilyPond input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> string = r"\markup { \with-color #red Allegro }"
        >>> markup = abjad.Markup(string, literal=True)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     tag=abjad.Tag("RED_MARKUP"),
        ...     )

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> print(text)
        \new Staff {
            c'4
            - \markup { \with-color #red Allegro }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Deactivates tag:

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text, count = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff {
            c'4
            %%% - \markup { \with-color #red Allegro }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile(items=[string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff {
            c'4
            - \markup { \with-color #red Allegro }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile(items=[string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff {
            c'4
            %%% - \markup { \with-color #red Allegro }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile(items=[string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns text, count pair.

    Count gives number of deactivated tags.
    """
    assert isinstance(tag, Tag) or callable(tag), repr(tag)
    lines, count, skipped_count = [], 0, 0
    treated_last_line, last_index = False, None
    found_already_deactivated_on_last_line = False
    text_lines = text.split("\n")
    text_lines = [_ + "\n" for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    previous_line_was_tweak = False
    for line in text_lines:
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if not Line(line).match(tag):
            lines.append(line)
            treated_last_line, last_index = False, None
            found_already_deactivated_on_last_line = False
            continue
        if line[index] != "%":
            if last_index is None:
                last_index = index
            if " %@%" in line:
                prefix = "%@% "
                line = line.replace(" %@%", "")
            else:
                prefix = "%%% "
            if prepend_empty_chord and not previous_line_was_tweak:
                prefix += "<> "
            target = line[last_index - 4 : last_index]
            assert target == "    ", repr((line, target, index, tag))
            characters = list(line)
            characters[last_index - 4 : last_index] = list(prefix)
            line = "".join(characters)
            if not treated_last_line:
                count += 1
            treated_last_line = True
            found_already_deactivated_on_last_line = False
        else:
            if not found_already_deactivated_on_last_line:
                skipped_count += 1
            found_already_deactivated_on_last_line = True
            treated_last_line = False
        lines.append(line)
        previous_line_was_tweak = "tweak" in line
    text = "".join(lines)
    if skipped is True:
        return text, count, skipped_count
    else:
        return text, count


def tag(strings, tag, deactivate=None) -> typing.List[str]:
    """
    Tags ``strings`` with ``tag``.
    """
    if not tag:
        return strings
    if not strings:
        return strings
    if deactivate is not None:
        assert isinstance(deactivate, type(True)), repr(deactivate)
    length = max([len(_) for _ in strings])
    strings_ = []
    for string in strings:
        if "%!" in string and r"\tweak" in string:
            strings_.append(string)
            continue
        if "%!" not in string:
            pad = length - len(string)
        else:
            pad = 0
        tag_ = pad * " " + " " + "%!" + " " + str(tag)
        string = string + tag_
        strings_.append(string)
    if deactivate is True:
        strings_ = ["%@% " + _ for _ in strings_]
    return strings_
