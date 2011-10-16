from abjad.tools.lilypondfiletools._AttributedBlock import _AttributedBlock
import types


class PaperBlock(_AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file paper block::

        abjad> paper_block = lilypondfiletools.PaperBlock()

    ::

        abjad> paper_block
        PaperBlock()

    ::

        abjad> paper_block.print_page_number = True
        abjad> paper_block.print_first_page_number = False

    ::

        abjad> f(paper_block)
        \paper {
            print-first-page-number = ##f
            print-page-number = ##t
        }

    Return paper block.
    '''

    def __init__(self):
        _AttributedBlock.__init__(self)
        self._escaped_name = r'\paper'
        self.minimal_page_breaking = None

    ### PRIVATE ATTRIBUTES ###

    @property
    def _formatted_user_attributes(self):
        result = []
        if self.minimal_page_breaking:
            result.append('#(define page-breaking ly:minimal-breaking)')
        result.extend(_AttributedBlock._formatted_user_attributes.fget(self))
        return result

    ### PUBLIC ATTRIBUTES ###

    @apply
    def minimal_page_breaking():
        def fget(self):
            return self._minimal_page_breaking
        def fset(self, expr):
            if isinstance(expr, (bool, type(None))):
                self._minimal_page_breaking = expr
            else:
                raise TypeError('must be boolean or none')
        return property(**locals())
