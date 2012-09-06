def _cycle_token_to_sieve(cycle_token):
    r'''.. versionadded:: 2.0

    Make Xenakis sieve from `cycle_token`.

    When `cycle_token` has length 2, interpret `cycle_token` as ``modulo, residues`` pair. ::

        >>> from abjad.tools.sievetools._cycle_token_to_sieve import _cycle_token_to_sieve

        >>> cycle_token = (6, [0, 4, 5])
        >>> _cycle_token_to_sieve(cycle_token)
        {ResidueClass(6, 0) | ResidueClass(6, 4) | ResidueClass(6, 5)}

    When `cycle_token` has length 3, interpret `cycle_token` as ``modulo, residues, offset`` triple. ::

        >>> cycle_token = (10, [0, 1, 2], 6)
        >>> _cycle_token_to_sieve(cycle_token)
        {ResidueClass(10, 6) | ResidueClass(10, 7) | ResidueClass(10, 8)}

    Return sieve.
    '''
    from abjad.tools import sievetools

    # sieves count as cycle tokens in themselves
    if isinstance(cycle_token, sievetools.ResidueClassExpression):
        return sievetools.ResidueClassExpression(cycle_token)

    # parse cycle token
    modulo = cycle_token[0]
    residues = cycle_token[1]
    try:
        offset = cycle_token[2]
    except IndexError:
        offset = 0

    # create residue classes from cycle token
    residue_classes = []
    for residue in residues:
        adjusted_residue = (residue + offset) % modulo
        residue_class = sievetools.ResidueClass(modulo, adjusted_residue)
        residue_classes.append(residue_class)

    residue_classes.sort(lambda x, y: cmp(x.residue, y.residue))

    # return sieve as residue class combination
    sieve = sievetools.ResidueClassExpression(residue_classes, operator='or')
    return sieve
