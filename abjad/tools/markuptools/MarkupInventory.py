# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.markuptools.Markup import Markup


class MarkupInventory(TypedList):
    '''Abjad model of an ordered list of markup:

    ::

        >>> inventory = markuptools.MarkupInventory(['foo', 'bar'])

    ::

        >>> inventory
        MarkupInventory([Markup(contents=('foo',)), Markup(contents=('bar',))])

    Markup inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    # TODO: add verifiable code in doctest
    def __illustrate__(self):
        r'''Illustrates markup inventory.

        ..  container:: example

            ::

                >>> inventory = markuptools.MarkupInventory(['foo', 'bar'])
                >>> show(inventory) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        for name in ('layout', 'paper', 'score'):
            block = lilypond_file[name]
            lilypond_file.items.remove(block)
        lilypond_file.header_block.tagline = False
        for item in self:
            lilypond_file.items.append(item)
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        return Markup
