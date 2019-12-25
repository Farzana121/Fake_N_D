import os
import errno
def create_dir(dir_name):
    """Create directory if folder not exist"""
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

