# For testing: dump the contents of the initfs.
import os
from machine import Pin

# Restore the initial filesystem.
def restore():
    print("Restoring initial filesystem")

    import initfs
    import tarfile
    import deflate
    import errno
    import io
    import os
    from machine import Pin

    def maybe_mkdir(filename):
        if filename[-1] == '/':
            filename = filename[:-1]
        try:
            os.mkdir(filename)
        except OSError as e:
            if e.errno == errno.EEXIST:
                return
            raise e

    with deflate.DeflateIO(io.BytesIO(initfs.tarball)) as gzfile:
        tf = tarfile.TarFile(fileobj=gzfile)
        for i in tf:
            # Strip the leading directory.
            filename=i.name.split('/', 1)[1]
            if len(filename) == 0:
                continue

            print(filename)
            if i.type == tarfile.DIRTYPE:
                maybe_mkdir(filename)
            else:
                fp = tf.extractfile(i)
                with open(filename, "wb") as outfile:
                    outfile.write(fp.read())

if __name__ == '__main__':
    # Automatically restore the filesystem if main.py is missing.
    if "main.py" not in os.listdir("/"):
        restore()

    # If both SW4 and SW5 are pressed at boot - restore the filesystem.
    else:
        sw4 = Pin(10, Pin.IN)
        sw5 = Pin(11, Pin.IN)
        if sw4.value() == 0 and sw5.value() == 0:
            restore()

        del sw4, sw5
