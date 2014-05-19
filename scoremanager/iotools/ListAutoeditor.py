# -*- encoding: utf-8 -*-
import types
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.iotools.Autoeditor import Autoeditor


class ListAutoeditor(Autoeditor):
    r'''List editor.

    ::

        >>> session = scoremanager.core.Session()
        >>> autoeditor = scoremanager.iotools.ListAutoeditor(session=session)
        >>> autoeditor._target = ['first', 'second', 'third']
        >>> autoeditor
        <ListAutoeditor(target=list)>

    ::

        >>> autoeditor._run(pending_input='rm 1 q')

    ::

        >>> autoeditor
        <ListAutoeditor(target=list)>

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
        superclass = super(ListAutoeditor, self)
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
            if not isinstance(self.target._item_callable, types.TypeType):
                return
            self._item_class = self.target._item_callable
            dummy_item = self.target._item_callable()
            helper = stringtools.upper_camel_case_to_space_delimited_lowercase
            asset_identifier = helper(type(dummy_item).__name__)
            if isinstance(dummy_item, datastructuretools.TypedList):
                self._item_creator_class = iotools.ListAutoeditor
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
            'rm': self.remove_items,
            'mv': self.move_item,
            }
        return result

    @property
    def _items(self):
        return self.target

    @property
    def _target_name(self):
        if self.target is not None:
            return 'edit'

    ### PRIVATE METHODS ###

    def _get_item_from_item_number(self, item_number):
        try:
            return self._items[int(item_number) - 1]
        except:
            pass

    def _get_target_summary_lines(self):
        result = []
        for item in self._items:
            result.append(self._io_manager._get_one_line_menu_summary(item))
        return result

    def _handle_main_menu_result(self, result):
        if not isinstance(result, str):
            message = 'result must be string: {!r}.'
            message = message.format(result)
            raise TypeError(message)
        if result in self._input_to_method:
            self._input_to_method[result]()
        elif mathtools.is_integer_equivalent_expr(result):
            if self.allow_item_edit:
                self.edit_item(result)
        else:
            superclass = super(ListAutoeditor, self)
            superclass._handle_main_menu_result(result)

    def _initialize_target(self):
        if self.target is not None:
            return
        else:
            self._target = self._target_class([])

    # TODO: encapsulate section-making code into separate methods
    def _make_main_menu(self, name='list editor'):
        menu = self._io_manager.make_menu(name=name)
        menu_entries = self._make_target_attribute_tokens()
        if menu_entries:
            section = menu.make_keyed_attribute_section(
                menu_entries=menu_entries,
                name='keyed attribute section',
                )
        menu_entries = self._get_target_summary_lines()
        if menu_entries:
            section = menu.make_numbered_section(
                menu_entries=menu_entries,
                name='numbered section',
                )
            self._numbered_section = section
        commands = []
        commands.append(('elements - add', 'add'))
        if 1 < len(self._items):
            commands.append(('elements - move', 'mv'))
        if 0 < len(self._items):
            commands.append(('elements - remove', 'rm'))
        section = menu.make_command_section(
            commands=commands,
            name='add, move, remove',
            )
        self._make_done_menu_section(menu)
        return menu

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
        r'''Adds items to list.

        Returns none.
        '''
        from scoremanager import iotools
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
            getter = self._io_manager.make_getter()
            self._item_getter_configuration_method(
                getter,
                self._asset_identifier,
                )
            item_initialization_token = getter._run()
            if self._session.is_backtracking:
                return
            if item_initialization_token == 'done':
                self._session._is_autoadding = False
                return
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
        self._items.extend(items)

    def edit_item(self, item_number):
        r'''Edits item in list.

        Returns none.
        '''
        from scoremanager import iotools
        item = self._get_item_from_item_number(item_number)
        if item is None:
            return
        item_editor_class = self._item_editor_class or iotools.Autoeditor
        item_editor = item_editor_class(
            session=self._session,
            target=item,
            )
        item_editor._run()
        item_index = int(item_number) - 1
        self._items[item_index] = item_editor.target

    def move_item(self):
        r'''Moves items in list.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_integer_in_range('old number', 1, len(self._items))
        getter.append_integer_in_range('new number', 1, len(self._items))
        result = getter._run()
        if self._session.is_backtracking:
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        item = self._items[old_index]
        self._items.remove(item)
        self._items.insert(new_index, item)

    def remove_items(self):
        r'''Removes items from list.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        items_identifier = stringtools.pluralize(self._asset_identifier)
        getter.append_menu_section_range(
            items_identifier, self._numbered_section)
        argument_range = getter._run()
        if self._session.is_backtracking:
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        items = self._items[:]
        items = sequencetools.remove_elements(items, indices)
        self._items[:] = items