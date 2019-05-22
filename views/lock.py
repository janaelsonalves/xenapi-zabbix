import fcntl

class Lock:
    """
    Lock class s for a system wide unix lock
    """
    def __init__(self, filename):
        """
        init of class Lock

        Args:
        filename (str): path of file will be use for locking (eg. /tmp/mylockfile)
        """
        self.filename = filename
        self.handle = open(filename, 'w')
 
    def acquire(self):
        """
        class function acuire - start lock
        """
        fcntl.flock(self.handle, fcntl.LOCK_EX)

    def release(self):
        """
        class function release - end lock
        """
        fcntl.flock(self.handle, fcntl.LOCK_UN)
 
    def __del__(self):
        """
        del of class Lock
        """
        self.handle.close()
        if os.path.isfile(self.filename): os.remove(self.filename)