import types
from experimental.tools.scoremanagertools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scoremanagertools.selectors.Selector import Selector
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class AttributeDetail(object):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        is_null = False
        if len(args) == 0:
            name = retrievable_name = space_delimited_lowercase_name = \
                menu_key = editor_callable = is_positional = None
            is_null = True
        elif len(args) == 3:
            name, menu_key, editor_callable = args
            space_delimited_lowercase_name = None
            is_positional = True
            retrievable_name = name
        elif len(args) == 4:
            name, space_delimited_lowercase_name, menu_key, editor_callable = args
            is_positional = True
            retrievable_name = name
        elif len(args) == 5:
            name, space_delimited_lowercase_name, menu_key, editor_callable, is_positional = args
            retrievable_name = name
        elif len(args) == 6:
            name, retrievable_name, space_delimited_lowercase_name, \
                menu_key, editor_callable, is_positional = args
        else:
            raise ValueError('can not parse attribute detail {!r}.'.format(args))
        if not space_delimited_lowercase_name and name:
            space_delimited_lowercase_name = name.replace('_', ' ')
        self.name = name
        self.retrievable_name = retrievable_name
        self.space_delimited_lowercase_name = space_delimited_lowercase_name
        self.menu_key = menu_key
        self.editor_callable = editor_callable
        self.is_positional = is_positional
        self.allow_none = kwargs.get('allow_none', True)
        self.is_null = is_null

    ### SPECIAL METHODS ###

    def __repr__(self):
        parts = [
            repr(self.space_delimited_lowercase_name),
            repr(self.menu_key),
            self.editor_callable.__name__]
        if not self.allow_none:
            parts.append('allow_none=False')
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC METHODS ###

    def get_editor(self, space_delimited_attribute_name, existing_value, session=None, **kwargs):
        if isinstance(self.editor_callable, types.FunctionType):
            editor = self.editor_callable(space_delimited_attribute_name,
                session=session, existing_value=existing_value, allow_none=self.allow_none, **kwargs)
        elif issubclass(self.editor_callable, InteractiveEditor):
            editor = self.editor_callable(session=session, target=existing_value, **kwargs)
        elif issubclass(self.editor_callable, Selector):
            editor = self.editor_callable(session=session, **kwargs)
        elif issubclass(self.editor_callable, Wizard):
            editor = self.editor_callable(session=session, target=existing_value, **kwargs)
        else:
            raise ValueError('what is {!r}?'.format(self.editor_callable))
        return editor
