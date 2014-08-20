# -*- encoding: utf-8 -*-
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
                        parts=Exact,
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

    def __call__(self, expr):
        r'''Selects components from component or selection `expr`.

        Returns a selection of selections or containers.
        '''
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
            expr = callback(expr)
        return selectiontools.Selection(expr)

    def __getitem__(self, item):
        r'''Gets `item` from selector.

        Returns another selector.
        '''
        from experimental.tools import selectortools
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
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='callbacks',
                display_string='callbacks',
                command='c',
                editor=idetools.getters.get_list,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets selector callbacks.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def by_class(
        self,
        prototype=None,
        ):
        r'''Configures selector to select components of class `prototype`.

        ..  todo:: Maybe add a depth=None keyword.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(prototype)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_duration(
        self,
        duration=None,
        parts=Exact,
        ):
        r'''Configures selector to selector containers or selections of
        duration `duration`.

        ..  todo:: Generalize `duration` to accept a ``DurationInequality``.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.DurationSelectorCallback(
            duration=duration,
            parts=parts,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_leaves(self):
        r'''Configures selector to select leaves.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(scoretools.Leaf)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_length(
        self,
        length=None,
        parts=Exact,
        ):
        r'''Configures selector to selector containers or selections of length
        `length`.

        ..  todo:: Generalize `length` to accept a ``LengthInequality``.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=length,
            parts=parts,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_logical_tie(
        self,
        flatten=True,
        only_with_head=False,
        only_with_tail=False,
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

        ..  container:: example

            **Example 4.** Selects pitched nontrivial logical ties whose head
            is contained in the expression to be selected from:

            ::

                >>> staff = Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> container = staff[2]
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(
                ...     only_with_head=True,
                ...     pitched=True,
                ...     trivial=False,
                ...     )

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie(Note("f'8"), Note("f'8"))

        ..  container:: example

            **Example 5.** Selects pitched nontrivial logical ties whose tail
            is contained in the expression to be selected from:

            ::

                >>> staff = Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> container = staff[2]
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(
                ...     only_with_tail=True,
                ...     pitched=True,
                ...     trivial=False,
                ...     )

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie(Note("d'8"), Note("d'8"))

        ..  container:: example

            **Example 5.** Selects logical ties whose head and tail is
            contained in the expression to be selected from:

            ::

                >>> staff = Staff("c'8 d' ~ { d' e' r f'~ } f' r")
                >>> container = staff[2]
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_logical_tie(
                ...     only_with_head=True,
                ...     only_with_tail=True,
                ...     )

            ::

                >>> for x in selector(container):
                ...     x
                ...
                LogicalTie(Note("e'8"),)
                LogicalTie(Rest('r8'),)

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LogicalTieSelectorCallback(
            flatten=flatten,
            pitched=pitched,
            trivial=trivial,
            only_with_head=only_with_head,
            only_with_tail=only_with_tail,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_logical_measure(self):
        r'''Configures selector to group components by logical measure.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LogicalMeasureSelectorCallback()
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_run(
        self,
        prototype=None,
        ):
        r'''Configures selector to select runs of `prototype`.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.RunSelectorCallback(prototype)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def first(self):
        r'''Configures selector to select first selection.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=0,
            apply_to_each=False,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def flatten(self, depth=-1):
        r'''Configures selector to flatten its selections to `depth`.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.FlattenSelectorCallback(depth=depth)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def last(self):
        r'''Configures selector to select the last selection.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.ItemSelectorCallback(
            item=-1,
            apply_to_each=False,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def less_than(self, length):
        r'''Configures selector to select containers or selections whose length
        is less than `length`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.less_than(3)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Note("d'8"), Note("e'8"))

        ..  todo:: Replace in favor of
            ``self.by_length(length=inequality)``.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=length - 1,
            parts=Less,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def longer_than(self, duration):
        r'''Configures selector to select containers or selections whose
        duration is longer than `duration`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.longer_than((1, 8))

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("e'8"))
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

        ..  todo:: Replace in favor of
            ``self.by_duration(duration=inequality)``.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.DurationSelectorCallback(
            duration=duration,
            parts=More,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def middle(self):
        r'''Configures selector to select all but the first or last selection.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            start=1,
            stop=-1,
            apply_to_each=False,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def more_than(self, length):
        r'''Configures selector to select containers or selections whose length
        is more than `length`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.more_than(1)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("e'8"))
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

        ..  todo:: Replace in favor of
            ``self.by_length(length=inequality)``.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=length + 1,
            parts=More,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def most(self):
        r'''Configures selector to select all but the last selection.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            stop=-1,
            apply_to_each=False,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def rest(self):
        r'''Configures selector to select all but the first selection.

        ..  container:: example

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
        from experimental.tools import selectortools
        callback = selectortools.SliceSelectorCallback(
            start=1,
            apply_to_each=False,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def shorter_than(self, duration):
        r'''Configures selector to select containers or selections whose
        duration is shorter than `duration`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.shorter_than((3, 8))

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Note("d'8"), Note("e'8"))

        ..  todo:: Replace in favor of
            ``self.by_duration(duration=inequality)``.

        Returns new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.DurationSelectorCallback(
            duration=duration,
            parts=Less,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)