import collections
import inspect
import itertools
import math
import numbers
import sys
from abjad import enums
from abjad import mathtools
from abjad.system import AbjadValueObject
from abjad.system.Signature import Signature
from .Expression import Expression


class Sequence(AbjadValueObject, collections.Sequence):
    """
    Sequence.

    ..  container:: example

        Initializes sequence:

        ..  container:: example

            >>> abjad.sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            >>> expression = abjad.sequence()
            >>> expression([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes and reverses sequence:

        ..  container:: example

            >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.reverse()
            Sequence([6, 5, 4, 3, 2, 1])

        ..  container:: example expression

            >>> expression = abjad.sequence()
            >>> expression = expression.reverse()
            >>> expression([1, 2, 3, 4, 5, 6])
            Sequence([6, 5, 4, 3, 2, 1])

    ..  container:: example

        Initializes, reverses and flattens sequence:

        ..  container:: example

            >>> sequence = abjad.sequence([1, 2, 3, [4, 5, [6]]])
            >>> sequence = sequence.reverse()
            >>> sequence = sequence.flatten(depth=-1)
            >>> sequence
            Sequence([4, 5, 6, 3, 2, 1])

        ..  container:: example expression

            >>> expression = abjad.sequence()
            >>> expression = expression.reverse()
            >>> expression = expression.flatten(depth=-1)
            >>> expression([1, 2, 3, [4, 5, [6]]])
            Sequence([4, 5, 6, 3, 2, 1])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_equivalence_markup',
        '_expression',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._equivalence_markup = None
        self._expression = None
        items = items or ()
        if not isinstance(items, collections.Iterable):
            items = [items]
        self._items = tuple(items)

    ### SPECIAL METHODS ###

    @Signature(
        markup_maker_callback='_make___add___markup',
        string_template_callback='_make___add___string_template',
        )
    def __add__(self, argument):
        r"""
        Adds ``argument`` to sequence.

        ..  container:: example

            Adds tuple to sequence:

            ..  container:: example

                >>> abjad.sequence([1, 2, 3]) + (4, 5, 6)
                Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression + (4, 5, 6)

                >>> expression([1, 2, 3])
                Sequence([1, 2, 3, 4, 5, 6])

                >>> expression.get_string()
                'J + (4, 5, 6)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                "(4, 5, 6)"
                            }
                        }

        ..  container:: example

            Adds list to sequence:

            ..  container:: example

                >>> abjad.sequence([1, 2, 3]) + [4, 5, 6]
                Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression + [4, 5, 6]

                >>> expression([1, 2, 3])
                Sequence([1, 2, 3, 4, 5, 6])

                >>> expression.get_string()
                'J + [4, 5, 6]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                "[4, 5, 6]"
                            }
                        }

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                >>> sequence_1 = abjad.sequence([1, 2, 3])
                >>> sequence_2 = abjad.sequence([4, 5, 6])
                >>> sequence_1 + sequence_2
                Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                >>> expression_1 = abjad.Expression(name='J')
                >>> expression_1 = expression_1.sequence()
                >>> expression_2 = abjad.Expression(name='K')
                >>> expression_2 = expression_2.sequence()
                >>> expression = expression_1 + expression_2

                >>> expression([1, 2, 3], [4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

                >>> expression.get_string()
                'J + K'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                \bold
                                    K
                            }
                        }

        ..  container:: example

            Reverses result:

            ..  container:: example

                >>> sequence_1 = abjad.sequence([1, 2, 3])
                >>> sequence_2 = abjad.sequence([4, 5, 6])
                >>> sequence = sequence_1 + sequence_2
                >>> sequence.reverse()
                Sequence([6, 5, 4, 3, 2, 1])

            ..  container:: example expression

                >>> expression_1 = abjad.Expression(name='J')
                >>> expression_1 = expression_1.sequence()
                >>> expression_2 = abjad.Expression(name='K')
                >>> expression_2 = expression_2.sequence()
                >>> expression = expression_1 + expression_2
                >>> expression = expression.reverse()

                >>> expression([1, 2, 3], [4, 5, 6])
                Sequence([6, 5, 4, 3, 2, 1])

                >>> expression.get_string()
                'R(J + K)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                R
                                \concat
                                    {
                                        (
                                        \line
                                            {
                                                \bold
                                                    J
                                                +
                                                \bold
                                                    K
                                            }
                                        )
                                    }
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a sequence with items equal to those of
        this sequence.

        ..  container:: example

            Is true when ``argument`` is a sequence with items equal to those
            of this sequence:

            >>> abjad.sequence([1, 2, 3, 4, 5, 6]) == abjad.sequence([1, 2, 3, 4, 5, 6])
            True

        ..  container:: example

            Is false when ``argument`` is not a sequence with items equal to
            those of this sequence:

            >>> abjad.sequence([1, 2, 3, 4, 5, 6]) == ([1, 2, 3, 4, 5, 6])
            False

        Returns true or false.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        """
        Formats sequence.

        ..  container:: example

            Formats sequence:

            >>> abjad.f(abjad.sequence([1, 2, 3, 4, 5, 6]))
            Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            Formats expression:

            >>> expression = abjad.Expression(name='J')
            >>> expression = expression.sequence()
            >>> abjad.f(expression)
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='abjad.utilities.Sequence',
                        is_initializer=True,
                        string_template='{}',
                        ),
                    ],
                name='J',
                proxy_class=abjad.Sequence,
                )

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    @Signature(
        markup_maker_callback='_make___getitem___markup',
        string_template_callback='_make___getitem___string_template',
        )
    def __getitem__(self, argument):
        r"""
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets first item in sequence:

            ..  container:: example

                >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])

                >>> sequence[0]
                1

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression[0]

                >>> expression([1, 2, 3, 4, 5, 6])
                1

                >>> expression.get_string()
                'J[0]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    0
                            }
                        }

        ..  container:: example

            Gets last item in sequence:

            ..  container:: example

                >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])

                >>> sequence[-1]
                6

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression[-1]

                >>> expression([1, 2, 3, 4, 5, 6])
                6

                >>> expression.get_string()
                'J[-1]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    -1
                            }
                        }

        ..  container:: example

            Gets slice from sequence:

            ..  container:: example

                >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])
                >>> sequence = sequence[:3]

                >>> sequence
                Sequence([1, 2, 3])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression[:3]

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3])

                >>> expression.get_string()
                'J[:3]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    [:3]
                            }
                        }

        ..  container:: example

            Gets item in sequence and wraps result in new sequence:

            ..  container:: example

                >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])
                >>> sequence = abjad.sequence(sequence[0])

                >>> sequence
                Sequence([1])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression[0]
                >>> expression = expression.sequence()

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([1])

                >>> expression.get_string()
                'J[0]'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    0
                            }
                        }

        ..  container:: example

            Gets slice from sequence and flattens slice:

            ..  container:: example

                >>> sequence = abjad.sequence([1, 2, [3, [4]], 5])
                >>> sequence = sequence[:-1]
                >>> sequence = sequence.flatten(depth=-1)

                >>> sequence
                Sequence([1, 2, 3, 4])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression[:-1]
                >>> expression = expression.flatten(depth=-1)

                >>> expression([1, 2, [3, [4]], 5])
                Sequence([1, 2, 3, 4])

                >>> expression.get_string()
                'flatten(J[:-1], depth=-1)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \concat
                                    {
                                        \bold
                                            J
                                        \sub
                                            [:-1]
                                    }
                                ", depth=-1)"
                            }
                        }

        Returns item or new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self._items.__getitem__(argument)
        if isinstance(argument, slice):
            return type(self)(result)
        return result

    def __hash__(self):
        """
        Hashes sequence.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __len__(self):
        """
        Gets length of sequence.

        ..  container:: example

            Gets length of sequence:

            >>> len(abjad.sequence([1, 2, 3, 4, 5, 6]))
            6

        ..  container:: example

            Gets length of sequence:

            >>> len(abjad.sequence('text'))
            4

        Returns nonnegative integer.
        """
        return len(self._items)

    @Signature(
        markup_maker_callback='_make___radd___markup',
        string_template_callback='_make___radd___string_template',
        )
    def __radd__(self, argument):
        r"""
        Adds sequence to ``argument``.

        ..  container:: example

            Adds sequence to tuple:

            ..  container:: example

                >>> (1, 2, 3) + abjad.sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='K')
                >>> expression = expression.sequence()
                >>> expression = (1, 2, 3) + expression

                >>> expression([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

                >>> expression.get_string()
                '(1, 2, 3) + K'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                "(1, 2, 3)"
                                +
                                \bold
                                    K
                            }
                        }

        ..  container:: example

            Adds sequence to list:

            ..  container:: example

                >>> [1, 2, 3] + abjad.sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='K')
                >>> expression = expression.sequence()
                >>> expression = [1, 2, 3] + expression

                >>> expression([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

                >>> expression.get_string()
                '[1, 2, 3] + K'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                "[1, 2, 3]"
                                +
                                \bold
                                    K
                            }
                        }

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                >>> abjad.sequence([1, 2, 3]) + abjad.sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                >>> expression_1 = abjad.Expression(name='J')
                >>> expression_1 = expression_1.sequence()
                >>> expression_2 = abjad.Expression(name='K')
                >>> expression_2 = expression_2.sequence()
                >>> expression = expression_1 + expression_2

                >>> expression([1, 2, 3], [4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

                >>> expression.get_string()
                'J + K'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                \bold
                                    K
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        argument = type(self)(items=argument)
        items = argument.items + self.items
        return type(self)(items)

    def __repr__(self):
        """
        Gets interpreter representation of sequence.

        ..  container:: example

            Gets interpreter representation:

            >>> abjad.sequence([99])
            Sequence([99])

        ..  container:: example

            Gets interpreter representation:

            >>> abjad.sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

        Returns string.
        """
        items = ', '.join([repr(_) for _ in self.items])
        string = '{}([{}])'
        string = string.format(type(self).__name__, items)
        if self._expression:
            string = '*' + string
        return string

    ### PRIVATE METHODS ###

    @staticmethod
    def _flatten_at_indices_helper(sequence, indices, classes, depth):
        if classes is None:
            classes = (list, tuple)
        if not isinstance(sequence, classes):
            raise TypeError()
        ltype = type(sequence)
        len_l = len(sequence)
        indices = [_ if 0 <= _ else len_l + _ for _ in indices]
        result = []
        for i, item in enumerate(sequence):
            if i in indices:
                try:
                    flattened = Sequence._flatten_helper(
                        item,
                        classes=classes,
                        depth=depth,
                        )
                    result.extend(flattened)
                except:
                    result.append(item)
            else:
                result.append(item)
        return ltype(result)

    # creates an iterator that can generate a flattened list,
    # descending down into child elements to a depth given in the arguments.
    # note that depth < 0 is effectively equivalent to infinity.
    @staticmethod
    def _flatten_helper(sequence, classes, depth):
        if not isinstance(sequence, classes):
            yield sequence
        elif depth == 0:
            for item in sequence:
                yield item
        else:
            for item in sequence:
                # flatten an iterable by one level
                depth_ = depth - 1
                for item_ in Sequence._flatten_helper(item, classes, depth_):
                    yield item_

    @staticmethod
    def _make_map_markup(markup, operand):
        import abjad
        markup_list = abjad.MarkupList()
        operand_markup = operand.get_markup(name='X')
        markup_list.append(operand_markup)
        markup_list.append('/@')
        markup_list.append(markup)
        markup = markup_list.line()
        return markup

    @staticmethod
    def _make_map_string_template(operand):
        try:
            string_template = '{operand} /@ {{}}'
            operand = operand.get_string(name='X')
            string_template = string_template.format(operand=operand)
            return string_template
        except ValueError:
            return 'unknown string template'

    @staticmethod
    def _make_partition_indicator(
        counts,
        cyclic,
        enchain,
        overhang,
        reversed_,
        ):
        indicator = [str(_) for _ in counts]
        indicator = ', '.join(indicator)
        if cyclic:
            indicator = '<{}>'.format(indicator)
        else:
            indicator = '[{}]'.format(indicator)
        if enchain:
            indicator = 'E' + indicator
        if reversed_:
            indicator = 'R' + indicator
        if overhang is True:
            indicator += '+'
        elif overhang is enums.Exact:
            indicator += '!'
        return indicator

    @staticmethod
    def _make_partition_ratio_indicator(ratio):
        return str(ratio)

    @staticmethod
    def _make_reverse_method_name(recurse=False):
        if recurse:
            return 'R*'
        return 'R'

    @staticmethod
    def _make_split_indicator(weights, cyclic, overhang):
        indicator = [str(_) for _ in weights]
        indicator = ', '.join(indicator)
        if cyclic:
            indicator = '<{}>'.format(indicator)
        else:
            indicator = '[{}]'.format(indicator)
        if overhang:
            indicator += '+'
        return indicator

    @classmethod
    def _partition_sequence_cyclically_by_weights_at_least(
        class_,
        sequence,
        weights,
        overhang=False,
        ):
        l_copy = list(sequence)
        result = []
        current_part = []
        target_weight_index = 0
        len_weights = len(weights)
        while l_copy:
            target_weight = weights[target_weight_index % len_weights]
            item = l_copy.pop(0)
            current_part.append(item)
            if target_weight <= mathtools.weight(current_part):
                result.append(current_part)
                current_part = []
                target_weight_index += 1
        assert not l_copy
        if current_part:
            if overhang:
                result.append(current_part)
        #return result
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_cyclically_by_weights_at_most(
        class_,
        sequence,
        weights,
        overhang=False,
        ):
        result = []
        current_part = []
        current_target_weight_index = 0
        current_target_weight = weights[current_target_weight_index]
        l_copy = list(sequence)
        while l_copy:
            current_target_weight = weights[
                current_target_weight_index % len(weights)]
            item = l_copy.pop(0)
            current_part_weight = mathtools.weight(current_part)
            candidate_part_weight = current_part_weight + mathtools.weight([item])
            if candidate_part_weight < current_target_weight:
                current_part.append(item)
            elif candidate_part_weight == current_target_weight:
                current_part.append(item)
                result.append(current_part)
                current_part = []
                current_target_weight_index += 1
            elif current_target_weight < candidate_part_weight:
                if current_part:
                    l_copy.insert(0, item)
                    result.append(current_part)
                    current_part = []
                    current_target_weight_index += 1
                else:
                    message = 'elements in sequence too big.'
                    raise Exception(message)
            else:
                message = 'candidate and target rates must compare.'
                raise ValueError(message)
        if current_part:
            if overhang:
                result.append(current_part)
        #return result
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_once_by_weights_at_least(
        class_,
        sequence,
        weights,
        overhang=False,
        ):
        result = []
        current_part = []
        l_copy = list(sequence)
        for num_weight, target_weight in enumerate(weights):
            while True:
                try:
                    item = l_copy.pop(0)
                except IndexError:
                    if num_weight + 1 == len(weights):
                        if current_part:
                            result.append(current_part)
                            break
                    message = 'too few elements in sequence.'
                    raise Exception(message)
                current_part.append(item)
                if target_weight <= mathtools.weight(current_part):
                    result.append(current_part)
                    current_part = []
                    break
        if l_copy:
            if overhang:
                result.append(l_copy)
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_once_by_weights_at_most(
        class_,
        sequence,
        weights,
        overhang=False,
        ):
        l_copy = list(sequence)
        result = []
        current_part = []
        for target_weight in weights:
            while True:
                try:
                    item = l_copy.pop(0)
                except IndexError:
                    message = 'too few elements in sequence.'
                    raise Exception(message)
                current_weight = mathtools.weight(current_part)
                candidate_weight = current_weight + mathtools.weight([item])
                if candidate_weight < target_weight:
                    current_part.append(item)
                elif candidate_weight == target_weight:
                    current_part.append(item)
                    result.append(current_part)
                    current_part = []
                    break
                elif target_weight < candidate_weight:
                    if current_part:
                        result.append(current_part)
                        current_part = []
                        l_copy.insert(0, item)
                        break
                    else:
                        message = 'elements in sequence too big.'
                        raise Exception(message)
                else:
                    message = 'candidate and target weights must compare.'
                    raise ValueError(message)
        if overhang:
            left_over = current_part + l_copy
            if left_over:
                result.append(left_over)
        result = [class_(_) for _ in result]
        return class_(items=result)

    def _update_expression(
        self,
        frame,
        evaluation_template=None,
        map_operand=None,
        ):
        callback = Expression._frame_to_callback(
            frame,
            evaluation_template=evaluation_template,
            map_operand=map_operand,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        """
        Gets sequence items.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                >>> abjad.sequence([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

                Initializes items from keyword:

                >>> abjad.sequence([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

            ..  container:: example expression

                Initializes items positionally:

                >>> expression = abjad.sequence()
                >>> expression([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

                Initializes items from keyword:

                >>> expression = abjad.sequence()
                >>> expression([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

        Returns tuple.
        """
        return self._items

    ### PUBLIC METHODS ###

    @Signature()
    def filter(self, predicate=None):
        """
        Filters sequence by ``predicate``.

        ..  container:: example

            By length:

            ..  container:: example

                With lambda:

                >>> items = [[1], [2, 3, [4]], [5], [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.filter(lambda _: len(_) == 1)
                Sequence([[1], [5]])

            ..  container:: example

                With inequality:

                >>> items = [[1], [2, 3, [4]], [5], [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.filter(abjad.LengthInequality('==', 1))
                Sequence([[1], [5]])

            ..  container:: example expression

                As expression:

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> inequality = abjad.LengthInequality('==', 1)
                >>> expression = expression.filter(inequality)

                >>> expression([[1], [2, 3, [4]], [5], [6, 7, [8]]])
                Sequence([[1], [5]])

        ..  container:: example

            By duration:

            ..  container:: example

                With inequality:

                >>> staff = abjad.Staff("c'4. d'8 e'4. f'8 g'2")
                >>> sequence = abjad.sequence(staff)

                >>> sequence.filter(abjad.DurationInequality('==', (1, 8)))
                Sequence([Note("d'8"), Note("f'8")])

            ..  container:: example expression

                As expression:

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> inequality = abjad.DurationInequality('==', (1, 8))
                >>> expression = expression.filter(inequality)

                >>> expression(staff)
                Sequence([Note("d'8"), Note("f'8")])

        ..  todo:: supply with clean string and markup templates.

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if predicate is None:
            return self[:]
        items = []
        for item in self:
            if predicate(item):
                items.append(item)
        return type(self)(items)

    # TODO: remove indices=None parameter
    @Signature()
    def flatten(self, classes=None, depth=1, indices=None):
        r"""
        Flattens sequence.

        ..  container:: example

            Flattens sequence:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.flatten()
                Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.flatten()

                >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

                >>> expression.get_string()
                'flatten(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            Flattens sequence to depth 2:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.flatten(depth=2)
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.flatten(depth=2)

                >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

                >>> expression.get_string()
                'flatten(J, depth=2)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", depth=2)"
                            }
                        }

        ..  container:: example

            Flattens sequence to depth -1:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.flatten(depth=-1)
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.flatten(depth=-1)

                >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

                >>> expression.get_string()
                'flatten(J, depth=-1)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", depth=-1)"
                            }
                        }


        ..  container:: example

            Flattens sequence at indices:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.flatten(indices=[3])
                Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.flatten(indices=[3])

                >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

                >>> expression.get_string()
                'flatten(J, indices=[3])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", indices=[3])"
                            }
                        }

        ..  container:: example

            Flattens sequence at negative indices:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.sequence(items)

                >>> sequence.flatten(indices=[-1])
                Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.flatten(indices=[-1])

                >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

                >>> expression.get_string()
                'flatten(J, indices=[-1])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", indices=[-1])"
                            }
                        }

        ..  container:: example

            Flattens tuples in sequence only:

            ..  container:: example

                >>> items = ['ab', 'cd', ('ef', 'gh'), ('ij', 'kl')]
                >>> sequence = abjad.sequence(items)

                >>> sequence.flatten(classes=(tuple,))
                Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.flatten(classes=(tuple,))

                >>> expression(['ab', 'cd', ('ef', 'gh'), ('ij', 'kl')])
                Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

                >>> expression.get_string()
                'flatten(J, classes=(tuple,))'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", classes=(tuple,))"
                            }
                        }

        Returns new sequence.
        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if classes is None:
            classes = (collections.Sequence, abjad.Selection)
        if Sequence not in classes:
            classes = tuple(list(classes) + [Sequence])
        if indices is None:
            items = self._flatten_helper(self, classes, depth)
            return type(self)(items)
        else:
            return type(self)(
                self._flatten_at_indices_helper(self, indices, classes, depth)
                )

    def group_by(self, predicate=None):
        """
        Groups sequence items by value of items.

        ..  container:: example

            >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]
            >>> sequence = abjad.sequence(items)
            >>> for item in sequence.group_by():
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1, 1])
            Sequence([5])
            Sequence([-5])

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' d' e' e' e'")
            >>> predicate = abjad.PitchSet.from_selection
            >>> for item in abjad.sequence(staff).group_by(predicate):
            ...     item
            ...
            Sequence([Note("c'8")])
            Sequence([Note("d'8"), Note("d'8")])
            Sequence([Note("e'8"), Note("e'8"), Note("e'8")])

        ..  container:: expression

            >>> predicate = abjad.select().leaves().pitch_set()
            >>> expression = abjad.sequence().group_by(predicate)

            >>> staff = abjad.Staff("c'8 d' d' e' e' e'")
            >>> for item in expression(staff):
            ...     item
            ...
            Sequence([Note("c'8")])
            Sequence([Note("d'8"), Note("d'8")])
            Sequence([Note("e'8"), Note("e'8"), Note("e'8")])

        Returns nested sequence.
        """
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='group_by',
                map_operand=predicate,
                )
        items = []
        if predicate is None:
            pairs = itertools.groupby(self, lambda _: _)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        else:
            pairs = itertools.groupby(self, predicate)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        return type(self)(items)

    def is_decreasing(self, strict=True):
        """
        Is true when sequence decreases.

        ..  container:: example

            Is true when sequence is strictly decreasing:

            >>> abjad.sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=True)
            True

            >>> abjad.sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=True)
            False

            >>> abjad.sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=True)
            False

            >>> abjad.Sequence().is_decreasing(strict=True)
            True

        ..  container:: example

            Is true when sequence decreases monotonically:

            >>> abjad.sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=False)
            True

            >>> abjad.sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=False)
            True

            >>> abjad.sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=False)
            True

            >>> abjad.Sequence().is_decreasing(strict=False)
            True

        Returns true or false.
        """
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current < previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current <= previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_increasing(self, strict=True):
        """
        Is true when sequence increases.

        ..  container:: example

            Is true when sequence is strictly increasing:

            >>> abjad.sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=True)
            True

            >>> abjad.sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=True)
            False

            >>> abjad.sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=True)
            False

            >>> abjad.Sequence().is_increasing(strict=True)
            True

        ..  container:: example

            Is true when sequence increases monotonically:

            >>> abjad.sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=False)
            True

            >>> abjad.sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=False)
            True

            >>> abjad.sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=False)
            True

            >>> abjad.Sequence().is_increasing(strict=False)
            True

        Returns true or false.
        """
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous < current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous <= current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_permutation(self, length=None):
        """
        Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            >>> abjad.sequence([4, 5, 0, 3, 2, 1]).is_permutation()
            True

        ..  container:: example

            Is false when sequence is not a permutation:

            >>> abjad.sequence([1, 1, 5, 3, 2, 1]).is_permutation()
            False

        Returns true or false.
        """
        return tuple(sorted(self)) == tuple(range(len(self)))

    def is_repetition_free(self):
        """
        Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence is repetition-free:

            >>> abjad.sequence([0, 1, 2, 6, 7, 8]).is_repetition_free()
            True

        ..  container:: example

            Is true when sequence is empty:

            >>> abjad.Sequence().is_repetition_free()
            True

        ..  container:: example

            Is false when sequence contains repetitions:

            >>> abjad.sequence([0, 1, 2, 2, 7, 8]).is_repetition_free()
            False

        Returns true or false.
        """
        try:
            for left, right in self.nwise():
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    @Signature()
    def join(self):
        r"""
        Join subsequences in ``sequence``.

        ..  container:: example

            >>> items = [(1, 2, 3), (), (4, 5), (), (6,)]
            >>> sequence = abjad.sequence(items)
            >>> sequence
            Sequence([(1, 2, 3), (), (4, 5), (), (6,)])

            >>> sequence.join()
            Sequence([(1, 2, 3, 4, 5, 6)])

        ..  container:: example expression

            >>> expression = abjad.Expression(name='J')
            >>> expression = expression.sequence()
            >>> expression = expression.split([10], cyclic=True)
            >>> expression = expression.join()

            >>> expression(range(1, 11))
            Sequence([Sequence([1, 2, 3, 4, 5, 5, 1, 7, 2, 6, 4, 5, 5])])

            >>> expression.get_string()
            'join(split(J, <10>))'

            >>> markup = expression.get_markup()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \concat
                        {
                            join(
                            \concat
                                {
                                    split(
                                    \bold
                                        J
                                    ", <10>)"
                                }
                            )
                        }
                    }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        cumulative_sum = mathtools.cumulative_sums(self, start=None)[-1]
        return type(self)([cumulative_sum])

    @Signature(
        markup_maker_callback='_make_map_markup',
        string_template_callback='_make_map_string_template',
        )
    def map(self, operand=None):
        r"""
        Maps ``operand`` to sequence items.

        ..  container:: example

            Partitions sequence and sums parts:

            ..  container:: example

                >>> sequence = abjad.sequence(range(1, 10+1))
                >>> sequence = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     )
                >>> sequence = sequence.map(sum)

                >>> sequence
                Sequence([6, 15, 24])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     )
                >>> expression = expression.map(abjad.sequence().sum())

                >>> expression(range(1, 10+1))
                Sequence([6, 15, 24])

                >>> expression.get_string()
                'sum(X) /@ partition(J, <3>)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        sum(
                                        \bold
                                            X
                                        )
                                    }
                                /@
                                \concat
                                    {
                                        partition(
                                        \bold
                                            J
                                        ", <3>)"
                                    }
                            }
                        }

        ..  container:: example

            Maps identity:

            >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.map()
            Sequence([1, 2, 3, 4, 5, 6])

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='map',
                map_operand=operand,
                )
        if operand is not None:
            items = [operand(_) for _ in self]
        else:
            items = self.items[:]
        return type(self)(items)

    def nwise(self, n=2, cyclic=False, wrapped=False):
        """
        Iterates sequence ``n`` at a time.

        ..  container:: example

            Iterates iterable by pairs:

            >>> sequence = abjad.sequence(range(10))
            >>> for item in sequence.nwise():
            ...     item
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])

        ..  container:: example

            Iterates iterable by triples:

            >>> sequence = abjad.sequence(range(10))
            >>> for item in sequence.nwise(n=3):
            ...     item
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])

        ..  container:: example

            Iterates iterable by pairs. Wraps around at end:

            >>> sequence = abjad.sequence(range(10))
            >>> for item in sequence.nwise(n=2, wrapped=True):
            ...     item
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])
            Sequence([9, 0])

        ..  container:: example

            Iterates iterable by triples. Wraps around at end:

            >>> sequence = abjad.sequence(range(10))
            >>> for item in sequence.nwise(n=3, wrapped=True):
            ...     item
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])
            Sequence([8, 9, 0])
            Sequence([9, 0, 1])

        ..  container:: example

            Iterates iterable by pairs. Cycles indefinitely:

            >>> sequence = abjad.sequence(range(10))
            >>> pairs = sequence.nwise(n=2, cyclic=True)
            >>> for _ in range(15):
            ...     next(pairs)
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])
            Sequence([9, 0])
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])

            Returns infinite generator.

        ..  container:: example

            Iterates iterable by triples. Cycles indefinitely:

            >>> sequence = abjad.sequence(range(10))
            >>> triples = sequence.nwise(n=3, cyclic=True)
            >>> for _ in range(15):
            ...     next(triples)
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])
            Sequence([8, 9, 0])
            Sequence([9, 0, 1])
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])

            Returns infinite generator.

        ..  container:: example

            Iterates items one at a time:

            >>> sequence = abjad.sequence(range(10))
            >>> for item in sequence.nwise(n=1):
            ...     item
            ...
            Sequence([0])
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])
            Sequence([5])
            Sequence([6])
            Sequence([7])
            Sequence([8])
            Sequence([9])

        Ignores ``wrapped`` when ``cyclic`` is true.

        Returns generator.
        """
        if cyclic:
            item_buffer = []
            long_enough = False
            for item in self:
                item_buffer.append(item)
                if not long_enough:
                    if n <= len(item_buffer):
                        long_enough = True
                if long_enough:
                    yield type(self)(item_buffer[-n:])
            len_sequence = len(item_buffer)
            current = len_sequence - n + 1
            while True:
                output = []
                for local_offset in range(n):
                    index = (current + local_offset) % len_sequence
                    output.append(item_buffer[index])
                yield type(self)(output)
                current += 1
                current %= len_sequence
        elif wrapped:
            first_n_minus_1 = []
            item_buffer = []
            for item in self:
                item_buffer.append(item)
                if len(item_buffer) == n:
                    yield type(self)(item_buffer)
                    item_buffer.pop(0)
                if len(first_n_minus_1) < n - 1:
                    first_n_minus_1.append(item)
            item_buffer = item_buffer + first_n_minus_1
            if item_buffer:
                for x in range(n - 1):
                    stop = x + n
                    yield type(self)(item_buffer[x:stop])
        else:
            item_buffer = []
            for item in self:
                item_buffer.append(item)
                if len(item_buffer) == n:
                    yield type(self)(item_buffer)
                    item_buffer.pop(0)

    @Signature(
        argument_list_callback='_make_partition_indicator',
        method_name='partition',
        )
    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        enchain=False,
        overhang=False,
        reversed_=False,
        ):
        r"""
        Partitions sequence by ``counts``.

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> sequence = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> sequence
                Sequence([Sequence([0, 1, 2])])

                >>> for part in sequence:
                ...     part
                Sequence([0, 1, 2])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2])

                >>> expression.get_string()
                'partition(J, [3])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [3])"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])

                >>> expression.get_string()
                'partition(J, [4, 3])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [4, 3])"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])

                >>> expression.get_string()
                'partition(J, <3>)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <3>)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])

                >>> expression.get_string()
                'partition(J, <4, 3>)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <4, 3>)"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, [3]+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [3]+)"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, [4, 3]+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [4, 3]+)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])
                Sequence([15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])
                Sequence([15])

                >>> expression.get_string()
                'partition(J, <3>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <3>+)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])
                Sequence([14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])
                Sequence([14, 15])

                >>> expression.get_string()
                'partition(J, <4, 3>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <4, 3>+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([13, 14, 15])

                >>> expression.get_string()
                'partition(J, R[3])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[3])"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, R[4, 3])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[4, 3])"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

                >>> expression.get_string()
                'partition(J, R<3>)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<3>)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, R<4, 3>)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<4, 3>)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                Sequence([13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                Sequence([13, 14, 15])

                >>> expression.get_string()
                'partition(J, R[3]+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[3]+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, R[4, 3]+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[4, 3]+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0])
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0])
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

                >>> expression.get_string()
                'partition(J, R<3>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<3>+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, R<4, 3>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<4, 3>+)"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts and asserts that sequence
            partitions exactly (with no overhang):

            ..  container:: example

                >>> sequence = abjad.sequence(range(10))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 3, 5],
                ...     cyclic=False,
                ...     overhang=abjad.Exact,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8, 9])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [2, 3, 5],
                ...     cyclic=False,
                ...     overhang=abjad.Exact,
                ...     )

                >>> for part in expression(range(10)):
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8, 9])

                >>> expression.get_string()
                'partition(J, [2, 3, 5]!)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [2, 3, 5]!)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts and asserts that sequence
            partitions exactly Exact partitioning means partitioning with no
            overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(10))
                >>> parts = sequence.partition_by_counts(
                ...     [2],
                ...     cyclic=True,
                ...     overhang=abjad.Exact,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])
                Sequence([8, 9])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [2],
                ...     cyclic=True,
                ...     overhang=abjad.Exact,
                ...     )

                >>> for part in expression(range(10)):
                ...     part
                Sequence([0, 1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])
                Sequence([8, 9])

                >>> expression.get_string()
                'partition(J, <2>!)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <2>!)"
                            }
                        }

        ..  container:: example

            Partitions string:

            ..  container:: example

                >>> sequence = abjad.sequence('some text')
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence(['s', 'o', 'm'])
                Sequence(['e', ' ', 't', 'e', 'x', 't'])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in expression('some text'):
                ...     part
                Sequence(['s', 'o', 'm'])
                Sequence(['e', ' ', 't', 'e', 'x', 't'])

                >>> expression.get_string()
                'partition(J, [3]+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [3]+)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically into enchained parts by counts;
            truncates overhang:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=False,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])

                >>> expression.get_string()
                'partition(J, E<2, 6>)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", E<2, 6>)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically into enchained parts by counts;
            returns overhang at end:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])
                Sequence([13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])
                Sequence([13, 14, 15])

                >>> expression.get_string()
                'partition(J, E<2, 6>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", E<2, 6>+)"
                            }
                        }

        ..  container:: example

            REGRESSION: partitions sequence cyclically into enchained parts by
            counts; does not return false 1-element part at end:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [5],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4])
                Sequence([4, 5, 6, 7, 8])
                Sequence([8, 9, 10, 11, 12])
                Sequence([12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts(
                ...     [5],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3, 4])
                Sequence([4, 5, 6, 7, 8])
                Sequence([8, 9, 10, 11, 12])
                Sequence([12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, E<5>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", E<5>+)"
                            }
                        }

        ..  container:: example

            Edge case: empty counts nests sequence and ignores keywords:

            ..  container:: example

                >>> sequence = abjad.sequence(range(16))
                >>> parts = sequence.partition_by_counts([])

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.partition_by_counts([])

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

                >>> expression.get_string()
                'partition(J, [])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [])"
                            }
                        }

        Returns nested sequence.
        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if not all(isinstance(_, int) and 0 <= _ for _ in counts):
            message = 'must be nonnegative integers: {!r}.'
            message = message.format(counts)
            raise Exception(counts)
        sequence = self
        if reversed_:
            sequence = type(self)(reversed(sequence))
        if counts:
            counts = abjad.CyclicTuple(counts)
        else:
            return type(self)([sequence])
        result = []
        i, start = 0, 0
        while True:
            count = counts[i]
            stop = start + count
            part = sequence[start:stop]
            if len(sequence) < stop:
                if enchain and len(part) == 1:
                    part = None
                break
            result.append(part)
            start = stop
            i += 1
            if not cyclic and len(counts) <= i:
                part = sequence[start:]
                break
            if enchain:
                start -= 1
        if part:
            if overhang is True:
                result.append(part)
            elif overhang is enums.Exact and len(part) == count:
                result.append(part)
            elif overhang is enums.Exact and len(part) != count:
                message = 'sequence does not partition exactly.'
                raise Exception(message)
        if reversed_:
            result_ = []
            for part in reversed(result):
                part_type = type(part)
                part = reversed(part)
                part = part_type(part)
                result_.append(part)
            result = result_
        return type(self)(result)

    @Signature(
        argument_list_callback='_make_partition_ratio_indicator',
        method_name='partition',
        )
    def partition_by_ratio_of_lengths(self, ratio):
        r"""
        Partitions sequence by ``ratio`` of lengths.

        ..  container:: example

            Partitions sequence by ``1:1:1`` ratio:

            ..  container:: example

                >>> numbers = abjad.sequence(range(10))
                >>> ratio = abjad.Ratio((1, 1, 1))

                >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6])
                Sequence([7, 8, 9])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> ratio = abjad.Ratio((1, 1, 1))
                >>> expression = expression.partition_by_ratio_of_lengths(ratio)

                >>> for part in expression(range(10)):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6])
                Sequence([7, 8, 9])

                >>> expression.get_string()
                'partition(J, 1:1:1)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", 1:1:1)"
                            }
                        }

        ..  container:: example

            Partitions sequence by ``1:1:2`` ratio:

            ..  container:: example

                >>> numbers = abjad.sequence(range(10))
                >>> ratio = abjad.Ratio((1, 1, 2))

                >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4])
                Sequence([5, 6, 7, 8, 9])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> ratio = abjad.Ratio((1, 1, 2))
                >>> expression = expression.partition_by_ratio_of_lengths(ratio)

                >>> for part in expression(range(10)):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4])
                Sequence([5, 6, 7, 8, 9])

                >>> expression.get_string()
                'partition(J, 1:1:2)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", 1:1:2)"
                            }
                        }

        Returns a sequence of sequences.
        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        ratio = abjad.Ratio(ratio)
        length = len(self)
        counts = mathtools.partition_integer_by_ratio(length, ratio)
        parts = self.partition_by_counts(
            counts,
            cyclic=False,
            overhang=enums.Exact,
            )
        return type(self)(parts)

    def partition_by_ratio_of_weights(self, weights):
        """
        Partitions sequence by ratio of ``weights``.

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> sequence = abjad.sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1, 1, 1])
            Sequence([1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1, 1])
            >>> sequence = abjad.sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([2, 2, 3])
            >>> sequence = abjad.sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([3, 2, 2])
            >>> sequence = abjad.sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1])
            >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
            >>> sequence = abjad.sequence(items)
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1, 1, 1, 2, 2])
            Sequence([2, 2, 2, 2])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
            >>> sequence = abjad.sequence(items)
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1, 1, 1])
            Sequence([2, 2, 2])
            Sequence([2, 2, 2])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> sequence = abjad.sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1, 1])
            >>> sequence = abjad.sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([2, 2, 3])
            >>> sequence = abjad.sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([3, 2, 2])
            >>> sequence = abjad.sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        Rounded weight-proportions of sequences returned equal to rounded
        ``weights``.

        Returns nested sequence.
        """
        import abjad
        list_weight = abjad.mathtools.weight(self)
        weights_parts = abjad.mathtools.partition_integer_by_ratio(
            list_weight,
            weights,
            )
        cumulative_weights = abjad.mathtools.cumulative_sums(
            weights_parts,
            start=None,
            )
        items = []
        sublist = []
        items.append(sublist)
        current_cumulative_weight = cumulative_weights.pop(0)
        for item in self:
            if not isinstance(item, (int, float, abjad.Fraction)):
                message = 'must be number: {!r}.'
                message = message.format(item)
                raise TypeError(message)
            sublist.append(item)
            while current_cumulative_weight <= abjad.mathtools.weight(
                type(self)(items).flatten(depth=-1)):
                try:
                    current_cumulative_weight = cumulative_weights.pop(0)
                    sublist = []
                    items.append(sublist)
                except IndexError:
                    break
        items = [type(self)(_) for _ in items]
        return type(self)(items)

    def partition_by_weights(
        self,
        weights,
        cyclic=False,
        overhang=False,
        allow_part_weights=enums.Exact,
        ):
        r"""
        Partitions sequence by ``weights`` exactly.

        >>> sequence = abjad.sequence([3, 3, 3, 3, 4, 4, 4, 4, 5])

        ..  container:: example

            Partitions sequence once by weights with overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=False,
            ...     ):
            ...     item
            ...
            Sequence([3])
            Sequence([3, 3, 3])

        ..  container:: example

            Partitions sequence once by weights. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=True,
            ...     ):
            ...     item
            ...
            Sequence([3])
            Sequence([3, 3, 3])
            Sequence([4, 4, 4, 4, 5])

        ..  container:: example

            Partitions sequence cyclically by weights:

            >>> for item in sequence.partition_by_weights(
            ...     [12],
            ...     cyclic=True,
            ...     overhang=False,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4, 4, 4])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [12],
            ...     cyclic=True,
            ...     overhang=True,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4, 4, 4])
            Sequence([4, 5])

        >>> sequence = abjad.sequence([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            less than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            less than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just less than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4])
            Sequence([4])
            Sequence([4, 5])
            Sequence([5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just less than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4])
            Sequence([4])
            Sequence([4, 5])
            Sequence([5])

        >>> sequence = abjad.sequence([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence once by weights. Allow part weights to be just
            more than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            more than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just more than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4])
            Sequence([5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just more than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4])
            Sequence([5])
            Sequence([5])

        Returns nested sequence.
        """
        import abjad
        if allow_part_weights is enums.Exact:
            candidate = type(self)(self)
            candidate = candidate.split(
                weights,
                cyclic=cyclic,
                overhang=overhang,
                )
            flattened_candidate = candidate.flatten(depth=-1)
            if flattened_candidate == self[:len(flattened_candidate)]:
                return candidate
            else:
                message = 'can not partition exactly.'
                raise Exception(message)
        elif allow_part_weights is enums.More:
            if not cyclic:
                return Sequence._partition_sequence_once_by_weights_at_least(
                    self,
                    weights,
                    overhang=overhang,
                    )
            else:
                return Sequence._partition_sequence_cyclically_by_weights_at_least(
                    self,
                    weights,
                    overhang=overhang,
                    )
        elif allow_part_weights is enums.Less:
            if not cyclic:
                return Sequence._partition_sequence_once_by_weights_at_most(
                    self,
                    weights,
                    overhang=overhang,
                    )
            else:
                return Sequence._partition_sequence_cyclically_by_weights_at_most(
                    self,
                    weights,
                    overhang=overhang,
                    )
        else:
            message = 'allow_part_weights must be ordinal constant: {!r}.'
            message = message.format(allow_part_weights)
            raise ValueError(message)

    @Signature()
    def permute(self, permutation):
        r"""
        Permutes sequence by ``permutation``.

        ..  container:: example

            >>> sequence = abjad.sequence([10, 11, 12, 13, 14, 15])
            >>> sequence.permute([5, 4, 0, 1, 2, 3])
            Sequence([15, 14, 10, 11, 12, 13])

        ..  container:: example

            >>> sequence = abjad.sequence([11, 12, 13, 14])
            >>> sequence.permute([1, 0, 3, 2])
            Sequence([12, 11, 14, 13])

        ..  container:: example expression

            >>> expression = abjad.Expression(name='J')
            >>> expression = expression.sequence()
            >>> expression = expression.permute([1, 0, 3, 2])

            >>> expression([11, 12, 13, 14])
            Sequence([12, 11, 14, 13])

            >>> expression.get_string()
            'permute(J, [1, 0, 3, 2])'

            >>> markup = expression.get_markup()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \concat
                        {
                            permute(
                            \bold
                                J
                            ", permutation=[1, 0, 3, 2])"
                        }
                    }

        ..  container:: example

            Raises exception when lengths do not match:

            >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.permute([3, 0, 1, 2])
            Traceback (most recent call last):
                ...
            ValueError: permutation Sequence([3, 0, 1, 2]) must match length of sequence Sequence([1, 2, 3, 4, 5, 6]).

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        permutation = type(self)(permutation)
        if not permutation.is_permutation():
            message = 'must be permutation: {!r}.'
            message = message.format(permutation)
            raise ValueError(message)
        if len(permutation) != len(self):
            message = 'permutation {!r} must match length of sequence {!r}.'
            message = message.format(permutation, self)
            raise ValueError(message)
        result = []
        for i, item in enumerate(self):
            j = permutation[i]
            item_ = self[j]
            result.append(item_)
        return type(self)(result)

    # TODO: change input to pattern
    def remove(self, indices=None, period=None):
        """
        Removes items at ``indices``.

        ..  container:: example

            >>> sequence = abjad.sequence(range(15))

        ..  container:: example

            >>> sequence.remove()
            Sequence([])

        ..  container:: example

            >>> sequence.remove(indices=[2, 3])
            Sequence([0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            Removes elements and indices -2 and -3:

            >>> sequence.remove(indices=[-2, -3])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14])

        ..  container:: example

            >>> sequence.remove(indices=[2, 3], period=4)
            Sequence([0, 1, 4, 5, 8, 9, 12, 13])

        ..  container:: example

            >>> sequence.remove(indices=[-2, -3], period=4)
            Sequence([2, 3, 6, 7, 10, 11, 14])

        ..  container:: example

            >>> sequence.remove(indices=[])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            >>> sequence.remove(indices=[97, 98, 99])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            Removes no elements:

            >>> sequence.remove(indices=[-97, -98, -99])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        Returns new sequence.
        """
        items = []
        length = len(self)
        period = period or length
        if indices is None:
            indices = range(length)
        new_indices = []
        for i in indices:
            if length < abs(i):
                continue
            if i < 0:
                i = length + i
            i = i % period
            new_indices.append(i)
        indices = new_indices
        indices.sort()
        for i, item in enumerate(self):
            if i % period not in indices:
                items.append(item)
        return type(self)(items)

    def remove_repeats(self):
        """
        Removes repeats from ``sequence``.

        ..  container:: example

            >>> items = [31, 31, 35, 35, 31, 31, 31, 31, 35]
            >>> sequence = abjad.sequence(items)
            >>> sequence.remove_repeats()
            Sequence([31, 35, 31, 35])

        Returns new sequence.
        """
        items = [self[0]]
        for item in self[1:]:
            if item != items[-1]:
                items.append(item)
        return type(self)(items)

    @Signature()
    def repeat(self, n=1):
        r"""
        Repeats sequence.

        ..  container:: example

            ..  container:: example

                >>> abjad.sequence([1, 2, 3]).repeat(n=0)
                Sequence([])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.repeat(n=0)

                >>> expression([1, 2, 3])
                Sequence([])

                >>> expression.get_string()
                'repeat(J, n=0)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                repeat(
                                \bold
                                    J
                                ", n=0)"
                            }
                        }

        ..  container:: example

            ..  container:: example

                >>> abjad.sequence([1, 2, 3]).repeat(n=1)
                Sequence([Sequence([1, 2, 3])])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.repeat(n=1)

                >>> expression([1, 2, 3])
                Sequence([Sequence([1, 2, 3])])

                >>> expression.get_string()
                'repeat(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                repeat(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            ..  container:: example

                >>> abjad.sequence([1, 2, 3]).repeat(n=2)
                Sequence([Sequence([1, 2, 3]), Sequence([1, 2, 3])])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.repeat(n=2)

                >>> expression([1, 2, 3])
                Sequence([Sequence([1, 2, 3]), Sequence([1, 2, 3])])

                >>> expression.get_string()
                'repeat(J, n=2)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                repeat(
                                \bold
                                    J
                                ", n=2)"
                            }
                        }

        Returns sequence of sequences.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = []
        for i in range(n):
            items.append(self[:])
        return type(self)(items)

    def repeat_to_length(self, length=None, start=0):
        """
        Repeats sequence to ``length``.

        ..  container:: example

            Repeats list to length 11:

            >>> abjad.sequence(range(5)).repeat_to_length(11)
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0])

        ..  container:: example

            >>> abjad.sequence(range(5)).repeat_to_length(11, start=2)
            Sequence([2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2])

        ..  container:: example

            >>> sequence = abjad.sequence([0, -1, -2, -3, -4])
            >>> sequence.repeat_to_length(11)
            Sequence([0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0])

        ..  container:: example

            >>> sequence.repeat_to_length(0)
            Sequence([])

        ..  container:: example

            >>> abjad.sequence([1, 2, 3]).repeat_to_length(10, start=100)
            Sequence([2, 3, 1, 2, 3, 1, 2, 3, 1, 2])

        Returns new sequence.
        """
        assert mathtools.is_nonnegative_integer(length), repr(length)
        assert len(self), repr(self)
        items = []
        start %= len(self)
        stop_index = start + length
        repetitions = int(math.ceil(float(stop_index) / len(self)))
        for i in range(repetitions):
            for item in self:
                items.append(item)
        return type(self)(items[start:stop_index])

    def repeat_to_weight(self, weight, allow_total=enums.Exact):
        """
        Repeats sequence to ``weight``.

        ..  container:: example

            Repeats sequence to weight of 23 exactly:

            >>> abjad.sequence([5, -5, -5]).repeat_to_weight(23)
            Sequence([5, -5, -5, 5, -3])

        ..  container:: example

            Repeats sequence to weight of 23 more:

            >>> sequence = abjad.sequence([5, -5, -5])
            >>> sequence.repeat_to_weight(23, allow_total=abjad.More)
            Sequence([5, -5, -5, 5, -5])

        ..  container:: example

            Repeats sequence to weight of 23 or less:

            >>> sequence = abjad.sequence([5, -5, -5])
            >>> sequence.repeat_to_weight(23, allow_total=abjad.Less)
            Sequence([5, -5, -5, 5])

        ..  container:: example

            >>> items = [abjad.NonreducedFraction(3, 16)]
            >>> sequence = abjad.sequence(items)
            >>> weight = abjad.NonreducedFraction(5, 4)
            >>> sequence = sequence.repeat_to_weight(weight)
            >>> sum(sequence)
            NonreducedFraction(20, 16)

            >>> [_.pair for _ in sequence]
            [(3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]

        Returns new sequence.
        """
        import abjad
        assert isinstance(weight, numbers.Number), repr(weight)
        assert 0 <= weight
        if allow_total is enums.Exact:
            sequence_weight = abjad.mathtools.weight(self)
            complete_repetitions = int(
                math.ceil(float(weight) / float(sequence_weight))
                )
            items = list(self)
            items = complete_repetitions * items
            overage = complete_repetitions * sequence_weight - weight
            for item in reversed(items):
                if 0 < overage:
                    element_weight = abs(item)
                    candidate_overage = overage - element_weight
                    if 0 <= candidate_overage:
                        overage = candidate_overage
                        items.pop()
                    else:
                        absolute_amount_to_keep = element_weight - overage
                        assert 0 < absolute_amount_to_keep
                        signed_amount_to_keep = absolute_amount_to_keep
                        signed_amount_to_keep *= abjad.mathtools.sign(item)
                        items.pop()
                        items.append(signed_amount_to_keep)
                        break
                else:
                    break
        elif allow_total is enums.Less:
            items = [self[0]]
            i = 1
            while abjad.mathtools.weight(items) < weight:
                items.append(self[i % len(self)])
                i += 1
            if weight < abjad.mathtools.weight(items):
                items = items[:-1]
            return type(self)(items)
        elif allow_total is enums.More:
            items = [self[0]]
            i = 1
            while abjad.mathtools.weight(items) < weight:
                items.append(self[i % len(self)])
                i += 1
            return type(self)(items)
        else:
            message = 'is not an ordinal value constant: {!r}.'
            message = message.format(allow_total)
            raise ValueError(message)
        return type(self)(items=items)

    def replace(self, indices, new_material):
        """
        Replaces items at ``indices`` with ``new_material``.

        ..  container:: example

            Replaces items at indices 0, 2, 4, 6:

            >>> sequence = abjad.sequence(range(16))
            >>> sequence.replace(
            ...     ([0], 2),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            Sequence(['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Replaces elements at indices 0, 1, 8, 13:

            >>> sequence = abjad.sequence(range(16))
            >>> sequence.replace(
            ...     ([0, 1, 8, 13], None),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            Sequence(['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15])

        ..  container:: example

            Replaces every item at even index:

            >>> sequence = abjad.sequence(range(16))
            >>> sequence.replace(
            ...     ([0], 2),
            ...     (['*'], 1),
            ...     )
            Sequence(['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15])

        ..  container:: example

            Replaces every element at an index congruent to 0 (mod 6) with
            ``'A'``; replaces every element at an index congruent to 2 (mod 6)
            with ``'B'``:

            >>> sequence = abjad.sequence(range(16))
            >>> sequence.replace(
            ...     ([0], 2),
            ...     (['A', 'B'], 3),
            ...     )
            Sequence(['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15])

        Returns new sequence.
        """
        assert isinstance(indices, collections.Iterable)
        assert len(indices) == 2
        index_values, index_period = indices
        assert isinstance(index_values, collections.Iterable)
        index_values = list(index_values)
        assert isinstance(index_period, (int, type(None)))
        assert isinstance(new_material, collections.Iterable)
        assert len(new_material) == 2
        material_values, material_period = new_material
        assert isinstance(material_values, collections.Iterable)
        material_values = list(material_values)
        assert isinstance(material_period, (int, type(None)))
        try:
            maxint = sys.maxint
        except AttributeError:
            maxint = sys.maxsize
        if index_period is None:
            index_period = maxint
        if material_period is None:
            material_period = maxint
        items = []
        material_index = 0
        for index, item in enumerate(self):
            if index % index_period in index_values:
                try:
                    cyclic_material_index = material_index % material_period
                    material_value = material_values[cyclic_material_index]
                    items.append(material_value)
                except IndexError:
                    items.append(item)
                material_index += 1
            else:
                items.append(item)
        return type(self)(items=items)

    # TODO: remove in favor of self.retain_pattern()
    def retain(self, indices=None, period=None):
        """
        Retains items at ``indices``.

        ..  container:: example

            >>> sequence = abjad.sequence(range(10))
            >>> sequence.retain()
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        ..  container:: example

            >>> sequence.retain(indices=[2, 3])
            Sequence([2, 3])

        ..  container:: example

            >>> sequence.retain(indices=[-2, -3])
            Sequence([7, 8])

        ..  container:: example

            >>> sequence.retain(indices=[2, 3], period=4)
            Sequence([2, 3, 6, 7])

        ..  container:: example

            >>> sequence.retain(indices=[-2, -3], period=4)
            Sequence([0, 3, 4, 7, 8])

        ..  container:: example

            >>> sequence.retain(indices=[])
            Sequence([])

        ..  container:: example

            >>> sequence.retain(indices=[97, 98, 99])
            Sequence([])

        ..  container:: example

            >>> sequence.retain(indices=[-97, -98, -99])
            Sequence([])

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        length = len(self)
        period = period or length
        if indices is None:
            indices = range(length)
        new_indices = []
        for i in indices:
            if length < abs(i):
                continue
            if i < 0:
                i = length + i
            i = i % period
            new_indices.append(i)
        indices = new_indices
        indices.sort()
        items = []
        for i, item in enumerate(self):
            if i % period in indices:
                items.append(item)
        return type(self)(items=items)

    def retain_pattern(self, pattern):
        """
        Retains items at indices matching ``pattern``.

        ..  container:: example

            >>> sequence = abjad.sequence(range(10))
            >>> sequence.retain_pattern(abjad.index_all())
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([2, 3]))
            Sequence([2, 3])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-2, -3]))
            Sequence([7, 8])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([2, 3], 4))
            Sequence([2, 3, 6, 7])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-2, -3], 4))
            Sequence([0, 3, 4, 7, 8])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([97, 98, 99]))
            Sequence([])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-97, -98, -99]))
            Sequence([])

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        length = len(self)
        items = []
        for i, item in enumerate(self):
            if pattern.matches_index(i, length):
                items.append(item)
        return type(self)(items=items)

    @Signature(
        is_operator=True,
        method_name_callback='_make_reverse_method_name',
        )
    def reverse(self, recurse=False):
        r"""
        Reverses sequence.

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                >>> sequence = abjad.sequence([[1, 2], 3, [4, 5]])

                >>> sequence.reverse()
                Sequence([[4, 5], 3, [1, 2]])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.reverse()

                >>> expression([[1, 2], 3, [4, 5]])
                Sequence([[4, 5], 3, [1, 2]])

                >>> expression.get_string()
                'R(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                R
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Reverses recursively:

            ..  container:: example

                >>> segment_1 = abjad.PitchClassSegment([1, 2])
                >>> pitch = abjad.NumberedPitch(3)
                >>> segment_2 = abjad.PitchClassSegment([4, 5])
                >>> sequence = abjad.sequence([segment_1, pitch, segment_2])

                >>> for item in sequence.reverse(recurse=True):
                ...     item
                ...
                PitchClassSegment([5, 4])
                NumberedPitch(3)
                PitchClassSegment([2, 1])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.reverse(recurse=True)

                >>> for item in expression([segment_1, pitch, segment_2]):
                ...     item
                ...
                PitchClassSegment([5, 4])
                NumberedPitch(3)
                PitchClassSegment([2, 1])

                >>> expression.get_string()
                'R*(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                R*
                                \bold
                                    J
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if not recurse:
            return type(self)(items=reversed(self))

        def _reverse_helper(item):
            if isinstance(item, collections.Iterable):
                subitems_ = [_reverse_helper(_) for _ in reversed(item)]
                return type(item)(subitems_)
            else:
                return item
        items = _reverse_helper(self.items)
        return type(self)(items=items)

    @Signature(
        is_operator=True,
        method_name='r',
        subscript='n',
        )
    def rotate(self, n=0):
        r"""
        Rotates sequence by index ``n``.

        ..  container:: example

            Rotates sequence to the right:

            ..  container:: example

                >>> sequence = abjad.sequence(range(10))

                >>> sequence.rotate(n=4)
                Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.rotate(n=4)

                >>> expression(range(10))
                Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

                >>> expression.get_string()
                'r4(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    4
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Rotates sequence to the left:

            ..  container:: example

                >>> sequence = abjad.sequence(range(10))

                >>> sequence.rotate(n=-3)
                Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.rotate(n=-3)

                >>> expression(range(10))
                Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

                >>> expression.get_string()
                'r-3(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    -3
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Rotates sequence neither to the right nor the left:

            ..  container:: example

                >>> sequence = abjad.sequence(range(10))

                >>> sequence.rotate(n=0)
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.rotate(n=0)

                >>> expression(range(10))
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

                >>> expression.get_string()
                'r0(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    0
                                \bold
                                    J
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        n = n or 0
        items = []
        if len(self):
            n = n % len(self)
            for item in self[-n:len(self)] + self[:-n]:
                items.append(item)
        return type(self)(items=items)

    def select(self):
        """
        Selects sequence.

        Returns selection.
        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return abjad.select(self)

    def sort(self, key=None, reverse=False):
        """
        Sorts sequence.

        ..  container:: example

            >>> sequence = abjad.sequence([3, 2, 5, 4, 1, 6])
            >>> sequence.sort()
            Sequence([1, 2, 3, 4, 5, 6])

            >>> sequence
            Sequence([3, 2, 5, 4, 1, 6])

        Returns new sequence.
        """
        items = list(self)
        items.sort(key=key, reverse=reverse)
        return type(self)(items=items)

    @Signature(
        argument_list_callback='_make_split_indicator',
        )
    def split(self, weights, cyclic=False, overhang=False):
        r"""
        Splits sequence by ``weights``.

        ..  container:: example

            Splits sequence cyclically by weights with overhang:

            ..  container:: example

                >>> sequence = abjad.sequence([10, -10, 10, -10])

                >>> for part in sequence.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     ):
                ...     part
                ...
                Sequence([3])
                Sequence([7, -8])
                Sequence([-2, 1])
                Sequence([3])
                Sequence([6, -9])
                Sequence([-1])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in expression([10, -10, 10, -10]):
                ...     part
                ...
                Sequence([3])
                Sequence([7, -8])
                Sequence([-2, 1])
                Sequence([3])
                Sequence([6, -9])
                Sequence([-1])

                >>> expression.get_string()
                'split(J, <3, 15, 3>+)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                split(
                                \bold
                                    J
                                ", <3, 15, 3>+)"
                            }
                        }

        ..  container:: example

            Splits sequence once by weights with overhang:

            >>> for part in sequence.split(
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=True,
            ...     ):
            ...     part
            ...
            Sequence([3])
            Sequence([7, -8])
            Sequence([-2, 1])
            Sequence([9, -10])

        ..  container:: example

            Splits sequence once by weights without overhang:

            >>> for part in sequence.split(
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=False,
            ...     ):
            ...     part
            ...
            Sequence([3])
            Sequence([7, -8])
            Sequence([-2, 1])

        Returns new sequence.
        """
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        current_index = 0
        current_piece = []
        if cyclic:
            weights = Sequence(weights).repeat_to_weight(
                mathtools.weight(self),
                allow_total=enums.Less,
                )
        for weight in weights:
            current_piece_weight = mathtools.weight(current_piece)
            while current_piece_weight < weight:
                current_piece.append(self[current_index])
                current_index += 1
                current_piece_weight = mathtools.weight(current_piece)
            if current_piece_weight == weight:
                current_piece = type(self)(current_piece)
                result.append(current_piece)
                current_piece = []
            elif weight < current_piece_weight:
                overage = current_piece_weight - weight
                current_last_element = current_piece.pop(-1)
                needed = abs(current_last_element) - overage
                needed *= mathtools.sign(current_last_element)
                current_piece.append(needed)
                current_piece = type(self)(current_piece)
                result.append(current_piece)
                overage *= mathtools.sign(current_last_element)
                current_piece = [overage]
        if overhang:
            last_piece = current_piece
            last_piece.extend(self[current_index:])
            if last_piece:
                last_piece = type(self)(last_piece)
                result.append(last_piece)
        return type(self)(items=result)

    @Signature()
    def sum(self):
        r"""
        Sums sequence.

        ..  container:: example

            Sums sequence of positive numbers:

            ..  container:: example

                >>> sequence = abjad.sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

                >>> sequence.sum()
                55

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.sum()

                >>> expression([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                55

                >>> expression.get_string()
                'sum(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                sum(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            Sum sequence of numbers with mixed signs:

            ..  container:: example

                >>> sequence = abjad.sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

                >>> sequence.sum()
                5

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.sum()

                >>> expression([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
                5

                >>> expression.get_string()
                'sum(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                sum(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            Sums sequence and wraps result in new sequence:

            ..  container:: example

                >>> sequence = abjad.sequence(range(1, 10+1))
                >>> result = sequence.sum()
                >>> sequence = abjad.sequence(result)

                >>> sequence
                Sequence([55])

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.sum()
                >>> expression = expression.sequence()

                >>> expression(range(1, 10+1))
                Sequence([55])

                >>> expression.get_string()
                'sum(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                sum(
                                \bold
                                    J
                                )
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if len(self) == 0:
            return 0
        result = self[0]
        for item in self[1:]:
            result += item
        return result

    def sum_by_sign(self, sign=(-1, 0, 1)):
        """
        Sums consecutive sequence items by ``sign``.

        >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]
        >>> sequence = abjad.sequence(items)

        ..  container:: example

            >>> sequence.sum_by_sign()
            Sequence([0, -2, 5, -5, 8, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1])
            Sequence([0, 0, -2, 2, 3, -5, 1, 2, 5, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[0])
            Sequence([0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[1])
            Sequence([0, 0, -1, -1, 5, -5, 8, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 0])
            Sequence([0, -2, 2, 3, -5, 1, 2, 5, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 1])
            Sequence([0, 0, -2, 5, -5, 8, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[0, 1])
            Sequence([0, -1, -1, 5, -5, 8, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 0, 1])
            Sequence([0, -2, 5, -5, 8, -11])

        Sumsn consecutive negative elements when ``-1`` in ``sign``.

        Sums consecutive zero-valued elements when ``0`` in ``sign``.

        Sums consecutive positive elements when ``1`` in ``sign``.

        Returns new sequence.
        """
        items = []
        generator = itertools.groupby(self, mathtools.sign)
        for current_sign, group in generator:
            if current_sign in sign:
                items.append(sum(group))
            else:
                for item in group:
                    items.append(item)
        return type(self)(items=items)

    def truncate(self, sum_=None, weight=None):
        """
        Truncates sequence.

        >>> sequence = abjad.sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

        ..  container:: example

            Truncates sequence to weights ranging from 1 to 10:

            >>> for weight in range(1, 11):
            ...     result = sequence.truncate(weight=weight)
            ...     print(weight, result)
            ...
            1 Sequence([-1])
            2 Sequence([-1, 1])
            3 Sequence([-1, 2])
            4 Sequence([-1, 2, -1])
            5 Sequence([-1, 2, -2])
            6 Sequence([-1, 2, -3])
            7 Sequence([-1, 2, -3, 1])
            8 Sequence([-1, 2, -3, 2])
            9 Sequence([-1, 2, -3, 3])
            10 Sequence([-1, 2, -3, 4])

        ..  container:: example

            Truncates sequence to sums ranging from 1 to 10:

            >>> for sum_ in range(1, 11):
            ...     result = sequence.truncate(sum_=sum_)
            ...     print(sum_, result)
            ...
            1 Sequence([-1, 2])
            2 Sequence([-1, 2, -3, 4])
            3 Sequence([-1, 2, -3, 4, -5, 6])
            4 Sequence([-1, 2, -3, 4, -5, 6, -7, 8])
            5 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            6 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            7 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            8 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            9 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            10 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

        ..  container:: example

            Truncates sequence to zero weight:

            >>> sequence.truncate(weight=0)
            Sequence([])

        ..  container:: example

            Truncates sequence to zero sum:

            >>> sequence.truncate(sum_=0)
            Sequence([])

        Ignores ``sum`` when ``weight`` and ``sum`` are both set.

        Raises value error on negative ``sum``.

        Returns new sequence.
        """
        if weight is not None:
            assert 0 <= weight, repr(weight)
            items = []
            if 0 < weight:
                total = 0
                for item in self:
                    total += abs(item)
                    if total < weight:
                        items.append(item)
                    else:
                        sign = mathtools.sign(item)
                        trimmed_part = weight - mathtools.weight(items)
                        trimmed_part *= sign
                        items.append(trimmed_part)
                        break
        elif sum_ is not None:
            assert 0 <= sum_, repr(sum_)
            items = []
            if 0 < sum_:
                total = 0
                for item in self:
                    total += item
                    if total < sum_:
                        items.append(item)
                    else:
                        items.append(sum_ - sum(items))
                        break
        return type(self)(items=items)

    def weight(self):
        """
        Gets weight.

        ..  container:: example

            >>> abjad.sequence([]).weight()
            0

            >>> abjad.sequence([1]).weight()
            1

            >>> abjad.sequence([1, 2, 3]).weight()
            6

            >>> abjad.sequence([1, 2, -3]).weight()
            6

            >>> abjad.sequence([-1, -2, -3]).weight()
            6

            >>> sequence = abjad.sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            >>> sequence.weight()
            55

        ..  container:: example

            >>> abjad.sequence([[1, -7, -7], [1, -8 -8]]).weight()
            32

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        weights = []
        for item in self:
            if hasattr(item, 'weight'):
                weights.append(item.weight())
            elif isinstance(item, collections.Iterable):
                item = Sequence(item)
                weights.append(item.weight())
            else:
                weights.append(abs(item))
        return sum(weights)

    def zip(self, cyclic=False, truncate=True):
        """
        Zips sequences in sequence.

        ..  container:: example

            Zips cyclically:

            >>> sequence = abjad.sequence([[1, 2, 3], ['a', 'b']])
            >>> for item in sequence.zip(cyclic=True):
            ...     item
            ...
            Sequence([1, 'a'])
            Sequence([2, 'b'])
            Sequence([3, 'a'])

            >>> items = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
            >>> sequence = abjad.sequence(items)
            >>> for item in sequence.zip(cyclic=True):
            ...     item
            ...
            Sequence([10, 20, 30])
            Sequence([11, 21, 31])
            Sequence([12, 20, 32])
            Sequence([10, 21, 33])

        ..  container:: example

            Zips without truncation:

            >>> items = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
            >>> sequence = abjad.sequence(items)
            >>> for item in sequence.zip(truncate=False):
            ...     item
            ...
            Sequence([1, 11, 21])
            Sequence([2, 12, 22])
            Sequence([3, 13, 23])
            Sequence([4])

        ..  container:: example

            Zips strictly:

            >>> items = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
            >>> for item in abjad.sequence(items).zip():
            ...     item
            ...
            Sequence([1, 11, 21])
            Sequence([2, 12, 22])
            Sequence([3, 13, 23])

        Returns nested sequence.
        """
        for item in self:
            if not isinstance(item, collections.Iterable):
                message = 'must by iterable: {!r}.'
                message = message.format(item)
                raise Exception(message)
        items = []
        if cyclic:
            if not min(len(_) for _ in self):
                return type(self)(items=items)
            maximum_length = max([len(_) for _ in self])
            for i in range(maximum_length):
                part = []
                for item in self:
                    index = i % len(item)
                    element = item[index]
                    part.append(element)
                part = type(self)(items=part)
                items.append(part)
        elif not truncate:
            maximum_length = max([len(_) for _ in self])
            for i in range(maximum_length):
                part = []
                for item in self:
                    try:
                        part.append(item[i])
                    except IndexError:
                        pass
                part = type(self)(items=part)
                items.append(part)
        elif truncate:
            for item in zip(*self):
                item = type(self)(items=item)
                items.append(item)
        return type(self)(items=items)
