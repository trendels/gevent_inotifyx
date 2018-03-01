#!/usr/bin/env python
from __future__ import print_function

import os
import gevent
import gevent_inotifyx as inotify

def create_file_events():
    """Open and close a file to generate inotify events."""
    while True:
        with open('/tmp/test.txt', 'a'):
            pass
        gevent.sleep(1)


def watch_for_events():
    """Wait for events and print them to stdout."""
    fd = inotify.init()
    try:
        wd = inotify.add_watch(fd, '/tmp', inotify.IN_CLOSE_WRITE)
        while True:
            for event in inotify.get_events(fd):
                print("event:", event.name, event.get_mask_description())
    finally:
        os.close(fd)

if __name__ == '__main__':
    tasks = [
        gevent.spawn(watch_for_events),
        gevent.spawn(create_file_events),
    ]
    gevent.joinall(tasks)
