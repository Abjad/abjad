def compare(string_1, string_2):

    split_lines = string_2.split('\n')

    if not split_lines[0] or split_lines.isspace():
        split_lines.pop(0)
    if not split_lines[-1] or split_lines[-1].isspace():
        split_lines.pop(-1)

    for indent_width, character in enumerate(split_lines[0]):
        if character != ' ':
            break

    tab_string = 4 * ' '
    massaged_lines = []
    for split_line in split_lines:
        massaged_line = split_line[indent_width:]
        massaged_line = massaged_line.replace(tab_string, '\t')
        massaged_lines.append(massaged_line)
    massaged_string = '\n'.join(massaged_lines)

    return string_1 == massaged_string
