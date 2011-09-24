import os
import unittest
import gevent

#import inotifyx as inotify
import gevent_inotifyx as inotify

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.workdir = os.path.abspath(os.getcwd())
        self.testdir = os.path.join(self.workdir, 'test')
        os.mkdir(self.testdir)
        os.chdir(self.testdir)
        self.fd = inotify.init()

    def tearDown(self):
        os.close(self.fd)
        os.rmdir(self.testdir)
        os.chdir(self.workdir)

    def _create_file(self, path, content = ''):
        f = open(path, 'w')
        try:
            f.write(content)
        finally:
            f.close()

    def test_get_events(self):
        wd = inotify.add_watch(self.fd, self.testdir, inotify.IN_CREATE)
        self._create_file('foo')
        try:
            events = inotify.get_events(self.fd)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].mask, inotify.IN_CREATE)
            self.assertEqual(events[0].name, 'foo')
        finally:
            os.unlink('foo')

    def test_get_events_async(self):
        wd = inotify.add_watch(self.fd, self.testdir, inotify.IN_CREATE)
        task1 = gevent.spawn(inotify.get_events, self.fd, 10)
        task2 = gevent.spawn(self._create_file, 'bar')
        try:
            # in the synchronous case we would block here for 10s and the
            # return value in task1.value would be empty
            task1.join()
            task2.join()
            events = task1.value
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].mask, inotify.IN_CREATE)
            self.assertEqual(events[0].name, 'bar')
        finally:
            os.unlink('bar')

if __name__ == "__main__":
    unittest.main()

