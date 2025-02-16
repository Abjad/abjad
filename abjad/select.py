import collections
import itertools
import typing

from . import _getlib, _iterlib, _updatelib
from . import cyclictuple as _cyclictuple
from . import duration as _duration
from . import enums as _enums
from . import get as _get
from . import iterate as _iterate
from . import math as _math
from . import parentage as _parentage
from . import pattern as _pattern
from . import pcollections as _pcollections
from . import score as _score
from . import sequence as _sequence
from . import typings as _typings


def _head_filter_subresult(result, head):
    result_ = []
    for item in result:
        if isinstance(item, _score.Component):
            leaves = _iterlib._get_logical_tie_leaves(item)
            if head == (item is leaves[0]):
                result_.append(item)
            else:
                pass
        else:
            if not all(isinstance(_, _score.Component) for _ in item):
                raise NotImplementedError(item)
            selection = []
            for component in item:
                leaves = _iterlib._get_logical_tie_leaves(component)
                if head == leaves[0]:
                    selection.append(item)
                else:
                    pass
            result_.append(selection)
    assert isinstance(result_, list), repr(result_)
    return result_


def _is_immediate_child_of_outermost_voice(component):
    parentage = _parentage.Parentage(component)
    context = parentage.get(_score.Voice, -1) or parentage.get(_score.Context)
    if context is not None:
        return parentage.component._parent is context
    return None


def _tail_filter_subresult(result, tail):
    result_ = []
    for item in result:
        if isinstance(item, _score.Component):
            leaves = _iterlib._get_logical_tie_leaves(item)
            if tail == (item is leaves[-1]):
                result_.append(item)
            else:
                pass
        else:
            if not all(isinstance(_, _score.Component) for _ in item):
                raise NotImplementedError(item)
            selection = []
            for component in item:
                leaves = _iterlib._get_logical_tie_leaves(component)
                if tail == leaves[-1]:
                    selection.append(item)
                else:
                    pass
            result_.append(selection)
    assert isinstance(result_, list), repr(result_)
    return result_


def _trim_subresult(result, trim):
    assert trim in (True, _enums.LEFT)
    prototype = (_score.MultimeasureRest, _score.Rest, _score.Skip)
    result_ = []
    found_good_component = False
    for item in result:
        if isinstance(item, _score.Component):
            if not isinstance(item, prototype):
                found_good_component = True
        else:
            if not all(isinstance(_, _score.Component) for _ in item):
                raise NotImplementedError(item)
            selection = []
            for component in item:
                if not isinstance(component, prototype):
                    found_good_component = True
                if found_good_component:
                    selection.append(component)
            item = selection
        if found_good_component:
            result_.append(item)
    if trim is _enums.LEFT:
        result = result_
    else:
        result__ = []
        found_good_component = False
        for item in reversed(result_):
            if isinstance(item, _score.Component):
                if not isinstance(item, prototype):
                    found_good_component = True
            else:
                if not all(isinstance(_, _score.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in reversed(item):
                    if not isinstance(component, prototype):
                        found_good_component = True
                    if found_good_component:
                        selection.insert(0, component)
                item = selection
            if found_good_component:
                result__.insert(0, item)
        assert isinstance(result__, list), repr(result__)
        result = result__
    return result


class LogicalTie(collections.abc.Sequence):
    """
    Logical tie of a component.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' ~ e'")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.select.logical_tie(staff[2])
        LogicalTie(items=[Note("e'4"), Note("e'4")])

    """

    __slots__ = ("_items",)

    def __init__(self, items=None):
        if items is None:
            items = []
        if isinstance(items, _score.Component):
            items = [items]
        items = tuple(items)
        for item in items:
            if not isinstance(item, _score.Component):
                raise Exception("components only:\n    {items!r}")
        self._items = tuple(items)

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` is in selection.
        """
        return argument in self.items

    def __eq__(self, argument) -> bool:
        """
        Is true when selection and ``argument`` are of the same type
        and when items in selection equal item in ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.items == argument.items
        elif isinstance(argument, collections.abc.Sequence):
            return self.items == tuple(argument)
        return False

    def __hash__(self) -> int:
        """
        Hashes selection.
        """
        return id(self)

    def __len__(self) -> int:
        """
        Gets number of items in selection.
        """
        return len(self.items)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of selection.
        """
        return f"{type(self).__name__}(items={list(self.items)!r})"

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or list (not logical tie).
        """
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = list(result)
        return result

    def _scale(self, multiplier):
        for leaf in list(self):
            leaf._scale(multiplier)

    @property
    def head(self) -> _score.Leaf:
        """
        Reference to element ``0`` in logical tie.
        """
        assert self.items
        return self.items[0]

    @property
    def items(self) -> tuple:
        """
        Gets items in selection.
        """
        return self._items

    @property
    def is_pitched(self) -> bool:
        """
        Is true when logical tie head is a note or chord.
        """
        return hasattr(self.head, "written_pitch") or hasattr(
            self.head, "written_pitches"
        )

    @property
    def is_trivial(self) -> bool:
        """
        Is true when length of logical tie is less than or equal to ``1``.
        """
        return len(self) <= 1

    @property
    def tail(self) -> _score.Leaf:
        """
        Gets last leaf in logical tie.
        """
        assert self.items
        return self.items[-1]

    @property
    def written_duration(self) -> _duration.Duration:
        """
        Sum of written duration of all components in logical tie.
        """
        return _duration.Duration(sum([_.written_duration for _ in self]))


def chord(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> _score.Chord:
    r"""
    Selects chord ``n`` in ``argument``.

    ..  container:: example

        Selects chord -1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.chord(staff, -1)
        >>> result
        Chord("<fs' gs'>16")

        >>> abjad.label.color_leaves(result, "#green")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    return chords(argument, exclude=exclude, grace=grace)[n]


def chords(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[_score.Chord]:
    r"""
    Selects chords in ``argument``.

    ..  container:: example

        Selects chords:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.chords(staff)
        >>> for item in result:
        ...     item
        ...
        Chord("<a'' b''>16")
        Chord("<d' e'>4")
        Chord("<d' e'>16")
        Chord("<a'' b''>16")
        Chord("<e' fs'>4")
        Chord("<e' fs'>16")
        Chord("<a'' b''>16")
        Chord("<fs' gs'>4")
        Chord("<fs' gs'>16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            bf'16
                            \abjad-color-music #'red
                            <a'' b''>16
                            c'16
                            \abjad-color-music #'blue
                            <d' e'>4
                            ~
                            \abjad-color-music #'red
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            bf'16
                            \abjad-color-music #'blue
                            <a'' b''>16
                            d'16
                            \abjad-color-music #'red
                            <e' fs'>4
                            ~
                            \abjad-color-music #'blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            bf'16
                            \abjad-color-music #'red
                            <a'' b''>16
                            e'16
                            \abjad-color-music #'blue
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'red
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    items = []
    prototype = _score.Chord
    for item in components(argument, prototype=prototype, exclude=exclude, grace=grace):
        assert isinstance(item, prototype)
        items.append(item)
    return items


def components(
    argument,
    prototype=None,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    reverse: bool | None = None,
) -> list[_score.Component]:
    r"""
    Selects components.

    ..  container:: example

        Selects notes:

        >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Note)
        >>> for item in result:
        ...     item
        ...
        Note("c'4")
        Note("d'8")
        Note("d'16")
        Note("e'16")
        Note("e'8")
        Note("g'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'4
                \abjad-color-music #'blue
                d'8
                ~
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'blue
                e'16
                ~
                \abjad-color-music #'red
                e'8
                r4
                \abjad-color-music #'blue
                g'8
            }

    ..  container:: example

        Selects both main notes and graces when ``grace=None``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Leaf, grace=None)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("cf''16")
        Note("bf'16")
        Note("d'8")
        Note("af'16")
        Note("gf'16")
        Note("e'8")
        Note("f'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \grace {
                    \abjad-color-music #'blue
                    cf''16
                    \abjad-color-music #'red
                    bf'16
                }
                \abjad-color-music #'blue
                \afterGrace
                d'8
                {
                    \abjad-color-music #'red
                    af'16
                    \abjad-color-music #'blue
                    gf'16
                }
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Leaf, grace=None)
        >>> for item in result:
        ...     item
        ...
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("gf'16")
        Note("f'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'blue
                        gf'16
                    }
                    \abjad-color-music #'red
                    f'4
                }
            }

    ..  container:: example

        Excludes grace notes when ``grace=False``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Leaf, grace=False)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \grace {
                    cf''16
                    bf'16
                }
                \abjad-color-music #'blue
                \afterGrace
                d'8
                {
                    af'16
                    gf'16
                }
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Leaf, grace=False)
        >>> for item in result:
        ...     item
        ...
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("f'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    \abjad-color-music #'blue
                    f'4
                }
            }

    ..  container:: example

        Selects only grace notes when ``grace=True``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Leaf, grace=True)
        >>> for item in result:
        ...     item
        ...
        Note("cf''16")
        Note("bf'16")
        Note("af'16")
        Note("gf'16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                \grace {
                    \abjad-color-music #'red
                    cf''16
                    \abjad-color-music #'blue
                    bf'16
                }
                \afterGrace
                d'8
                {
                    \abjad-color-music #'red
                    af'16
                    \abjad-color-music #'blue
                    gf'16
                }
                e'8
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Leaf, grace=True)
        >>> for item in result:
        ...     item
        ...
        Note("gf'16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    f'4
                }
            }

    """
    generator = _iterlib._public_iterate_components(
        argument, prototype=prototype, exclude=exclude, grace=None, reverse=reverse
    )
    result = []
    for component in generator:
        if (
            grace is None
            or (grace is True and _get.grace(component))
            or (grace is False and not _get.grace(component))
        ):
            result.append(component)
    return result


_components_alias = components


def exclude(argument, indices: typing.Sequence[int], period: int | None = None) -> list:
    r"""
    Excludes items at ``indices`` by ``period``.

    ..  container:: example

        Excludes every other leaf:

        >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.exclude(result, [0], 2)
        >>> for item in result:
        ...     item
        ...
        Note("d'8")
        Note("e'8")
        Note("e'8")
        Note("f'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                \abjad-color-music #'red
                d'8
                ~
                d'8
                \abjad-color-music #'blue
                e'8
                ~
                e'8
                ~
                \abjad-color-music #'red
                e'8
                r8
                \abjad-color-music #'blue
                f'8
            }

    ..  container:: example

        Excludes every other logical tie:

        >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = abjad.select.exclude(result, [0], 2)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("d'8"), Note("d'8")])
        LogicalTie(items=[Note("f'8")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                \abjad-color-music #'red
                d'8
                ~
                \abjad-color-music #'red
                d'8
                e'8
                ~
                e'8
                ~
                e'8
                r8
                \abjad-color-music #'blue
                f'8
            }

    ..  container:: example

        Excludes note 1 (or nothing) in each pitched logical tie:

        >>> staff = abjad.Staff(r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = [abjad.select.leaves(_) for _ in result]
        >>> result = [abjad.select.exclude(_, [1]) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Note("d'8")]
        [Note("e'8"), Note("e'8")]
        [Note("f'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                d'8
                ~
                d'8
                \abjad-color-music #'red
                e'8
                ~
                e'8
                ~
                \abjad-color-music #'red
                e'8
                r8
                \abjad-color-music #'blue
                f'8
            }

    """
    pattern = _pattern.Pattern(indices, period=period, inverted=True)
    items = _sequence.retain_pattern(argument, pattern)
    return list(items)


def filter(argument, predicate=None) -> list:
    r"""
    Filters ``argument`` by ``predicate``.

    ..  container:: example

        Selects runs with duration equal to 2/8:

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.runs(staff)
        >>> result = abjad.select.filter(
        ...     result, lambda _ : abjad.get.duration(_) == abjad.Duration((2, 8))
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("d'8"), Note("e'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                e'8
                r8
                f'8
                g'8
                a'8
            }

    """
    if predicate is None:
        return list(argument)
    items = [_ for _ in argument if predicate(_)]
    return items


def flatten(argument, depth: int = 1) -> list:
    r"""
    Flattens ``argument``.

    ..  container:: example

        Selects first two leaves of each tuplet:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplets(staff)
        >>> result = [abjad.select.leaves(_)[:2] for _ in result]
        >>> for item in result:
        ...     item
        [Rest('r16'), Note("bf'16")]
        [Rest('r16'), Note("bf'16")]
        [Rest('r16'), Note("bf'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'red
                            \time 7/4
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            \abjad-color-music #'blue
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                }
            }

    ..  container:: example

        Selects first two leaves of all tuplets:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplets(staff)
        >>> result = [abjad.select.leaves(_)[:2] for _ in result]
        >>> result = abjad.select.flatten(result)
        >>> for item in result:
        ...     item
        Rest('r16')
        Note("bf'16")
        Rest('r16')
        Note("bf'16")
        Rest('r16')
        Note("bf'16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'red
                            \time 7/4
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    items = _sequence.flatten(argument, depth=depth)
    return list(items)


def get(
    argument,
    indices: typing.Sequence[int] | tuple[list[int], int] | _pattern.Pattern,
    period: int | None = None,
    *,
    invert: bool = False,
) -> list:
    r"""
    Gets items in ``argument`` at ``indices`` according to ``period``.

    ..  container:: example

        Gets every other leaf:

        >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.get(result, [0], 2)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Rest('r8')

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                d'8
                ~
                \abjad-color-music #'blue
                d'8
                e'8
                ~
                \abjad-color-music #'red
                e'8
                ~
                e'8
                \abjad-color-music #'blue
                r8
                f'8
            }

    ..  container:: example

        Gets every other logical tie:

        >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = abjad.select.get(result, [0], 2)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'8")])
        LogicalTie(items=[Note("e'8"), Note("e'8"), Note("e'8")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                d'8
                ~
                d'8
                \abjad-color-music #'blue
                e'8
                ~
                \abjad-color-music #'blue
                e'8
                ~
                \abjad-color-music #'blue
                e'8
                r8
                f'8
            }

    ..  container:: example

        Gets note 1 (or nothing) in each pitched logical tie:

        >>> staff = abjad.Staff(r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = [abjad.select.leaves(_) for _ in result]
        >>> result = [abjad.select.get(_, [1]) for _ in result]
        >>> for item in result:
        ...     item
        []
        [Note("d'8")]
        [Note("e'8")]
        []

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                d'8
                ~
                \abjad-color-music #'blue
                d'8
                e'8
                ~
                \abjad-color-music #'red
                e'8
                ~
                e'8
                r8
                f'8
            }

    """
    if isinstance(indices, _pattern.Pattern):
        assert period is None
        pattern = indices
    elif isinstance(indices, tuple):
        assert len(indices) == 2, repr(indices)
        indices_, period = indices
        assert isinstance(indices_, list), repr(indices_)
        assert isinstance(period, int), repr(period)
        pattern = _pattern.Pattern(indices_, period=period)
    else:
        pattern = _pattern.Pattern(indices, period=period)
    if invert is True:
        pattern = ~pattern
    items = _sequence.retain_pattern(argument, pattern)
    return list(items)


def group(argument) -> list[list]:
    r"""
    Groups ``argument`` in selection.

    ..  container:: example

        >>> staff = abjad.Staff(r'''
        ...     c'8 ~ c'16 c'16 r8 c'16 c'16
        ...     d'8 ~ d'16 d'16 r8 d'16 d'16
        ...     ''')
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, pitched=True)
        >>> result = abjad.select.group(result)
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")]

        >>> abjad.label.color_leaves(result, "#green")
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'green
                c'8
                ~
                \abjad-color-music #'green
                c'16
                \abjad-color-music #'green
                c'16
                r8
                \abjad-color-music #'green
                c'16
                \abjad-color-music #'green
                c'16
                \abjad-color-music #'green
                d'8
                ~
                \abjad-color-music #'green
                d'16
                \abjad-color-music #'green
                d'16
                r8
                \abjad-color-music #'green
                d'16
                \abjad-color-music #'green
                d'16
            }

    """
    return group_by(argument)


def group_by(argument, predicate=None) -> list[list]:
    r'''
    Groups items in ``argument`` by ``predicate``.

    ..  container:: example

        Wraps selection in selection when ``predicate`` is none:

        >>> staff = abjad.Staff(r"""
        ...     c'8 ~ c'16 c'16 r8 c'16 c'16
        ...     d'8 ~ d'16 d'16 r8 d'16 d'16
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, pitched=True)
        >>> result = abjad.select.group_by(result)
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")]

        >>> abjad.label.color_leaves(result, "#green")
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'green
                c'8
                ~
                \abjad-color-music #'green
                c'16
                \abjad-color-music #'green
                c'16
                r8
                \abjad-color-music #'green
                c'16
                \abjad-color-music #'green
                c'16
                \abjad-color-music #'green
                d'8
                ~
                \abjad-color-music #'green
                d'16
                \abjad-color-music #'green
                d'16
                r8
                \abjad-color-music #'green
                d'16
                \abjad-color-music #'green
                d'16
            }

    '''
    items = []
    if predicate is None:

        def predicate(argument):
            return True

    pairs = itertools.groupby(argument, predicate)
    for count, group in pairs:
        items.append(list(group))
    return items


def group_by_contiguity(argument) -> list[list]:
    r'''
    Groups items in ``argument`` by contiguity.

    ..  container:: example

        Groups pitched leaves by contiguity:

        >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False
        >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")

        >>> result = abjad.select.leaves(staff, pitched=True)
        >>> result = abjad.select.group_by_contiguity(result)
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8")]
        [Note("e'8")]
        [Note("f'8"), Note("g'8"), Note("a'8")]
        [Chord("<c' e' g'>8"), Chord("<c' e' g'>4")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                d'8
                r8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    r8
                    \abjad-color-music #'red
                    f'8
                }
                \abjad-color-music #'red
                g'8
                \abjad-color-music #'red
                a'8
                r8
                r8
                \abjad-color-music #'blue
                <c' e' g'>8
                ~
                \abjad-color-music #'blue
                <c' e' g'>4
            }

    ..  container:: example

        Groups sixteenths by contiguity:

        >>> staff = abjad.Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.filter(
        ...     result, lambda _: abjad.get.duration(_) == abjad.Duration(1, 16)
        ... )
        >>> result = abjad.select.group_by_contiguity(result)
        >>> for item in result:
        ...     item
        ...
        [Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")]
        [Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'4
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'red
                d'16
                e'4
                \abjad-color-music #'blue
                f'16
                \abjad-color-music #'blue
                f'16
                \abjad-color-music #'blue
                f'16
                \abjad-color-music #'blue
                f'16
            }

    ..  container:: example

        Groups short-duration logical ties by contiguity; then gets leaf 0 in each
        group:

        >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 f'4 g'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff)
        >>> result = abjad.select.filter(
        ...     result, lambda _: abjad.get.duration(_) < abjad.Duration(1, 4)
        ... )
        >>> result = abjad.select.group_by_contiguity(result)
        >>> result = [abjad.select.leaf(_, 0) for _ in result]
        >>> for item in result:
        ...     item
        Note("d'8")
        Note("g'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'4
                \abjad-color-music #'red
                d'8
                ~
                d'16
                e'16
                ~
                e'8
                f'4
                \abjad-color-music #'blue
                g'8
            }

    ..  container:: example

        Groups pitched leaves pitch; then regroups each group by contiguity:

        >>> staff = abjad.Staff(r"""
        ...     c'8 ~ c'16 c'16 r8 c'16 c'16
        ...     d'8 ~ d'16 d'16 r8 d'16 d'16
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, pitched=True)
        >>> result = abjad.select.group_by_pitch(result)
        >>> result = [abjad.select.group_by_contiguity(_) for _ in result]
        >>> result = abjad.select.flatten(result)
        >>> for item in result:
        ...     item
        [Note("c'8"), Note("c'16"), Note("c'16")]
        [Note("c'16"), Note("c'16")]
        [Note("d'8"), Note("d'16"), Note("d'16")]
        [Note("d'16"), Note("d'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                ~
                \abjad-color-music #'red
                c'16
                \abjad-color-music #'red
                c'16
                r8
                \abjad-color-music #'blue
                c'16
                \abjad-color-music #'blue
                c'16
                \abjad-color-music #'red
                d'8
                ~
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'red
                d'16
                r8
                \abjad-color-music #'blue
                d'16
                \abjad-color-music #'blue
                d'16
            }

    ..  container:: example

        Groups pitched logical ties by contiguity; then regroups each group by pitch:

        >>> staff = abjad.Staff(r"""
        ...     c'8 ~ c'16 c'16 r8 c'16 c'16
        ...     d'8 ~ d'16 d'16 r8 d'16 d'16
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = abjad.select.group_by_contiguity(result)
        >>> result = [abjad.select.group_by_pitch(_) for _ in result]
        >>> result = abjad.select.flatten(result)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'8"), Note("c'16")]), LogicalTie(items=[Note("c'16")])]
        [LogicalTie(items=[Note("c'16")]), LogicalTie(items=[Note("c'16")])]
        [LogicalTie(items=[Note("d'8"), Note("d'16")]), LogicalTie(items=[Note("d'16")])]
        [LogicalTie(items=[Note("d'16")]), LogicalTie(items=[Note("d'16")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                ~
                \abjad-color-music #'red
                c'16
                \abjad-color-music #'red
                c'16
                r8
                \abjad-color-music #'blue
                c'16
                \abjad-color-music #'blue
                c'16
                \abjad-color-music #'red
                d'8
                ~
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'red
                d'16
                r8
                \abjad-color-music #'blue
                d'16
                \abjad-color-music #'blue
                d'16
            }

    '''
    result = []
    selection = []
    selection.extend(argument[:1])
    for item in argument[1:]:
        this_timespan = _getlib._get_timespan(selection[-1])
        that_timespan = _getlib._get_timespan(item)
        # remove displacement
        this_stop_offset = this_timespan.stop_offset
        this_stop_offset = _duration.Offset(this_stop_offset.pair)
        that_start_offset = that_timespan.start_offset
        that_start_offset = _duration.Offset(that_start_offset.pair)
        # if this_timespan.stop_offset == that_timespan.start_offset:
        if this_stop_offset == that_start_offset:
            selection.append(item)
        else:
            result.append(selection)
            selection = [item]
    if selection:
        result.append(selection)
    return result


def group_by_duration(argument) -> list[list]:
    r"""
    Groups items in ``argument`` by duration.

    ..  container:: example

        Groups logical ties by duration:

        >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff)
        >>> result = abjad.select.group_by_duration(result)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'4"), Note("c'16")])]
        [LogicalTie(items=[Note("d'16"), Note("d'16")])]
        [LogicalTie(items=[Note("d'16")])]
        [LogicalTie(items=[Note("e'4"), Note("e'16")])]
        [LogicalTie(items=[Note("f'16"), Note("f'16")])]
        [LogicalTie(items=[Note("f'16")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'4
                ~
                \abjad-color-music #'red
                c'16
                \abjad-color-music #'blue
                d'16
                ~
                \abjad-color-music #'blue
                d'16
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'blue
                e'4
                ~
                \abjad-color-music #'blue
                e'16
                \abjad-color-music #'red
                f'16
                ~
                \abjad-color-music #'red
                f'16
                \abjad-color-music #'blue
                f'16
            }

    """

    def predicate(argument):
        return _getlib._get_duration(argument)

    return group_by(argument, predicate=predicate)


def group_by_length(argument) -> list[list]:
    r"""
    Groups items in ``argument`` by length.

    ..  container:: example

        Groups logical ties by length:

        >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff)
        >>> result = abjad.select.group_by_length(result)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'4"), Note("c'16")]), LogicalTie(items=[Note("d'16"), Note("d'16")])]
        [LogicalTie(items=[Note("d'16")])]
        [LogicalTie(items=[Note("e'4"), Note("e'16")]), LogicalTie(items=[Note("f'16"), Note("f'16")])]
        [LogicalTie(items=[Note("f'16")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'4
                ~
                \abjad-color-music #'red
                c'16
                \abjad-color-music #'red
                d'16
                ~
                \abjad-color-music #'red
                d'16
                \abjad-color-music #'blue
                d'16
                \abjad-color-music #'red
                e'4
                ~
                \abjad-color-music #'red
                e'16
                \abjad-color-music #'red
                f'16
                ~
                \abjad-color-music #'red
                f'16
                \abjad-color-music #'blue
                f'16
            }

    """

    def predicate(argument):
        if isinstance(argument, _score.Leaf):
            return 1
        return len(argument)

    return group_by(argument, predicate)


def group_by_measure(argument) -> list[list]:
    r"""
    Groups items in ``argument`` by measure.

    ..  container:: example

        Groups leaves by measure:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.group_by_measure(result)
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8")]
        [Note("e'8"), Note("f'8")]
        [Note("g'8"), Note("a'8"), Note("b'8")]
        [Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                \time 2/8
                c'8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                \time 3/8
                g'8
                \abjad-color-music #'red
                a'8
                \abjad-color-music #'red
                b'8
                \abjad-color-music #'blue
                \time 1/8
                c''8
            }

    ..  container:: example

        Groups leaves by measure and joins pairs of consecutive groups:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.group_by_measure(result)
        >>> result = abjad.select.partition_by_counts(result, [2], cyclic=True)
        >>> result = [abjad.select.flatten(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
        [Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                \time 2/8
                c'8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'blue
                \time 3/8
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'blue
                b'8
                \abjad-color-music #'blue
                \time 1/8
                c''8
            }

    ..  container:: example

        Groups leaves by measure; then gets item 0 in each group:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.group_by_measure(result)
        >>> result = [_[0] for _ in result]
        >>> for item in result:
        ...     item
        Note("c'8")
        Note("e'8")
        Note("g'8")
        Note("c''8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                \time 2/8
                c'8
                d'8
                \abjad-color-music #'blue
                e'8
                f'8
                \abjad-color-music #'red
                \time 3/8
                g'8
                a'8
                b'8
                \abjad-color-music #'blue
                \time 1/8
                c''8
            }

    ..  container:: example

        Groups leaves by measure; then gets item -1 in each group:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.group_by_measure(result)
        >>> result = [_[-1] for _ in result]
        >>> for item in result:
        ...     item
        ...
        Note("d'8")
        Note("f'8")
        Note("b'8")
        Note("c''8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \time 2/8
                c'8
                \abjad-color-music #'red
                d'8
                e'8
                \abjad-color-music #'blue
                f'8
                \time 3/8
                g'8
                a'8
                \abjad-color-music #'red
                b'8
                \abjad-color-music #'blue
                \time 1/8
                c''8
            }

    ..  container:: example

        Works with implicit time signatures:

        >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
        >>> abjad.setting(staff).autoBeaming = False
        >>> score = abjad.Score([staff])
        >>> string = r"\musicLength 16"
        >>> abjad.setting(score).proportionalNotationDuration = string

        >>> result = abjad.select.leaves(score)
        >>> result = abjad.select.group_by_measure(result)
        >>> for item in result:
        ...     item
        ...
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]
        [Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'4
                \abjad-color-music #'red
                d'4
                \abjad-color-music #'red
                e'4
                \abjad-color-music #'red
                f'4
                \abjad-color-music #'blue
                g'4
                \abjad-color-music #'blue
                a'4
                \abjad-color-music #'blue
                b'4
                \abjad-color-music #'blue
                c''4
            }

    ..  container:: example

        Groups logical ties by measure:

        >>> staff = abjad.Staff("c'8 d' ~ d' e' ~ e' f' g' ~ g'")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = abjad.select.logical_ties(staff)
        >>> result = abjad.select.group_by_measure(result)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'8")]), LogicalTie(items=[Note("d'8"), Note("d'8")])]
        [LogicalTie(items=[Note("e'8"), Note("e'8")])]
        [LogicalTie(items=[Note("f'8")]), LogicalTie(items=[Note("g'8"), Note("g'8")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                \time 2/8
                c'8
                \abjad-color-music #'red
                d'8
                ~
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'blue
                e'8
                ~
                \abjad-color-music #'blue
                \time 3/8
                e'8
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'red
                g'8
                ~
                \abjad-color-music #'red
                \time 1/8
                g'8
            }

    ..  container:: example

        REGRESSION: works for pickup measure:

        >>> staff = abjad.Staff(r"c'4 | d'4 e'4 f'4 | g'4 a'4 b'4")
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=abjad.Duration(1, 4))
        >>> abjad.attach(time_signature, staff[0])

        >>> leaves = abjad.select.leaves(staff)
        >>> for measure in abjad.select.group_by_measure(leaves):
        ...     print(measure)
        ...
        [Note("c'4")]
        [Note("d'4"), Note("e'4"), Note("f'4")]
        [Note("g'4"), Note("a'4"), Note("b'4")]

    """

    def _get_first_component(argument):
        component = components(argument)[0]
        assert isinstance(component, _score.Component)
        return component

    def _get_measure_number(argument):
        first_component = _get_first_component(argument)
        assert first_component._measure_number is not None
        return first_component._measure_number

    selections = []
    first_component = _get_first_component(argument)
    _updatelib._update_measure_numbers(first_component)
    pairs = itertools.groupby(argument, _get_measure_number)
    for value, group in pairs:
        selections.append(list(group))
    return selections


def group_by_pitch(argument) -> list[list]:
    r"""
    Groups items in ``argument`` by pitch.

    ..  container:: example

        Groups logical ties by pitches:

        >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> lts = abjad.select.logical_ties(staff)
        >>> result = abjad.select.group_by_pitch(lts)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'4"), Note("c'16")])]
        [LogicalTie(items=[Note("d'16"), Note("d'16")]), LogicalTie(items=[Note("d'16")])]
        [LogicalTie(items=[Note("e'4"), Note("e'16")])]
        [LogicalTie(items=[Note("f'16"), Note("f'16")]), LogicalTie(items=[Note("f'16")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'4
                ~
                \abjad-color-music #'red
                c'16
                \abjad-color-music #'blue
                d'16
                ~
                \abjad-color-music #'blue
                d'16
                \abjad-color-music #'blue
                d'16
                \abjad-color-music #'red
                e'4
                ~
                \abjad-color-music #'red
                e'16
                \abjad-color-music #'blue
                f'16
                ~
                \abjad-color-music #'blue
                f'16
                \abjad-color-music #'blue
                f'16
            }

    """

    def predicate(argument):
        generator = _iterate.pitches(argument)
        return _pcollections.PitchSet(generator)

    return group_by(argument, predicate)


def leaf(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    head: bool | None = None,
    pitched: bool | None = None,
    prototype=None,
    reverse: bool | None = None,
    tail: bool | None = None,
    trim: bool | _enums.Horizontal | None = None,
) -> _score.Leaf:
    r"""
    Selects leaf ``n` in ``argument``.

    ..  container:: example

        Selects leaf -1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.leaf(staff, -1)
        >>> result
        Chord("<fs' gs'>16")

        >>> abjad.label.color_leaves(result, "#green")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    return leaves(
        argument,
        exclude=exclude,
        grace=grace,
        head=head,
        pitched=pitched,
        prototype=prototype,
        reverse=reverse,
        tail=tail,
        trim=trim,
    )[n]


@typing.overload
def leaves(
    argument,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    head: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
    tail: bool | None = None,
    trim: bool | _enums.Horizontal | None = None,
) -> list[_score.Leaf]:
    pass


@typing.overload
def leaves(
    argument,
    prototype: typing.Type[_score.Chord],
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    head: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
    tail: bool | None = None,
    trim: bool | _enums.Horizontal | None = None,
) -> list[_score.Chord]:
    pass


@typing.overload
def leaves(
    argument,
    prototype: typing.Type[_score.MultimeasureRest],
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    head: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
    tail: bool | None = None,
    trim: bool | _enums.Horizontal | None = None,
) -> list[_score.MultimeasureRest]:
    pass


@typing.overload
def leaves(
    argument,
    prototype: typing.Type[_score.Note],
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    head: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
    tail: bool | None = None,
    trim: bool | _enums.Horizontal | None = None,
) -> list[_score.Note]:
    pass


def leaves(
    argument,
    prototype=None,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    head: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
    tail: bool | None = None,
    trim: bool | _enums.Horizontal | None = None,
):
    r'''
    Selects leaves in ``argument``.

    ..  container:: example

        Selects leaves:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> for item in result:
        ...     item
        ...
        Rest('r8')
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Rest('r8')
        Rest('r8')
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Rest('r8')

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                }
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'red
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    r8
                }
            }

    ..  container:: example

        Selects pitched leaves:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, pitched=True)
        >>> for item in result:
        ...     item
        ...
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                }
                \abjad-color-music #'red
                f'8
                r8
                r8
                \abjad-color-music #'blue
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    d'8
                    r8
                }
            }

    ..  container:: example

        Trimmed leaves are the correct selection for ottava brackets.

        Selects trimmed leaves:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, trim=True)
        >>> for item in result:
        ...     item
        ...
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Rest('r8')
        Rest('r8')
        Note("f'8")
        Note("e'8")
        Note("d'8")

        >>> abjad.ottava(result)
        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    r8
                    \abjad-color-music #'red
                    \ottava 1
                    d'8
                    \abjad-color-music #'blue
                    e'8
                }
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    d'8
                    \ottava 0
                    r8
                }
            }

    ..  container:: example

        Set ``trim`` to ``abjad.LEFT`` to trim rests at left (and preserve rests at
        right):

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, trim=abjad.LEFT)
        >>> for item in result:
        ...     item
        ...
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Rest('r8')
        Rest('r8')
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Rest('r8')

        >>> abjad.ottava(result)
        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    r8
                    \abjad-color-music #'red
                    \ottava 1
                    d'8
                    \abjad-color-music #'blue
                    e'8
                }
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    r8
                    \ottava 0
                }
            }

    ..  container:: example

        REGRESSION: selects trimmed leaves (even when there are no rests to trim):

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { c'8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' c' }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, trim=True)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Rest('r8')
        Rest('r8')
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                }
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'red
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    c'8
                }
            }

    ..  container:: example

        Selects leaves in tuplets:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)
        >>> result = abjad.select.leaves(result)
        >>> for item in result:
        ...     item
        ...
        Rest('r8')
        Note("d'8")
        Note("e'8")
        Note("e'8")
        Note("d'8")
        Rest('r8')

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                }
                f'8
                r8
                r8
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    r8
                }
            }

    ..  container:: example

        Selects trimmed leaves in tuplets:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)
        >>> result = abjad.select.leaves(result, trim=True)
        >>> for item in result:
        ...     item
        ...
        Note("d'8")
        Note("e'8")
        Note("e'8")
        Note("d'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                }
                f'8
                r8
                r8
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    d'8
                    r8
                }
            }

    ..  container:: example

        Pitched heads is the correct selection for most articulations.

        Selects pitched heads in tuplets:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { c'8 d' ~ d' } e' r
        ...     r e' \times 2/3 { d' ~ d' c' }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)
        >>> result = abjad.select.leaves(result, head=True, pitched=True)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Note("d'8")
        Note("c'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    ~
                    d'8
                }
                e'8
                r8
                r8
                e'8
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    d'8
                    ~
                    d'8
                    \abjad-color-music #'blue
                    c'8
                }
            }

    ..  container:: example

        Pitched tails in the correct selection for laissez vibrer.

        Selects pitched tails in tuplets:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { c'8 d' ~ d' } e' r
        ...     r e' \times 2/3 { d' ~ d' c' }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)
        >>> result = abjad.select.leaves(result, tail=True, pitched=True)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Note("d'8")
        Note("c'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'8
                    d'8
                    ~
                    \abjad-color-music #'blue
                    d'8
                }
                e'8
                r8
                r8
                e'8
                \tuplet 3/2
                {
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    c'8
                }
            }

    ..  container:: example

        Chord heads are the correct selection for arpeggios.

        Selects chord heads in tuplets:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { <c' e' g'>8 ~ <c' e' g'> d' } e' r
        ...     r <g d' fs'> \times 2/3 { e' <c' d'> ~ <c' d'> }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)
        >>> result = abjad.select.leaves(result, abjad.Chord, head=True)
        >>> for item in result:
        ...     item
        ...
        Chord("<c' e' g'>8")
        Chord("<c' d'>8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    <c' e' g'>8
                    ~
                    <c' e' g'>8
                    d'8
                }
                e'8
                r8
                r8
                <g d' fs'>8
                \tuplet 3/2
                {
                    e'8
                    \abjad-color-music #'blue
                    <c' d'>8
                    ~
                    <c' d'>8
                }
            }

    ..  container:: example

        Excludes leaves with ``"HIDDEN"`` indicator:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { r8 d' e' } f' r
        ...     r f' \times 2/3 { e' d' r8 }
        ...     """)
        >>> abjad.attach("HIDDEN", staff[-1][-2])
        >>> abjad.attach("HIDDEN", staff[-1][-1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, exclude="HIDDEN")
        >>> for item in result:
        ...     item
        ...
        Rest('r8')
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Rest('r8')
        Rest('r8')
        Note("f'8")
        Note("e'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                }
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'red
                f'8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    d'8
                    r8
                }
            }

    ..  container:: example

        Selects both main notes and graces when ``grace=None``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, grace=None)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("cf''16")
        Note("bf'16")
        Note("d'8")
        Note("af'16")
        Note("gf'16")
        Note("e'8")
        Note("f'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \grace {
                    \abjad-color-music #'blue
                    cf''16
                    \abjad-color-music #'red
                    bf'16
                }
                \abjad-color-music #'blue
                \afterGrace
                d'8
                {
                    \abjad-color-music #'red
                    af'16
                    \abjad-color-music #'blue
                    gf'16
                }
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, grace=None)
        >>> for item in result:
        ...     item
        ...
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("gf'16")
        Note("f'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'blue
                        gf'16
                    }
                    \abjad-color-music #'red
                    f'4
                }
            }

    ..  container:: example

        Excludes grace notes when ``grace=False``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, grace=False)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \grace {
                    cf''16
                    bf'16
                }
                \abjad-color-music #'blue
                \afterGrace
                d'8
                {
                    af'16
                    gf'16
                }
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, grace=False)
        >>> for item in result:
        ...     item
        ...
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("f'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    \abjad-color-music #'blue
                    f'4
                }
            }

    ..  container:: example

        Selects only grace notes when ``grace=True``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, grace=True)
        >>> for item in result:
        ...     item
        ...
        Note("cf''16")
        Note("bf'16")
        Note("af'16")
        Note("gf'16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                \grace {
                    \abjad-color-music #'red
                    cf''16
                    \abjad-color-music #'blue
                    bf'16
                }
                \afterGrace
                d'8
                {
                    \abjad-color-music #'red
                    af'16
                    \abjad-color-music #'blue
                    gf'16
                }
                e'8
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff, grace=True)
        >>> for item in result:
        ...     item
        ...
        Note("gf'16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    f'4
                }
            }

    '''
    assert trim in (True, False, _enums.LEFT, None)
    if pitched:
        prototype = (_score.Chord, _score.Note)
    elif prototype is None:
        prototype = _score.Leaf
    prototype = prototype or _score.Component
    if not isinstance(prototype, tuple):
        prototype = (prototype,)
    result = []
    components = _components_alias(
        argument, prototype=prototype, exclude=exclude, grace=grace, reverse=reverse
    )
    if components:
        if trim in (True, _enums.LEFT):
            components = _trim_subresult(components, trim)
        if head is not None:
            components = _head_filter_subresult(components, head)
        if tail is not None:
            components = _tail_filter_subresult(components, tail)
        result.extend(components)
    return result


def logical_tie(
    argument,
    n: int = 0,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    nontrivial: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
) -> LogicalTie:
    r"""
    Selects logical tie ``n`` in ``argument``.

    ..  todo:: Make work on nonhead leaves.

    ..  todo:: Write examples.

    ..  todo:: Remove ``abjad.get.logical_tie()``.

    """
    return logical_ties(
        argument,
        exclude=exclude,
        grace=grace,
        nontrivial=nontrivial,
        pitched=pitched,
        reverse=reverse,
    )[n]


def logical_ties(
    argument,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
    nontrivial: bool | None = None,
    pitched: bool | None = None,
    reverse: bool | None = None,
) -> list[LogicalTie]:
    r'''
    Selects logical ties in ``argument``.

    ..  container:: example

        Selects logical ties:

        >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'8")])
        LogicalTie(items=[Note("d'8"), Note("d'8")])
        LogicalTie(items=[Note("e'8")])
        LogicalTie(items=[Rest('r8')])
        LogicalTie(items=[Note("f'8"), Note("f'8")])
        LogicalTie(items=[Rest('r8')])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                d'8
                ~
                {
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    ~
                }
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'blue
                r8
            }

    ..  container:: example

        Selects pitched logical ties:

        >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'8")])
        LogicalTie(items=[Note("d'8"), Note("d'8")])
        LogicalTie(items=[Note("e'8")])
        LogicalTie(items=[Note("f'8"), Note("f'8")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                d'8
                ~
                {
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    ~
                }
                \abjad-color-music #'blue
                f'8
                r8
            }

    ..  container:: example

        Selects pitched nontrivial logical ties:

        >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(
        ...     staff,
        ...     pitched=True,
        ...     nontrivial=True,
        ... )
        >>> for item in result:
        ...     item
        LogicalTie(items=[Note("d'8"), Note("d'8")])
        LogicalTie(items=[Note("f'8"), Note("f'8")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                \abjad-color-music #'red
                d'8
                ~
                {
                    \abjad-color-music #'red
                    d'8
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    ~
                }
                \abjad-color-music #'blue
                f'8
                r8
            }

    ..  container:: example

        Selects pitched logical ties (starting) in each tuplet:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
        ...     \times 2/3 { f' g' a' ~ } a' b' ~
        ...     \times 2/3 { b' c'' d'' }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)
        >>> result = [abjad.select.logical_ties(_, pitched=True) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'8")]), LogicalTie(items=[Note("d'8")]), LogicalTie(items=[Note("e'8"), Note("e'8")])]
        [LogicalTie(items=[Note("g'8")]), LogicalTie(items=[Note("a'8"), Note("a'8")])]
        [LogicalTie(items=[Note("c''8")]), LogicalTie(items=[Note("d''8")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    ~
                }
                \abjad-color-music #'red
                e'8
                f'8
                ~
                \tuplet 3/2
                {
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    ~
                }
                \abjad-color-music #'blue
                a'8
                b'8
                ~
                \tuplet 3/2
                {
                    b'8
                    \abjad-color-music #'red
                    c''8
                    \abjad-color-music #'red
                    d''8
                }
            }

    ..  container:: example

        Selects pitched logical ties (starting) in each of the last two tuplets:

        >>> staff = abjad.Staff(r"""
        ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
        ...     \times 2/3 { f' g' a' ~ } a' b' ~
        ...     \times 2/3 { b' c'' d'' }
        ...     """)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.components(staff, abjad.Tuplet)[-2:]
        >>> result = [abjad.select.logical_ties(_, pitched=True) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("g'8")]), LogicalTie(items=[Note("a'8"), Note("a'8")])]
        [LogicalTie(items=[Note("c''8")]), LogicalTie(items=[Note("d''8")])]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \tuplet 3/2
                {
                    c'8
                    d'8
                    e'8
                    ~
                }
                e'8
                f'8
                ~
                \tuplet 3/2
                {
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                    ~
                }
                \abjad-color-music #'red
                a'8
                b'8
                ~
                \tuplet 3/2
                {
                    b'8
                    \abjad-color-music #'blue
                    c''8
                    \abjad-color-music #'blue
                    d''8
                }
            }

    ..  container:: example

        Selects both main notes and graces when ``grace=None``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, grace=None)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'8")])
        LogicalTie(items=[Note("cf''16")])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("af'16")])
        LogicalTie(items=[Note("gf'16")])
        LogicalTie(items=[Note("e'8")])
        LogicalTie(items=[Note("f'8")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \grace {
                    \abjad-color-music #'blue
                    cf''16
                    \abjad-color-music #'red
                    bf'16
                }
                \abjad-color-music #'blue
                \afterGrace
                d'8
                {
                    \abjad-color-music #'red
                    af'16
                    \abjad-color-music #'blue
                    gf'16
                }
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, grace=None)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("e'4")])
        LogicalTie(items=[Note("gf'16")])
        LogicalTie(items=[Note("f'4")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'blue
                        gf'16
                    }
                    \abjad-color-music #'red
                    f'4
                }
            }

    ..  container:: example

        Excludes grace notes when ``grace=False``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, grace=False)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'8")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("e'8")])
        LogicalTie(items=[Note("f'8")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \grace {
                    cf''16
                    bf'16
                }
                \abjad-color-music #'blue
                \afterGrace
                d'8
                {
                    af'16
                    gf'16
                }
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, grace=False)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("d'4")])
        LogicalTie(items=[Note("e'4")])
        LogicalTie(items=[Note("f'4")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        gf'16
                    }
                    \abjad-color-music #'blue
                    f'4
                }
            }

    ..  container:: example

        Selects only grace notes when ``grace=True``:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False


        >>> result = abjad.select.logical_ties(staff, grace=True)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("cf''16")])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Note("af'16")])
        LogicalTie(items=[Note("gf'16")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                \grace {
                    \abjad-color-music #'red
                    cf''16
                    \abjad-color-music #'blue
                    bf'16
                }
                \afterGrace
                d'8
                {
                    \abjad-color-music #'red
                    af'16
                    \abjad-color-music #'blue
                    gf'16
                }
                e'8
                f'8
            }

        Works with independent after-grace containers:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, grace=True)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("gf'16")])

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    f'4
                }
            }

    '''
    generator = _iterlib._iterate_logical_ties(
        argument,
        exclude=exclude,
        grace=None,
        nontrivial=nontrivial,
        pitched=pitched,
        reverse=reverse,
    )
    result = []
    for logical_tie in generator:
        if (
            grace is None
            or (grace is True and _get.grace(logical_tie.head))
            or (grace is False and not _get.grace(logical_tie.head))
        ):
            result.append(logical_tie)
    return result


def nontrivial(argument) -> list:
    r"""
    Selects nontrivial items in ``argument``.

    ..  container:: example

        Selects nontrivial runs:

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.runs(staff)
        >>> result = abjad.select.nontrivial(result)
        >>> for item in result:
        ...     item
        ...
        [Note("d'8"), Note("e'8")]
        [Note("f'8"), Note("g'8"), Note("a'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                e'8
                r8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'blue
                g'8
                \abjad-color-music #'blue
                a'8
            }

    """
    items = [_ for _ in argument if len(_) > 1]
    return items


def note(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> _score.Note:
    r"""
    Selects note ``n`` in ``argument``.

    ..  container:: example

        Selects note -1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.note(staff, -1)
        >>> result
        Note("e'16")

        >>> abjad.label.color_leaves(result, "#green")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'green
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    return notes(argument, exclude=exclude, grace=grace)[n]


def notes(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[_score.Note]:
    r"""
    Selects notes in ``argument``.

    ..  container:: example

        Selects notes:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.notes(staff)
        >>> for item in result:
        ...     item
        ...
        Note("bf'16")
        Note("c'16")
        Note("bf'16")
        Note("d'16")
        Note("bf'16")
        Note("e'16")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'blue
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'blue
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'blue
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    items = []
    for item in components(argument, _score.Note, exclude=exclude, grace=grace):
        assert isinstance(item, _score.Note)
        items.append(item)
    return items


def partition_by_counts(
    argument,
    counts,
    *,
    cyclic: bool = False,
    enchain: bool = False,
    fuse_overhang: bool = False,
    nonempty: bool = False,
    overhang: bool | _enums.Comparison = False,
) -> list[list]:
    r"""
    Partitions items in ``argument`` by ``counts``.

    ..  container:: example

        Partitions leaves into a single part of length 3; truncates overhang:

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     result,
        ...     [3],
        ...     cyclic=False,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8'), Note("d'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'red
                d'8
                e'8
                r8
                f'8
                g'8
                a'8
            }

    ..  container:: example

        Cyclically partitions leaves into parts of length 3; truncates overhang:

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     result,
        ...     [3],
        ...     cyclic=True,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8'), Note("d'8")]
        [Note("e'8"), Rest('r8'), Note("f'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                f'8
                g'8
                a'8
            }

    ..  container:: example

        Cyclically partitions leaves into parts of length 3; returns overhang at end:

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     result,
        ...     [3],
        ...     cyclic=True,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8'), Note("d'8")]
        [Note("e'8"), Rest('r8'), Note("f'8")]
        [Note("g'8"), Note("a'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                g'8
                \abjad-color-music #'red
                a'8
            }

    ..  container:: example

        Cyclically partitions leaves into parts of length 3; fuses overhang to last
        part:

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     result,
        ...     [3],
        ...     cyclic=True,
        ...     fuse_overhang=True,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8'), Note("d'8")]
        [Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'blue
                g'8
                \abjad-color-music #'blue
                a'8
            }

    ..  container:: example

        Cyclically partitions leaves into parts of length 3; returns overhang at end:

        >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     leaves,
        ...     [1, 2, 3],
        ...     cyclic=True,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Rest('r8'), Note("d'8")]
        [Note("e'8"), Rest('r8'), Note("f'8")]
        [Note("g'8")]
        [Note("a'8"), Note("b'8")]
        [Rest('r8'), Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue", "#cyan"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'cyan
                e'8
                \abjad-color-music #'cyan
                r8
                \abjad-color-music #'cyan
                f'8
                \abjad-color-music #'red
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'blue
                b'8
                \abjad-color-music #'cyan
                r8
                \abjad-color-music #'cyan
                c''8
            }

    ..  container:: example

        With negative ``counts``.

        Partitions leaves alternately into parts 2 and -3 (without overhang):

        >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     leaves,
        ...     [2, -3],
        ...     cyclic=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8')]
        [Note("f'8"), Note("g'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                d'8
                e'8
                r8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'blue
                g'8
                a'8
                b'8
                r8
                c''8
            }

    ..  container:: example

        With negative ``counts``.

        Partitions leaves alternately into parts 2 and -3 (with overhang):

        >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     leaves,
        ...     [2, -3],
        ...     cyclic=True,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8')]
        [Note("f'8"), Note("g'8")]
        [Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                d'8
                e'8
                r8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'blue
                g'8
                a'8
                b'8
                r8
                \abjad-color-music #'red
                c''8
            }

    ..  container:: example

        REGRESSION. Noncyclic counts work when ``overhang`` is true:

        >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_counts(
        ...     leaves,
        ...     [3],
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8'), Note("d'8")]
        [Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8'), Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'blue
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'blue
                b'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                c''8
            }

    """
    result = []
    groups_ = _sequence.partition_by_counts(
        argument,
        [abs(_) for _ in counts],
        cyclic=cyclic,
        enchain=enchain,
        overhang=overhang,
    )
    groups = list(groups_)
    total = len(groups)
    if overhang and fuse_overhang and 1 < len(groups):
        last_count = counts[(len(groups) - 1) % len(counts)]
        if len(groups[-1]) != last_count:
            last_group = groups.pop()
            groups[-1] += last_group
    subresult = []
    if cyclic:
        counts = _cyclictuple.CyclicTuple(counts)
    for i, group in enumerate(groups):
        if overhang and i == total - 1:
            pass
        else:
            try:
                count = counts[i]
            except Exception:
                raise Exception(counts, i)
            if count < 0:
                continue
        subresult.append(group)
    if nonempty and not subresult:
        subresult.append(groups[0])
    result.extend(subresult)
    return result


def partition_by_durations(
    argument,
    durations,
    *,
    cyclic: bool = False,
    fill: _enums.Comparison | None = None,
    in_seconds: bool = False,
    overhang: bool | _enums.Comparison = False,
) -> list[list]:
    r"""
    Partitions items in ``argument`` by ``durations``.

    ..  container:: example

        Cyclically partitions leaves into parts equal to exactly 3/8; returns
        overhang at end:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> leaves = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     leaves,
        ...     [abjad.Duration(3, 8)],
        ...     cyclic=True,
        ...     fill=abjad.EXACT,
        ...     in_seconds=False,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Note("e'8")]
        [Note("f'8"), Note("g'8"), Note("a'8")]
        [Note("b'8"), Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }
                {
                    \abjad-color-music #'blue
                    \time 2/8
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    b'8
                    \abjad-color-music #'red
                    c''8
                }
            }

    ..  container:: example

        Partitions leaves into one part equal to exactly 3/8; truncates overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [abjad.Duration(3, 8)],
        ...     cyclic=False,
        ...     fill=abjad.EXACT,
        ...     in_seconds=False,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Note("e'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    f'8
                }
                {
                    \time 2/8
                    g'8
                    a'8
                }
                {
                    \time 2/8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Cyclically partitions leaves into parts equal to (or just less than) 3/16 and
        1/16; returns overhang at end:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [abjad.Duration(3, 16), abjad.Duration(1, 16)],
        ...     cyclic=True,
        ...     fill=abjad.MORE,
        ...     in_seconds=False,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8")]
        [Note("e'8")]
        [Note("f'8"), Note("g'8")]
        [Note("a'8")]
        [Note("b'8"), Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                }
                {
                    \abjad-color-music #'blue
                    \time 2/8
                    e'8
                    \abjad-color-music #'red
                    f'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    b'8
                    \abjad-color-music #'red
                    c''8
                }
            }

    ..  container:: example

        Cyclically partitions leaves into parts equal to (or just less than) 3/16;
        truncates overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [abjad.Duration(3, 16)],
        ...     cyclic=True,
        ...     fill=abjad.LESS,
        ...     in_seconds=False,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Note("d'8")]
        [Note("e'8")]
        [Note("f'8")]
        [Note("g'8")]
        [Note("a'8")]
        [Note("b'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \time 2/8
                    c'8
                    \abjad-color-music #'blue
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Partitions leaves into a single part equal to (or just less than) 3/16;
        truncates overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [abjad.Duration(3, 16)],
        ...     cyclic=False,
        ...     fill=abjad.LESS,
        ...     in_seconds=False,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    \time 2/8
                    e'8
                    f'8
                }
                {
                    \time 2/8
                    g'8
                    a'8
                }
                {
                    \time 2/8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Cyclically partitions leaves into parts equal to exactly 1.5 seconds;
        truncates overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(mark, leaf, context='Staff')

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [1.5],
        ...     cyclic=True,
        ...     fill=abjad.EXACT,
        ...     in_seconds=True,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Note("e'8")]
        [Note("f'8"), Note("g'8"), Note("a'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \tempo 4=60
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }
                {
                    \abjad-color-music #'blue
                    \time 2/8
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }
                {
                    \time 2/8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Cyclically partitions leaves into parts equal to exactly 1.5 seconds; returns
        overhang at end:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(mark, leaf, context='Staff')

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [1.5],
        ...     cyclic=True,
        ...     fill=abjad.EXACT,
        ...     in_seconds=True,
        ...     overhang=True,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Note("e'8")]
        [Note("f'8"), Note("g'8"), Note("a'8")]
        [Note("b'8"), Note("c''8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \tempo 4=60
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }
                {
                    \abjad-color-music #'blue
                    \time 2/8
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    b'8
                    \abjad-color-music #'red
                    c''8
                }
            }

    ..  container:: example

        Partitions leaves into a single part equal to exactly 1.5 seconds; truncates
        overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(mark, leaf, context='Staff')

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [1.5],
        ...     cyclic=False,
        ...     fill=abjad.EXACT,
        ...     in_seconds=True,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Note("e'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \tempo 4=60
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    f'8
                }
                {
                    \time 2/8
                    g'8
                    a'8
                }
                {
                    \time 2/8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Cyclically partitions leaves into parts equal to (or just less than) 0.75
        seconds; truncates overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(mark, leaf, context='Staff')

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [0.75],
        ...     cyclic=True,
        ...     fill=abjad.LESS,
        ...     in_seconds=True,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Note("d'8")]
        [Note("e'8")]
        [Note("f'8")]
        [Note("g'8")]
        [Note("a'8")]
        [Note("b'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \tempo 4=60
                    \time 2/8
                    c'8
                    \abjad-color-music #'blue
                    d'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }
                {
                    \abjad-color-music #'red
                    \time 2/8
                    b'8
                    c''8
                }
            }

    ..  container:: example

        Partitions leaves into one part equal to (or just less than) 0.75 seconds;
        truncates overhang:

        >>> staff = abjad.Staff([
        ...     abjad.Container("c'8 d'"),
        ...     abjad.Container("e'8 f'"),
        ...     abjad.Container("g'8 a'"),
        ...     abjad.Container("b'8 c''"),
        ... ])
        >>> score = abjad.Score([staff], name="Score")
        >>> for container in staff:
        ...     time_signature = abjad.TimeSignature((2, 8))
        ...     abjad.attach(time_signature, container[0])
        ...
        >>> abjad.setting(staff).autoBeaming = False
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(mark, leaf, context='Staff')

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_durations(
        ...     result,
        ...     [0.75],
        ...     cyclic=False,
        ...     fill=abjad.LESS,
        ...     in_seconds=True,
        ...     overhang=False,
        ... )
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {
                    \abjad-color-music #'red
                    \tempo 4=60
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    \time 2/8
                    e'8
                    f'8
                }
                {
                    \time 2/8
                    g'8
                    a'8
                }
                {
                    \time 2/8
                    b'8
                    c''8
                }
            }

    Interprets ``fill`` as ``Exact`` when ``fill`` is none.

    Parts must equal ``durations`` exactly when ``fill`` is ``Exact``.

    Parts must be less than or equal to ``durations`` when ``fill`` is ``Less``.

    Parts must be greater or equal to ``durations`` when ``fill`` is ``More``.

    Reads ``durations`` cyclically when ``cyclic`` is true.

    Reads component durations in seconds when ``in_seconds`` is true.

    Returns remaining components at end in final part when ``overhang`` is true.
    """
    fill = fill or _enums.EXACT
    durations = [_duration.Duration(_) for _ in durations]
    if cyclic:
        durations = _cyclictuple.CyclicTuple(durations)
    result = []
    part = []
    current_duration_index = 0
    target_duration = durations[current_duration_index]
    cumulative_duration = _duration.Duration(0)
    components_copy = list(argument)
    while True:
        try:
            component = components_copy.pop(0)
        except IndexError:
            break
        component_duration = component._get_duration()
        if in_seconds:
            component_duration = _getlib._get_duration_in_seconds(component)
        candidate_duration = cumulative_duration + component_duration
        if candidate_duration < target_duration:
            part.append(component)
            cumulative_duration = candidate_duration
        elif candidate_duration == target_duration:
            part.append(component)
            result.append(part)
            part = []
            cumulative_duration = _duration.Duration(0)
            current_duration_index += 1
            try:
                target_duration = durations[current_duration_index]
            except IndexError:
                break
        elif target_duration < candidate_duration:
            if fill is _enums.EXACT:
                raise Exception("must partition exactly.")
            elif fill is _enums.LESS:
                result.append(part)
                part = [component]
                if in_seconds:
                    sum_ = sum([_getlib._get_duration_in_seconds(_) for _ in part])
                    cumulative_duration = _duration.Duration(sum_)
                else:
                    sum_ = sum([_getlib._get_duration(_) for _ in part])
                    cumulative_duration = _duration.Duration(sum_)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
                if target_duration < cumulative_duration:
                    message = f"target duration {target_duration} is less"
                    message += " than cumulative duration"
                    message += f" {cumulative_duration}."
                    raise Exception(message)
            elif fill is _enums.MORE:
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = _duration.Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
    if len(part):
        if overhang:
            result.append(part)
    if len(components_copy):
        if overhang:
            result.append(components_copy)
    selections = [list(_) for _ in result]
    return selections


def partition_by_ratio(argument, ratio: tuple[int, ...]) -> list[list]:
    r"""
    Partitions items in ``argument`` by ``ratio``.

    ..  container:: example

        Partitions leaves by a ratio of 1:1:

        >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_ratio(result, (1, 1))
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8')]
        [Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                r8
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    f'8
                }
                \abjad-color-music #'blue
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'blue
                r8
            }

    ..  container:: example

        Partitions leaves by a ratio of 1:1:1:

        >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.partition_by_ratio(result, (1, 1, 1))
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Note("d'8"), Rest('r8')]
        [Note("e'8"), Rest('r8'), Note("f'8")]
        [Note("g'8"), Note("a'8"), Rest('r8')]

        >>> abjad.label.color_leaves(result, ["#red", "#blue", "#cyan"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                r8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                }
                \abjad-color-music #'cyan
                g'8
                \abjad-color-music #'cyan
                a'8
                \abjad-color-music #'cyan
                r8
            }

    """
    ratio = ratio or (1,)
    counts = _math.partition_integer_by_ratio(len(argument), ratio)
    parts = _sequence.partition_by_counts(argument, counts=counts)
    selections = [list(_) for _ in parts]
    return selections


def rest(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> _score.Rest | _score.MultimeasureRest:
    r"""
    Selects rest ``n`` in ``argument``.

    ..  container:: example

        Selects rest -1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.rest(staff, -1)
        >>> result
        Rest('r16')

        >>> abjad.label.color_leaves(result, "#green")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'green
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    return rests(argument, exclude=exclude, grace=grace)[n]


def rests(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[_score.Rest | _score.MultimeasureRest]:
    r"""
    Selects rests in ``argument``.

    ..  container:: example

        Selects rests:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.rests(staff)
        >>> for item in result:
        ...     item
        ...
        Rest('r16')
        Rest('r16')
        Rest('r16')

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'red
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            \abjad-color-music #'blue
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'red
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    items = []
    prototype = (_score.MultimeasureRest, _score.Rest)
    for item in components(argument, prototype=prototype, exclude=exclude, grace=grace):
        assert isinstance(item, prototype)
        items.append(item)
    return items


def run(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> list[_score.Leaf]:
    r"""
    Selects run ``n`` in ``argument``.

    ..  container:: example

        Selects run -1:

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.run(staff, -1)
        >>> result
        [Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

        >>> abjad.label.color_leaves(result, "#green")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            d'16
                            d'16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    return runs(argument, exclude=exclude)[n]


def runs(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[list]:
    r"""
    Selects runs in ``argument``.

    ..  container:: example

        Selects runs:

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.runs(staff)
        >>> for item in result:
        ...     item
        ...
        [Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")]
        [Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")]
        [Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            \abjad-color-music #'red
                            c'16
                            \abjad-color-music #'red
                            c'16
                            \abjad-color-music #'red
                            c'16
                            \abjad-color-music #'red
                            <d' e'>4
                            ~
                            \abjad-color-music #'red
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            \abjad-color-music #'blue
                            d'16
                            \abjad-color-music #'blue
                            d'16
                            \abjad-color-music #'blue
                            d'16
                            \abjad-color-music #'blue
                            <e' fs'>4
                            ~
                            \abjad-color-music #'blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            r16
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'red
                            <fs' gs'>16
                        }
                    }
                }
            }

    ..  container:: example

        REGRESSION. Works with grace note (and containers):

        >>> music_voice = abjad.Voice(
        ...     "c'16 d' e' r d'4 e' r8 f'", name="MusicVoice"
        ... )
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[4])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[5:7])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[-1])
        >>> staff = abjad.Staff([music_voice])

        >>> result = abjad.select.runs(staff)
        >>> for item in result:
        ...     item
        ...
        [Note("c'16"), Note("d'16"), Note("e'16")]
        [Note("cs'16"), Note("d'4"), Chord("<e' g'>16"), Note("gs'16"), Note("a'16"), Note("as'16"), Note("e'4")]
        [Note("f'8"), Note("fs'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'16
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'red
                    e'16
                    r16
                    \grace {
                        \abjad-color-music #'blue
                        cs'16
                    }
                    \abjad-color-music #'blue
                    d'4
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \abjad-color-music #'blue
                            \set fontSize = #-3
                            \slash
                            \voiceOne
                            <
                                \tweak font-size 0
                                \tweak transparent ##t
                                e'
                                g'
                            >16
                            - \accent
                            [
                            (
                            \abjad-color-music #'blue
                            gs'16
                            \abjad-color-music #'blue
                            a'16
                            \abjad-color-music #'blue
                            as'16
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \abjad-color-music #'blue
                            \voiceTwo
                            e'4
                            r8
                        }
                    >>
                    \abjad-color-music #'red
                    \oneVoice
                    \afterGrace
                    f'8
                    {
                        \abjad-color-music #'red
                        fs'16
                    }
                }
            }

    """
    result = leaves(argument, exclude=exclude, grace=grace, pitched=True)
    groups = group_by_contiguity(result)
    return groups


def top(argument, *, exclude: _typings.Exclude | None = None) -> list[_score.Component]:
    r"""
    Selects top components in ``argument``.

    ..  container:: example

        Selects top components (up from leaves):

        >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.leaves(staff)
        >>> result = abjad.select.top(result)
        >>> for item in result:
        ...     item
        ...
        Note("c'8")
        Note("d'8")
        Rest('r8')
        Tuplet('3:2', "e'8 r8 f'8")
        Note("g'8")
        Note("a'8")
        Rest('r8')

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'red
                r8
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                }
                \abjad-color-music #'red
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'red
                r8
            }

    """
    result = []
    for component in _iterlib._public_iterate_components(argument, exclude=exclude):
        for component_ in _parentage.Parentage(component):
            if (
                _is_immediate_child_of_outermost_voice(component_)
                and component_ not in result
            ):
                result.append(component_)
    return result


def tuplet(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    level: int | None = None,
) -> _score.Tuplet:
    r"""
    Selects tuplet ``n`` in ``argument``.

    ..  container:: example

        Selects tuplet -1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, -1)
        >>> result
        Tuplet('9:10', "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 <fs' gs'>16")

        >>> abjad.label.color_leaves(result, "#green")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \context Voice = "Voice"
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \tuplet 9/8
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 9/10
                        {
                            \abjad-color-music #'green
                            r16
                            \abjad-color-music #'green
                            bf'16
                            \abjad-color-music #'green
                            <a'' b''>16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                }
            }

    """
    return tuplets(argument, exclude=exclude, level=level)[n]


def tuplets(
    argument, *, exclude: _typings.Exclude | None = None, level: int | None = None
) -> list[_score.Tuplet]:
    r"""
    Selects tuplets in ``argument``.

    ..  container:: example

        Selects tuplets at every level:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
        ... )

        >>> result = abjad.select.tuplets(staff)
        >>> for item in result:
        ...     item
        ...
        Tuplet('3:2', "c'2 { 3:2 d'8 e'8 f'8 }")
        Tuplet('3:2', "d'8 e'8 f'8")
        Tuplet('3:2', "c'4 d'4 e'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'2
                    \tuplet 3/2
                    {
                        \abjad-color-music #'blue
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        \abjad-color-music #'red
                        f'8
                    }
                }
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'red
                    d'4
                    \abjad-color-music #'red
                    e'4
                }
            }

    ..  container:: example

        Selects tuplets at level -1:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
        ... )

        >>> result = abjad.select.tuplets(staff, level=-1)
        >>> for item in result:
        ...     item
        ...
        Tuplet('3:2', "d'8 e'8 f'8")
        Tuplet('3:2', "c'4 d'4 e'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 3/2
                {
                    c'2
                    \tuplet 3/2
                    {
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'red
                        f'8
                    }
                }
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'blue
                    e'4
                }
            }

        Tuplets at level -1 are bottom-level tuplet: tuplets at level -1 contain only
        one tuplet (themselves) and do not contain any other tuplets.

    ..  container:: example

        Selects tuplets at level 1:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
        ... )

        >>> result = abjad.select.tuplets(staff, level=1)
        >>> for item in result:
        ...     item
        ...
        Tuplet('3:2', "c'2 { 3:2 d'8 e'8 f'8 }")
        Tuplet('3:2', "c'4 d'4 e'4")

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 3/2
                {
                    \abjad-color-music #'red
                    c'2
                    \tuplet 3/2
                    {
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'red
                        f'8
                    }
                }
                \tuplet 3/2
                {
                    \abjad-color-music #'blue
                    c'4
                    \abjad-color-music #'blue
                    d'4
                    \abjad-color-music #'blue
                    e'4
                }
            }

        Tuplets at level 1 are top-level tuplets: level-1 tuplets contain only 1
        tuplet (themselves) and are not contained by any other tuplets.

    """
    tuplets: list[_score.Tuplet] = []
    for item in components(argument, _score.Tuplet, exclude=exclude):
        assert isinstance(item, _score.Tuplet)
        tuplets.append(item)
    if level is None:
        return tuplets
    elif level < 0:
        result = []
        for tuplet in tuplets:
            count = 0
            for component in _iterlib._iterate_descendants(tuplet):
                if isinstance(component, _score.Tuplet):
                    count += 1
            if -count == level:
                result.append(tuplet)
    else:
        result = []
        for tuplet in tuplets:
            if _parentage.Parentage(tuplet).count(_score.Tuplet) == level:
                result.append(tuplet)
    return result


def with_next_leaf(argument, *, grace: bool | None = None) -> list[_score.Leaf]:
    r"""
    Extends ``argument`` with next leaf.

    ..  container:: example

        Selects runs (each with next leaf):

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.runs(staff)
        >>> result = [abjad.select.with_next_leaf(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8')]
        [Note("d'8"), Note("e'8"), Rest('r8')]
        [Note("f'8"), Note("g'8"), Note("a'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'red
                g'8
                \abjad-color-music #'red
                a'8
            }

    ..  container:: example

        Selects pitched tails (each with next leaf):

        >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = [abjad.select.with_next_leaf(_[-1:]) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8')]
        [Note("d'8"), Note("e'8")]
        [Note("e'8"), Rest('r8')]
        [Note("f'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'red
                r8
                d'8
                ~
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'blue
                e'8
                ~
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'blue
                f'8
            }

    ..  container:: example

        Pitched logical ties (each with next leaf) is the correct selection
        for single-pitch sustain pedal applications.

        Selects pitched logical ties (each with next leaf):

        >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.setting(staff).pedalSustainStyle = "#'mixed"

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = [abjad.select.with_next_leaf(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8')]
        [Note("d'8"), Note("d'8"), Note("e'8")]
        [Note("e'8"), Note("e'8"), Rest('r8')]
        [Note("f'8")]

        >>> for item in result:
        ...     abjad.piano_pedal(item, context="Staff")
        ...

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 6
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = 6
                autoBeaming = ##f
                pedalSustainStyle = #'mixed
            }
            {
                \abjad-color-music #'red
                c'8
                \sustainOn
                \abjad-color-music #'red
                r8
                \sustainOff
                \abjad-color-music #'blue
                d'8
                \sustainOn
                ~
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'blue
                \abjad-color-music #'red
                e'8
                \sustainOff
                \sustainOn
                ~
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'red
                r8
                \sustainOff
                \abjad-color-music #'blue
                f'8
                \sustainOff
                \sustainOn
            }

    ..  container:: example

        REGRESSION. Works with grace note (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
        >>> staff = abjad.Staff([music_voice])

        >>> prototype = (
        ...     abjad.BeforeGraceContainer,
        ...     abjad.OnBeatGraceContainer,
        ...     abjad.AfterGraceContainer,
        ... )
        >>> result = abjad.select.components(staff, prototype)
        >>> result = [abjad.select.leaves(_) for _ in result]
        >>> result = [abjad.select.with_next_leaf(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("cs'16"), Note("d'4")]
        [Chord("<e' g'>16"), Note("gs'16"), Note("a'16"), Note("as'16"), Note("e'4")]
        [Note("fs'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    \grace {
                        \abjad-color-music #'red
                        cs'16
                    }
                    \abjad-color-music #'red
                    d'4
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \abjad-color-music #'blue
                            \set fontSize = #-3
                            \slash
                            \voiceOne
                            <
                                \tweak font-size 0
                                \tweak transparent ##t
                                e'
                                g'
                            >16
                            - \accent
                            [
                            (
                            \abjad-color-music #'blue
                            gs'16
                            \abjad-color-music #'blue
                            a'16
                            \abjad-color-music #'blue
                            as'16
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \abjad-color-music #'blue
                            \voiceTwo
                            e'4
                        }
                    >>
                    \oneVoice
                    \afterGrace
                    f'4
                    {
                        \abjad-color-music #'red
                        fs'16
                    }
                }
            }

        Works with independent after-grace containers (grace-to-main):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = [abjad.select.with_next_leaf(_) for _ in [leaves[2:3]]]
        >>> for item in result:
        ...     item
        ...
        [Note("e'4"), Note("gf'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    f'4
                }
            }

        Works with independent after-grace containers (grace-to-main):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = [abjad.select.with_next_leaf(_) for _ in [leaves[3:4]]]
        >>> for item in result:
        ...     item
        ...
        [Note("gf'16"), Note("f'4")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    \abjad-color-music #'red
                    f'4
                }
            }

    """
    items = leaves(argument)
    previous_leaf = items[-1]
    while True:
        next_leaf = _iterlib._get_leaf(previous_leaf, n=1)
        if next_leaf is None:
            break
        if (
            grace is None
            or (grace is True and _getlib._get_grace_container(next_leaf))
            or (grace is False and not _getlib._get_grace_container(next_leaf))
        ):
            items.append(next_leaf)
            break
        previous_leaf = next_leaf
    return items


def with_previous_leaf(argument) -> list[_score.Leaf]:
    r"""
    Extends ``argument`` with previous leaf.

    ..  container:: example

        Selects runs (each with previous leaf):

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.runs(staff)
        >>> result = [abjad.select.with_previous_leaf(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Rest('r8'), Note("d'8"), Note("e'8")]
        [Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'blue
                e'8
                \abjad-color-music #'red
                r8
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'red
                g'8
                \abjad-color-music #'red
                a'8
            }

    ..  container:: example

        Selects pitched heads (each with previous leaf):

        >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.logical_ties(staff, pitched=True)
        >>> result = [abjad.select.with_previous_leaf(_[:1]) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Rest('r8'), Note("d'8")]
        [Note("d'8"), Note("e'8")]
        [Rest('r8'), Note("f'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \abjad-color-music #'red
                c'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                d'8
                ~
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                e'8
                ~
                e'8
                \abjad-color-music #'blue
                r8
                \abjad-color-music #'blue
                f'8
            }

    ..  container:: example

        REGRESSION. Works with grace note (and containers):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, music_voice[1])
        >>> obgc = abjad.on_beat_grace_container("g'16 gs' a' as'", music_voice[2:3])
        >>> abjad.attach(abjad.Articulation(">"), obgc[0])
        >>> container = abjad.AfterGraceContainer("fs'16")
        >>> abjad.attach(container, music_voice[3])
        >>> staff = abjad.Staff([music_voice])

        >>> prototype = (
        ...     abjad.BeforeGraceContainer,
        ...     abjad.OnBeatGraceContainer,
        ...     abjad.AfterGraceContainer,
        ... )
        >>> result = abjad.select.components(staff, prototype)
        >>> result = [abjad.select.leaves(_) for _ in result]
        >>> result = [abjad.select.with_previous_leaf(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'4"), Note("cs'16")]
        [Note("d'4"), Chord("<e' g'>16"), Note("gs'16"), Note("a'16"), Note("as'16")]
        [Note("f'4"), Note("fs'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    \abjad-color-music #'red
                    c'4
                    \grace {
                        \abjad-color-music #'red
                        cs'16
                    }
                    \abjad-color-music #'blue
                    d'4
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \abjad-color-music #'blue
                            \set fontSize = #-3
                            \slash
                            \voiceOne
                            <
                                \tweak font-size 0
                                \tweak transparent ##t
                                e'
                                g'
                            >16
                            - \accent
                            [
                            (
                            \abjad-color-music #'blue
                            gs'16
                            \abjad-color-music #'blue
                            a'16
                            \abjad-color-music #'blue
                            as'16
                            )
                            ]
                        }
                        \context Voice = "MusicVoice"
                        {
                            \voiceTwo
                            e'4
                        }
                    >>
                    \abjad-color-music #'red
                    \oneVoice
                    \afterGrace
                    f'4
                    {
                        \abjad-color-music #'red
                        fs'16
                    }
                }
            }

        Works with independent after-grace containers (grace-to-main):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = [abjad.select.with_previous_leaf(_) for _ in [leaves[3:4]]]
        >>> for item in result:
        ...     item
        ...
        [Note("e'4"), Note("gf'16")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \abjad-color-music #'red
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    f'4
                }
            }

        Works with independent after-grace containers (main-to-grace):

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("gf'16")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> abjad.setting(staff).autoBeaming = False

        >>> leaves = abjad.select.leaves(staff)
        >>> result = [abjad.select.with_previous_leaf(_) for _ in [leaves[-1:]]]
        >>> for item in result:
        ...     item
        ...
        [Note("gf'16"), Note("f'4")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        \abjad-color-music #'red
                        gf'16
                    }
                    \abjad-color-music #'red
                    f'4
                }
            }

    """
    items = leaves(argument)
    previous_leaf = _iterlib._get_leaf(items[0], n=-1)
    if previous_leaf is not None:
        items.insert(0, previous_leaf)
    return items
