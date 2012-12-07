"""
gevent compatibility for inotifyx

Usage:
    >>> import gevent_inotifyx as inotifyx

This module is designed as a drop-in replacement for inotifyx.
Calling gevent_inotifyx.get_events() will only block the current greenlet
instead of the current thread.
"""

__version__ = '0.1.0'

import os
import struct

from inotifyx import *
from gevent.select import select

_EVENT_FMT = 'iIII'
_EVENT_SIZE = struct.calcsize(_EVENT_FMT)
_BUF_LEN = 1024 * (_EVENT_SIZE + 16)

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
                name = buf[start:end].rstrip('\0')

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
        print >>sys.stderr, 'usage: gevent_inotifyx path [path ...]'
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
                    print '%s: %s' % (path, ' '.join(parts))
        except KeyboardInterrupt:
            pass

    finally:
        os.close(fd)

