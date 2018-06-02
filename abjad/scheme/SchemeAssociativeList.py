import typing
from .Scheme import Scheme
from .SchemePair import SchemePair


class SchemeAssociativeList(Scheme):
    """
    Abjad model of Scheme associative list.

    ..  container:: example

        >>> scheme_alist = abjad.SchemeAssociativeList([
        ...     ('space', 2),
        ...     ('padding', 0.5),
        ...     ])
        >>> abjad.f(scheme_alist)
        abjad.SchemeAssociativeList(
            [
                abjad.SchemePair(('space', 2)),
                abjad.SchemePair(('padding', 0.5)),
                ]
            )

        >>> print(format(scheme_alist))
        #'((space . 2) (padding . 0.5))

    Scheme associative lists are immutable.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.List = None,
        ) -> None:
        value = value or []
        pairs = []
        for item in value:
            if isinstance(item, tuple):
                pair = SchemePair(item)
            elif isinstance(item, SchemePair):
                pair = item
            else:
                message = f'must be Python pair or Scheme pair: {item!r}.'
                raise TypeError(message)
            pairs.append(pair)
        Scheme.__init__(self, value=pairs, quoting="'")
