# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.idetools.CollectionAutoeditor import CollectionAutoeditor


class DictionaryAutoeditor(CollectionAutoeditor):
    r'''Dictionary editor.

    ::

        >>> session = scoremanager.idetools.Session()
        >>> autoeditor = scoremanager.idetools.DictionaryAutoeditor(
        ...     session=session,
        ...     )
        >>> dictionary = {'flavor': 'cherry', 'age': 94}
        >>> autoeditor._target = dictionary
        >>> autoeditor
        <DictionaryAutoeditor(target=dict)>

    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(DictionaryAutoeditor, self)
        result = superclass._command_to_method
        result.update({
            'ren': self.rename_item,
            })
        return result

    ### PRIVATE METHODS ###

    def _dictionary_item_to_menu_summary(self, item):
        key, value = item
        try:
            value = [str(_) for _ in value]
            value = ', '.join(value)
        except TypeError:
            pass
        string = '{}: {}'.format(key, value)
        return string

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

    def _get_target_summary_lines(self):
        result = []
        for item in self._collection.items():
            result.append(self._dictionary_item_to_menu_summary(item))
        return result

    def _make_command_menu_section(self, menu):
        superclass = super(DictionaryAutoeditor, self)
        commands = superclass._make_command_menu_section(
            menu, commands_only=True)
        if 0 < len(self._collection):
            commands.append(('elements - rename', 'ren'))
        commands.append(('editing - done', 'done'))
        section = menu.make_command_section(
            commands=commands,
            is_alphabetized=False,
            name='commands'
            )

    ### PUBLIC METHODS ###

    def add_items(self):
        r'''Adds items to dictionary.

        Returns none.
        '''
        from scoremanager import idetools
        getter = self._io_manager._make_getter()
        getter.append_string('enter item name')
        key = getter._run()
        if self._session.is_backtracking or not key:
            return
        result = self._get_item_to_add(item_name=key)
        if self._session.is_backtracking:
            return
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
        from scoremanager import idetools
        item = self._get_item_from_item_number(number)
        if item is None:
            return
        key, value = item
        if self._item_editor_class is not None:
            item_editor_class = self._item_editor_class
            autoeditor = item_editor_class(session=self._session, target=value)
        else:
            autoeditor = self._io_manager._make_autoeditor(target=value)
        autoeditor._breadcrumb = key
        autoeditor._run()
        value = autoeditor.target
        self._collection[key] = value

    def remove_items(self):
        r'''Removes items from dictionary.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        items_identifier = stringtools.pluralize(self._item_identifier)
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
            key = result
            value = self._collection.get(key)
            item = (key, value)
        else:
            return
        if not item:
            return
        assert isinstance(item, tuple) and len(item) == 2
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