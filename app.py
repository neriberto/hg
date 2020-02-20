"""HG - Hazardous Garbage, a malware collector."""

# -*- coding: utf-8 -*-

import asyncio
import hashlib
import os

import click
from malwarefeeds.engine import Engine
from requests import get


class GarbageCollector:
    """The Hazardous Garbage Collector class."""

    def __init__(self, repo: str):
        """Class construtor."""
        if repo and repo != '':
            self.repo = repo
        else:
            self.repo = os.path.expanduser(os.path.join('~', '.samples'))

    def store_file(self, content: bytes):
        """Store a file in hard drive."""
        file_hash = hashlib.sha256(content).hexdigest()
        directory = os.path.join(
            self.repo,
            file_hash[0],
            file_hash[1],
            file_hash[2],
            file_hash[3])

        if not os.path.isdir(directory):
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
        io_loop = asyncio.get_event_loop()
        q = asyncio.Queue(loop=io_loop)
        producer = GarbageCollector.download_from_feeds(q)
        consumer = self.download_samples(q)
        io_loop.run_until_complete(asyncio.gather(producer, consumer))
        io_loop.close()

    @staticmethod
    async def download_from_feeds(q):
        """Download the feeds and put each url in queue."""
        engine = Engine()
        engine.download()
        for _, url in engine.get_urls():
            if not url.startswith('http://'):
                url = f'http://{url}'
            await q.put(url)

        await q.put(None)

    async def download_samples(self, q):
        """Get an URL from queue and try download it."""
        while True:
            url = await q.get()
            if url is None:
                break

            print("Downloading URL: %s" % url)
            content = GarbageCollector.download(url=url)
            if content:
                self.store_file(content)
            q.task_done()

    @staticmethod
    def download(url):
        """Safe download that logs the exceptions."""
        try:
            r = get(url, stream=True)
            return r.content
        except Exception as ex:
            print(ex)
            return None


@click.command()
@click.option('--repo', default='', help='The directory to store files')
def cli(repo):
    """A command line parser."""
    try:
        collector = GarbageCollector(repo=repo)
        collector.run()
    except KeyboardInterrupt:
        pass
    except PermissionError as ex:
        print(ex)
    except SystemExit:
        pass


if __name__ == "__main__":
    cli(None)
