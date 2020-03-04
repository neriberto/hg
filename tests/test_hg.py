from os.path import dirname
from unittest import mock, TestCase

from hg import GarbageCollector


class GarbageCollectorTestCase(TestCase):

    def setUp(self) -> None:
        self.collector = GarbageCollector(
            repo=dirname(__file__)
        )

    def test_constructor(self):
        """Test Garbage Collector construction."""
        self.assertIsInstance(self.collector, GarbageCollector)

    def test_constructor_without_repo(self):
        """Test Garbage Collector construction without repo."""
        collector = GarbageCollector(
            repo=None
        )
        self.assertIsInstance(collector, GarbageCollector)

    @mock.patch('hg.get')
    def test_download(self, mock_get):
        """Safe download that logs the exceptions."""
        mock_get.return_value = mock.MagicMock()
        mock_get.return_value.content = ''
        result = self.collector.download(
            url=''
        )
        self.assertEqual(result, '')

    @mock.patch('hg.get')
    def test_download_exception(self, mock_get):
        """Safe download that logs the exceptions."""
        mock_get.side_effect = Exception('Testing exceptions')
        result = self.collector.download(
            url=''
        )
        self.assertIsNone(result)

    @mock.patch('malwarefeeds.engine.Engine.download')
    @mock.patch('malwarefeeds.engine.Engine.get_urls')
    def test_download_from_feeds(self, get_urls, download):
        get_urls.return_value = [
            ('feed', 'http://my.url/'),
            ('feed', 'my.url'),
            ('feed', None)
        ]
        self.collector.download_from_feeds()
        get_urls.assert_called()
        download.assert_called()

    @mock.patch('hg.GarbageCollector.store_file')
    @mock.patch('hg.GarbageCollector.download')
    def test_download_samples(self, download, store_file):

        # First run in a empty queue
        self.collector.download_samples()

        # Second, populate the queue and try again
        download.return_value = None
        urls = [
            'http://my.url/',
            None,
            'my.url'
        ]

        for url in urls:
            self.collector.queue.put(url)

        self.collector.download_samples()

        download.assert_called()
        store_file.assert_called()

    def test_store_file(self):
        self.collector.repo = ''

        self.collector.store_file(
            content=None
        )

        self.collector.store_file(
            content=b'buffer'
        )

        self.collector.repo = dirname(__file__)
        self.collector.store_file(
            content=b'buffer'
        )

    @mock.patch('os.makedirs')
    @mock.patch('hg.GarbageCollector.download_samples')
    @mock.patch('hg.GarbageCollector.download_from_feeds')
    def test_run(self, from_feeds, samples, makedirs):
        self.collector.run()

        from_feeds.assert_called()
        samples.assert_called()

        self.collector.repo = ''
        self.collector.run()
        makedirs.assert_called()