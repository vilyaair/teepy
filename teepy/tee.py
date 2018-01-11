import contextlib


@contextlib.contextmanager
def tee(input, *files, mode='w', filter=None):
    '''Duplicates input stream to output stream and also to any files.

    Arguments:
    input: A file object, either a text file or binary file.
    Usually sys.stdout, sys.stderr, sys.stdout.buffer or sys.stderr.buffer

    *files: The pathname of files to be opened in the similar mode with the input.

    mode: An optional string that specifies the mode in which the files are opened.
    It defaults to 'w' for writing, and uses 'a' for appending.

    Examples:
    >>> import sys
    >>> from teepy import tee
    >>> def files_filter(text):
    ...     lines = text.splitlines(keepends=True)
    ...     return ''.join(line for line in lines if '\\n' in line)
    ...
    >>> with tee(sys.stdout, 'output.txt', filter=files_filter), tee(sys.stderr, 'error1.txt', 'error2.txt'):
    ...     sys.stdout.write('[info]:stdout\\n[0%]\\r[50%]\\r[100%]\\r[info]:stdout\\n')
    ...     sys.stderr.write('This is a copy of stderr!\\n')
    ...
    [info]:stdout
    [info]:stdout
    This is a copy of stderr!

    '''

    original_write = input.write
    file_list = [open(file, mode + input.mode[1:]) for file in files]

    def duplicate(data):
        original_write(data)
        if filter:
            data = filter(data)
        for f in file_list:
            f.write(data)

    input.write = duplicate
    yield
    input.write = original_write
    for f in file_list:
        f.close()
