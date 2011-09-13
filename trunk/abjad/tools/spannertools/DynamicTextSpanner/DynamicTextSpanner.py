from abjad.tools.spannertools.DynamicTextSpanner._DynamicTextSpannerFormatInterface import _DynamicTextSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class DynamicTextSpanner(Spanner):
    r'''Abjad dynamic text spanner::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> spannertools.DynamicTextSpanner(staff[:], 'f')
        DynamicTextSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 \f
            d'8
            e'8
            f'8
        }

    Format dynamic `mark` at first leaf in spanner.

    Return dynamic text spanner.
    '''

    def __init__(self, components = None, mark = ''):
        Spanner.__init__(self, components)
        self._format = _DynamicTextSpannerFormatInterface(self)
        self.mark = mark

    ### PUBLIC ATTRIBUTES ###

    @apply
    def mark():
        def fget(self):
            '''Get dynamic string::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> dynamic_text_spanner = spannertools.DynamicTextSpanner(staff[:], 'f')
                abjad> dynamic_text_spanner.mark
                'f'

            Set dynamic string::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> dynamic_text_spanner = spannertools.DynamicTextSpanner(staff[:], 'f')
                abjad> dynamic_text_spanner.mark = 'p'
                abjad> dynamic_text_spanner.mark
                'p'

            Set string.
            '''
            return self._mark
        def fset(self, arg):
            assert isinstance(arg, str)
            self._mark = arg
        return property(**locals())
