def _extract_productions_from_parser_output(filepath):
    f = open(filepath, 'r')
    lines = f.read( ).split('\n')
    f.close( )

    productions = { }
    nonterminal = None
    in_grammar = False

    for line in lines:

        text = line.strip( )

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

        parts = text.split( )[1:]

        if parts[0].startswith('$'):
            continue

        elif parts[0] == '|':
            right_hand = filter(lambda x: not x.startswith('$'), parts[1:])
            productions[nonterminal].append(parts[1:])

        else:
            nonterminal = parts[0][:-1]
            if nonterminal not in productions:
                productions[nonterminal] = [ ]

            right_hand = parts[1:]
            if right_hand[0] == '/*': # /* empty */
                productions[nonterminal].append([ ])
            else:
                right_hand = filter(lambda x: not x.startswith('$'), right_hand)
                productions[nonterminal].append(right_hand)

    return productions
