import dataclasses
import typing

from . import _indentlib
from . import string as _string


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tag:
    """
    Tag.

    ..  container:: example

        >>> abjad.Tag("YELLOW")
        Tag(string='YELLOW')

        >>> abjad.Tag("YELLOW:RED")
        Tag(string='YELLOW:RED')

        Raises exception on duplicate words in tag:

        >>> abjad.Tag("YELLOW:RED:RED")
        Traceback (most recent call last):
        ...
        Exception: duplicate words in tag: 'YELLOW:RED:RED'

        Raises exception on multiple only-edition tags:

        >>> abjad.Tag("+SEGMENT:+PARTS")
        Traceback (most recent call last):
            ...
        Exception: at most one only-edition tag: ['+SEGMENT', '+PARTS'].

        Raises exception on mixed only-edition / not-edition tags:

        >>> abjad.Tag("+SEGMENT:-PARTS")
        Traceback (most recent call last):
        ...
        Exception: only-edition and not-edition forbidden in same tag:
        <BLANKLINE>
          ['+SEGMENT'] / ['-PARTS']

    """

    string: str = ""

    def __post_init__(self):
        assert isinstance(self.string, str), repr(self.string)
        self.words()

    def append(self, word: "Tag") -> "Tag":
        """
        Appends ``word`` to tag.

        ..  container:: example

            >>> abjad.Tag("-PARTS").append(abjad.Tag("DEFAULT_CLEF"))
            Tag(string='-PARTS:DEFAULT_CLEF')

        """
        if not bool(word.string):
            return Tag(self.string)
        assert isinstance(word, Tag), repr(word)
        words = []
        if self.string:
            words.append(self.string)
        if word.string in self.words():
            raise Exception(f"{word} duplicates {self}.")
        words.append(word.string)
        string = ":".join(words)
        return Tag(string)

    def editions(self) -> list["Tag"]:
        """
        Gets edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").editions()
            []

            >>> abjad.Tag("+SEGMENT").only_edition()
            Tag(string='+SEGMENT')

            >>> abjad.Tag("+SEGMENT:FOO").only_edition()
            Tag(string='+SEGMENT')

            >>> abjad.Tag("-SEGMENT").editions()
            [Tag(string='-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:FOO").editions()
            [Tag(string='-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:-PARTS").editions()
            [Tag(string='-SEGMENT'), Tag(string='-PARTS')]

        """
        result = []
        for word in self.words():
            if word.startswith("+") or word.startswith("-"):
                result.append(Tag(word))
        return result

    def invert_edition_tags(self) -> "Tag":
        """
        Inverts edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").invert_edition_tags()
            Tag(string='FOO')

            >>> abjad.Tag("FOO:-PARTS").invert_edition_tags()
            Tag(string='FOO:+PARTS')

            >>> abjad.Tag("FOO:+PARTS").invert_edition_tags()
            Tag(string='FOO:-PARTS')

        """
        words = []
        for word in self.words():
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

    def not_editions(self) -> list["Tag"]:
        """
        Gets not-edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").not_editions()
            []

            >>> abjad.Tag("-SEGMENT").not_editions()
            [Tag(string='-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:FOO").not_editions()
            [Tag(string='-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:-PARTS").not_editions()
            [Tag(string='-SEGMENT'), Tag(string='-PARTS')]

        """
        result = []
        for word in self.words():
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
            Tag(string='+SEGMENT')

            >>> abjad.Tag("+SEGMENT:FOO").only_edition()
            Tag(string='+SEGMENT')

        """
        for word in self.words():
            if word.startswith("+"):
                return Tag(word)
        else:
            return None

    def retain_shoutcase(self) -> "Tag":
        """
        Retains shoutcase.

        ..  container:: example

            >>> tag = abjad.Tag("-PARTS:DEFAULT_CLEF:_apply_clef()")
            >>> tag.retain_shoutcase()
            Tag(string='-PARTS:DEFAULT_CLEF')

            >>> tag = abjad.Tag("_debug_function()")
            >>> tag.retain_shoutcase()
            Tag(string='')

        """
        words = []
        for word in self.words():
            if _string.is_shout_case(word) or word[0] in ("-", "+"):
                words.append(word)
        string = ":".join(words)
        return type(self)(string)

    def words(self) -> list[str]:
        """
        Gets words.

        ..  container:: example

            >>> abjad.Tag("-PARTS:DEFAULT_CLEF").words()
            ['-PARTS', 'DEFAULT_CLEF']

        """
        assert not self.string.startswith(":"), repr(self.string)
        words = self.string.split(":")
        assert isinstance(words, list), repr(words)
        words_ = []
        for word in words:
            if word in words_:
                raise Exception(f"duplicate words in tag: {self.string!r}")
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
        assert all(isinstance(_, str) for _ in words_), repr(words_)
        return words_


def _match_line(line, tag, current_tags):
    assert all(isinstance(_, Tag) for _ in current_tags), repr(current_tags)
    if tag in current_tags:
        return True
    if callable(tag):
        return tag(current_tags)
    assert isinstance(tag, Tag), repr(tag)
    return False


def activate(text: str, tag: Tag | typing.Callable) -> tuple[str, int, int]:
    r"""
    Activates ``tag`` in ``text``.

    ..  container:: example

        Writes (deactivated) tag with ``"%@%"`` prefix into LilyPond input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup { \with-color #red Allegro }")
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("RED_MARKUP"),
        ... )

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            %@% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Activates tag:

        >>> text, count, skipped = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            - \markup { \with-color #red Allegro } %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count, skipped = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            %@% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count, skipped = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            - \markup { \with-color #red Allegro } %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns (text, count, skipped) triple.

    Count gives number of activated tags.

    Skipped gives number of skipped tags.
    """
    assert isinstance(text, str), repr(text)
    assert isinstance(tag, Tag) or callable(tag), repr(tag)
    lines: list[str] = []
    count, skipped_count = 0, 0
    treated_last_line = False
    found_already_active_on_last_line = False
    text_lines = text.split("\n")
    text_lines = [_ + "\n" for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    current_tags = []
    for line in text_lines:
        if line.lstrip().startswith("%! "):
            lines.append(line)
            current_tag = Tag(line.strip()[3:])
            current_tags.append(current_tag)
            continue
        if not _match_line(line, tag, current_tags):
            lines.append(line)
            treated_last_line = False
            found_already_active_on_last_line = False
            current_tags = []
            continue
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if line[index : index + 4] in ("%%% ", "%@% "):
            if "%@% " in line:
                line = line.replace("%@% ", "")
                suffix = " %@%"
            else:
                # TODO: replace with "" instead of "    "?
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
        current_tags = []
    text = "".join(lines)
    return text, count, skipped_count


def deactivate(
    text: str,
    tag: Tag | typing.Callable,
    prepend_empty_chord: bool = False,
) -> tuple[str, int, int]:
    r"""
    Deactivates ``tag`` in ``text``.

    ..  container:: example

        Writes (active) tag into LilyPond input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> string = r"\markup { \with-color #red Allegro }"
        >>> markup = abjad.Markup(string)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     tag=abjad.Tag("RED_MARKUP"),
        ... )

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Deactivates tag:

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text, count, skipped = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
        %%% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count, skipped = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count, skipped = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
        %%% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.
    """
    assert isinstance(text, str), repr(text)
    assert isinstance(tag, Tag) or callable(tag), repr(tag)
    count, skipped_count = 0, 0
    treated_last_line = False
    found_already_deactivated_on_last_line = False
    previous_line_was_tweak = False
    text_lines = text.split("\n")
    text_lines = [_ + "\n" for _ in text_lines[:-1]] + text_lines[-1:]
    lines, current_tags = [], []
    for line in text_lines:
        if line.lstrip().startswith("%! "):
            lines.append(line)
            current_tag = Tag(line.strip()[3:])
            current_tags.append(current_tag)
            continue
        if not _match_line(line, tag, current_tags):
            lines.append(line)
            treated_last_line = False
            found_already_deactivated_on_last_line = False
            current_tags = []
            continue
        start_column = len(line) - len(line.lstrip())
        if line[start_column] != "%":
            if " %@%" in line:
                prefix = "    " + "%@% "
                line = line.replace(" %@%", "")
            else:
                prefix = "%%% "
            if prepend_empty_chord and not previous_line_was_tweak:
                prefix += "<> "
            target = line[start_column - 4 : start_column]
            assert target == "    ", repr((line, target, start_column, tag))
            characters = list(line)
            characters[start_column - 4 : start_column] = list(prefix)
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
        current_tags = []
    text = "".join(lines)
    return text, count, skipped_count


def double_tag(strings: list[str], tag_: Tag, deactivate: bool = False) -> list[str]:
    """
    Double tags ``strings``.
    """
    assert all(isinstance(_, str) for _ in strings), repr(strings)
    assert isinstance(tag_, Tag), repr(tag_)
    half_indent = 2 * " "
    tag_lines = []
    if tag_.string:
        tag_lines_ = tag_.string.split(":")
        tag_lines_ = [half_indent + "%! " + _ for _ in tag_lines_]
        tag_lines.extend(tag_lines_)
        tag_lines.sort()
    if deactivate is True:
        strings = ["%@% " + _ for _ in strings]
    result = []
    for string in strings:
        if string.strip().startswith("%!"):
            result.append(string)
            continue
        result.extend(tag_lines)
        result.append(string)
    return result


def left_shift_tags(text: str) -> str:
    """
    Left shifts tags in ``strings``.
    """
    strings = text.split("\n")
    strings_ = []
    for string in strings:
        if "%@% " not in string or "%!" not in string:
            strings_.append(string)
            continue
        if not string.startswith(4 * " "):
            strings_.append(string)
            continue
        string_ = string[4:]
        tag_start = string_.find("%!")
        strings__ = list(string_)
        strings__[tag_start:tag_start] = _indentlib.INDENT
        string_ = "".join(strings__)
        strings_.append(string_)
    text = "\n".join(strings_)
    return text


def remove_tags(string: str) -> str:
    """
    Removes all tags from ``string``.
    """
    lines = []
    for line in string.split("\n"):
        if "%!" not in line:
            lines.append(line)
            continue
        tag_start = line.find("%!")
        line = line[:tag_start]
        line = line.rstrip()
        if line:
            lines.append(line)
    string = "\n".join(lines)
    return string
