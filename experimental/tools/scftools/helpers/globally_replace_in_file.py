def globally_replace_in_file(file_name, old, new):
    file_pointer = file(file_name, 'r')
    new_file_lines = []
    for line in file_pointer.readlines():
        line = line.replace(old, new)
        new_file_lines.append(line)
    file_pointer.close()
    file_pointer = file(file_name, 'w')
    file_pointer.write(''.join(new_file_lines))
    file_pointer.close()
