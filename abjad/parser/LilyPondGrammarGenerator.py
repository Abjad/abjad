from abjad.system.AbjadObject import AbjadObject


class LilyPondGrammarGenerator(AbjadObject):
    """
    Generates a syntax skeleton from LilyPond grammar files.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        skeleton_path,
        parser_output_path,
        parser_tab_hh_path,
        ):
        """
        Calls LilyPond grammar generator.
        """
        self._write_parser_syntax_skeleton(
            self,
            skeleton_path,
            parser_output_path,
            parser_tab_hh_path,
            )

    ### PRIVATE METHODS ###

    def _extract_productions_from_parser_output(
        self,
        file_path,
        ):
        with open(file_path, 'r') as f:
            lines = f.read().split('\n')
        productions = { }
        nonterminal = None
        in_grammar = False
        for line in lines:
            text = line.strip()
            # starting and stopping
            if text == 'Terminals, with rules where they appear':
                break
            elif text == 'Grammar':
                in_grammar = True
                continue
            if not in_grammar:
                continue
            if not text:
                continue
            parts = text.split()[1:]
            if parts[0].startswith('$'):
                continue
            elif parts[0] == '|':
                right_hand = filter(lambda x: not x.startswith('$'), parts[1:])
                productions[nonterminal].append(parts[1:])
            else:
                nonterminal = parts[0][:-1]
                if nonterminal not in productions:
                    productions[nonterminal] = []
                right_hand = parts[1:]
                if right_hand[0] == '/*': # /* empty */
                    productions[nonterminal].append([])
                else:
                    right_hand = filter(lambda x: not x.startswith('$'), right_hand)
                    productions[nonterminal].append(right_hand)
        return productions

    def _extract_token_names_from_parser_tab_hh(
        self,
        file_path,
        ):
        with open(file_path, 'r') as f:
            lines = f.read().split('\n')
        token_names = { }
        in_enum = False
        for line in lines:
            text = line.strip()
            if in_enum and text == '};':
                break;
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
        file_path,
        ):
        with open(file_path, 'r') as f:
            lines = f.read().split('\n')
        token_values = { }
        in_token_list = False
        for line in lines:
            text = line.strip()
            if in_token_list and text == 'Nonterminals, with rules where they appear':
                break;
            elif text == 'Terminals, with rules where they appear':
                in_token_list = True
                continue
            elif not text:
                continue
            elif not in_token_list:
                continue
            parts = text.split()
            if parts[0].isdigit():
                continue
            elif parts[0].startswith('$'):
                continue
            value = parts[0]
            number = int(parts[1][1:-1])
            token_values[number] = value
        return token_values

    def _generate_production_map(
        self,
        output_path,
        tab_hh_path,
        ):
        productions = self._extract_productions_from_parser_output(
            output_path)
        names = self._extract_token_names_from_parser_tab_hh(
            tab_hh_path)
        values = self._extract_token_values_from_parser_output(
            output_path)
        matches = self._match_token_names_with_token_values(
            names, values)
        rewrites = { }
        for nonterminal in productions:
            for rh in productions[nonterminal]:
                for i, r in enumerate(rh):
                    if r in matches:
                        rh[i] = matches[r]
                docstring = '{} : {}'.format(nonterminal, ' '.join(rh))
                for i, r in enumerate(rh):
                    if r[0] == "'" and r[-1] == "'":
                        rh[i] = 'Chr{}'.format(ord(r[-2]))
                funcname = 'p_{}__{}'.format(nonterminal, '__'.join(rh))
                rewrites[funcname] = docstring
        return rewrites

    def _match_token_names_with_token_values(
        self,
        names,
        values,
        ):
        matches = { }
        for number, value in values.items():
            if number in names:
                name = names[number]
                matches[value] = name
        return matches

    def _write_parser_syntax_skeleton(
        self,
        skeleton_path,
        parser_output_path,
        parser_tab_hh_path,
        ):
        productions = self._generate_production_map(
            parser_output_path, parser_tab_hh_path)
        with open(skeleton_path, 'w') as f:
            f.write('from abjad import *\n')
            f.write('from abjad.parser.SyntaxNode.SyntaxNode \\\n')
            f.write('    import SyntaxNode as Node\n\n\n')
            f.write('class _LilyPondSyntacticalDefinition(object):\n\n')
            f.write('    def __init__(self, client):\n')
            f.write('        self.client = client\n')
            f.write('        self.tokens = self.client.lexdef.tokens\n\n\n')
            f.write("    start_symbol = 'start_symbol'\n\n\n")
            f.write("    precedence = (\n")
            f.write("        ('nonassoc', 'COMPOSITE'),\n")
            f.write("        ('nonassoc', 'REPEAT'),\n")
            f.write("        ('nonassoc', 'ALTERNATIVE'),\n")
            f.write("        ('left', 'ADDLYRICS'),\n")
            f.write("        ('nonassoc', 'DEFAULT'),\n")
            f.write("        ('nonassoc', 'FUNCTION_ARGLIST'),\n")
            f.write("        ('right', 'PITCH_IDENTIFIER', 'NOTENAME_PITCH', 'TONICNAME_PITCH', 'UNSIGNED', 'REAL', 'DURATION_IDENTIFIER', ':'),\n")
            f.write("        ('nonassoc', 'NUMBER_IDENTIFIER', '/'),\n")
            f.write("    )\n\n\n")
            f.write('    ### SYNTACTICAL RULES (ALPHABETICAL) ###\n\n\n')
            current_nonterminal = 'start_symbol'
            ly_keys = sorted(key for key in productions
                if key.startswith('p_start_symbol'))
            for key in ly_keys:
                funcname = key
                docstring = productions[key]
                f.write('    def {}(self, p):\n'.format(funcname))
                f.write("        {!r}\n".format(docstring))
                f.write("        p[0] = Node('{}', p[1:])\n\n\n".format(
                    current_nonterminal))
            for funcname, docstring in sorted(productions.items()):
                nonterminal = funcname.split('__')[0][2:]
                if nonterminal == 'start_symbol':
                    continue
                if nonterminal != current_nonterminal:
                    current_nonterminal = nonterminal
                    f.write('    ### {} ###\n\n\n'.format(current_nonterminal))
                f.write('    def {}(self, p):\n'.format(funcname))
                f.write("        {!r}\n".format(docstring))
                f.write("        p[0] = Node('{}', p[1:])\n\n\n".format(
                    current_nonterminal))
            f.write('    def p_error(self, p):\n')
            f.write('        pass\n\n')
