"""HG - Hazardous Garbage, a malware collector."""

# -*- coding: utf-8 -*-

__author__ = 'Neriberto C. Prado'
__maintainer__ = 'Neriberto C. Prado'
__email__ = 'neriberto@gmail.com'
__license__ = 'BSD 3-Clause License'
__version__ = '0.4.0'


import hashlib
import os
from queue import PriorityQueue

import click
from malwarefeeds.engine import Engine
from requests import get, head


class GarbageCollector:
    """The Hazardous Garbage Collector class."""

    def __init__(self, repo: str):
        """Class construtor."""
        self.queue = PriorityQueue()
        if repo and repo != '':
            self.repo = repo
        else:
            self.repo = os.path.expanduser(os.path.join('~', '.samples'))

    def store_file(self, content: bytes):
        """Store a file in hard drive."""
        if not content or len(content) <= 0:
            return

        file_hash = hashlib.sha256(content).hexdigest()
        directory = os.path.join(
            self.repo,
            file_hash[0],
            file_hash[1],
            file_hash[2],
            file_hash[3]
        )

        if not os.path.isdir(directory):
            return

        if os.path.isdir(directory) and not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_hash)
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as fd:
                fd.write(content)

    def run(self):
        """Run to get the malware samples."""
        if not os.path.isdir(self.repo):
            print("Creating directory %s" % self.repo)
            os.makedirs(self.repo)

        print("Storing files in %s" % self.repo)
        self.download_from_feeds()
        self.download_samples()

    def download_from_feeds(self):
        """Download the feeds and put each url in queue."""
        engine = Engine()
        engine.download()
        for feed_name, url in engine.get_urls():
            if not url or not feed_name:
                continue

            if not url.startswith('http://'):
                url = f'http://{url}'

            try:
                status_code = head(url, timeout=10).status_code

                if status_code == 200:
                    priority = 1
                elif status_code == 404:
                    priority = 3
                else:
                    priority = 2

                self.queue.put((priority, feed_name, url))
                print(f'URL: {url}, priority: {priority}')
            except Exception as ex:
                message = str(ex)
                print(f'URL: {url}, error: {message}')
                continue

    def download_samples(self):
        """Get an URL from queue and try download it."""
        while not self.queue.empty():
            _, _, url = self.queue.get()

            if not url:
                self.queue.task_done()
                continue

            content = GarbageCollector.download(
                url=url
            )
            self.store_file(content)
            self.queue.task_done()

    @staticmethod
    def download(url):
        """Safe download that logs the exceptions."""
        try:
            print("Downloading URL: %s" % url)
            r = get(url, stream=True)
            return r.content
        except Exception as ex:
            print(ex)
            return None


@click.command()
@click.option('--repo', default='', help='The directory to store files')
def cli(repo):
    """
    HG - Hazardous Garbage, a malware collector.

    Version: 0.2.0
    """
    try:
        collector = GarbageCollector(repo=repo)
        collector.run()
    except KeyboardInterrupt:
        pass
    except PermissionError as ex:
        print(ex)
    except SystemExit:
        pass
