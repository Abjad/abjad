# -*- encoding: utf-8 -*-
import collections
import os
from scoremanager.managers.FileManager \
    import FileManager


class MetadataModuleManager(FileManager):

    ### PUBLIC METHODS ###

    @staticmethod
    def make_metadata_lines(metadata):
        if metadata:
            lines = []
            for key, value in sorted(metadata.iteritems()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = \
                        value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    if hasattr(value, '_storage_format_specification'):
                        string = format(value)
                    else:
                        string = repr(value)
                    lines.append('({}, {})'.format(key, string))
            lines = ',\n    '.join(lines)
            result = 'tags = collections.OrderedDict([\n    {}])'.format(lines)
        else:
            result = 'tags = collections.OrderedDict([])'
        return result

    def write_metadata_to_disk(self, metadata):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('import collections\n')
        lines.append('\n\n')
        metadata_lines = self.make_metadata_lines(metadata) 
        lines.extend(metadata_lines)
        lines = ''.join(lines)
        file_pointer = file(self.filesystem_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()
