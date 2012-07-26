from abc import abstractproperty
from abjad.tools import abctools


class QTarget(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items',)

    ### INITIALIZATION ###

    def __init__(self, items):
        assert len(items)
        assert all([isinstance(x, self.item_klass) for x in items])
        self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence, grace_handler=None):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abstractproperty
    def beats(self):
        raise NotImplemented

    @property
    def duration_in_ms(self):
        last_item = self._items[-1]
        return last_item.offset_in_ms + last_item.duration_in_ms

    @abstractproperty
    def item_klass(self):
        raise NotImplemented

    @property
    def items(self):
        return self._items

    ### PUBLIC METHODS ###

