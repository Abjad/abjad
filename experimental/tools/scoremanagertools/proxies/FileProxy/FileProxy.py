import os
from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy


class FileProxy(AssetProxy):

    ### CLASS ATTRIBUTES ###

    generic_class_name = 'file'
    temporary_asset_name = 'temporary_file.txt'

    ### INITIALIZER ###

    def __init__(self, file_path=None, session=None):
        AssetProxy.__init__(self, asset_filesystem_path=file_path, session=session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def extension(self):
        return ''

    @property
    def file_lines(self):
        result = []
        if self.file_path:
            if os.path.exists(self.file_path):
                file_pointer = file(self.file_path)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    @property
    def file_path(self):
        return self.asset_filesystem_path

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        return self.file_lines

    ### PUBLIC METHODS ###

    def conditionally_make_empty_asset(self, is_interactive=False):
        if not os.path.exists(self.file_path):
            file_reference = file(self.file_path, 'w')
            file_reference.write('')
            file_reference.close()
        self.io.proceed(is_interactive=is_interactive)

    def display_formatted_lines(self):
        self.io.display(self.formatted_lines)

    def edit(self):
        os.system('vi + {}'.format(self.file_path))

    def fix(self):
        pass

    def has_line(self, line):
        file_reference = open(self.file_path, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    def profile(self):
        pass

    def view(self):
        os.system('vi -R {}'.format(self.file_path))
