# -*- encoding: utf-8 -*-
import collections
import types
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.iotools.Autoeditor import Autoeditor


class DictionaryAutoeditor(Autoeditor):
    r'''Dictionary editor.

    ::

        >>> session = scoremanager.core.Session()
        >>> autoeditor = scoremanager.iotools.DictionaryAutoeditor(
        ...     session=session,
        ...     )
        >>> dictionary = {'flavor': 'cherry', 'age': 94}
        >>> autoeditor._target = dictionary
        >>> autoeditor
        <DictionaryAutoeditor(target=dict)>

    ::

        >>> autoeditor._run(input_='rm 1 q')

    ::

        >>> autoeditor
        <DictionaryAutoeditor(target=dict)>

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_allow_item_edit',
        '_item_class',
        '_item_creator_class',
        '_item_creator_class_kwargs',
        '_item_editor_class',
        '_item_getter_configuration_method',
        '_asset_identifier',
        '_numbered_section',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        allow_item_edit=True,
        breadcrumb=None,
        session=None, 
        target=None,
        ):
        from scoremanager import iotools
        if target is None:
            target = []
        superclass = super(DictionaryAutoeditor, self)
        superclass.__init__(
            breadcrumb=breadcrumb,
            session=session, 
            target=target,
            )
        self._allow_item_edit = allow_item_edit
        self._item_class = None
        self._item_creator_class = None
        self._item_creator_class_kwargs = {}
        self._item_editor_class = None
        self._item_getter_configuration_method = \
            iotools.UserInputGetter.append_expr
        self._asset_identifier = 'element'
        if hasattr(target, '_item_creator_class'):
            self._item_creator_class = target._item_creator_class
            kwargs = getattr(target, '_item_creator_class_kwargs', None)
            self._item_creator_class_kwargs = kwargs
        elif getattr(target, '_item_callable', None):
            assert self.target._item_callable
            if not isinstance(self.target._item_callable, type):
                return
            self._item_class = self.target._item_callable
            dummy_item = self.target._item_callable()
            helper = stringtools.upper_camel_case_to_space_delimited_lowercase
            asset_identifier = helper(type(dummy_item).__name__)
            if isinstance(dummy_item, datastructuretools.TypedList):
                self._item_creator_class = iotools.CollectionAutoeditor
            else:
                self._item_creator_class = iotools.Autoeditor

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest()

    @property
    def _input_to_method(self):
        result = {
            'add': self.add_items,
            'ren': self.rename_item,
            'rm': self.remove_items,
            'mv': self.move_item,
            }
        return result

    @property
    def _collection(self):
        return self.target

    @property
    def _target_name(self):
        if self.target is not None:
            return 'edit'

    ### PRIVATE METHODS ###

    def _get_item_from_item_number(self, number):
        number = int(number)
        assert isinstance(number, int), repr(number)
        items = list(self._collection.items())
        try:
            item = items[number-1]
        except IndexError:
            pass
        assert isinstance(item, tuple) and len(item) == 2
        return item

    def _dictionary_item_to_menu_summary(self, item):
        key, value = item
        try:
            value = [str(_) for _ in value]
            value = ', '.join(value)
            value = '[{}]'.format(value)
        except TypeError:
            pass
        string = '{}: {}'.format(key, value)
        return string

    def _get_target_summary_lines(self):
        result = []
        for item in self._collection.items():
            result.append(self._dictionary_item_to_menu_summary(item))
        return result

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str), repr(result)
        if result in self._input_to_method:
            self._input_to_method[result]()
        elif mathtools.is_integer_equivalent_expr(result):
            if self.allow_item_edit:
                self.edit_item(result)
        else:
            superclass = super(DictionaryAutoeditor, self)
            superclass._handle_main_menu_result(result)

    def _initialize_target(self):
        if self.target is not None:
            return
        self._target = self._target_class([])

    def _make_command_menu_section(self, menu):
        commands = []
        commands.append(('elements - add', 'add'))
        if 1 < len(self._collection):
            commands.append(('elements - move', 'mv'))
        if 0 < len(self._collection):
            commands.append(('elements - rename', 'ren'))
            commands.append(('elements - remove', 'rm'))
        section = menu.make_command_section(
            commands=commands,
            name='add, move, remove',
            )

    def _make_keyed_attributes_menu_section(self, menu):
        menu_entries = self._make_target_attribute_tokens()
        if menu_entries:
            section = menu.make_keyed_attribute_section(
                menu_entries=menu_entries,
                name='keyed attributes',
                )

    def _make_main_menu(self):
        name = self._spaced_class_name
        menu = self._io_manager._make_menu(name=name)
        self._make_keyed_attributes_menu_section(menu)
        self._make_numbered_entries_menu_section(menu)
        self._make_command_menu_section(menu)
        self._make_done_menu_section(menu)
        return menu

    def _make_numbered_entries_menu_section(self, menu):
        menu_entries = self._get_target_summary_lines()
        if not menu_entries:
            return
        section = menu.make_numbered_section(
            menu_entries=menu_entries,
            name='numbered entries',
            )
        self._numbered_section = section

    ### PUBLIC PROPERTIES ###

    @property
    def allow_item_edit(self):
        r'''Is true when list items can be edited.

        Set to false to allow rearrangement of list items
        without giving user the ability to edit list items.

        Returns boolean.
        '''
        return self._allow_item_edit

    ### PUBLIC METHODS ###

    def add_items(self):
        r'''Adds items to dictionary.

        Returns none.
        '''
        from scoremanager import iotools
        getter = self._io_manager._make_getter()
        getter.append_string('enter dictionary key')
        key = getter._run()
        if self._session.is_backtracking or not key:
            return
        if self._item_creator_class:
            item_creator_class = self._item_creator_class
            if self._item_class:
                target = self._item_class()
            else:
                target = None
            item_creator = item_creator_class(
                session=self._session,
                target=target,
                **self._item_creator_class_kwargs
                )
            result = item_creator._run()
            if self._session.is_backtracking:
                return
            if result == 'done':
                self._session._is_autoadding = False
                return
            result = result or item_creator.target
        elif self._item_getter_configuration_method:
            getter = self._io_manager._make_getter()
            self._item_getter_configuration_method(
                getter,
                self._asset_identifier,
                )
            lines = []
            lines.append('from abjad import *')
            lines.append('evaluated_input = {}')
            getter.prompts[0].setup_statements.extend(lines)
            item_initialization_token = getter._run()
            if self._session.is_backtracking or not item_initialization_token:
                return
            if item_initialization_token == 'done':
                self._session._is_autoadding = False
                return
            print(repr(self._item_class))
            if self._item_class:
                if isinstance(item_initialization_token, str):
                    exec(self._abjad_import_statement)
                    try:
                        expression = eval(item_initialization_token)
                    except (NameError, SyntaxError):
                        expression = item_initialization_token
                else:
                    expression = item_initialization_token
                result = self._item_class(expression)
            else:
                result = item_initialization_token
        else:
            result = self._item_class()
        if result is None:
            result = []
        if type(result) is list:
            items = result
        else:
            items = [result]
        assert isinstance(items, list), repr(items)
        assert len(items) == 1, repr(items)
        value = items[0]
        self._collection[key] = value

    def edit_item(self, number):
        r'''Edits item `number` in dictionary.

        Returns none.
        '''
        from scoremanager import iotools
        item = self._get_item_from_item_number(number)
        if item is None:
            return
        key, value = item
        if self._item_editor_class is not None:
            item_editor_class = self._item_editor_class
            autoeditor = item_editor_class(session=self._session, target=value)
        else:
            autoeditor = self._io_manager._make_autoeditor(target=value)
        autoeditor._run()
        value = autoeditor.target
        self._collection[key] = value

    def move_item(self):
        r'''Moves items in ordered dictionary.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_integer_in_range('old number', 1, len(self._collection))
        getter.append_integer_in_range('new number', 1, len(self._collection))
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        item = self._get_item_from_item_number(old_number)
        assert isinstance(item, tuple) and len(item) == 2
        items = list(self._collection.items())
        del(items[old_index])
        items.insert(new_index, item)
        class_ = type(self._collection)
        dictionary = class_(items)
        self._target = dictionary

    def remove_items(self):
        r'''Removes items from dictionary.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        items_identifier = stringtools.pluralize(self._asset_identifier)
        getter.append_menu_section_range(
            items_identifier, self._numbered_section)
        argument_range = getter._run()
        if self._session.is_backtracking or argument_range is None:
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        keys = list(self._collection.keys())
        keys = sequencetools.retain_elements(keys, indices)
        for key in keys:
            del(self._collection[key])

    def rename_item(self):
        r'''Renames item.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_expr('item to rename')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        if isinstance(result, int):
            item = self._get_item_from_item_number(result)
            if not item:
                return
        elif isinstance(result, str):
            item = self._collection.get(result)
        else:
            return
        if not item:
            return
        key, value = item
        getter = self._io_manager._make_getter()
        getter.append_string('new name')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        new_name = result
        new_item = (new_name, value)
        keys = list(self._collection.keys())
        index = keys.index(key)
        items = list(self._collection.items())
        items[index] = new_item
        class_ = type(self._collection)
        dictionary = class_(items)
        self._target = dictionary