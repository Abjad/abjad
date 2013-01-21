import abc
import copy
from abjad.tools.abctools import AbjadObject
from experimental.tools.settingtools.AttributeNameEnumeration import AttributeNameEnumeration


class CallbackMixin(AbjadObject):
    '''Callback mixin.

    Base class from which other callback mixin classes inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, callbacks=None):
        from experimental.tools import settingtools
        callbacks = callbacks or []
        self._callbacks = settingtools.CallbackInventory(callbacks)

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('callbacks=CallbackInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _apply_callbacks(self):
        pass

    def _copy_and_append_callback(self, callback):
        result = copy.deepcopy(self)
        result.callbacks.append(callback)
        return result

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty callbacks list.
        '''
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        '''Read-only list of callbacks to be applied 
        to expression during evaluation:

        Return callback inventory of zero or more strings.
        '''
        return self._callbacks


