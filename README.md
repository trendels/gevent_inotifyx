# gevent_inotifyx

[![build-status-img]][build-status-url]

Gevent-compatible low-level inotify bindings based on [inotifyx].

  - Python 2 and 3 compatible
  - Exposes a low-level [inotify(7)][inotify] API
  - Allows to wait for events in a non-blocking way when using [gevent].

[inotify]: http://man7.org/linux/man-pages/man7/inotify.7.html
[inotifyx]: https://launchpad.net/inotifyx/
[gevent]: http://www.gevent.org/
[build-status-url]: https://travis-ci.org/trendels/gevent_inotifyx
[build-status-img]: https://travis-ci.org/trendels/gevent_inotifyx.svg

## Installation

    $ pip install gevent_inotifyx

From source:

    $ python setup.py install

To run the tests:

    $ python setup.py test

## Examples

Watch a directory while creating new files. This prints

    event: test.txt IN_CLOSE|IN_CLOSE_WRITE|IN_ALL_EVENTS

every second:

```python
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
```

## License

gevent_inotifyx is licensed under the MIT License. See the included file `LICENSE` for details.
