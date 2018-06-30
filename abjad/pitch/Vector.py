import abc
import collections
import types
from abjad import mathtools
from abjad.system.FormatSpecification import FormatSpecification
from abjad.utilities.TypedCollection import TypedCollection
from abjad.utilities.TypedCounter import TypedCounter


class Vector(TypedCounter):
    """
    Abstract vector.
    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        prototype_1 = (collections.Iterator, types.GeneratorType)
        prototype_2 = (TypedCounter, collections.Counter)
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype_1):
            items = [item for item in items]
        elif isinstance(items, dict):
            items = self._dictionary_to_items(items, item_class)
        if isinstance(items, prototype_2):
            new_tokens = []
            for item, count in items.items():
                new_tokens.extend(count * [item])
            items = new_tokens
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if (isinstance(items, TypedCollection) and
                    issubclass(items.item_class, self._parent_item_class)):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.Set):
                        items = tuple(items)
                    if isinstance(items, dict):
                        item_class = self._dictionary_to_item_class(items)
                    elif isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedCounter.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        """
        String representation of vector.

        Returns string.
        """
        parts = ['{}: {}'.format(key, value)
            for key, value in self.items()]
        return '<{}>'.format(', '.join(parts))

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

    def _dictionary_to_item_class(self, dictionary):
        if not len(dictionary):
            return self._named_item_class
        keys = dictionary.keys()
        first_key = keys[0]
        assert isinstance(first_key, str), repr(first_key)
        try:
            float(first_key)
            item_class = self._numbered_item_class
        except ValueError:
            item_class = self._named_item_class
        return item_class

    def _dictionary_to_items(self, dictionary, item_class):
        items = []
        for initializer_token, count in dictionary.items():
            for _ in range(count):
                item = item_class(initializer_token)
                items.append(item)
        return items

    def _get_format_specification(self):
        if self.item_class.__name__.startswith('Named'):
            repr_items = {str(k): v for k, v in self.items()}
        else:
            repr_items = {
                mathtools.integer_equivalent_number_to_integer(
                    float(k.number)): v
                for k, v in self.items()
                }
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[repr_items],
            storage_format_args_values=[self._collection],
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes vector from `selection`.

        Returns vector.
        """
        raise NotImplementedError
