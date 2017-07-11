# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class ContiguitySelectorCallback(AbjadValueObject):
    r'''Contiguity selector callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.
        '''
        result = []
        subresult = []
        subresult.extend(argument[:1])
        for subexpr in argument[1:]:
            try:
                that_timespan = subresult[-1]._get_timespan()
            except AttributeError:
                that_timespan = subresult[-1].get_timespan()
            try:
                this_timespan = subexpr._get_timespan()
            except AttributeError:
                this_timespan = subexpr.get_timespan()
            if that_timespan.stop_offset == this_timespan.start_offset:
                subresult.append(subexpr)
            else:
                result.append(select(subresult))
                subresult = [subexpr]
        if subresult:
            result.append(select(subresult))
        return tuple(result)
