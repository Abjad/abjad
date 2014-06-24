# -*- encoding: utf-8 -*-
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
        '_is_autoadding',
        '_is_autoadvancing',
        '_is_autostarting',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        breadcrumb=None,
        is_autoadding=False,
        is_autoadvancing=False,
        is_autostarting=False,
        session=None,
        target=None,
        ):
        assert target is not None
        Controller.__init__(self, session=session)
        self._attributes_in_memory = {}
        self._breadcrumb = breadcrumb
        self._is_autoadding = is_autoadding
        self._is_autoadvancing = is_autoadvancing
        self._is_autostarting = is_autostarting
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
        #return self.target._attribute_manifest
        return getattr(self.target, '_attribute_manifest', [])

    ### PRIVATE METHODS ###

    def _attribute_name_to_menu_key(self, attribute_name, menu_keys):
        found_menu_key = False
        attribute_parts = attribute_name.split('_')
        i = 1
        while True:
            menu_key = ''.join([part[:i] for part in attribute_parts])
            if menu_key not in menu_keys:
                break
            i = i + 1
        return menu_key

    def _clean_up_attributes_in_memory(self):
        if self.target is None:
            try:
                self._initialize_target_from_attributes_in_memory()
            except ValueError:
                pass
        self._attributes_in_memory = {}

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

    def _get_attribute_editor(
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
        attribute_name = manifest._menu_key_to_attribute_name(result)
        prepopulated_value = self._menu_key_to_prepopulated_value(result)
        attribute_editor = self._menu_key_to_attribute_editor(
            result,
            session=self._session,
            prepopulated_value=prepopulated_value,
            )
        if attribute_editor is None:
            return
        result = attribute_editor._run()
        if self._session.is_backtracking:
            self._is_autoadvancing = False
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
            is_numbered=True,
            menu_entries=menu_entries,
            name='attributes',
            )
        self._attribute_section = section

    def _make_command_menu_section(self, menu):
        commands = []
        commands.append(('done', 'done'))
        commands.append(('set to none', 'none'))
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
            key = attribute_detail.menu_key
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

    def _menu_key_to_attribute_editor(
        self,
        menu_key,
        prepopulated_value,
        session=None,
        ):
        manifest = self._attribute_manifest
        assert manifest
        attribute_name = manifest._menu_key_to_attribute_name(menu_key)
        attribute_name = attribute_name.replace('_', ' ')
        attribute_detail = manifest._menu_key_to_attribute_detail(menu_key)
        attribute_editor = self._get_attribute_editor(
            attribute_detail,
            attribute_name,
            prepopulated_value,
            )
        return attribute_editor

    def _menu_key_to_prepopulated_value(self, menu_key):
        manifest = self._attribute_manifest
        attribute_name = manifest._menu_key_to_attribute_name(menu_key)
        return getattr(self.target, attribute_name, None)

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
            entry_point = None
            is_first_pass = True
            while True:
                if self._session.is_autoadding:
                    self._session._pending_redraw = True
                    menu = self._make_main_menu()
                    result = 'add'
                    menu._predetermined_input = result
                    menu._run()
                    is_first_pass = False
                elif is_first_pass and self._is_autostarting:
                    menu = self._make_main_menu()
                    result = menu._get_first_nonhidden_return_value_in_menu()
                    menu._predetermined_input = result
                    menu._run()
                    is_first_pass = False
                elif result and self._is_autoadvancing:
                    entry_point = entry_point or result
                    result = menu._to_next_return_value_in_section(result)
                    if result == entry_point:
                        self._is_autoadvancing = False
                        continue
                else:
                    menu = self._make_main_menu()
                    result = menu._run()
                    if self._session.is_backtracking:
                        return
                    elif not result:
                        continue
                if result == 'done':
                    break
                self._handle_input(result)
                self._session._pending_redraw = True
                if self._session.pending_done:
                    break
                if self._session.is_backtracking:
                    return

    def _set_target_attribute(self, attribute_name, attribute_value):
        from abjad.tools import pitchtools
        # TODO: maybe remove this check
        if self._session.is_quitting:
            return
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
    def is_autoadding(self):
        r'''Is true when autoeditor is autoadding. Otherwise false.

        Returns boolean.
        '''
        return self._is_autoadding

    @property
    def is_autoadvancing(self):
        r'''Is true when autoeditor is autoadvancing. Otherwise false.

        Returns boolean.
        '''
        return self._is_autoadvancing

    @property
    def is_autostarting(self):
        r'''Is true when autoeditor is autostarting. Otherwise false.

        Returns boolean.
        '''
        return self._is_autostarting

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