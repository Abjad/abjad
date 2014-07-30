# -*- encoding: utf-8 -*-
from scoremanager.idetools.CollectionAutoeditor import CollectionAutoeditor


class ListAutoeditor(CollectionAutoeditor):
    r'''List editor.

    ::

        >>> session = scoremanager.idetools.Session()
        >>> autoeditor = scoremanager.idetools.ListAutoeditor(
        ...     session=session,
        ...     )
        >>> autoeditor._target = ['first', 'second', 'third']
        >>> autoeditor
        <ListAutoeditor(target=list)>

    '''

    ### PRIVATE METHODS ###

    @property
    def _command_to_method(self):
        superclass = super(ListAutoeditor, self)
        result = superclass._command_to_method
        result.update({
            'mv': self.move_item,
            })
        return result

    def _make_command_menu_section(self, menu):
        superclass = super(ListAutoeditor, self)
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

    def move_item(self):
        r'''Moves items in list.

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
        self._collection.remove(item)
        self._collection.insert(new_index, item)