# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select


class PrototypeSelectorCallback(AbjadValueObject):
    r'''Prototype selector callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_flatten',
        '_head',
        '_prototype',
        '_tail',
        '_trim',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        prototype=None,
        flatten=None,
        head=None,
        tail=None,
        trim=None,
        ):
        prototype = prototype or ()
        if isinstance(prototype, collections.Sequence):
            prototype = tuple(prototype)
            assert all(isinstance(_, type) for _ in prototype)
        assert isinstance(prototype, (tuple, type))
        self._prototype = prototype
        if flatten is not None:
            flatten = bool(flatten)
        self._flatten = flatten
        if head is not None:
            head = bool(head)
        self._head = head
        if tail is not None:
            tail = bool(tail)
        self._tail = tail
        if trim is not None:
            if isinstance(trim, collections.Sequence):
                trim = tuple(trim)
                assert all(isinstance(x, type) for x in trim)
            assert isinstance(trim, (tuple, type))
        self._trim = trim

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates `argument`.

        Returns tuple of selections.
        '''
        import abjad
        assert isinstance(argument, collections.Iterable), repr(argument)
        result = []
        prototype = self.prototype
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for subexpr in argument:
            subresult = iterate(subexpr).by_class(prototype)
            subresult = select(subresult)
            if subresult:
                if self.trim:
                    subresult = self._trim_subresult(subresult, self.trim)
                if self.head is not None:
                    subresult = self._head_filter_subresult(
                        subresult,
                        self.head,
                        )
                if self.tail is not None:
                    subresult = self._tail_filter_subresult(
                        subresult,
                        self.tail,
                        )
                if self.flatten:
                    result.extend(subresult)
                else:
                    result.append(subresult)
        return tuple(result)

    ### PRIVATE METHODS ###

    @staticmethod
    def _head_filter_subresult(result, head):
        import abjad
        result_ = []
        for item in result:
            if isinstance(item, abjad.Component):
                logical_tie = abjad.inspect(item).get_logical_tie()
                if head == (item is logical_tie.head):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    logical_tie = abjad.inspect(component).get_logical_tie()
                    if head == logical_tie.head:
                        selection.append(item)
                    else:
                        pass
                selection = abjad.select(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return abjad.select(result_)

    @staticmethod
    def _tail_filter_subresult(result, tail):
        import abjad
        result_ = []
        for item in result:
            if isinstance(item, abjad.Component):
                logical_tie = abjad.inspect(item).get_logical_tie()
                if tail == (item is logical_tie.tail):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    logical_tie = abjad.inspect(component).get_logical_tie()
                    if tail == logical_tie.tail:
                        selection.append(item)
                    else:
                        pass
                selection = abjad.select(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return abjad.select(result_)

    @staticmethod
    def _trim_subresult(result, trim):
        import abjad
        result_ = []
        found_good_component = False
        for item in result:
            if isinstance(item, abjad.Component):
                if not isinstance(item, trim):
                    found_good_component = True
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    if not isinstance(component, trim):
                        found_good_component = True
                    if found_good_component:
                        selection.append(component)
                item = abjad.select(selection)
            else:
                raise TypeError(item)
            if found_good_component:
                result_.append(item)
        result__ = []
        found_good_component = False
        for item in reversed(result_):
            if isinstance(item, abjad.Component):
                if not isinstance(item, trim):
                    found_good_component = True
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in reversed(item):
                    if not isinstance(component, trim):
                        found_good_component = True
                    if found_good_component:
                        selection.insert(0, component)
                item = abjad.select(selection)
            else:
                raise TypeError(item)
            if found_good_component:
                result__.insert(0, item)
        assert isinstance(result__, list), repr(result__)
        result = abjad.select(result__)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def flatten(self):
        r'''Is true if selector callback returns a single, rather than nested
        selection. Otherwise false.

        Returns true or false.
        '''
        return self._flatten

    @property
    def head(self):
        r'''Is true when selector returns logical tie heads only.

        Is false when selector returns logical tie nonheads only.

        Is none when selector does not test for logical tie part.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._head

    @property
    def prototype(self):
        r'''Gets prototype selector callback prototype.

        Returns tuple of classes.
        '''
        return self._prototype

    @property
    def tail(self):
        r'''Is true when selector returns logical tie tails only.

        Is false when selector returns logical tie nontails only.

        Is none when selector does not test for logical tie part.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._tail

    @property
    def trim(self):
        r'''Gets trim prototype.

        Returns tuple of classes.
        '''
        return self._trim
