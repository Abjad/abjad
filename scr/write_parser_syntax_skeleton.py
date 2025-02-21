#!/usr/bin/env python
import os
import sys

from abjad.parser.LilyPondGrammarGenerator import LilyPondGrammarGenerator


def usage():
    result = []
    result.append("")
    result.append("Usage:")
    result.append("")
    result.append(
        "write_parser_syntax_skeleton.py PARSER_output_PATH PARSER_TAB_HH_PATH SKELETON_PATH"
    )
    result.append("")
    result.append(
        "Given PARSER_output_PATH (to parser.output) and PARSER_TAB_HH_PATH (to parser.tab.hh),"
    )
    result.append(
        "generate a PLY-compliant parser skeleton, and write it to SKELETON_PATH."
    )
    result.append("")
    result = "\n".join(["\t" + line for line in result])
    return result


def write(parser_output_path, parser_tab_hh_path, skeleton_path):
    assert os.path.exists(parser_output_path)
    assert os.path.exists(parser_tab_hh_path)
    LilyPondGrammarGenerator()._write_parser_syntax_skeleton(
        skeleton_path,
        parser_output_path,
        parser_tab_hh_path,
    )


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(usage())
        sys.exit(2)
    parser_output_path = sys.argv[1]
    parser_tab_hh_path = sys.argv[2]
    skeleton_path = sys.argv[3]
    write(parser_output_path, parser_tab_hh_path, skeleton_path)
