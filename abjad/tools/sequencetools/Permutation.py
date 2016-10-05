# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TypedTuple


class Permutation(TypedTuple):
    r'''Permutation.

    ..  container:: example:

        **Example 1.** Permutes list:

        ::

            >>> permutation = sequencetools.Permutation([1, 0, 3, 2, 5, 4])

        ::
        
            >>> permutation([90, 91, 92, 93, 94, 95])
            [91, 90, 93, 92, 95, 94]

    ..  container:: example:

        **Example 2.** Permutes string:

        ::

            >>> permutation('winter')
            'iwtnre'

    ..  container:: example

        **Example 3.** Empty permutation:

        ::

            >>> sequencetools.Permutation()
            Permutation(())

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        superclass = super(Permutation, self)
        superclass.__init__(
            items=items,
            item_class=int,
            )
        if items is None:
            return
        sorted_items = list(sorted(self.items))
        prototype = list(range(len(items)))
        if not sorted_items == prototype:
            message = '{} must be permutation of {}.'
            message = message.format(items, prototype)
            raise Exception(message)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls permutation on `expr`.

        ..  container:: example

            **Example 1.** Calls permutation on list:

            ::

                >>> permutation = sequencetools.Permutation([1, 0, 3, 2, 5, 4])

            ::

                >>> permutation([90, 91, 92, 93, 94, 95])
                [91, 90, 93, 92, 95, 94]

        ..  container:: example

            **Example 2.** Calls permutation on string:

            ::

                >>> permutation('winter')
                'iwtnre'

        Returns new object of `expr` type.
        '''
        pass
        result = []
        for i, item in enumerate(expr):
            j = self[i]
            item_ = expr[j]
            result.append(item_)
        if isinstance(expr, str):
            result = ''.join(result)
        else:
            result = type(expr)(result)
        return result

    def __getitem__(self, i):
        r'''Gets item at index `i` in permutation.

        ..  container:: example

            **Example 1.** Gets item:

            ::

                >>> permutation = sequencetools.Permutation([1, 0, 3, 2, 5, 4])

            ::

                >>> permutation[0]
                1

            ::

                >>> permutation[-1]
                4

        ..  container:: example

            **Example 2.** Gets slice:

            ::

                >>> permutation[:4]
                (1, 0, 3, 2)

        '''
        superclass = super(Permutation, self)
        if isinstance(i, int):
            return superclass.__getitem__(i)
        #return tuple(self.items.__getitem__(i))
        return tuple(self._collection.__getitem__(i))
