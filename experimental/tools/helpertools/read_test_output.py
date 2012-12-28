import os


def read_test_output(full_file_name, current_function_name):
    r'''
    '''
    segment_ly_file_name = '{}.ly'.format(current_function_name)
    directory_name = os.path.dirname(full_file_name)
    segment_ly_path_name = os.path.join(directory_name, segment_ly_file_name)
    return file(segment_ly_path_name, 'r').read()
