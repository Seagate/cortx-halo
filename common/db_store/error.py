class DBError(Exception):

    def __init__(self, message, rc=1, *args):
        """Handle Exception in DB store."""
        self._rc = rc
        self._desc = message % (args)

    @property
    def rc(self):
        return self._rc

    @property
    def desc(self):
        return self._desc

    def __str__(self):
        """String representation of the object."""
        if self._rc == 0:
            return self._desc
        return "error(%d): %s" % (self._rc, self._desc)
