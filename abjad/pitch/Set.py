import abc
import collections
import types
from abjad.system.FormatSpecification import FormatSpecification
from abjad.utilities.TypedCollection import TypedCollection
from abjad.utilities.TypedFrozenset import TypedFrozenset


class Set(TypedFrozenset):
    """
    Abstract set.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, (
            collections.Iterator,
            types.GeneratorType,
            )):
            items = [item for item in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if (isinstance(items, TypedCollection) and
                    issubclass(items.item_class, self._parent_item_class)):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedFrozenset.__init__(
            self,
            items=items,
            item_class=item_class,
            )
        self._expression = None

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        Gets string representation.

        Returns string.
        """
        items = self._get_sorted_repr_items()
        items = [str(_) for _ in items]
        return '{{{}}}'.format(', '.join(items))

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        repr_items = self._get_sorted_repr_items()
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[repr_items],
            storage_format_args_values=[repr_items],
            storage_format_kwargs_names=[],
            )

    def _get_sorted_repr_items(self):
        items = sorted(self, key=lambda x: (float(x.number), str(x)))
        if self.item_class.__name__.startswith('Named'):
            repr_items = [str(x) for x in items]
        elif hasattr(self.item_class, 'number'):
            repr_items = [x.number for x in items]
        elif hasattr(self.item_class, 'pitch_class_number'):
            repr_items = [x.pitch_class_number for x in items]
        elif hasattr(self.item_class, '__abs__'):
            repr_items = [abs(x) for x in items]
        else:
            message = 'invalid item class: {!r}.'
            message = message.format(self.item_class)
            raise ValueError(message)
        return repr_items

    def _sort_self(self):
        return tuple(self)

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        """
        Gets cardinality of set.

        Defined equal to length of set.

        Returns nonnegative integer.
        """
        return len(self)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes set from `selection`.

        Returns set.
        """
        raise NotImplementedError
