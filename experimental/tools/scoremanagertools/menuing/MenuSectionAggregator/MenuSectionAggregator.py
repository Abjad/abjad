from experimental.tools.scoremanagertools.menuing.MenuObject import MenuObject


class MenuSectionAggregator(MenuObject):

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._menu_sections = []

    ### PUBLIC PROPERTIES ###

    @property
    def menu_sections(self):
        return self._menu_sections

    ### PUBLIC METHODS ###

    def display_calling_code_line_number(self):
        lines = []
        if self.where is not None:
            line = '{} file: {}'.format(self._make_tab(1), self.where[1])
            lines.append(line)
            line = '{} line: {}'.format(self._make_tab(1), self.where[2])
            lines.append(line)
            line = '{} meth: {}'.format(self._make_tab(1), self.where[3])
            lines.append(line)
            lines.append('')
            self._io.display(lines, capitalize_first_character=False)
        else:
            lines.append("where-tracking not enabled. " + 
                "Use 'tw' to toggle where-tracking.")
            lines.append('')
            self._io.display(lines)
        self._session.hide_next_redraw = True

    def display_hidden_menu_section(self):
        menu_lines = []
        for menu_section in self.menu_sections:
            if menu_section.is_hidden:
                for menu_token in menu_section.menu_tokens:
                    key = menu_token.key
                    display_string = menu_token.display_string
                    menu_line = self._make_tab(1) + ' '
                    menu_line += '{} ({})'.format(display_string, key)
                    menu_lines.append(menu_line)
                menu_lines.append('')
        self._io.display(menu_lines, capitalize_first_character=False)
        self._session.hide_next_redraw = True

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

    def handle_hidden_menu_token_return_value(self, directive):
        if isinstance(directive, list) and len(directive) == 1:
            key = directive[0]
        else:
            key = directive
        if key in ('b', 'back'):
            self._session.is_backtracking_locally = True
        elif key == 'exec':
            self.exec_statement()
        elif key == 'grep':
            self.grep_directories()
        elif key == 'here':
            self.interactively_edit_calling_code()
        elif key == 'hidden':
            self.display_hidden_menu_section()
        elif key == 'next':
            self._session.is_navigating_to_next_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key == 'prev':
            self._session.is_navigating_to_prev_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key in ('q', 'quit'):
            self._session.user_specified_quit = True
#        # TODO: make this redraw!
#        elif key == 'r':
#            pass
        elif isinstance(key, str) and \
            3 <= len(key) and 'score'.startswith(key):
            if self._session.is_in_score:
                self._session.is_backtracking_to_score = True
        elif isinstance(key, str) and \
            3 <= len(key) and 'home'.startswith(key):
            self._session.is_backtracking_to_score_manager = True
        elif key == 'tm':
            self.toggle_menu()
        elif key == 'tw':
            self._session.enable_where = not self._session.enable_where
        elif key == 'where':
            self.display_calling_code_line_number()
        else:
            return directive

    def interactively_edit_calling_code(self):
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

    def toggle_menu(self):
        if self._session.nonnumbered_menu_sections_are_hidden:
            self._session.nonnumbered_menu_sections_are_hidden = False
        else:
            self._session.nonnumbered_menu_sections_are_hidden = True
