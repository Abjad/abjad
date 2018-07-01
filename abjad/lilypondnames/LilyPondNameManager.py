import copy


class LilyPondNameManager(object):
    """
    LilyPond name manager.

    Base class from which grob, setting and tweak managers inherit.
    """

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a LilyPond name manager with attribute
        pairs equal to those of this LilyPond name manager.
        """
        if isinstance(argument, type(self)):
            attribute_pairs_1 = self._get_attribute_pairs()
            attribute_pairs_2 = argument._get_attribute_pairs()
            return attribute_pairs_1 == attribute_pairs_2
        return False

    def __getstate__(self) -> dict:
        """
        Gets object state.
        """
        return copy.deepcopy(vars(self))

    def __hash__(self) -> int:
        """
        Hashes LilyPond name manager.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation of LilyPond name manager.
        """
        body_string = ''
        pairs = self._get_attribute_pairs()
        pairs = [str(_) for _ in pairs]
        body_string = ', '.join(pairs)
        return f'{type(self).__name__}({body_string})'

    def __setstate__(self, state) -> None:
        """
        Sets object state.
        """
        for key, value in state.items():
            self.__dict__[key] = value

    ### PRIVATE METHODS ###

    def _get_attribute_pairs(self):
        return list(sorted(vars(self).items()))
