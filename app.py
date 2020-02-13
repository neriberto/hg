"""HG - Hazardous Garbage, a malware collector."""

# -*- coding: utf-8 -*-

import asyncio
import hashlib
import os

import click
from malwarefeeds.engine import Engine
from requests import get

SAMPLES_PATH = os.path.expanduser('~/.samples')


def store_file(content: bytes):
    """Store a file in hard drive."""
    fhash = hashlib.sha256(content).hexdigest()
    directory = os.path.join(
        SAMPLES_PATH,
        fhash[0],
        fhash[1],
        fhash[2],
        fhash[3])
    if not os.path.isdir(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, fhash)
    if not os.path.exists(filepath):
        with open(filepath, 'wb') as fd:
            fd.write(content)


async def download_from_feeds(q):
    """Download the feeds and put each url in queue."""
    engine = Engine()
    engine.download()
    for _, url in engine.get_urls():
        if not url.startswith('http://'):
            url = f'http://{url}'
        await q.put(url)

    await q.put(None)


async def download_samples(q):
    """Get an URL from queue and try download it."""
    while True:
        url = await q.get()
        if url is None:
            break

        print("Downloading URL: %s" % url)
        r = get(url, stream=True)
        store_file(r.content)
        q.task_done()


@click.command()
@click.option('--repo', default=SAMPLES_PATH, help='The directory to store files')
def cli(repo):
    """A command line parser."""
    try:
        if not os.path.isdir(repo):
            print("Creating directory %s" % repo)
            os.makedirs(repo)

        SAMPLES_PATH = repo

        print("Storing files in %s" % SAMPLES_PATH)
        ioloop = asyncio.get_event_loop()
        q = asyncio.Queue(loop=ioloop)
        producer = download_from_feeds(q)
        consumer = download_samples(q)
        ioloop.run_until_complete(asyncio.gather(producer, consumer))
        ioloop.close()
    except KeyboardInterrupt:
        pass
    except PermissionError as ex:
        print(ex)
    except SystemExit:
        pass


if __name__ == "__main__":
    cli(None)
