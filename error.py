class PySideInotifyError(Exception):
    """Indicates exceptions raised by a PySideInotify class."""
    pass


class PysideNotFoundError(PySideInotifyError):
    def __init__(self):
        err = "not find pyside, Please install"
        PySideInotifyError.__init__(self, err)
