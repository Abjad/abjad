# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import select


class Selector(AbjadObject):
    r'''A component selector.

    ::

        >>> staff = Staff(r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4")

    ::

        >>> selector = selectortools.Selector()
        >>> selector(staff)
        Selection(<Staff{6}>,)

    ::

        >>> selector = selector.by_leaves()
        >>> selector = selector.by_run(Note)
        >>> for x in selector(staff):
        ...     x
        ...
        Selection(Note("c'4"), Note("d'8"))
        Selection(Note("e'8"),)
        Selection(Note("f'16"), Note("g'8"), Note("a'4"))

    ::

        >>> selector = selector.by_length(3)
        >>> selector(staff)
        Selection(Selection(Note("f'16"), Note("g'8"), Note("a'4")),)

    ::

        >>> selector = selector[0]
        >>> selector(staff)
        Selection(ContiguousSelection(Note("f'16"),),)

    ::

        >>> print format(selector)
        selectortools.Selector(
            callbacks=(
                selectortools.PrototypeSelectorCallback(
                    (
                        scoretools.Leaf,
                        )
                    ),
                selectortools.RunSelectorCallback(
                    (
                        scoretools.Note,
                        )
                    ),
                selectortools.LengthSelectorCallback(
                    length=3,
                    parts=Exact,
                    ),
                selectortools.SliceSelectorCallback(
                    0
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
        r'''Selects components from `expr`.

        Returns a selection of selections or containers.
        '''
        prototype = (scoretools.Container, selectiontools.Selection)
        if not isinstance(expr, prototype):
            expr = select(expr)
        expr = (expr,)
        assert all(isinstance(x, prototype) for x in expr), expr
        callbacks = self.callbacks or ()
        for callback in callbacks:
            expr = callback(expr)
            assert all(isinstance(x, prototype) for x in expr), \
                (expr, callback)
        return selectiontools.Selection(expr)

    def __getitem__(self, item):
        from experimental.tools import selectortools
        callback = selectortools.SliceSelectorCallback(item)
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

    def by_class(
        self,
        prototype=None):
        r'''Configures selector to select components of class `prototype`.

        Emits new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(prototype)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_leaves(self):
        r'''Configures selector to select leaves.

        Emits new selector.
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

        Emits new selector.
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
        only_with_head=False,
        only_with_tail=False,
        pitched=False,
        trivial=True,
        ):
        r'''Configures selector to select logical ties.

        ..  container:: example

            **Example 1.** Select all logical ties.

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

            **Example 2.** Select pitched logical ties.

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

            **Example 3.** Select pitched non-trivial logical ties.

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

            **Example 4.** Select pitched non-trivial logical ties whose head
            is contained in the expression to be selected from.

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

            **Example 5.** Select pitched non-trivial logical ties whose tail
            is contained in the expression to be selected from.

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

            **Example 5.** Select logical ties whose head and tail is contained
            in the expression to be selected from.

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

        Emits new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LogicalTieSelectorCallback(
            pitched=pitched,
            trivial=trivial,
            only_with_head=only_with_head,
            only_with_tail=only_with_tail,
            )
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

        Emits new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.RunSelectorCallback(prototype)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def longer_than(self, count):
        r'''Configures selector to select containers or selections whose length
        is longer than `count`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.longer_than(1)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("d'8"), Note("e'8"))
                Selection(Note("f'8"), Note("g'8"), Note("a'8"))

        Emits new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=count + 1,
            parts=More,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def shorter_than(self, count):
        r'''Configures selector to select containers or selections whose length
        is shorter than `count`.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> selector = selectortools.Selector()
                >>> selector = selector.by_leaves()
                >>> selector = selector.by_run(Note)
                >>> selector = selector.shorter_than(3)

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                Selection(Note("c'8"),)
                Selection(Note("d'8"), Note("e'8"))

        Emits new selector.
        '''
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=count - 1,
            parts=Less,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)
