# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock
import types


class PaperBlock(AttributedBlock):
    r'''Abjad model of LilyPond input file paper block:

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

    Returns paper block.
    '''

    ### INITIALIZER ###

    def __init__(self):
        AttributedBlock.__init__(self)
        self._escaped_name = r'\paper'
        self.minimal_page_breaking = None

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_user_attributes(self):
        result = []
        if self.minimal_page_breaking:
            result.append('#(define page-breaking ly:minimal-breaking)')
        result.extend(AttributedBlock._formatted_user_attributes.fget(self))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def minimal_page_breaking(self):
        return self._minimal_page_breaking

    @minimal_page_breaking.setter
    def minimal_page_breaking(self, expr):
        if isinstance(expr, (bool, type(None))):
            self._minimal_page_breaking = expr
        else:
            message = 'must be boolean or none.'
            raise TypeError(message)
