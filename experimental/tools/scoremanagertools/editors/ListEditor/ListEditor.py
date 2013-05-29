from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import menuing
from experimental.tools.scoremanagertools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest


class ListEditor(InteractiveEditor):

    ### CLASS VARIABLES ###

    item_class = None
    item_creator_class = None
    item_creator_class_kwargs = {}
    item_editor_class = None
    item_getter_configuration_method = menuing.UserInputGetter.append_expr
    item_identifier = 'element'
    target_manifest = TargetManifest(list,)

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_item_interactively(result)
        else:
            super(ListEditor, self)._handle_main_menu_result(result)

    def _make_main_menu(self):
        menu, attribute_management_section = self._io.make_menu(where=self._where,
            is_keyed=getattr(self.target_manifest, 'is_keyed', False))
        attribute_management_section.tokens = self.target_attribute_tokens
        attribute_management_section.show_existing_values = True
        item_management_section = menu.make_section(is_parenthetically_numbered=True)
        item_management_section.tokens = self.target_summary_lines
        item_management_section.return_value_attribute = 'number'
        command_section = menu.make_section()
        command_section.append(('add', 'add elements'))
        if 0 < len(self.items):
            command_section.append(('rm', 'remove elements'))
        if 1 < len(self.items):
            command_section.append(('mv', 'move elements'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('done', 'done'))
        return menu

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self.target_name or self.space_delimited_lowercase_target_class_name

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
            result.append(self._io.get_one_line_menuing_summary(item))
        return result

    ### PUBLIC METHODS ###

    def add_items_interactively(self):
        if self.item_creator_class:
            item_creator = self.item_creator_class(
                session=self._session, **self.item_creator_class_kwargs)
            self._session.push_backtrack()
            result = item_creator._run()
            self._session.pop_backtrack()
            if self._session.backtrack():
                return
            if result == 'done':
                self._session.is_autoadding = False
                return
            result = result or item_creator.target
        elif self.item_getter_configuration_method:
            getter = self._io.make_getter(where=self._where)
            self.item_getter_configuration_method(getter, self.item_identifier)
            self._session.push_backtrack()
            item_initialization_token = getter._run()
            self._session.pop_backtrack()
            if self._session.backtrack():
                return
            if item_initialization_token == 'done':
                self._session.is_autoadding = False
                return
            if self.item_class:
                result = self.item_class(item_initialization_token)
            else:
                result = item_initialization_token
        else:
            result = self.item_class()
        if result is None:
            result = []
        if result.__class__.__name__ == 'list':
            items = result
        else:
            items = [result]
        self.items.extend(items)

    def conditionally_initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self.target_class([])

    def edit_item_interactively(self, item_number):
        item = self.get_item_from_item_number(item_number)
        if item is not None:
            item_editor = self.item_editor_class(session=self._session, target=item)
            item_editor._run()
            item_index = int(item_number) - 1
            self.items[item_index] = item_editor.target

    def get_item_from_item_number(self, item_number):
        try:
            return self.items[int(item_number) - 1]
        except:
            pass

    def move_item_interactively(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_integer_in_range('old number', 1, len(self.items))
        getter.append_integer_in_range('new number', 1, len(self.items))
        result = getter._run()
        if self._session.backtrack():
            return
        old_number, new_number = result
        old_index, new_index = old_number - 1, new_number - 1
        item = self.items[old_index]
        self.items.remove(item)
        self.items.insert(new_index, item)

    def remove_items_interactively(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_argument_range(self.items_identifier, self.target_summary_lines)
        argument_range = getter._run()
        if self._session.backtrack():
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        items = self.items[:]
        items = sequencetools.remove_sequence_elements_at_indices(items, indices)
        self.items[:] = items

    ### UI MANIFEST ###

    user_input_to_action = {
        'add':  add_items_interactively,
        'rm':   remove_items_interactively,
        'mv':   move_item_interactively,
    }
