# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class Selector(AbjadValueObject):
    r'''A selector.

    Selectors select components.

    Selectors aggregate a sequence of callable classes which describe the
    process of component selection.

    Selectors provide methods for configuring and making new selectors.

    Composers may chain selectors together.

    ..  todo:: Add notation to every example.

    ..  container:: example

        Score for examples:

        ::

            >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
            >>> staff = Staff(string)
            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 1.** Selects a component:

        ::

            >>> selector = selectortools.Selector()
            >>> selector(staff)
            Selection([<Staff{6}>])

    ..  container:: example

        **Example 2.** Selects all of the leaves in a component:

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector(staff)
            Selection([Selection([Note("c'4"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r16'), Note("f'16"), Note("g'8"), Note("a'4")])])

    ..  container:: example

        **Example 3.** Selects runs of notes:

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_run(Note)
            >>> for selection in selector(staff):
            ...     selection
            ...
            Selection([Note("c'4"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'16"), Note("g'8"), Note("a'4")])

    ..  container:: example

        **Example 4.** Selects the first item in each selection:

        ::

            >>> selector = selectortools.Selector()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_run(Note)
            >>> selector = selector.get_item(0, apply_to_each=True)
            >>> selector(staff)
            Selection([Note("c'4"), Note("e'8"), Note("f'16")])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selectors'

    __slots__ = (
        '_callbacks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        callbacks=None,
        ):
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Calls selector on `expr`.

        Returns a selection.
        '''
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        prototype = (
            scoretools.Component,
            selectiontools.Selection,
            )
        if not isinstance(expr, prototype):
            expr = select(expr)
        expr = (expr,)
        assert all(isinstance(x, prototype) for x in expr), repr(expr)
        callbacks = self.callbacks or ()
        for callback in callbacks:
            expr = callback(expr, rotation=rotation)
        if isinstance(expr, tuple):
            expr = selectiontools.Selection(expr)
        return expr

    def __getitem__(self, item):
        r'''Gets `item` in selector.

        Returns another selector.
        '''
        from abjad.tools import selectortools
        if isinstance(item, slice):
            callback = selectortools.SliceSelectorCallback(
                start=item.start,
                stop=item.stop,
                apply_to_each=True,
                )
        elif isinstance(item, int):
            callback = selectortools.ItemSelectorCallback(
                item=item,
                apply_to_each=True,
                )
        else:
            raise ValueError(item)
        return self._append_callback(callback)

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    ### PUBLIC METHODS ###

    def append_callback(self, callback):
        r'''Appends `callback` to selector.

        Composers can create their own selector callback classes with
        specialized composition-specific logic. `Selector.append_callback()`
        allows composers to use those composition-specific selector callbacks
        in the component selector pipeline.

        ..  container:: example

            **Example.** A custom selector callback class can be created to
            only select chords containing the pitch-classes C, E and G. A
            selector can then be configured with that custom callback via
            `append_callback()`:

            ::

                >>> class CMajorSelectorCallback(abctools.AbjadValueObject):
                ...     def __call__(self, expr, rotation=None):
                ...         c_major_pcs = pitchtools.PitchClassSet("c e g")
                ...         result = []
                ...         for subexpr in expr:
                ...             subresult = []
                ...             for x in subexpr:
                ...                 if not isinstance(x, scoretools.Chord):
                ...                     continue
                ...                 pitches = x.written_pitches
                ...                 pcs = pitchtools.PitchClassSet(pitches)
                ...                 if pcs == c_major_pcs:
                ...                     subresult.append(x)
                ...             if subresult:
                ...                 result.append(tuple(subresult))
                ...         return tuple(result)

            ::

                >>> staff = Staff("<g' d'>4 <c' e' g'>4 r4 <e' g' c''>2 fs,4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.append_callback(CMajorSelectorCallback())

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection([Chord("<c' e' g'>4"), Chord("<e' g' c''>2")])

        Returns new selector.
        '''
        return self._append_callback(callback)

    # TODO: maybe add a depth=None keyword
    def by_class(
        self,
        prototype=None,
        flatten=None,
        ):
        r'''Configures selector by class.

        ..  container:: example

            **Example 1.** Selects notes and does not flatten:

            ::

                >>> staff = Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'8 ~
                    d'16
                    e'16 ~
                    e'8
                    r4
                    g'8
                }

            ::

                >>> selector = select().by_class(prototype=Note)
                >>> for selection in selector(staff):
                ...     selection
                Selection([Note("c'4"), Note("d'8"), Note("d'16"), Note("e'16"), Note("e'8"), Note("g'8")])

            Call returns a selection containing a selection of notes.

        ..  container:: example

            **Example 2.** Selects notes and flattens:

            ::

                >>> staff = Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'8 ~
                    d'16
                    e'16 ~
                    e'8
                    r4
                    g'8
                }

            ::

                >>> selector = select().by_class(prototype=Note, flatten=True)
                >>> for note in selector(staff):
                ...     note
                Note("c'4")
                Note("d'8")
                Note("d'16")
                Note("e'16")
                Note("e'8")
                Note("g'8")

            Call returns a selection of notes.

        ..  container:: example

            **Example 3.** Selects rests:

            ::

                >>> staff = Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'8 ~
                    d'16
                    e'16 ~
                    e'8
                    r4
                    g'8
                }

            ::

                >>> selector = select().by_class(prototype=Rest, flatten=True)
                >>> for rest in selector(staff):
                ...     rest
                Rest('r4')

            Call returns a selection of rests.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(
            prototype=prototype,
            flatten=flatten,
            )
        return self._append_callback(callback)

    def by_contiguity(self):
        r'''Configures selector by contiguity.

        ..  container:: example

            **Example 1.** Selects contiguous groups of sixteenth notes:

            ::

                >>> staff = Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'16
                    d'16
                    d'16
                    d'16
                    e'4
                    f'16
                    f'16
                    f'16
                    f'16
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.flatten()
                >>> selector = selector.by_duration('==', (1, 16))
                >>> selector = selector.by_contiguity()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])
                Selection([Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")])

        ..  container:: example

            **Example 2.** Selects contiguous groups of logical ties each less
            than a quarter note in duration:

            ::

                >>> staff = Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 f'4 g'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'8 ~
                    d'16
                    e'16 ~
                    e'8
                    f'4
                    g'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie()
                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Note("d'8"), Note("d'16")])
                LogicalTie([Note("e'16"), Note("e'8")])
                LogicalTie([Note("f'4")])
                LogicalTie([Note("g'8")])

            ::

                >>> selector = selector.by_duration('<', (1, 4))
                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("d'8"), Note("d'16")])
                LogicalTie([Note("e'16"), Note("e'8")])
                LogicalTie([Note("g'8")])

            ::

                >>> selector = selector.by_contiguity()
                >>> for x in selector(staff):
                ...     x
                ...
                Selection([LogicalTie([Note("d'8"), Note("d'16")]), LogicalTie([Note("e'16"), Note("e'8")])])
                Selection([LogicalTie([Note("g'8")])])

            ::

                >>> selector = selector.by_leaf()
                >>> for x in selector(staff):
                ...     x
                ...
                Selection([Note("d'8"), Note("d'16"), Note("e'16"), Note("e'8")])
                Selection([Note("g'8")])

            ::

                >>> selector = selector[0].flatten()
                >>> for x in selector(staff):
                ...     attach(indicatortools.Articulation('snappizzicato'), x)
                ...
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'8 -\snappizzicato ~
                    d'16
                    e'16 ~
                    e'8
                    f'4
                    g'8 -\snappizzicato
                }

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ContiguitySelectorCallback()
        return self._append_callback(callback)

    def by_counts(
        self,
        counts,
        cyclic=False,
        fuse_overhang=False,
        nonempty=False,
        overhang=False,
        rotate=False,
        ):
        r'''Configures selector by counts.

        Partitions components.

        ..  container:: example

            **Example 1.** Selects first three components:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])

            Call returns a selection containing a component selection.

        ..  container:: example

            **Example 2.** Selects every complete group of three components:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])

            Call returns a selection containing two component selections.

        ..  container:: example

            **Example 3.** Selects every group of three components plus any
            overhang:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8"), Note("a'8")])

            Call returns a selection containing three component selections.

        ..  container:: example

            **Example 4.** Selects the first three components and then the
            remaining components:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     fuse_overhang=True,
                ...     overhang=True,
                ...     )

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            Call returns a selection of two component selections.

        ..  container:: example

            **Example 5.** Selects components grouped by counts 1, 2, 3:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                    b'8
                    r8
                    c''8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_counts(
                ...     [1, 2, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8")])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8")])
                Selection([Note("a'8"), Note("b'8")])
                Selection([Rest('r8'), Note("c''8")])

            Call returns a selection containing multiple component selections.

        ..  container:: example

            **Example 6.** Selects components grouped 1, 2, 3 rotated one to
            the left:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                    b'8
                    r8
                    c''8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_counts(
                ...     [1, 2, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     rotate=True,
                ...     )

            ::

                >>> for selection in selector(staff, rotation=1):
                ...     selection
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8")])
                Selection([Note("g'8"), Note("a'8")])
                Selection([Note("b'8"), Rest('r8'), Note("c''8")])

            Call returns a selection containing multiple component selections.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.CountsSelectorCallback(
            counts,
            cyclic=cyclic,
            fuse_overhang=fuse_overhang,
            nonempty=nonempty,
            overhang=overhang,
            rotate=rotate,
            )
        return self._append_callback(callback)

    def by_duration(self, inequality=None, duration=None, preprolated=None):
        r'''Configures selector by duration.

        ..  container:: example

            **Example 1.** Selects all runs of notes with duration equal to
            ``2/8``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_duration(Duration(2, 8))

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("d'8"), Note("e'8")])

            Call returns a selection containing one component selection.

        ..  container:: example

            **Example 2.** Selects all runs of notes with duration shorter than
            ``3/8``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_duration('<', Duration(3, 8))

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

            Call returns a selection containing component selections.

        ..  container:: example

            **Example 3.** Selects all runs of notes with duration longer than
            or equal to ``1/4``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_duration('>=', Duration(1, 4))

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            Call returns a selection containing component selections.

        ..  container:: example

            **Example 4.** Selects all logical ties whose leaves sum to
            ``1/8``, before prolation:

            ::

                >>> staff = Staff(r"""
                ... \times 3/4 { c'16 d'16 ~ d'16 e'16 ~ }
                ... { e'16 f'16 ~ f'16 g'16 ~ }
                ... \times 5/4 { g'16 a'16 ~ a'16 b'16 }
                ... """)
                >>> show(staff) # doctest: +SKIP

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie()
                >>> selector = selector.by_duration(
                ...     '==', Duration(1, 8),
                ...     preprolated=True,
                ...     )

            ::

                >>> selections = selector(staff)
                >>> for logical_tie in selections:
                ...     attach(Articulation('accent'), logical_tie[0])
                ...     print(logical_tie)
                ...
                LogicalTie([Note("d'16"), Note("d'16")])
                LogicalTie([Note("e'16"), Note("e'16")])
                LogicalTie([Note("f'16"), Note("f'16")])
                LogicalTie([Note("g'16"), Note("g'16")])
                LogicalTie([Note("a'16"), Note("a'16")])

            ::

                >>> show(staff) # doctest: +SKIP

            Call returns a selection containing logical tie selections.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        duration_expr = None
        if isinstance(inequality, (
            durationtools.Duration,
            selectortools.DurationInequality,
            )):
            duration_expr = inequality
        elif isinstance(inequality, str) and duration is not None:
            duration_expr = selectortools.DurationInequality(
                duration=duration,
                operator_string=inequality,
                )
        elif inequality is None and duration is not None:
            duration_expr = selectortools.DurationInequality(
                duration=duration,
                operator_string='==',
                )
        if not isinstance(duration_expr, (
            durationtools.Duration,
            selectortools.DurationInequality,
            )):
            raise ValueError(inequality, duration)
        callback = selectortools.DurationSelectorCallback(
            duration=duration_expr,
            preprolated=preprolated,
            )
        return self._append_callback(callback)

    def by_leaf(self, flatten=None):
        r'''Configures selector by leaves.

        ..  container:: example

            **Example 1.** Selects leaves without flattening:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()

            ::

                >>> selections = selector(staff)
                >>> for selection in selections:
                ...     selection
                ...
                Selection([Note("c'8"), Rest('r8'), Note("d'8"), Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            Returns a selection of leaf selections.

        ..  container:: example

            **Example 2.** Selects leaves with flattening:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf(flatten=True)

            ::

                >>> selection = selector(staff)
                >>> for leaf in selection:
                ...     leaf
                ...
                Note("c'8")
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Rest('r8')
                Note("f'8")
                Note("g'8")
                Note("a'8")

            Returns a leaf selection.

        ..  container:: example

            **Example 3.** Selects leaves:

            ::

                >>> staff = Staff("abj: | 4/4 c'2 d'2 || 3/4 e'4 f'4 g'4 |")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 4/4
                        c'2
                        d'2
                    }
                    {
                        \time 3/4
                        e'4
                        f'4
                        g'4
                    }
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_class(Measure)
                >>> selections = selector(staff)
                >>> for selection in selections:
                ...     selection
                ...
                Selection([Measure((4, 4), "c'2 d'2"), Measure((3, 4), "e'4 f'4 g'4")])

            Returns a selection of measure selections.

            ::

                >>> selector = selector.by_leaf()
                >>> selections = selector(staff)
                >>> for selection in selections:
                ...     selection
                ...
                Selection([Note("c'2"), Note("d'2"), Note("e'4"), Note("f'4"), Note("g'4")])

            Returns a selection of leaf selections.

        ..  container:: example

            **Example 4.** Selects leaves grouped by measure:

            ::

                >>> staff = Staff("abj: | 4/4 c'2 d'2 || 3/4 e'4 f'4 g'4 |")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 4/4
                        c'2
                        d'2
                    }
                    {
                        \time 3/4
                        e'4
                        f'4
                        g'4
                    }
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_class(Measure, flatten=True)
                >>> selection = selector(staff)
                >>> for measure in selection:
                ...     measure
                ...
                Measure((4, 4), "c'2 d'2")
                Measure((3, 4), "e'4 f'4 g'4")

            Returns a measure selection.

            ::

                >>> selector = selector.by_leaf()
                >>> selections = selector(staff)
                >>> for selection in selections:
                ...     selection
                ...
                Selection([Note("c'2"), Note("d'2")])
                Selection([Note("e'4"), Note("f'4"), Note("g'4")])

            Returns a selection of leaf selections.

        ..  container:: example

            **Example 5.** Selects leaves:

            ::

                >>> staff = Staff("abj: | 4/4 c'2 d'2 || 3/4 e'4 f'4 g'4 |")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 4/4
                        c'2
                        d'2
                    }
                    {
                        \time 3/4
                        e'4
                        f'4
                        g'4
                    }
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_class(Measure, flatten=True)
                >>> selection = selector(staff)
                >>> for measure in selection:
                ...     measure
                ...
                Measure((4, 4), "c'2 d'2")
                Measure((3, 4), "e'4 f'4 g'4")

            Returns a measure selection.

            ::

                >>> selector = selector.by_leaf(flatten=True)
                >>> selection = selector(staff)
                >>> for leaf in selection:
                ...     leaf
                ...
                Note("c'2")
                Note("d'2")
                Note("e'4")
                Note("f'4")
                Note("g'4")

            Returns a leaf selection.

        ..  container:: example

            **Example 7.** Selects leaves with flattening:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> f(staff)
                \new Staff {
                    c'8
                    r8
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf(flatten=True)
                >>> selection = selector(staff)

            ::

                >>> selection
                Selection([Note("c'8"), Rest('r8'), Note("d'8"), Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            Returns leaf selection.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(
            prototype=scoretools.Leaf,
            flatten=flatten,
            )
        return self._append_callback(callback)

    def by_length(self, inequality=None, length=None):
        r'''Configures selector by length.

        ..  container:: example

            **Example 1.** Selects all runs of more than one note:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_length('>', 1)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection([Note("d'8"), Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example

            **Example 2.** Selects all runs of less than three notes:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_length('<', 3)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection([Note("c'8")])
                Selection([Note("d'8"), Note("e'8")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        length_expr = None
        if isinstance(inequality, (
            int,
            float,
            selectortools.LengthInequality,
            )):
            length_expr = inequality
        elif isinstance(inequality, str) and length is not None:
            length_expr = selectortools.LengthInequality(
                length=int(length),
                operator_string=inequality,
                )
        elif inequality is None and length is not None:
            length_expr = selectortools.LengthInequality(
                length=int(length),
                operator_string='==',
                )
        if not isinstance(length_expr, (
            int,
            float,
            selectortools.LengthInequality,
            )):
            raise ValueError(inequality, length)
        callback = selectortools.LengthSelectorCallback(
            length=length_expr,
            )
        return self._append_callback(callback)

    def by_logical_measure(self):
        r'''Configures selector by logical measure.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.LogicalMeasureSelectorCallback()
        return self._append_callback(callback)

    def by_logical_tie(
        self,
        flatten=True,
        pitched=False,
        trivial=True,
        ):
        r'''Configures selector by logical tie.

        ..  container:: example

            **Example 1.** Selects all logical ties:

            ::

                >>> staff = Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> container = staff[2]
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Rest('r8')])
                LogicalTie([Note("f'8"), Note("f'8")])
                LogicalTie([Rest('r8')])

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Rest('r8')])
                LogicalTie([Note("f'8"), Note("f'8")])

        ..  container:: example

            **Example 2.** Selects pitched logical ties:

            ::

                >>> staff = Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> container = staff[2]
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(
                ...     pitched=True,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

        ..  container:: example

            **Example 3.** Selects pitched nontrivial logical ties:

            ::

                >>> staff = Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> container = staff[2]
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(
                ...     pitched=True,
                ...     trivial=False,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie([Note("d'8"), Note("d'8")])
                LogicalTie([Note("f'8"), Note("f'8")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.LogicalTieSelectorCallback(
            flatten=flatten,
            pitched=pitched,
            trivial=trivial,
            )
        return self._append_callback(callback)

    def by_pattern(
        self,
        pattern=None,
        apply_to_each=None,
        ):
        r'''Configures selector by `pattern`.

        ..  todo:: Merge into Selector.get_item().

        ..  container:: example

            **Example 1.** Selects logical tie at index 1:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> pattern = patterntools.select([1])
                >>> selector = selector.by_pattern(pattern=pattern)

            ::

                >>> selection = selector(staff)
                >>> for logical_tie in selection:
                ...     logical_tie
                ...
                LogicalTie([Note("d'4"), Note("d'4")])

            Returns selection of logical tie.

        ..  container:: example

            **Example 2.** Selects every second logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> pattern = patterntools.select_every([0], period=2)
                >>> selector = selector.by_pattern(pattern=pattern)

            ::

                >>> selection = selector(staff)
                >>> for logical_tie in selection:
                ...     logical_tie
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])

            Returns selection of logical ties.

        ..  container:: example

            **Example 3.** Selects every second leaf:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> label(staff).with_indices(prototype=scoretools.Leaf)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #2
                } {
                    c'4
                        ^ \markup {
                            \small
                                0
                            }
                    d'4 ~
                        ^ \markup {
                            \small
                                1
                            }
                    d'4
                        ^ \markup {
                            \small
                                2
                            }
                    e'4 ~
                        ^ \markup {
                            \small
                                3
                            }
                    e'4 ~
                        ^ \markup {
                            \small
                                4
                            }
                    e'4
                        ^ \markup {
                            \small
                                5
                            }
                    r4
                        ^ \markup {
                            \small
                                6
                            }
                    f'4
                        ^ \markup {
                            \small
                                7
                            }
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf(flatten=True)
                >>> pattern = patterntools.select_every([0], period=2)
                >>> selector = selector.by_pattern(pattern=pattern)

            ::

                >>> selection = selector(staff)
                >>> for note in selection:
                ...     print(staff.index(note), repr(note))
                ...
                0 Note("c'4")
                2 Note("d'4")
                4 Note("e'4")
                6 Rest('r4')

            Returns selection of leaves.

        ..  container:: example

            **Example 4.** Selects every other leaf rotated one to the right:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> label(staff).with_indices(prototype=scoretools.Leaf)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #2
                } {
                    c'4
                        ^ \markup {
                            \small
                                0
                            }
                    d'4 ~
                        ^ \markup {
                            \small
                                1
                            }
                    d'4
                        ^ \markup {
                            \small
                                2
                            }
                    e'4 ~
                        ^ \markup {
                            \small
                                3
                            }
                    e'4 ~
                        ^ \markup {
                            \small
                                4
                            }
                    e'4
                        ^ \markup {
                            \small
                                5
                            }
                    r4
                        ^ \markup {
                            \small
                                6
                            }
                    f'4
                        ^ \markup {
                            \small
                                7
                            }
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf(flatten=True)
                >>> pattern = patterntools.select_every([0], period=2)
                >>> selector = selector.by_pattern(pattern=pattern)

            ::

                >>> selection = selector(staff, rotation=1)
                >>> for note in selection:
                ...     print(staff.index(note), repr(note))
                ...
                1 Note("d'4")
                3 Note("e'4")
                5 Note("e'4")
                7 Note("f'4")

            Returns selection of leaves.

        ..  container:: example

            **Example 5.** Selects note at index 1 in each logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> label(staff).with_indices(prototype=scoretools.Leaf)
                >>> override(staff).text_script.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #2
                } {
                    c'4
                        ^ \markup {
                            \small
                                0
                            }
                    d'4 ~
                        ^ \markup {
                            \small
                                1
                            }
                    d'4
                        ^ \markup {
                            \small
                                2
                            }
                    e'4 ~
                        ^ \markup {
                            \small
                                3
                            }
                    e'4 ~
                        ^ \markup {
                            \small
                                4
                            }
                    e'4
                        ^ \markup {
                            \small
                                5
                            }
                    r4
                        ^ \markup {
                            \small
                                6
                            }
                    f'4
                        ^ \markup {
                            \small
                                7
                            }
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> pattern = patterntools.select([1])
                >>> selector = selector.by_pattern(
                ...     apply_to_each=True,
                ...     pattern=pattern,
                ...     )

            ::

                >>> selection = selector(staff)
                >>> for selection_ in selection:
                ...     note = selection_[0]
                ...     print(staff.index(note), repr(note))
                2 Note("d'4")
                4 Note("e'4")

            Returns a selection of note selections.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PatternedSelectorCallback(
            apply_to_each=apply_to_each,
            pattern=pattern,
            )
        return self._append_callback(callback)

    # TODO: implement pitch-inequality class.
    def by_pitch(
        self,
        pitches=None,
        ):
        r'''Configures selector by pitch.

        ..  container:: example

            **Example 1.** Selects components matching a single pitch:

            ::

                >>> staff = Staff("c'4 d'4 ~ d'4 e'4")
                >>> staff.extend("r4 <c' e' g'>4 ~ <c' e' g'>2")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf(flatten=True)
                >>> selector = selector.by_pitch(pitches="c'")

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Note("c'4")
                Chord("<c' e' g'>4")
                Chord("<c' e' g'>2")

        ..  container:: example

            **Example 2.** Selects components matching multiple pitches:

            ::

                >>> staff = Staff("c'4 d'4 ~ d'4 e'4")
                >>> staff.extend("r4 <c' e' g'>4 ~ <c' e' g'>2")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf(flatten=True)
                >>> selector = selector.by_pitch(pitches="c' e'")

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Note("c'4")
                Note("e'4")
                Chord("<c' e' g'>4")
                Chord("<c' e' g'>2")

        ..  container:: example

            **Example 3.** Selects logical ties containing components matching
            multiple pitches:

            ::

                >>> staff = Staff("c'4 d'4 ~ d'4 e'4")
                >>> staff.extend("r4 <c' e' g'>4 ~ <c' e' g'>2")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie()
                >>> selector = selector.by_pitch(pitches=NamedPitch('C4'))

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Chord("<c' e' g'>4"), Chord("<c' e' g'>2")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PitchSelectorCallback(pitches=pitches)
        return self._append_callback(callback)

    def by_run(
        self,
        prototype=None,
        ):
        r'''Configures selector by run.

        ..  container:: example

            **Example 1.** Selects run of notes and chords at any depth:

            ::

                >>> staff = Staff(r"c'8 d' r \times 2/3 { e' r f' } g' a' r")
                >>> selector = selectortools.Selector()
                >>> prototype = (Note, Chord)
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(prototype)

            ::

                >>> selections = selector(staff)
                >>> for selection in selections:
                ...     selection
                ...
                Selection([Note("c'8"), Note("d'8")])
                Selection([Note("e'8")])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.RunSelectorCallback(prototype)
        return self._append_callback(callback)

    def first(self):
        r'''Gets first item in selection.

        ..  container:: example

            **Example 1.** Selects first pitched logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> for logical_tie in selector(staff):
                ...     logical_tie
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])
                LogicalTie([Note("f'4")])

            ::

                >>> selector = selector.first()
                >>> selector(staff)
                LogicalTie([Note("c'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=0,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def flatten(self, depth=-1):
        r'''Flattens selection.

        ..  container:: example

            **Example 1.** Selects all pitched logical ties except the first
            and last:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            Returns logical tie selection:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.middle()
                >>> for logical_tie in selector(staff):
                ...     logical_tie
                ...
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])

            Returns leaf selection:

                >>> selector = selector.flatten()
                >>> selector(staff)
                Selection([Note("d'4"), Note("d'4"), Note("e'4"), Note("e'4"), Note("e'4")])

        ..  container:: example

            **Example 2.** Selects leaves:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            Returns selection of leaf selections:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector(staff)
                Selection([Selection([Note("c'4"), Note("d'4"), Note("d'4"), Note("e'4"), Note("e'4"), Note("e'4"), Rest('r4'), Note("f'4")])])

            Returns leaf selection:

            ::

                >>> selector = selector.flatten()
                >>> selector(staff)
                Selection([Note("c'4"), Note("d'4"), Note("d'4"), Note("e'4"), Note("e'4"), Note("e'4"), Rest('r4'), Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.FlattenSelectorCallback(depth=depth)
        return self._append_callback(callback)

    def get_item(self, item, apply_to_each=False):
        r'''Gets `item` in selection.

        Maps the callback to each item in sequence when `apply_to_each` is
        true.

        Applies the callback to the entire sequence when `apply_to_each` is
        false.

        ..  container:: example

            **Example 1.** Selects leaf at index 1:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            Returns selection of leaf selections:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.flatten()
                >>> selector = selector.get_item(1)
                >>> selector(staff)
                Note("d'4")

        ..  container:: example

            **Example 2.** Selects logical tie at index 1:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            Returns selection of leaf selections:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_item(1)
                >>> selector(staff)
                LogicalTie([Note("d'4"), Note("d'4")])

        ..  container:: example

            **Example 3.** Selects the first note of each logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            Returns leaf selection:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_item(0, apply_to_each=True)
                >>> selector(staff)
                Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=item,
            apply_to_each=apply_to_each,
            )
        return self._append_callback(callback)

    def get_slice(self, start=None, stop=None, apply_to_each=True):
        r'''Gets slice from `start` to `stop` in selection.

        Maps the callback to each item in sequence when `apply_to_each` is
        true.

        Applies the callback to the entire sequence when `apply_to_each` is
        false.

        ..  container:: example

            **Example 1.** Gets all notes (except the first) in each
            pitched logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_slice(
                ...     start=1,
                ...     stop=None,
                ...     apply_to_each=True,
                ...     )

            ::

                >>> logical_ties = selector(staff)
                >>> for logical_tie in logical_ties:
                ...     logical_tie
                ...
                LogicalTie([Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4")])

            Returns selection of logical ties.

        ..  container:: example

            **Example 2.** Gets all pitched logical ties (except the last):

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_slice(
                ...     start=None,
                ...     stop=-1,
                ...     apply_to_each=False,
                ...     )

            ::

                >>> logical_ties = selector(staff)
                >>> for logical_tie in logical_ties:
                ...     logical_tie
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])

            Returns selection of logical ties.

        ..  container:: example

            **Example 3.** Selects last three leaves:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4 ~
                    d'4
                    e'4 ~
                    e'4 ~
                    e'4
                    r4
                    f'4
                }

            Returns leaf selection:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.flatten()
                >>> selector = selector.get_slice(
                ...     start=-3,
                ...     apply_to_each=False,
                ...     )
                >>> selector(staff)
                Selection([Note("e'4"), Rest('r4'), Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            start=start,
            stop=stop,
            apply_to_each=apply_to_each,
            )
        return self._append_callback(callback)

    def last(self):
        r'''Gets last item in selection.

        ..  container:: example

            **Example 1.** Selects the last pitched logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.last()
                >>> selector(staff)
                LogicalTie([Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=-1,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def middle(self):
        r'''Gets all but the first and last items in selection.

        ..  container:: example

            **Example 1.** Selects all pitched logical ties (except the first
            and last):

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.middle()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            start=1,
            stop=-1,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def most(self):
        r'''Gets all but the last item in selection.

        ..  container:: example

            **Example 1.** Selects all pitched logical ties (except the last):

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.most()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            stop=-1,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def partition_by_ratio(self, ratio):
        r'''Configures selector to partition by ratio.

        ..  container:: example

            **Example 1.** Partitions leaves by ratio of `1:1`:

            ::

                >>> staff = Staff(r"c'8 d' r \times 2/3 { e' r f' } g' a' r")
                >>> label(staff).with_start_offsets()
                >>> show(staff) # doctest:+SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ^ \markup { 0 }
                    d'8 ^ \markup { 1/8 }
                    r8 ^ \markup { 1/4 }
                    \times 2/3 {
                        e'8 ^ \markup { 3/8 }
                        r8 ^ \markup { 11/24 }
                        f'8 ^ \markup { 13/24 }
                    }
                    g'8 ^ \markup { 5/8 }
                    a'8 ^ \markup { 3/4 }
                    r8 ^ \markup { 7/8 }
                }

            Returns selection of leaf selection:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> result = selector(staff)
                >>> for selection in result:
                ...     selection
                ...
                Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

            Returns selection of leaf selections:

            ::

                >>> selector = selector.partition_by_ratio(mathtools.Ratio((1, 1)))
                >>> result = selector(staff)
                >>> for selection in result:
                ...     selection
                ...
                Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

            Gets second leaf selection:

            ::

                >>> selector = selector.get_item(1)
                >>> selector(staff)
                Selection([Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

        ..  container:: example

            **Example 2.** Partitions leaves by ratio of `1:1:1`:

            ::

                >>> staff = Staff(r"c'8 d' r \times 2/3 { e' r f' } g' a' r")
                >>> label(staff).with_start_offsets()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 ^ \markup { 0 }
                    d'8 ^ \markup { 1/8 }
                    r8 ^ \markup { 1/4 }
                    \times 2/3 {
                        e'8 ^ \markup { 3/8 }
                        r8 ^ \markup { 11/24 }
                        f'8 ^ \markup { 13/24 }
                    }
                    g'8 ^ \markup { 5/8 }
                    a'8 ^ \markup { 3/4 }
                    r8 ^ \markup { 7/8 }
                }

            Returns selection of leaf selection:

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> result = selector(staff)
                >>> for selection in result:
                ...     selection
                ...
                Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

            Return selection of leaf selections:

            ::

                >>> selector = selector.partition_by_ratio(mathtools.Ratio((1, 1, 1)))
                >>> result = selector(staff)
                >>> for selection in result:
                ...     selection
                ...
                Selection([Note("c'8"), Note("d'8"), Rest('r8')])
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Rest('r8')])

            Gets second leaf selection:

            ::

                >>> selector = selector.get_item(1)
                >>> selector(staff)
                Selection([Note("e'8"), Rest('r8'), Note("f'8")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PartitionByRatioCallback(ratio)
        return self._append_callback(callback)

    def rest(self):
        r'''Gets all but the first item in selection.

        ..  container:: example

            **Example 1.** Selects all pitched logical ties (except the first):

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.rest()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4"), Note("e'4"), Note("e'4")])
                LogicalTie([Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            start=1,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    @staticmethod
    def run_selectors(expr, selectors, rotation=None):
        r'''Processes multiple selectors against a single selection.

        Minimizes re-selection when selectors share identical prefixes of
        selector callbacks.

        ::

            >>> staff = Staff("c'4 d'8 e'8 f'4 g'8 a'4 b'8 c'8")

        ::

            >>> selector = selectortools.Selector()
            >>> logical_tie_selector = selector.by_logical_tie()
            >>> pitched_selector = logical_tie_selector.by_pitch('C4')
            >>> duration_selector = logical_tie_selector.by_duration('==', (1, 8))
            >>> contiguity_selector = duration_selector.by_contiguity()
            >>> selectors = [
            ...     selector,
            ...     logical_tie_selector,
            ...     pitched_selector,
            ...     duration_selector,
            ...     contiguity_selector,
            ...     ]

        ::

            >>> result = selectortools.Selector.run_selectors(staff, selectors)
            >>> all(selector in result for selector in selectors)
            True

        ::

            >>> for x in result[selector]:
            ...     x
            Staff("c'4 d'8 e'8 f'4 g'8 a'4 b'8 c'8")

        ::

            >>> for x in result[logical_tie_selector]:
            ...     x
            LogicalTie([Note("c'4")])
            LogicalTie([Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("f'4")])
            LogicalTie([Note("g'8")])
            LogicalTie([Note("a'4")])
            LogicalTie([Note("b'8")])
            LogicalTie([Note("c'8")])

        ::

            >>> for x in result[pitched_selector]:
            ...     x
            LogicalTie([Note("c'4")])
            LogicalTie([Note("c'8")])

        ::

            >>> for x in result[duration_selector]:
            ...     x
            LogicalTie([Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("g'8")])
            LogicalTie([Note("b'8")])
            LogicalTie([Note("c'8")])

        ::

            >>> for x in result[contiguity_selector]:
            ...     x
            ...
            Selection([LogicalTie([Note("d'8")]), LogicalTie([Note("e'8")])])
            Selection([LogicalTie([Note("g'8")])])
            Selection([LogicalTie([Note("b'8")]), LogicalTie([Note("c'8")])])

        Returns a dictionary of selector/selection pairs.
        '''
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        prototype = (
            scoretools.Component,
            selectiontools.Selection,
            )
        if not isinstance(expr, prototype):
            expr = select(expr)
        expr = (expr,)
        assert all(isinstance(x, prototype) for x in expr), repr(expr)
        maximum_length = 0
        for selector in selectors:
            if selector.callbacks:
                maximum_length = max(maximum_length, len(selector.callbacks))
        #print('MAX LENGTH', maximum_length)
        selectors = list(selectors)
        results_by_prefix = {(): expr}
        results_by_selector = collections.OrderedDict()
        for index in range(1, maximum_length + 2):
            #print('INDEX', index)
            #print('PRUNING')
            for selector in selectors[:]:
                callbacks = selector.callbacks or ()
                callback_length = index - 1
                if len(callbacks) == callback_length:
                    prefix = callbacks[:callback_length]
                    results_by_selector[selector] = results_by_prefix[prefix]
                    selectors.remove(selector)
                    #print('\tREMOVED:', selector)
                    #print('\tREMAINING:', len(selectors))
            if not selectors:
                #print('BREAKING')
                break
            #print('ADDING')
            for selector in selectors:
                callbacks = selector.callbacks or ()
                this_prefix = callbacks[:index]
                if this_prefix in results_by_prefix:
                    #print('\tSKIPPING', repr(selector))
                    continue
                #print('\tADDING', repr(selector))
                previous_prefix = callbacks[:index - 1]
                previous_expr = results_by_prefix[previous_prefix]
                callback = this_prefix[-1]
                expr = callback(
                    previous_expr,
                    rotation=rotation,
                    )
                results_by_prefix[this_prefix] = expr
        return results_by_selector

    def with_next_leaf(self):
        r'''Configures selector with next leaf after each selection.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.with_next_leaf()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example

            Handles flattened selections of leaves.

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_item(-1, apply_to_each=True)
                >>> selector(staff)
                Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

            ::

                >>> selector = selector.with_next_leaf()

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'4"), Note("d'4")])
                Selection([Note("d'4"), Note("e'4")])
                Selection([Note("e'4"), Rest('r4')])
                Selection([Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ExtraLeafSelectorCallback(
            with_next_leaf=True,
            )
        return self._append_callback(callback)

    def with_previous_leaf(self):
        r'''Configures selector with previous leaf before each selection.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.with_previous_leaf()

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example

            Handles flattened selections of leaves.

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaf()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_item(0, apply_to_each=True)
                >>> selector(staff)
                Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

            ::

                >>> selector = selector.with_previous_leaf()

            ::

                >>> for selection in selector(staff):
                ...     selection
                ...
                Selection([Note("c'4")])
                Selection([Note("c'4"), Note("d'4")])
                Selection([Note("d'4"), Note("e'4")])
                Selection([Rest('r4'), Note("f'4")])

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ExtraLeafSelectorCallback(
            with_previous_leaf=True,
            )
        return self._append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets callbacks of selector.
        '''
        return self._callbacks
