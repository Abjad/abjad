# -*- encoding: utf-8 -*-
import types
from abjad.tools.datastructuretools.PayloadTree import PayloadTree


class PitchClassTree(PayloadTree):
    r'''A pitch-class tree.

    ..  container:: example

        Numbered pitch-class tree::

            >>> tree = pitchtools.PitchClassTree(
            ...     items=[[0, 4, 7, 8], [9, 2, 3, 11]],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )
            >>> print(format(tree, 'storage'))
            pitchtools.PitchClassTree(
                [
                    [
                        pitchtools.NumberedPitchClass(0),
                        pitchtools.NumberedPitchClass(4),
                        pitchtools.NumberedPitchClass(7),
                        pitchtools.NumberedPitchClass(8),
                        ],
                    [
                        pitchtools.NumberedPitchClass(9),
                        pitchtools.NumberedPitchClass(2),
                        pitchtools.NumberedPitchClass(3),
                        pitchtools.NumberedPitchClass(11),
                        ],
                    ]
                )

    ..  container:: example

        Named pitch-class tree::

            >>> tree = pitchtools.PitchClassTree(
            ...     items=[['c', 'e', 'g', 'af'], ['a', 'd', 'ef', 'b']],
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> print(format(tree, 'storage'))
            pitchtools.PitchClassTree(
                [
                    [
                        pitchtools.NamedPitchClass('c'),
                        pitchtools.NamedPitchClass('e'),
                        pitchtools.NamedPitchClass('g'),
                        pitchtools.NamedPitchClass('af'),
                        ],
                    [
                        pitchtools.NamedPitchClass('a'),
                        pitchtools.NamedPitchClass('d'),
                        pitchtools.NamedPitchClass('ef'),
                        pitchtools.NamedPitchClass('b'),
                        ],
                    ]
                )

    Pitch-class trees are treated as immutable.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        PayloadTree.__init__(
            self,
            expr=items,
            item_class=item_class,
            )