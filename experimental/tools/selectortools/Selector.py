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

    def by_class(self, prototype=None):
        from experimental.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(prototype)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_leaves(self):
        from experimental.tools import selectortools
        callback = selectortools.PrototypeSelectorCallback(scoretools.Leaf)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_length(self, length=None, parts=Exact):
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=length,
            parts=parts,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def by_run(self, prototype=None):
        from experimental.tools import selectortools
        callback = selectortools.RunSelectorCallback(prototype)
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def longer_than(self, count):
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=count + 1,
            parts=More,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def shorter_than(self, count):
        from experimental.tools import selectortools
        callback = selectortools.LengthSelectorCallback(
            length=count - 1,
            parts=Less,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)
