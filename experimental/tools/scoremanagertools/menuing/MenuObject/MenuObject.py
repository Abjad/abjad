import os
import subprocess
from abjad.tools import iotools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject.ScoreManagerObject import \
    ScoreManagerObject
from experimental.tools.scoremanagertools import predicates


class MenuObject(ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, session=None, where=None, title=None):
        ScoreManagerObject.__init__(self, session=session)
        self.indent_level = 0
        self.prompt_default = None
        self.should_clear_terminal = False
        self.title = title
        self.where = where

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

    ### PUBLIC METHODS ###

    def conditionally_clear_terminal(self):
        if not self._session.hide_next_redraw:
            if self.should_clear_terminal:
                if self._session.is_displayable:
                    iotools.clear_terminal()

    def exec_statement(self):
        lines = []
        statement = self._io.handle_raw_input('XCF', include_newline=False)
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
        self._io.display(lines)
        self._session.hide_next_redraw = True

    def grep_directories(self):
        regex = self._io.handle_raw_input('regex')
        command = 'grep -Irn "{}" * | grep -v svn'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self._io.display(lines, capitalize_first_character=False)

    def interactively_edit_client_source_file(self):
        if self.where is not None:
            file_name = self.where[1]
            line_number = self.where[2]
            command = 'vim +{} {}'.format(line_number, file_name)
            os.system(command)
        else:
            lines = []
            lines.append("where-tracking not enabled. " +
                "Use 'tw' to toggle where-tracking.")
            lines.append('')
            self._io.display(lines)
            self._session.hide_next_redraw = True

    def make_default_hidden_section(self, session=None, where=None):
        from experimental.tools import scoremanagertools
        hidden_section = scoremanagertools.menuing.MenuSection(
            session=session,
            where=where,
            return_value_attribute='key',
            is_hidden=True,
            is_modern=True,
            )
        hidden_section.append(('back', 'b'))
        hidden_section.append(('exec statement', 'exec'))
        hidden_section.append(('grep directories', 'grep'))
        hidden_section.append(('edit client source', 'here'))
        hidden_section.append(('show hidden items', 'hidden'))
        hidden_section.append(('home', 'home'))
        hidden_section.append(('next score', 'next'))
        hidden_section.append(('prev score', 'prev'))
        hidden_section.append(('quit', 'q'))
        hidden_section.append(('redraw', 'r'))
        hidden_section.append(('score', 'score'))
        hidden_section.append(('toggle menu', 'tm'))
        hidden_section.append(('toggle where', 'tw'))
        hidden_section.append(('show menu client', 'where'))
        return hidden_section

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
                line = '{} {}'.format(
                    self.make_tab(self.indent_level), title_line)
                menu_lines.append(line)
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
            self._io.display(lines, capitalize_first_character=False)
        else:
            lines.append("where-tracking not enabled. " + 
                "Use 'tw' to toggle where-tracking.")
            lines.append('')
            self._io.display(lines)
        self._session.hide_next_redraw = True

    def toggle_menu(self):
        if self._session.nonnumbered_menu_sections_are_hidden:
            self._session.nonnumbered_menu_sections_are_hidden = False
        else:
            self._session.nonnumbered_menu_sections_are_hidden = True
