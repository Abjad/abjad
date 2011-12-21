def _match_token_names_with_token_values(names, values):

    matches = { }

    for number, value in values.iteritems( ):
        if number in names:
            name = names[number]
            matches[value] = name

    return matches
        
