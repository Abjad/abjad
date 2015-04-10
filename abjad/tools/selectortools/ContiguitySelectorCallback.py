# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class ContiguitySelectorCallback(AbjadValueObject):
    r'''A contiguity selector callback.
    '''
    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates tuple `expr`.
        '''
        result = []
        subresult = []
        subresult.extend(expr[:1])
        for subexpr in expr[1:]:
            that_timespan = subresult[-1]._get_timespan()
            this_timespan = subexpr._get_timespan()
            if that_timespan.stop_offset == this_timespan.start_offset:
                subresult.append(subexpr)
            else:
                result.append(select(subresult))
                subresult = [subexpr]
        if subresult:
            result.append(select(subresult))
        return tuple(result)