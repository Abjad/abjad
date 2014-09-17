# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.idetools.CollectionAutoeditor import CollectionAutoeditor


class TupleAutoeditor(CollectionAutoeditor):
    r'''Tuple editor.

    ::

        >>> session = scoremanager.idetools.Session()
        >>> autoeditor = scoremanager.idetools.TupleAutoeditor(
        ...     session=session,
        ...     )
        >>> autoeditor._target = ('first', 'second', 'third')
        >>> autoeditor
        <TupleAutoeditor(target=tuple)>

    '''

    ### PRIVATE METHODS ###

    @property
    def _command_to_method(self):
        superclass = super(TupleAutoeditor, self)
        result = superclass._command_to_method
        result.update({
            'mv': self.move_item,
            })
        return result

    def _make_command_menu_section(self, menu):
        superclass = super(TupleAutoeditor, self)
        commands = superclass._make_command_menu_section(
            menu, commands_only=True)
        if 1 < len(self._collection):
            commands.append(('elements - move', 'mv'))
        commands = list(sorted(commands))
        commands.append(('editing - done', 'done'))
        section = menu.make_command_section(
            commands=commands,
            is_alphabetized=False,
            name='commands'
            )

    ### PUBLIC METHODS ###

    def add_items(self):
        r'''Adds items to tuple.

        Returns none.
        '''
        result = self._get_item_to_add()
        if self._session.is_backtracking:
            return
        if result is None:
            result = []
        if type(result) is list:
            items = result
        else:
            items = [result]
        list_ = list(self._collection)
        list_.extend(items)
        class_ = type(self._collection)
        self._target = class_(list_)

    def edit_item(self, number):
        r'''Edits item `number` in collection.

        Returns none.
        '''
        from scoremanager import idetools
        item = self._get_item_from_item_number(number)
        if item is None:
            return
        if not hasattr(item, '_attribute_manifest'):
            return
        item_editor_class = self._item_editor_class or idetools.Autoeditor
        item_editor = item_editor_class(session=self._session, target=item)
        item_editor._run()
        item_index = int(number) - 1
        list_ = list(self._collection)
        list_[item_index] = item_editor.target
        class_ = type(self._collection)
        self._target = class_(list_)

    def move_item(self):
        r'''Moves items in tuple.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_integer_in_range('old number', 1, len(self._collection))
        getter.append_positive_integer('new number')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        if not isinstance(result, list) or not len(result) == 2:
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        item = self._collection[old_index]
        list_ = list(self._collection)
        list_.remove(item)
        list_.insert(new_index, item)
        class_ = type(self._collection)
        self._target = class_(list_)

    def remove_items(self):
        r'''Removes items from tuple.

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
        items = list(self._collection[:])
        items = sequencetools.remove_elements(items, indices)
        class_ = type(self._collection)
        self._target = class_(items)