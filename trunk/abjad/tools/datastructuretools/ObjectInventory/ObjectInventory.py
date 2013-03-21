from abjad.tools.abctools.AbjadObject import AbjadObject
import types


class ObjectInventory(list, AbjadObject):
    '''.. versionadded:: 2.8

    Ordered collection of custom objects.

    Object inventories extend ``append()``, ``extend()`` and
    ``__contains__()`` and allow token input.

    Object inventories inherit from list and are mutable.

    This class is an abstract base class that can not instantiate
    and should be subclassed.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, name=None):
        list.__init__(self)
        if isinstance(tokens, type(self)):
            for token in tokens:
                self.append(self._item_callable(token))
            self.name = tokens.name or name
        else:
            tokens = tokens or []
            items = []
            for token in tokens:
                items.append(self._item_callable(token))
            self.extend(items)
            self.name = name

    ### SPECIAL METHODS ###

    def __contains__(self, token):
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return list.__contains__(self, item)

    def __repr__(self):
        return AbjadObject.__repr__(self)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return lambda x: x

    @property
    def _keyword_argument_names(self):
        result = AbjadObject._keyword_argument_names.fget(self)
        result = list(result)
        if 'tokens' in result:
            result.remove('tokens')
        result = tuple(result)
        return result

    @property
    def _positional_argument_repr_string(self):
        positional_argument_repr_string = [repr(x) for x in self._positional_argument_values]
        positional_argument_repr_string = ', '.join(positional_argument_repr_string)
        positional_argument_repr_string = '[{}]'.format(positional_argument_repr_string)
        return positional_argument_repr_string

    @property
    def _positional_argument_values(self):
        return tuple(self)

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def name():
        def fget(self):
            '''Read / write name of inventory.
            '''
            return self._name
        def fset(self, _name):
            assert isinstance(_name, (str, type(None)))
            self._name = _name
        return property(**locals())

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        result = []
        if is_indented:
            prefix = '\t'
        else:
            prefix = ''
        positionals = self._get_tools_package_qualified_positional_argument_repr_pieces(is_indented=is_indented)
        keywords = self._get_tools_package_qualified_keyword_argument_repr_pieces(is_indented=is_indented)
        positionals, keywords = list(positionals), list(keywords)
        if not positionals and not keywords:
            result.append('{}([])'.format(self._tools_package_qualified_class_name))
        elif not positionals and keywords:
            result.append('{}([],'.format(self._tools_package_qualified_class_name))
            keywords[-1] = keywords[-1].rstrip(' ')
            keywords[-1] = keywords[-1].rstrip(',')
            result.extend(keywords)
            result.append('{})'.format(prefix))
        elif positionals and not keywords:
            result.append('{}(['.format(self._tools_package_qualified_class_name))
            positionals[-1] = positionals[-1].rstrip(' ')
            positionals[-1] = positionals[-1].rstrip(',')
            result.extend(positionals)
            result.append('{}])'.format(prefix))
        elif positionals and keywords:
            result.append('{}(['.format(self._tools_package_qualified_class_name))
            positionals[-1] = positionals[-1].rstrip(' ')
            positionals[-1] = positionals[-1].rstrip(',')
            result.extend(positionals)
            result.append('{}],'.format(prefix))
            keywords[-1] = keywords[-1].rstrip(' ')
            keywords[-1] = keywords[-1].rstrip(',')
            result.extend(keywords)
            result.append('{})'.format(prefix))
        else:
            raise ValueError("how'd we get here?")
        return result

    ### PUBLIC METHODS ###

    def append(self, token):
        '''Change `token` to item and append.
        '''
        item = self._item_callable(token)
        list.append(self, item)

    def extend(self, tokens):
        '''Change `tokens` to items and extend.
        '''
        for token in tokens:
            self.append(token)
