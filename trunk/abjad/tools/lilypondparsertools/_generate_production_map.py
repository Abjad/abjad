from abjad.tools.lilypondparsertools._extract_productions_from_parser_output \
    import _extract_productions_from_parser_output
from abjad.tools.lilypondparsertools._extract_token_names_from_parser_tab_hh \
    import _extract_token_names_from_parser_tab_hh
from abjad.tools.lilypondparsertools._extract_token_values_from_parser_output \
    import _extract_token_values_from_parser_output
from abjad.tools.lilypondparsertools._match_token_names_with_token_values \
    import _match_token_names_with_token_values


def _generate_production_map(output_path, tab_hh_path):

    productions = _extract_productions_from_parser_output(output_path)
    names = _extract_token_names_from_parser_tab_hh(tab_hh_path)
    values = _extract_token_values_from_parser_output(output_path)
    matches = _match_token_names_with_token_values(names, values)

    rewrites = { }

    for nonterminal in productions:
        for rh in productions[nonterminal]:
            for i, r in enumerate(rh):
                if r in matches:
                    rh[i] = matches[r]
            docstring = '%s : %s' % (nonterminal, ' '.join(rh))
            for i, r in enumerate(rh):
                if r[0] == "'" and r[-1] == "'":
                    rh[i] = 'Chr%d' % ord(r[-2])
            funcname = 'p_%s__%s' % (nonterminal, '__'.join(rh))
            rewrites[funcname] = docstring

    return rewrites
        
