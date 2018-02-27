gevent_inotifyx
===============

[gevent](http://www.gevent.org/) compatibility module for the
[inotifyx](http://www.alittletooquiet.net/software/inotifyx/) Python
inotify bindings.

This module is designed as a drop-in replacement for inotifyx. Calling
`gevent_inotifyx.get_events()` will only block the current greenlet
instead of the current thread.

Installation
------------

    $ pip install gevent_inotifyx

From source:

    $ python setup.py install

To run the tests:

    $ python setup.py test

You can also test the module from the command line:

    $ python -m gevent_inotifyx /some/path

will print inotify events for `/some/path`

Example
-------

Watch for newly created files and directories in `/tmp`:

    import os
    import gevent
    import gevent_inotifyx as inotify
    from gevent.queue import Queue

    def event_producer(fd, q):
       while True:
           events = inotify.get_events(fd)
           for event in events:
               q.put(event)

    q = Queue()
    fd = inotify.init()
    try:
        wd = inotify.add_watch(fd, '/tmp', inotify.IN_CREATE)
        gevent.spawn(event_producer, fd, q)
        while True:
           event = q.get()
           print "received event:", event.get_mask_description(), event.name
    finally:
        os.close(fd)
