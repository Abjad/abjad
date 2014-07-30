# -*- encoding: utf-8 -*-
import copy
import types
from abjad.tools import datastructuretools
from abjad.tools import stringtools
from abjad.tools.topleveltools import new
from scoremanager.idetools.Controller import Controller


class Autoeditor(Controller):
    r'''Autoeditor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attribute_section',
        '_attributes_in_memory',
        '_breadcrumb',
        '_original_target',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        breadcrumb=None,
        session=None,
        target=None,
        ):
        assert target is not None
        Controller.__init__(self, session=session)
        self._attributes_in_memory = {}
        self._breadcrumb = breadcrumb
        self._original_target = copy.deepcopy(target)
        self._target = target

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of autoeditor.

        Returns string.
        '''
        class_name = type(self.target).__name__
        summary = 'target={}'.format(class_name)
        return '<{}({})>'.format(type(self).__name__, summary)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        return getattr(self.target, '_attribute_manifest', [])

    @property
    def _target_has_changed(self):
        return not self.target == self._original_target

    ### PRIVATE METHODS ###

    def _attribute_name_to_command(self, attribute_name, commands):
        found_command = False
        attribute_parts = attribute_name.split('_')
        i = 1
        while True:
            command = ''.join([part[:i] for part in attribute_parts])
            if command not in commands:
                break
            i = i + 1
        return command

    def _clean_up_attributes_in_memory(self):
        if self.target is None:
            try:
                self._initialize_target_from_attributes_in_memory()
            except ValueError:
                pass
        self._attributes_in_memory = {}

    def _command_to_attribute_editor(
        self,
        command,
        prepopulated_value,
        session=None,
        ):
        manifest = self._attribute_manifest
        assert manifest
        attribute_name = manifest._command_to_attribute_name(command)
        attribute_name = attribute_name.replace('_', ' ')
        attribute_detail = manifest._command_to_attribute_detail(command)
        attribute_editor = self._get_attribute_autoeditor(
            attribute_detail,
            attribute_name,
            prepopulated_value,
            )
        return attribute_editor

    def _command_to_prepopulated_value(self, command):
        manifest = self._attribute_manifest
        attribute_name = manifest._command_to_attribute_name(command)
        return getattr(self.target, attribute_name, None)

    def _copy_target_attributes_to_memory(self):
        self._attributes_in_memory = {}
        manifest = self._attribute_manifest
        for attribute_detail in self._attribute_manifest:
            name = attribute_detail.name
            attribute_value = getattr(self.target, name, None)
            if attribute_value is not None:
                attribute_name = manifest._to_initializer_argument_names(name)
                self._attributes_in_memory[name] = attribute_value
        for attribute_detail in manifest:
            if not attribute_detail.is_keyword:
                continue
            name = attribute_detail.name
            attribute_value = getattr(self.target, name, None)
            if attribute_value is not None:
                self._attributes_in_memory[name] = attribute_value

    def _get_attribute_autoeditor(
        self,
        attribute_detail,
        space_delimited_attribute_name,
        prepopulated_value,
        ):
        from scoremanager import idetools
        if isinstance(attribute_detail.editor, types.FunctionType):
            autoeditor = attribute_detail.editor(
                space_delimited_attribute_name,
                session=self._session,
                prepopulated_value=prepopulated_value,
                allow_none=True,
                )
        elif issubclass(attribute_detail.editor, Autoeditor):
            autoeditor = attribute_detail.editor(
                session=self._session,
                target=prepopulated_value,
                )
        elif issubclass(attribute_detail.editor, datastructuretools.TypedList):
            target = getattr(self.target, attribute_detail.name)
            target = target or attribute_detail.editor()
            autoeditor = idetools.ListAutoeditor(
                session=self._session,
                target=target,
                )
        elif isinstance(attribute_detail.editor, type):
            target = getattr(self.target, attribute_detail.name)
            target = target or attribute_detail.editor()
            autoeditor = type(self)(
                session=self._session,
                target=target,
                )
        elif issubclass(attribute_detail.editor, idetools.Selector):
            autoeditor = attribute_detail.editor(session=self._session)
        else:
            message = 'what is {!r}?'
            message = message.format(attribute_detail.editor)
            raise ValueError(message)
        prototype = (
            Autoeditor,
            idetools.Selector,
            idetools.Getter,
            )
        return autoeditor

    def _get_target_summary_lines(self):
        result = []
        if self.target is not None:
            for attribute_detail in self._attribute_manifest:
                target_attribute_name = attribute_detail.name
                name = stringtools.to_space_delimited_lowercase(
                    target_attribute_name)
                value = self._io_manager._get_one_line_menu_summary(
                    getattr(self.target, target_attribute_name))
                result.append('{}: {}'.format(name, value))
        return result

    def _handle_input(self, result):
        assert isinstance(result, str), repr(result)
        if result == '<return>':
            self._session._is_backtracking_locally = True
            return
        elif result == 'none':
            self.set_attributes_to_none()
            return
        manifest = self._attribute_manifest
        attribute_name = manifest._command_to_attribute_name(result)
        prepopulated_value = self._command_to_prepopulated_value(result)
        attribute_editor = self._command_to_attribute_editor(
            result,
            prepopulated_value=prepopulated_value,
            session=self._session,
            )
        if attribute_editor is None:
            return
        if self._session.is_autoadvancing:
            self._session._autoadvance_depth += 1
        result = attribute_editor._run()
        # do not include 'or result is None' below
        if self._session.is_backtracking:
            self._session._autoadvance_depth -= 1
            return
        if hasattr(attribute_editor, 'target'):
            attribute_value = attribute_editor.target
        else:
            attribute_value = result
        self._set_target_attribute(attribute_name, attribute_value)

    def _initialize_target_from_attributes_in_memory(self):
        args, kwargs = [], {}
        manifest = self._attribute_manifest
        for attribute_detail in manifest:
            if attribute_detail.is_keyword:
                continue
            name = attribute_detail.name
            if name in self._attributes_in_memory:
                args.append(self._attributes_in_memory.get(name))
        for attribute_detail in manifest:
            if not attribute_detail.is_keyword:
                continue
            name = attribute_detail.name
            if name in self._attributes_in_memory:
                value = self._attributes_in_memory.get(name)
                kwargs[name] = value
        self._target = type(self.target)(*args, **kwargs)

    def _make_attributes_menu_section(self, menu):
        menu_entries = self._make_target_attribute_tokens()
        if not menu_entries:
            return
        section = menu.make_keyed_attribute_section(
            group_by_annotation=False,
            is_numbered=True,
            menu_entries=menu_entries,
            name='attributes',
            )
        self._attribute_section = section

    def _make_command_menu_section(self, menu):
        commands = []
        commands.append(('done', 'done'))
        commands.append(('none', 'none'))
        menu.make_navigation_section(
            commands=commands,
            name='done',
            )

    def _make_main_menu(self):
        name = self._spaced_class_name
        menu = self._io_manager._make_menu(name=name, prompt_character='|>')
        self._make_attributes_menu_section(menu)
        self._make_command_menu_section(menu)
        return menu

    def _make_target_attribute_tokens(self):
        result = []
        for attribute_detail in self._attribute_manifest.attribute_details:
            key = attribute_detail.command
            display_string = attribute_detail.display_string
            attribute_value = getattr(
                self.target,
                attribute_detail.name,
                None,
                )
            if attribute_value is None:
                attribute_value = getattr(
                    self.target, attribute_detail.name, None)
            if (hasattr(attribute_value, '__len__') and
                not len(attribute_value)):
                attribute_value = None
            prepopulated_value = self._io_manager._get_one_line_menu_summary(
                attribute_value)
            menu_entry = (display_string, key, prepopulated_value)
            result.append(menu_entry)
        return result

    def _run(self):
        with self._io_manager._controller(
            consume_local_backtrack=True,
            controller=self,
            on_exit_callbacks=(self._clean_up_attributes_in_memory,),
            ):
            self._session._pending_redraw = True
            if self._session.is_backtracking:
                return
            result = None
            while True:
                menu = self._make_main_menu()
                if result is None and self._session.is_autostarting:
                    #print 'case 1 ...'
                    result = menu._get_first_nonhidden_return_value_in_menu()
                    menu._predetermined_input = result
                    menu._run()
                elif self._session.is_autoadding:
                    #print 'case 2 ...'
                    self._session._pending_redraw = True
                    result = 'add'
                    menu._predetermined_input = result
                    menu._run()
                elif not result and self._session.is_autoadvancing:
                    #print 'case 3 ...'
                    result = menu._get_first_nonhidden_return_value_in_menu()
                    menu._predetermined_input = result
                    menu._run()
                elif result and self._session.is_autoadvancing:
                    #print 'case 4 ...'
                    result = menu._to_next_return_value_in_section(result)
                    menu._predetermined_input = result
                    menu._run()
                else:
                    #print 'case 5 ...'
                    result = menu._run()
                    if self._session.is_backtracking:
                        break
                    elif not result:
                        continue
                if result in ('done', 'done!'):
                    break
                self._handle_input(result)
                self._session._pending_redraw = True
                if self._session.pending_done:
                    break
                if self._session.is_backtracking:
                    break
                if (self._session.is_autoadvancing and 
                    result == menu._to_last_return_value_in_section(result)):
                    break
        if self._session.is_autoadvancing:
            self._session._autoadvance_depth -= 1

    def _set_target_attribute(self, attribute_name, attribute_value):
        kwargs = {attribute_name: attribute_value}
        try:
            new_target = new(self.target, **kwargs)
        except (AssertionError, TypeError, ValueError):
            message = 'can not set {!r} to {!r}.'
            message = message.format(attribute_name, attribute_value)
            self._io_manager._display(message)
            return -1
        self._target = new_target

    def _target_args_to_target_summary_lines(self, target):
        result = []
        for arg in getattr(target, 'args', []):
            name = stringtools.to_space_delimited_lowercase(arg)
            attribute = getattr(target, arg)
            value = self._io_manager._get_one_line_menu_summary(attribute)
            result.append('{}: {}'.format(name, value))
        return result

    def _target_kwargs_to_target_summary_lines(self, target):
        result = []
        for kwarg in getattr(target, 'kwargs', []):
            name = stringtools.to_space_delimited_lowercase(kwarg)
            value = self._io_manager._get_one_line_menu_summary(
                getattr(target, kwarg))
            result.append('{}: {}'.format(name, value))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        r'''Gets autoeditor breadcrumb.

        Returns none.
        '''
        if self._breadcrumb is None:
            name = type(self.target).__name__
            name = stringtools.to_space_delimited_lowercase(name)
            return name
        return self._breadcrumb

    @property
    def target(self):
        r'''Gets autoeditor target.

        Returns object or none.
        '''
        return self._target

    ### PUBLIC METHODS ###

    def set_attributes_to_none(self):
        r'''Sets attributes to none.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        name = 'enter attribute numbers to set to none'
        getter = self._io_manager._make_getter()
        getter.append_menu_section_range(name, self._attribute_section)
        numbers = getter._run()
        if self._session.is_backtracking or not numbers:
            return
        indices = [_ - 1 for _ in numbers]
        manifest = self._attribute_manifest
        results = []
        for index in indices:
            attribute_detail = manifest[index]
            result = self._set_target_attribute(attribute_detail.name, None)
            results.append(result)
        if any(_ == -1 for _ in results):
            self._io_manager._display('')
            message = 'press return to continue'
            self._io_manager._confirm(
                include_chevron=True,
                message=message,
                )