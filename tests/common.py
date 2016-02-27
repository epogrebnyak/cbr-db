"""
Common test utils.
"""
import io


def read_tail(file_path, length):
    """
    Reads file tail of the given length.
    """
    with open(file_path) as file:
        file.seek(0, io.SEEK_END)
        file.seek(file.tell() - length, io.SEEK_SET)
        return file.read()
