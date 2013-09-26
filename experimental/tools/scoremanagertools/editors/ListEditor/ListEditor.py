# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import io
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class ListEditor(InteractiveEditor):
    r'''List editor.

    ::

        >>> editor = scoremanagertools.editors.ListEditor()
        >>> editor.target = ['first', 'second', 'third']
        >>> editor
        ListEditor(target=['first', 'second', 'third'])

    ::

        >>> editor._run(pending_user_input='rm 1 q')

    ::

        >>> editor
        ListEditor(target=['second', 'third'])

    '''

    ### CLASS VARIABLES ###

    item_class = None

    item_creator_class = None

    item_creator_class_kwargs = {}

    item_editor_class = None

    item_getter_configuration_method = io.UserInputGetter.append_expr

    item_identifier = 'element'

    target_manifest = TargetManifest(list,)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self.target_name or \
            self.space_delimited_lowercase_target_class_name

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif mathtools.is_integer_equivalent_expr(result):
            self.interactively_edit_item(result)
        else:
            super(ListEditor, self)._handle_main_menu_result(result)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        keyed_attribute_section = main_menu.make_keyed_attribute_section()
        keyed_attribute_section.menu_entries = self.target_attribute_tokens
        numbered_section = main_menu.make_numbered_section()
        self._numbered_section = numbered_section
        numbered_section.menu_entries = self.target_summary_lines
        command_section = main_menu.make_command_section()
        command_section.append(('add elements', 'add'))
        if 1 < len(self.items):
            command_section.append(('move elements', 'mv'))
        if 0 < len(self.items):
            command_section.append(('remove elements', 'rm'))
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('done', 'done'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target

    @property
    def items_identifier(self):
        if hasattr(self, '_items_identifier'):
            return self._items_identifer
        else:
            return stringtools.pluralize_string(self.item_identifier)

    @property
    def target_summary_lines(self):
        result = []
        for item in self.items:
            result.append(
                self.session.io_manager.get_one_line_menuing_summary(item))
        return result

    ### PUBLIC METHODS ###

    def get_item_from_item_number(self, item_number):
        try:
            return self.items[int(item_number) - 1]
        except:
            pass

    def initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self.target_class([])

    def interactively_add_items(self):
        if self.item_creator_class:
            item_creator = self.item_creator_class(
                session=self.session, 
                **self.item_creator_class_kwargs
                )
            with self.backtracking:
                result = item_creator._run()
            if self.session.backtrack():
                return
            if result == 'done':
                self.session.is_autoadding = False
                return
            result = result or item_creator.target
        elif self.item_getter_configuration_method:
            getter = self.session.io_manager.make_getter(where=self._where)
            self.item_getter_configuration_method(getter, self.item_identifier)
            with self.backtracking:
                item_initialization_token = getter._run()
            if self.session.backtrack():
                return
            if item_initialization_token == 'done':
                self.session.is_autoadding = False
                return
            if self.item_class:
                result = self.item_class(item_initialization_token)
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

    def interactively_edit_item(self, item_number):
        item = self.get_item_from_item_number(item_number)
        if item is not None:
            if self.item_editor_class is not None:
                item_editor = self.item_editor_class(
                    session=self.session, 
                    target=item,
                    )
                item_editor._run()
                item_index = int(item_number) - 1
                self.items[item_index] = item_editor.target

    def interactively_move_item(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_integer_in_range('old number', 1, len(self.items))
        getter.append_integer_in_range('new number', 1, len(self.items))
        result = getter._run()
        if self.session.backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        item = self.items[old_index]
        self.items.remove(item)
        self.items.insert(new_index, item)

    def interactively_remove_items(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_menu_section_range(
            self.items_identifier, self._numbered_section)
        argument_range = getter._run()
        if self.session.backtrack():
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        items = self.items[:]
        items = sequencetools.remove_sequence_elements_at_indices(
            items, indices)
        self.items[:] = items

    ### UI MANIFEST ###

    user_input_to_action = {
        'add':  interactively_add_items,
        'rm':   interactively_remove_items,
        'mv':   interactively_move_item,
    }
