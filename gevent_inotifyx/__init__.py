"""
gevent compatibility for inotifyx

General usage:
    >>> import os
    >>> import gevent_inotifyx as inotify
    >>> fd = inotify.init()
    >>> try:
    ...     wd = inotify.add_watch(fd, '/path', inotify.IN_CREATE)
    ...     events = inotify.get_events(fd)
    ...     for event in events:
    ...         print("File created: ", os.path.join('/path', event.name))
    ...     inotify.rm_watch(fd, wd)
    ... finally:
    ...     os.close(fd)


This module is designed as a drop-in replacement for inotifyx.
Calling gevent_inotifyx.get_events() will only block the current greenlet
instead of the current thread.
"""

__version__ = '0.2'

import os
import struct
import sys

from .vendor import inotifyx
from .vendor.inotifyx import *
from gevent.select import select

_EVENT_FMT = 'iIII'
_EVENT_SIZE = struct.calcsize(_EVENT_FMT)
_BUF_LEN = inotifyx.BUF_LEN

__all__ = ['InotifyEvent', 'add_watch', 'get_events', 'init', 'rm_watch']
__all__.extend([name for name in dir(inotifyx) if name.startswith('IN_')])

ENCODING = sys.getfilesystemencoding()

# Replacement for the inotifyx_get_events() C function using gevent.select
def get_events(fd, timeout=None):
    """get_events(fd[, timeout])

    Return a list of InotifyEvent instances representing events read from
    inotify.  If timeout is None, this will block forever until at least one
    event can be read.  Otherwise, timeout should be an integer or float
    specifying a timeout in seconds.  If get_events times out waiting for
    events, an empty list will be returned.  If timeout is zero, get_events
    will not block.
    This version of get_events() will only block the current greenlet.
    """
    (rlist, _, _) = select([fd], [], [], timeout)
    if not rlist:
        return []
    events = []

    while True:
        buf = os.read(fd, _BUF_LEN)
        i = 0
        while i < len(buf):
            (wd, mask, cookie, len_) = struct.unpack_from(_EVENT_FMT, buf, i)
            name = None
            if len_ > 0:
                start = i + _EVENT_SIZE
                end = start + len_
                # remove \0 terminator and padding
                name = buf[start:end].rstrip(b'\0').decode(ENCODING)

            events.append(InotifyEvent(wd, mask, cookie, name))
            i += _EVENT_SIZE + len_

        (rlist, _, _) = select([fd], [], [], 0)
        if not rlist:
            break

    return events

# Reproduced here from inotifyx/__init__.py to enable command line use:
#   $ python -m gevent_inofityx /path
if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        sys.stderr.write('usage: gevent_inotifyx path [path ...]\n')
        sys.exit(1)

    paths = sys.argv[1:]
    fd = init()
    wd_to_path = {}
    try:
        for path in paths:
            wd = add_watch(fd, path)
            wd_to_path[wd] = path
        try:
            while True:
                events = get_events(fd)
                for event in events:
                    path = wd_to_path[event.wd]
                    parts = [event.get_mask_description()]
                    if event.name:
                        parts.append(event.name)
                    print('%s: %s' % (path, ' '.join(parts)))
        except KeyboardInterrupt:
            pass

    finally:
        os.close(fd)

