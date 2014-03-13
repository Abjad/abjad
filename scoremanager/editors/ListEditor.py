# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager import iotools
from scoremanager.editors.Editor import Editor


class ListEditor(Editor):
    r'''List editor.

    ::

        >>> session = scoremanager.core.Session()
        >>> editor = scoremanager.editors.ListEditor(session=session)
        >>> editor.target = ['first', 'second', 'third']
        >>> editor
        ListEditor(target=['first', 'second', 'third'])

    ::

        >>> editor._run(pending_user_input='rm 1 q')

    ::

        >>> editor
        ListEditor(target=['second', 'third'])

    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        superclass = super(ListEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = None
        self.item_creator_class = None
        self.item_creator_class_kwargs = {}
        self.item_editor_class = None
        self.item_getter_configuration_method = \
            iotools.UserInputGetter.append_expr
        self.item_identifier = 'element'

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        result = {
            'add': self.add_items,
            'rm': self.remove_items,
            'mv': self.move_item,
            }
        return result

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_item(result)
        else:
            super(ListEditor, self)._handle_main_menu_result(result)

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        keyed_attribute_section = menu.make_keyed_attribute_section(
            name='keyed attribute section',
            )
        keyed_attribute_section.menu_entries = \
            self._make_target_attribute_tokens()
        numbered_section = menu.make_numbered_section(
            name='numbered section',
            )
        self._numbered_section = numbered_section
        numbered_section.menu_entries = self._target_summary_lines
        section = menu.make_command_section(name='add, move, remove')
        section.append(('elements - add', 'add'))
        if 1 < len(self.items):
            section.append(('elements - move', 'mv'))
        if 0 < len(self.items):
            section.append(('elements - remove', 'rm'))
        self._make_done_menu_section(menu)
        return menu

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target

    @property
    def _target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(list,)

    @property
    def _target_summary_lines(self):
        result = []
        for item in self.items:
            result.append(
                self._io_manager._get_one_line_menu_summary(item))
        return result

    ### PUBLIC METHODS ###

    def add_items(self):
        r'''Adds items to list.

        Returns none.
        '''
        if self.item_creator_class:
            item_creator = self.item_creator_class(
                session=self._session, 
                **self.item_creator_class_kwargs
                )
            with self._backtracking:
                result = item_creator._run()
            if self._session._backtrack():
                return
            if result == 'done':
                self._session._is_autoadding = False
                return
            result = result or item_creator.target
        elif self.item_getter_configuration_method:
            getter = self._io_manager.make_getter(where=self._where)
            self.item_getter_configuration_method(getter, self.item_identifier)
            with self._backtracking:
                item_initialization_token = getter._run()
            if self._session._backtrack():
                return
            if item_initialization_token == 'done':
                self._session._is_autoadding = False
                return
            if self.item_class:
                if isinstance(item_initialization_token, str):
                    exec('from abjad import *')
                    try:
                        expression = eval(item_initialization_token)
                    except (NameError, SyntaxError):
                        expression = item_initialization_token
                else:
                    expression = item_initialization_token
                result = self.item_class(expression)
            else:
                result = item_initialization_token
        else:
            result = self.item_class()
        if result is None:
            result = []
        if type(result) is list:
            items = result
        else:
            items = [result]
        self.items.extend(items)

    def edit_item(self, item_number):
        r'''Edits item.

        Returns none.
        '''
        item = self._get_item_from_item_number(item_number)
        if item is not None:
            if self.item_editor_class is not None:
                item_editor = self.item_editor_class(
                    session=self._session, 
                    target=item,
                    )
                item_editor._run()
                item_index = int(item_number) - 1
                self.items[item_index] = item_editor.target

    def _get_item_from_item_number(self, item_number):
        try:
            return self.items[int(item_number) - 1]
        except:
            pass

    def _initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self._target_class([])

    def move_item(self):
        r'''Moves items.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_integer_in_range('old number', 1, len(self.items))
        getter.append_integer_in_range('new number', 1, len(self.items))
        result = getter._run()
        if self._session._backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        item = self.items[old_index]
        self.items.remove(item)
        self.items.insert(new_index, item)

    def remove_items(self):
        r'''Removes items.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        items_identifier = stringtools.pluralize_string(self.item_identifier)
        getter.append_menu_section_range(
            items_identifier, self._numbered_section)
        argument_range = getter._run()
        if self._session._backtrack():
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        items = self.items[:]
        items = sequencetools.remove_elements(
            items, indices)
        self.items[:] = items
