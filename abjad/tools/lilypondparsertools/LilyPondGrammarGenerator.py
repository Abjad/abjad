# -*- coding: utf-8 -*-
import re
from abjad.tools import stringtools
from abjad.tools.abctools import AbjadObject


class LilyPondGrammarGenerator(AbjadObject):
    r'''Generates a syntax skeleton from LilyPond grammar files.

    To generate LilyPond's ``parser.output`` and ``parser.tab.cc`` files,
    navigate to the ``lily`` directory in LilyPond's source code and run the
    following command::

        $ bison --defines --verbose parser.yy

    '''

    ### CLASS VARIABLES ###

    _module_header = stringtools.normalize(r"""
        # -*- encoding: utf-8 -*-
        from abjad.tools.abctools import AbjadObject
        from abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode import SyntaxNode


        class _LilyPondSyntacticalDefinition(AbjadObject):
            r'''The syntactical definition of LilyPond's syntax.

            Effectively equivalent to LilyPond's ``parser.yy`` file.

            Not composer-safe.

            Used internally by ``LilyPondParser``.
            '''

            ### CLASS VARIABLES ###

            __slots__ = ()

            start_symbol = 'start_symbol'

            precedence = (
                # ('nonassoc', 'REPEAT'),
                # ('nonassoc', 'ALTERNATIVE'),
                ('nonassoc', 'COMPOSITE'),
                # ('left', 'ADDLYRICS'),
                ('nonassoc', 'DEFAULT'),
                ('nonassoc', 'FUNCTION_ARGLIST'),
                ('right', 'PITCH_IDENTIFIER', 'NOTENAME_PITCH', 'TONICNAME_PITCH',
                    'UNSIGNED', 'REAL', 'DURATION_IDENTIFIER', ':'),
                ('nonassoc', 'NUMBER_IDENTIFIER', '/'),
                ('left', '+', '-'),
                # ('left', 'UNARY_MINUS')
                )

            ### INITIALIZER ###

            def __init__(self, client=None):
                self.client = client
                if client is not None:
                    self.tokens = self.client._lexdef.tokens
                else:
                    self.tokens = []

            ### SYNTACTICAL RULES (ALPHABETICAL) ###

        """
        )

    _production_template = stringtools.normalize(r'''
        def {funcname}(self, production):
            {docstring!r}
            production[0] = SyntaxNode({nonterminal!r}, production[1:])
        ''',
        indent=4,
        )

    _production_regex = re.compile(r'''\d+\s+([\w\$\@]+): (.+)''')

    _terminal_regex = re.compile(r'''^(".+"|'.+'|[A-Z_]+)\s+\((\d+)\).*$''')

    ### SPECIAL METHODS ###

    def __call__(
        self,
        output_path=None,
        parser_output_path=None,
        parser_tab_hh_path=None,
        ):
        r'''Calls LilyPond grammar generator.
        '''
        with open(parser_output_path, 'r') as file_pointer:
            parser_output_lines = file_pointer.readlines()
        with open(parser_tab_hh_path, 'r') as file_pointer:
            parser_tab_hh_lines = file_pointer.readlines()
        productions = self._generate_production_map(
            parser_output_lines,
            parser_tab_hh_lines,
            )
        skeleton_string = self._build_parser_syntax_skeleton(productions)
        with open(output_path, 'w') as file_pointer:
            file_pointer.write(skeleton_string)

    ### PRIVATE METHODS ###

    def _extract_productions_from_parser_output(
        self,
        parser_output_lines,
        ):
        productions = {}
        current_nonterminal = None
        in_grammar = False
        for line in parser_output_lines:
            line = line.strip()
            if line == 'Terminals, with rules where they appear':
                break
            elif line == 'Grammar':
                in_grammar = True
                continue
            if not in_grammar:
                continue
            if not line:
                continue
            match = self._production_regex.match(line)
            if match:
                current_nonterminal, right_hand_side = match.groups()
                if current_nonterminal.startswith(('$', '@')):
                    continue
                if current_nonterminal not in productions:
                    productions[current_nonterminal] = []
                if right_hand_side == '/* empty */':
                    productions[current_nonterminal].append([])
                else:
                    right_hand_side = right_hand_side.split()
                    right_hand_side = [_ for _ in right_hand_side
                        if not _.startswith('@')]
                    productions[current_nonterminal].append(right_hand_side)
                continue
            right_hand_side = line.partition('|')[-1].strip()
            right_hand_side = right_hand_side.split()
            right_hand_side = [_ for _ in right_hand_side
                if not _.startswith('@')]
            productions[current_nonterminal].append(right_hand_side)
        return productions

    def _extract_token_names_from_parser_tab_hh(
        self,
        parser_tab_hh_lines,
        ):
        token_names = {}
        in_enum = False
        for line in parser_tab_hh_lines:
            text = line.strip()
            if in_enum and text == '};':
                break
            if in_enum:
                parts = text.split(' ')
                name = parts[0]
                if parts[2].endswith(','):
                    number = int(parts[2][:-1])
                else:
                    number = int(parts[2])
                token_names[number] = name
            if text == 'enum yytokentype {':
                in_enum = True
        return token_names

    def _extract_token_values_from_parser_output(
        self,
        parser_output_lines,
        ):
        token_values = {}
        in_token_list = False
        for line in parser_output_lines:
            line = line.strip()
            if (
                in_token_list and
                line == 'Nonterminals, with rules where they appear'
                ):
                break
            elif line == 'Terminals, with rules where they appear':
                in_token_list = True
                continue
            elif not in_token_list:
                continue
            match = self._terminal_regex.match(line)
            if not match:
                continue
            value, number = match.groups()
            number = int(number)
            token_values[number] = value
        return token_values

    def _generate_production_map(
        self,
        parser_output_lines,
        parser_tab_hh_lines,
        ):
        productions = self._extract_productions_from_parser_output(
            parser_output_lines)
        names = self._extract_token_names_from_parser_tab_hh(
            parser_tab_hh_lines)
        values = self._extract_token_values_from_parser_output(
            parser_output_lines)
        matches = self._match_token_names_with_token_values(
            names, values)
        rewrites = {}
        for nonterminal in productions:
            for right_hand_side in productions[nonterminal]:
                for i, right_hand_item in enumerate(right_hand_side):
                    if right_hand_item in matches:
                        right_hand_side[i] = matches[right_hand_item]
                docstring = '{} : {}'.format(nonterminal, ' '.join(right_hand_side))
                for i, right_hand_item in enumerate(right_hand_side):
                    if right_hand_item[0] == "'" and right_hand_item[-1] == "'":
                        right_hand_side[i] = 'Chr{}'.format(ord(right_hand_item[-2]))
                if not right_hand_side:
                    right_hand_side = ['Empty']
                funcname = 'p_{}__{}'.format(nonterminal, '__'.join(right_hand_side))
                rewrites[funcname] = docstring
        return rewrites

    def _match_token_names_with_token_values(
        self,
        names,
        values,
        ):
        matches = {}
        for number, value in values.items():
            if number in names:
                name = names[number]
                matches[value] = name
        return matches

    def _build_parser_syntax_skeleton(
        self,
        productions,
        ):
        result = []
        result.append('{}\n'.format(self._module_header))
        current_nonterminal = 'start_symbol'
        ly_keys = sorted(key for key in productions
            if key.startswith('p_start_symbol'))
        for key in ly_keys:
            funcname = key
            docstring = productions[key]
            method_string = self._production_template.format(
                docstring=docstring,
                funcname=funcname,
                nonterminal=current_nonterminal,
                )
            method_string = '{}\n'.format(method_string)
            result.append(method_string)
        for funcname, docstring in sorted(productions.items()):
            nonterminal = funcname.split('__')[0][2:]
            if nonterminal == 'start_symbol':
                continue
            if nonterminal != current_nonterminal:
                current_nonterminal = nonterminal
                comment_string = '    ### {} ###\n'.format(nonterminal)
                result.append(comment_string)
            method_string = self._production_template.format(
                docstring=docstring,
                funcname=funcname,
                nonterminal=current_nonterminal,
                )
            method_string = '{}\n'.format(method_string)
            result.append(method_string)
        method_string = stringtools.normalize(r"""
            ### ERROR ###

            def p_error(self, production):
                r'''Error handling.'''
                pass
            """,
            indent=4,
            )
        result.append(method_string)
        string = '\n'.join(result)
        return string