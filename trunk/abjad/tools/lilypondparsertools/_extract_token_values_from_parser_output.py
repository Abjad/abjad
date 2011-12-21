def _extract_token_values_from_parser_output(filepath):

    f = open(filepath, 'r')
    lines = f.read( ).split('\n')
    f.close( )

    token_values = { }
    in_token_list = False

    for line in lines:

        text = line.strip( )

        if in_token_list and text == 'Nonterminals, with rules where they appear':
            break;
        elif text == 'Terminals, with rules where they appear':
            in_token_list = True
            continue
        elif not text:
            continue
        elif not in_token_list:
            continue

        parts = text.split( )

        if parts[0].isdigit( ):
            continue
        elif parts[0].startswith('$'):
            continue

        value = parts[0]
        number = int(parts[1][1:-1])

        token_values[number] = value

    return token_values
