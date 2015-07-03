# -*- encoding: utf-8 -*-
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
            >>> for x in selector(staff):
            ...     x
            ...
            <Staff{6}>

    ..  container:: example

        **Example 2.** Selects all of the leaves in a component:

        ::

            >>> selector = selector.by_leaves()
            >>> for x in selector(staff):
            ...     x
            ...
            Selection(Note("c'4"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r16'), Note("f'16"), Note("g'8"), Note("a'4"))

    ..  container:: example

        **Example 3.** Selects runs of notes:

        ::

            >>> selector = selector.by_run(Note)
            >>> for x in selector(staff):
            ...     x
            ...
            Selection(Note("c'4"), Note("d'8"))
            Selection(Note("e'8"),)
            Selection(Note("f'16"), Note("g'8"), Note("a'4"))

    ..  container:: example

        **Example 4.** Selects subselections with lengths equal to ``3``:

        ::

            >>> selector = selector.by_length(3)
            >>> for x in selector(staff):
            ...     x
            ...
            Selection(Note("f'16"), Note("g'8"), Note("a'4"))

    ..  container:: example

        **Example 5.** Selects the first item in each subselection:

        ::

            >>> selector = selector[0]
            >>> for x in selector(staff):
            ...     x
            ...
            ContiguousSelection(Note("f'16"),)

    ..  container:: example

        **Example 6.** Flattens all subselections and containers:

        ::

            >>> selector = selector.flatten()
            >>> for x in selector(staff):
            ...     x
            ...
            Note("f'16")

        ::

            >>> print(format(selector))
            selectortools.Selector(
                callbacks=(
                    selectortools.PrototypeSelectorCallback(
                        prototype=scoretools.Leaf,
                        ),
                    selectortools.RunSelectorCallback(
                        prototype=scoretools.Note,
                        ),
                    selectortools.LengthSelectorCallback(
                        length=3,
                        ),
                    selectortools.ItemSelectorCallback(
                        item=0,
                        apply_to_each=True,
                        ),
                    selectortools.FlattenSelectorCallback(
                        depth=-1,
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

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
        r'''Selects components from component or selection `expr`.

        Returns a selection of selections or containers.
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
            #print('EXPR', expr)
            try:
                expr = callback(expr, rotation=rotation)
            except TypeError:
                expr = callback(expr)
        return selectiontools.Selection(expr)

    def __getitem__(self, item):
        r'''Gets `item` from selector.

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

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets selector callbacks.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def append_callback(self, callback):
        r'''Configures selector with arbitrary `callback`.

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
                ...     def __call__(self, expr):
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
                >>> selector = selector.by_leaves()
                >>> selector = selector.append_callback(CMajorSelectorCallback())

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Chord("<c' e' g'>4"), Chord("<e' g' c''>2"))

        Returns new selector.
        '''
        return self._append_callback(callback)

    def by_class(
        self,
        prototype=None,
        flatten=None,
        ):
        r'''Configures selector to select components of class `prototype`.

        ..  todo:: Maybe add a depth=None keyword.

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(
            prototype=prototype,
            flatten=flatten,
            )
        return self._append_callback(callback)

    def by_contiguity(self):
        r'''Configures selector select components based on time-wise
        contiguity.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.flatten()
                >>> selector = selector.by_duration('==', (1, 16))
                >>> selector = selector.by_contiguity()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16"))
                Selection(Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16"))

        ..  container:: example

            ::

                >>> staff = Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 f'4 g'8.")
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
                    g'8.
                }

            ::

                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie()
                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie(Note("c'4"),)
                LogicalTie(Note("d'8"), Note("d'16"))
                LogicalTie(Note("e'16"), Note("e'8"))
                LogicalTie(Note("f'4"),)
                LogicalTie(Note("g'8."),)

            ::

                >>> selector = selector.by_duration('<', (1, 4))
                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie(Note("d'8"), Note("d'16"))
                LogicalTie(Note("e'16"), Note("e'8"))
                LogicalTie(Note("g'8."),)

            ::

                >>> selector = selector.by_contiguity()
                >>> for x in selector(staff):
                ...     x
                ...
                Selection(LogicalTie(Note("d'8"), Note("d'16")), LogicalTie(Note("e'16"), Note("e'8")))
                Selection(LogicalTie(Note("g'8."),),)

            ::

                >>> selector = selector.by_leaves()
                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("d'16"), Note("e'16"), Note("e'8"))
                Selection(Note("g'8."),)

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
                    g'8. -\snappizzicato
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
        r'''Configures selector to select components partitioned by `counts`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'), Note("d'8"))

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'), Note("d'8"))
                Selection(Note("e'8"), Rest('r8'), Note("f'8"))

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'), Note("d'8"))
                Selection(Note("e'8"), Rest('r8'), Note("f'8"))
                Selection(Note("g'8"), Note("a'8"))

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     fuse_overhang=True,
                ...     overhang=True,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'), Note("d'8"))
                Selection(Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"))

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_counts(
                ...     [1, 2, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Rest('r8'), Note("d'8"))
                Selection(Note("e'8"), Rest('r8'), Note("f'8"))
                Selection(Note("g'8"),)
                Selection(Note("a'8"), Note("b'8"))
                Selection(Rest('r8'), Note("c''8"))

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_counts(
                ...     [1, 2, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     rotate=True,
                ...     )

            ::

                >>> for x in selector(staff, rotation=1):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'))
                Selection(Note("d'8"), Note("e'8"), Rest('r8'))
                Selection(Note("f'8"),)
                Selection(Note("g'8"), Note("a'8"))
                Selection(Note("b'8"), Rest('r8'), Note("c''8"))

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
        r'''Configures selector to select containers or selections of
        duration `duration`.

        ..  container:: example

            **Example 1.** Selects all runs of notes with duration equal to
            ``2/8``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_duration(Duration(2, 8))

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("e'8"))

        ..  container:: example

            **Example 2.** Selects all runs of notes with duration shorter than
            ``3/8``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_duration(
                ...     selectortools.DurationInequality(
                ...          duration=Duration(3, 8),
                ...          operator_string='<',
                ...          ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Note("d'8"), Note("e'8"))

        ..  container:: example

            **Example 3.** Selects all runs of notes with duration longer than
            or equal to ``1/4``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_duration(
                ...     selectortools.DurationInequality(
                ...          duration=Duration(1, 4),
                ...          operator_string='>=',
                ...          ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("e'8"))
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

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
                ...     '==',
                ...     (1, 8),
                ...     preprolated=True,
                ...     )

            ::

                >>> selections = selector(staff)
                >>> for logical_tie in selections:
                ...     attach(Articulation('accent'), logical_tie[0])
                ...     print(logical_tie)
                ...
                LogicalTie(Note("d'16"), Note("d'16"))
                LogicalTie(Note("e'16"), Note("e'16"))
                LogicalTie(Note("f'16"), Note("f'16"))
                LogicalTie(Note("g'16"), Note("g'16"))
                LogicalTie(Note("a'16"), Note("a'16"))

            ::

                >>> show(staff) # doctest: +SKIP

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

    def by_leaves(self, flatten=None):
        r'''Configures selector to select leaves.

        ..  container:: example

            **Example 1.**

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'), Note("d'8"), Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"))

        ..  container:: example

            **Example 2.**

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves(flatten=True)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Note("c'8")
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Rest('r8')
                Note("f'8")
                Note("g'8")
                Note("a'8")

            **Example 3.**

            ::

                >>> staff = Staff("abj: | 4/4 c'2 d'2 || 3/4 e'4 f'4 g'4 |")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_class(Measure)
                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Measure((4, 4), "c'2 d'2"), Measure((3, 4), "e'4 f'4 g'4"))

            ::

                >>> selector = selector.by_leaves()
                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'2"), Note("d'2"), Note("e'4"), Note("f'4"), Note("g'4"))

        ..  container:: example

            **Example 4.**

            ::

                >>> staff = Staff("abj: | 4/4 c'2 d'2 || 3/4 e'4 f'4 g'4 |")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_class(Measure, flatten=True)
                >>> for x in selector(staff):
                ...     x
                ...
                Measure((4, 4), "c'2 d'2")
                Measure((3, 4), "e'4 f'4 g'4")

            ::

                >>> selector = selector.by_leaves()
                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'2"), Note("d'2"))
                Selection(Note("e'4"), Note("f'4"), Note("g'4"))

        ..  container:: example

            **Example 5.**

            ::

                >>> staff = Staff("abj: | 4/4 c'2 d'2 || 3/4 e'4 f'4 g'4 |")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_class(Measure, flatten=True)
                >>> for x in selector(staff):
                ...     x
                ...
                Measure((4, 4), "c'2 d'2")
                Measure((3, 4), "e'4 f'4 g'4")

            ::

                >>> selector = selector.by_leaves(flatten=True)
                >>> for x in selector(staff):
                ...     x
                ...
                Note("c'2")
                Note("d'2")
                Note("e'4")
                Note("f'4")
                Note("g'4")

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(
            prototype=scoretools.Leaf,
            flatten=flatten,
            )
        return self._append_callback(callback)

    def by_length(self, *args):
        r'''Configures selector to selector containers or selections of length
        `length`.

        ..  container:: example

            **Example 1.** Selects all runs of more than ``1`` note:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_length(
                ...     selectortools.LengthInequality(
                ...          length=1,
                ...          operator_string='>',
                ...          ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("e'8"))
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

        ..  container:: example

            **Example 1.** Selects all runs ``3`` or fewer notes:
            ``3``:

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.by_length(
                ...     selectortools.LengthInequality(
                ...          length=3,
                ...          operator_string='<',
                ...          ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Note("d'8"), Note("e'8"))

        Returns new selector.
        '''
        from abjad.tools import selectortools
        if len(args) == 1:
            length = args[0]
            if not isinstance(length, selectortools.LengthInequality):
                length = int(length)
        elif len(args) == 2:
            length = selectortools.LengthInequality(
                length=args[1],
                operator_string=args[0],
                )
        else:
            raise ValueError(args)
        callback = selectortools.LengthSelectorCallback(
            length=length,
            )
        return self._append_callback(callback)

    def by_logical_measure(self):
        r'''Configures selector to group components by logical measure.

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
        r'''Configures selector to select logical ties.

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
                LogicalTie(Note("c'8"),)
                LogicalTie(Note("d'8"), Note("d'8"))
                LogicalTie(Note("e'8"),)
                LogicalTie(Rest('r8'),)
                LogicalTie(Note("f'8"), Note("f'8"))
                LogicalTie(Rest('r8'),)

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie(Note("d'8"), Note("d'8"))
                LogicalTie(Note("e'8"),)
                LogicalTie(Rest('r8'),)
                LogicalTie(Note("f'8"), Note("f'8"))

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
                LogicalTie(Note("c'8"),)
                LogicalTie(Note("d'8"), Note("d'8"))
                LogicalTie(Note("e'8"),)
                LogicalTie(Note("f'8"), Note("f'8"))

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie(Note("d'8"), Note("d'8"))
                LogicalTie(Note("e'8"),)
                LogicalTie(Note("f'8"), Note("f'8"))

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
                LogicalTie(Note("d'8"), Note("d'8"))
                LogicalTie(Note("f'8"), Note("f'8"))

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie(Note("d'8"), Note("d'8"))
                LogicalTie(Note("f'8"), Note("f'8"))

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
        r'''Configures selector to select by `pattern`:

        ..  container:: example

            **Example 1.**

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.by_pattern(
                ...     pattern=rhythmmakertools.BooleanPattern(
                ...         indices=[1],
                ...         ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie(Note("d'4"), Note("d'4"))

        ..  container:: example

            **Example 2.**

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.by_pattern(
                ...     pattern=rhythmmakertools.BooleanPattern(
                ...         indices=[0],
                ...         period=2,
                ...         ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie(Note("c'4"),)
                LogicalTie(Note("e'4"), Note("e'4"), Note("e'4"))

        ..  container:: example

            **Example 3.**

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves(flatten=True)
                >>> selector = selector.by_pattern(
                ...     pattern=rhythmmakertools.BooleanPattern(
                ...         indices=[0],
                ...         period=2,
                ...         ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     print(staff.index(x), repr(x))
                ...
                0 Note("c'4")
                2 Note("d'4")
                4 Note("e'4")
                6 Rest('r4')

        ..  container:: example

            **Example 4.**

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves(flatten=True)
                >>> selector = selector.by_pattern(
                ...     pattern=rhythmmakertools.BooleanPattern(
                ...         indices=[0],
                ...         period=2,
                ...         ),
                ...     )

            ::

                >>> for x in selector(staff, rotation=1):
                ...     print(staff.index(x), repr(x))
                ...
                1 Note("d'4")
                3 Note("e'4")
                5 Note("e'4")
                7 Note("f'4")

        ..  container:: example

            **Example 5.**

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.by_pattern(
                ...     apply_to_each=True,
                ...     pattern=rhythmmakertools.BooleanPattern(
                ...         indices=[1],
                ...         ),
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'4"),)
                Selection(Note("e'4"),)

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PatternedSelectorCallback(
            pattern=pattern,
            apply_to_each=apply_to_each,
            )
        return self._append_callback(callback)

    def by_pitch(
        self,
        pitches=None,
        ):
        r'''Configures selector to selector expressions by `pitches`.

        ..  todo:: Implement a pitch-inequality class.

        ..  container:: example

            **Example 1.** Selects components matching a single pitch:

            ::

                >>> staff = Staff("c'4 d'4 ~ d'4 e'4")
                >>> staff.extend("r4 <c' e' g'>4 ~ <c' e' g'>2")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves(flatten=True)
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
                >>> selector = selector.by_leaves(flatten=True)
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
                LogicalTie(Note("c'4"),)
                LogicalTie(Chord("<c' e' g'>4"), Chord("<c' e' g'>2"))

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.PitchSelectorCallback(pitches=pitches)
        return self._append_callback(callback)

    def by_run(
        self,
        prototype=None,
        ):
        r'''Configures selector to select runs of `prototype`.

        ..  container:: example

            **Example 1.** Selects run of notes and chords at any depth:

            ::

                >>> staff = Staff(r"c'8 d' r \times 2/3 { e' r f' } g' a' r")
                >>> selector = selectortools.Selector()
                >>> prototype = (Note, Chord)
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(prototype)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Note("d'8"))
                Selection(Note("e'8"),)
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.RunSelectorCallback(prototype)
        return self._append_callback(callback)

    def first(self):
        r'''Configures selector to select first selection.

        ..  container:: example

            **Example 1.** Selects first pitched logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.first()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'4"),)

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=0,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def flatten(self, depth=-1):
        r'''Configures selector to flatten its selections to `depth`.

        ..  container:: example

            **Example 1.** Selects all pitched logical ties (except the first
            and last) and then flattens the pitch logical ties:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.middle()
                >>> selector = selector.flatten()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Note("d'4")
                Note("d'4")
                Note("e'4")
                Note("e'4")
                Note("e'4")

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.FlattenSelectorCallback(depth=depth)
        return self._append_callback(callback)

    def get_item(self, item, apply_to_each=True):
        r'''Configures selector to select `item`.

        Maps the callback to each item in sequence when `apply_to_each` is
        true.

        Applies the callback to the entire sequence when `apply_to_each` is
        false.

        ..  container:: example

            **Example 1.** Selects the first note of each logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_item(0, apply_to_each=True)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                ContiguousSelection(Note("c'4"),)
                ContiguousSelection(Note("d'4"),)
                ContiguousSelection(Note("e'4"),)
                ContiguousSelection(Note("f'4"),)

        ..  container:: example

            **Example 2.** Selects logical tie at index ``1``:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_item(1, apply_to_each=False)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'4"), Note("d'4"))

        '''
        from abjad.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=item,
            apply_to_each=apply_to_each,
            )
        return self._append_callback(callback)

    def get_slice(self, start=None, stop=None, apply_to_each=True):
        r'''Configures selector to select `start`:`stop`.

        Maps the callback to each item in sequence when `apply_to_each` is
        true.

        Applies the callback to the entire sequence when `apply_to_each` is
        false.

        ..  container:: example

            **Example 1.** Gets all notes (except the first) in each
            pitched logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_slice(
                ...     start=1,
                ...     stop=None,
                ...     apply_to_each=True,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie(Note("d'4"),)
                LogicalTie(Note("e'4"), Note("e'4"))

        ..  container:: example

            **Example 2.** Gets all pitched logical ties (except the last):

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.get_slice(
                ...     start=None,
                ...     stop=-1,
                ...     apply_to_each=False,
                ...     )

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie(Note("c'4"),)
                LogicalTie(Note("d'4"), Note("d'4"))
                LogicalTie(Note("e'4"), Note("e'4"), Note("e'4"))

        '''
        from abjad.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            start=start,
            stop=stop,
            apply_to_each=apply_to_each,
            )
        return self._append_callback(callback)

    def last(self):
        r'''Configures selector to select the last selection.

        ..  container:: example

            **Example 1.** Selects the last pitched logical tie:

            ::

                >>> staff = Staff(r"c'4 d'4 ~ d'4 e'4 ~ e'4 ~ e'4 r4 f'4")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(pitched=True)
                >>> selector = selector.last()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("f'4"),)

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=-1,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def middle(self):
        r'''Configures selector to select all but the first or last selection.

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
                LogicalTie(Note("d'4"), Note("d'4"))
                LogicalTie(Note("e'4"), Note("e'4"), Note("e'4"))

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
        r'''Configures selector to select all but the last selection.

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
                LogicalTie(Note("c'4"),)
                LogicalTie(Note("d'4"), Note("d'4"))
                LogicalTie(Note("e'4"), Note("e'4"), Note("e'4"))

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            stop=-1,
            apply_to_each=False,
            )
        return self._append_callback(callback)

    def rest(self):
        r'''Configures selector to select all but the first selection.

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
                LogicalTie(Note("d'4"), Note("d'4"))
                LogicalTie(Note("e'4"), Note("e'4"), Note("e'4"))
                LogicalTie(Note("f'4"),)

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
            LogicalTie(Note("c'4"),)
            LogicalTie(Note("d'8"),)
            LogicalTie(Note("e'8"),)
            LogicalTie(Note("f'4"),)
            LogicalTie(Note("g'8"),)
            LogicalTie(Note("a'4"),)
            LogicalTie(Note("b'8"),)
            LogicalTie(Note("c'8"),)

        ::

            >>> for x in result[pitched_selector]:
            ...     x
            LogicalTie(Note("c'4"),)
            LogicalTie(Note("c'8"),)

        ::

            >>> for x in result[duration_selector]:
            ...     x
            LogicalTie(Note("d'8"),)
            LogicalTie(Note("e'8"),)
            LogicalTie(Note("g'8"),)
            LogicalTie(Note("b'8"),)
            LogicalTie(Note("c'8"),)

        ::

            >>> for x in result[contiguity_selector]:
            ...     x
            Selection(LogicalTie(Note("d'8"),), LogicalTie(Note("e'8"),))
            Selection(LogicalTie(Note("g'8"),),)
            Selection(LogicalTie(Note("b'8"),), LogicalTie(Note("c'8"),))

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
                try:
                    expr = callback(previous_expr, rotation=rotation)
                except TypeError:
                    expr = callback(previous_expr)
                results_by_prefix[this_prefix] = expr

        return results_by_selector

    def with_next_leaf(self):
        r'''Configures selector to select the next leaf after each selection.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.with_next_leaf()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"), Rest('r8'))
                Selection(Note("d'8"), Note("e'8"), Rest('r8'))
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ExtraLeafSelectorCallback(
            with_next_leaf=True,
            )
        return self._append_callback(callback)

    def with_previous_leaf(self):
        r'''Configures selector to select the previous leaf before each
        selection.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.with_previous_leaf()

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Rest('r8'), Note("d'8"), Note("e'8"))
                Selection(Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"))

        Returns new selector.
        '''
        from abjad.tools import selectortools
        callback = selectortools.ExtraLeafSelectorCallback(
            with_previous_leaf=True,
            )
        return self._append_callback(callback)