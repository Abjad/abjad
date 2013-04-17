import os
import subprocess
from abjad.tools import stringtools
from experimental.tools.scoremanagementtools.core.SCFObject.SCFObject import SCFObject
from experimental.tools.scoremanagementtools import predicates


class MenuObject(SCFObject):

    ### INITIALIZER ###

    def __init__(self, session=None, where=None, title=None):
        SCFObject.__init__(self, session=session)
        self.indent_level = 0
        self.prompt_default = None
        self.should_clear_terminal = False
        self.where = where
        self.title = title

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def prompt_default():
        def fget(self):
            return self._prompt_default
        def fset(self, prompt_default):
            assert isinstance(prompt_default, (str, type(None)))
            self._prompt_default = prompt_default
        return property(**locals())

    @apply
    def should_clear_terminal():
        def fget(self):
            return self._should_clear_terminal
        def fset(self, should_clear_terminal):
            assert isinstance(should_clear_terminal, bool)
            self._should_clear_terminal = should_clear_terminal
        return property(**locals())

    @apply
    def title():
        def fget(self):
            return self._title
        def fset(self, title):
            assert isinstance(title, (str, list, type(None)))
            self._title = title
        return property(**locals())

    @apply
    def where():
        def fget(self):
            return self._where
        def fset(self, where):
            self._where = where
        return property(**locals())

    ### PUBLIC METHODS ###

    def conditionally_clear_terminal(self):
        if not self.session.hide_next_redraw:
            if self.should_clear_terminal:
                SCFObject.conditionally_clear_terminal(self)

    def edit_client_source_file(self):
        if self.where is not None:
            file_name = self.where[1]
            line_number = self.where[2]
            command = 'vi +{} {}'.format(line_number, file_name)
            os.system(command)
        else:
            lines = []
            lines.append("where-tracking not enabled. Use 'tw' to toggle where-tracking.")
            lines.append('')
            self.display(lines)
            self.session.hide_next_redraw = True

    def exec_statement(self):
        lines = []
        statement = self.handle_raw_input('XCF', include_newline=False)
        command = 'from abjad import *'
        exec(command)
        try:
            result = None
            command = 'result = {}'.format(statement)
            exec(command)
            lines.append('{!r}'.format(result))
        except:
            lines.append('expression not executable.')
        lines.append('')
        self.display(lines)
        self.session.hide_next_redraw = True

    def grep_directories(self):
        regex = self.handle_raw_input('regex')
        command = 'grep -Irn "{}" * | grep -v svn'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines, capitalize_first_character=False)

    def make_default_hidden_section(self, session=None, where=None):
        from experimental.tools.scoremanagementtools.menuing.MenuSection import MenuSection
        section = MenuSection(is_hidden=True, session=session, where=where)
        section.append(('b', 'back'))
        section.append(('exec', 'exec statement'))
        section.append(('grep', 'grep directories'))
        section.append(('here', 'edit client source'))
        section.append(('hidden', 'show hidden items'))
        section.append(('next', 'next score'))
        section.append(('prev', 'prev score'))
        section.append(('q', 'quit'))
        section.append(('r', 'redraw'))
        section.append(('score', 'score'))
        section.append(('studio', 'studio'))
        section.append(('tm', 'toggle menu'))
        section.append(('tw', 'toggle where'))
        section.append(('where', 'show menu client'))
        return section

    def make_is_integer_in_range(self, start=None, stop=None, allow_none=False):
        return lambda expr: (expr is None and allow_none) or \
            (predicates.is_integer(expr) and
            (start is None or start <= expr) and
            (stop is None or expr <= stop))

    def make_tab(self, n):
        return 4 * n * ' '

    def make_title_lines(self):
        menu_lines = []
        if isinstance(self.title, str):
            title_lines = [stringtools.capitalize_string_start(self.title)]
        elif isinstance(self.title, list):
            title_lines = self.title
        else:
            title_lines = []
        for title_line in title_lines:
            if self.indent_level:
                menu_lines.append('{} {}'.format(self.make_tab(self.indent_level), title_line))
            else:
                menu_lines.append(title_line)
        if menu_lines:
            menu_lines.append('')
        return menu_lines

    def show_menu_client(self):
        lines = []
        if self.where is not None:
            lines.append('{} file: {}'.format(self.make_tab(1), self.where[1]))
            lines.append('{} line: {}'.format(self.make_tab(1), self.where[2]))
            lines.append('{} meth: {}'.format(self.make_tab(1), self.where[3]))
            lines.append('')
            self.display(lines, capitalize_first_character=False)
        else:
            lines.append("where-tracking not enabled. Use 'tw' to toggle where-tracking.")
            lines.append('')
            self.display(lines)
        self.session.hide_next_redraw = True

    def toggle_menu(self):
        if self.session.nonnumbered_menu_sections_are_hidden:
            self.session.nonnumbered_menu_sections_are_hidden = False
        else:
            self.session.nonnumbered_menu_sections_are_hidden = True
