# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.Block import Block


class PaperBlock(Block):
    r'''A LilyPond input file paper block:

    ::

        >>> paper_block = lilypondfiletools.PaperBlock()

    ::

        >>> paper_block
        PaperBlock()

    ::

        >>> paper_block.print_page_number = True
        >>> paper_block.print_first_page_number = False

    ..  doctest::

        >>> print format(paper_block)
        \paper {
            print-first-page-number = ##f
            print-page-number = ##t
        }

    '''

    ### INITIALIZER ###

    def __init__(self):
        Block.__init__(self)
        self._escaped_name = r'\paper'
