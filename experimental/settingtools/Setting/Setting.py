import abc
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import requesttools
from experimental import selectortools


class Setting(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract setting class from which concrete settings inherit.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute, request, selector, 
        index=None, count=None, reverse=None, rotation=None, callback=None,
        fresh=True, persist=True, truncate=None):
        assert isinstance(attribute, str)
        assert isinstance(request, requesttools.Request), repr(request)
        assert isinstance(selector, (selectortools.TimespanSelector, type(None)))
        assert isinstance(fresh, bool)
        assert isinstance(persist, bool)
        assert isinstance(truncate, (bool, type(None)))
        self._attribute = attribute
        self._request = request
        self._selector = selector
        self._index = index
        self._count = count
        self._reverse = reverse
        self._rotation = rotation
        self._callback = callback
        self._fresh = fresh
        self._persist = persist
        self._truncate = truncate

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Setting attribute.

        Return string.
        '''
        return self._attribute

    @property
    def callback(self):
        '''Setting callback.

        Return callback or none
        '''
        return self._callback

    @property
    def count(self):
        '''Setting count.

        Return integer or none.
        '''
        return self._count

    @property
    def fresh(self):
        '''True when setting results from explicit composer command.
        Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def index(self):
        '''Setting index.

        Return integer or none.
        '''
        return self._index

    @property
    def persist(self):
        '''True when setting should persist.
         
        Return boolean.
        '''
        return self._persist

    @property
    def request(self):
        '''Setting request.

        Return request object.
        '''
        return self._request

    @property
    def reverse(self):
        '''Setting reverse flag.

        Return boolean or none.
        '''
        return self._reverse

    @property
    def rotation(self):
        '''Setting rotation indicator.

        Return integer or none.
        '''
        return self._rotation

    @property
    def selector(self):
        '''Setting selector.

        Return selector or none.
        '''
        return self._selector

    @property
    def truncate(self):
        '''True when setting should truncate.

        Return boolean.
        '''
        return self._truncate
