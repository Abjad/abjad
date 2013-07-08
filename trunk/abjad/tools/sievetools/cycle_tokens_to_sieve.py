def cycle_tokens_to_sieve(*cycle_tokens):
    '''.. versionadded:: 2.0

    Make Xenakis sieve from arbitrarily many `cycle_tokens`:

    ::

        >>> cycle_token_1 = (6, [0, 4, 5])
        >>> cycle_token_2 = (10, [0, 1, 2], 6)
        >>> sievetools.cycle_tokens_to_sieve(cycle_token_1, cycle_token_2)
        {ResidueClass(6, 0) | ResidueClass(6, 4) | ResidueClass(6, 5) |
         ResidueClass(10, 6) | ResidueClass(10, 7) | ResidueClass(10, 8)}

    Cycle token comprises `modulo`, `residues` and optional `offset`.
    '''
    from abjad.tools import sievetools

    def _cycle_token_to_sieve(cycle_token):
        if isinstance(cycle_token, sievetools.Sieve):
            return sievetools.Sieve(cycle_token)
        modulo = cycle_token[0]
        residues = cycle_token[1]
        try:
            offset = cycle_token[2]
        except IndexError:
            offset = 0
        residue_classes = []
        for residue in residues:
            adjusted_residue = (residue + offset) % modulo
            residue_class = sievetools.ResidueClass(modulo, adjusted_residue)
            residue_classes.append(residue_class)
        residue_classes.sort(key=lambda x: x.residue)
        sieve = sievetools.Sieve(residue_classes, logical_operator='or')
        return sieve

    sieves = []
    for cycle_token in cycle_tokens:
        sieve = _cycle_token_to_sieve(cycle_token)
        sieves.append(sieve)
    if sieves:
        current_sieve = sieves[0]
        for sieve in sieves[1:]:
            current_sieve = current_sieve | sieve
    else:
        current_sieve = sievetools.Sieve([])
    return current_sieve
