# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.datastructuretools.TypedCounter import TypedCounter


class OffsetCounter(TypedCounter):
    r'''An offset counter.

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __illustrate__(self, range_=None):
        r'''Illustrates offset counter.

        Returns LilyPond file.
        '''
        if not self:
            return markuptools.Markup.null().__illustrate__()
        if range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = min(self), max(self)
        minimum = float(durationtools.Offset(minimum))
        maximum = float(durationtools.Offset(maximum))
        postscript_scale = 125. / (maximum - minimum)
        postscript_x_offset = (minimum * postscript_scale) - 1
        ps = markuptools.Postscript()
        ps = ps.setlinewidth(0.2)
        ps = ps.setdash([2, 1])
        for offset, count in sorted(self.items()):
            offset = (float(offset) * postscript_scale)
            offset -= postscript_x_offset
            ps = ps.moveto(offset, -1)
            ps = ps.rlineto(0, (float(count) * -3) + 1)
            ps = ps.stroke()
        markup = markuptools.Markup.postscript(ps)
        for offset in sorted(self):
            offset = durationtools.Multiplier(offset)
            numerator, denominator = offset.numerator, offset.denominator
            fraction = markuptools.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            markup = markuptools.Markup.combine(markup, fraction)
        return markup.__illustrate__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import durationtools
        return durationtools.Offset