# -*- encoding: utf-8 -*-
import abc
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.idetools.Autoeditor import Autoeditor


class CollectionAutoeditor(Autoeditor):
    r'''Collection editor.

    Abstract base class for ListAutoeditor and DictionaryAutoeditor.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

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
        from scoremanager import idetools
        if target is None:
            target = []
        superclass = super(CollectionAutoeditor, self)
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
            idetools.UserInputGetter.append_expr
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
                self._item_creator_class = idetools.ListAutoeditor
            else:
                self._item_creator_class = idetools.Autoeditor

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest()

    @property
    def _collection(self):
        return self.target

    @property
    def _command_to_method(self):
        result = {
            'add': self.add_items,
            'rm': self.remove_items,
            }
        return result

    @property
    def _target_name(self):
        if self.target is not None:
            return 'edit'

    ### PRIVATE METHODS ###

    def _get_item_from_item_number(self, item_number):
        try:
            return self._collection[int(item_number) - 1]
        except:
            pass

    def _get_item_to_add(self, item_name=None):
        from scoremanager import idetools
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
            if item_name:
                item_creator._breadcrumb = item_name
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
        return result

    def _get_target_summary_lines(self):
        result = []
        for item in self._collection:
            result.append(self._io_manager._get_one_line_menu_summary(item))
        return result

    def _handle_input(self, result):
        assert isinstance(result, str), repr(result)
        if result.endswith('!') and 1 < len(result):
            self._session._is_autoadding = True
            result = result.strip('!')
        if result in self._command_to_method:
            self._command_to_method[result]()
        elif mathtools.is_integer_equivalent_expr(result):
            if self.allow_item_edit:
                self.edit_item(result)
        else:
            superclass = super(CollectionAutoeditor, self)
            superclass._handle_input(result)

    def _initialize_target(self):
        if self.target is not None:
            return
        self._target = self._target_class([])

    def _make_command_menu_section(self, menu, commands_only=False):
        commands = []
        commands.append(('elements - add', 'add'))
        if 0 < len(self._collection):
            commands.append(('elements - remove', 'rm'))
        if commands_only:
            return commands
        commands.append(('editing - done', 'done'))
        section = menu.make_command_section(
            commands=commands,
            is_alphabetized=False,
            name='commands',
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
        menu = self._io_manager._make_menu(name=name, prompt_character='|>')
        self._make_keyed_attributes_menu_section(menu)
        self._make_numbered_entries_menu_section(menu)
        self._make_command_menu_section(menu)
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
        r'''Adds items to list.

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
        self._collection.extend(items)

    def edit_item(self, number):
        r'''Edits item `number` in list.

        Returns none.
        '''
        from scoremanager import idetools
        item = self._get_item_from_item_number(number)
        if item is None:
            return
        item_editor_class = self._item_editor_class or idetools.Autoeditor
        item_editor = item_editor_class(session=self._session, target=item)
        item_editor._run()
        item_index = int(number) - 1
        self._collection[item_index] = item_editor.target

    def remove_items(self):
        r'''Removes items from list.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        items_identifier = stringtools.pluralize(self._asset_identifier)
        getter.append_menu_section_range(
            items_identifier, self._numbered_section)
        argument_range = getter._run()
        if self._session.is_backtracking:
            return
        indices = [argument_number - 1 for argument_number in argument_range]
        indices = list(reversed(sorted(set(indices))))
        items = self._collection[:]
        items = sequencetools.remove_elements(items, indices)
        self._collection[:] = items