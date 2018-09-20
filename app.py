#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import os
import sys
import asyncio
from requests import get
from malwarefeeds.engine import Engine

SAMPLES_PATH = os.path.expanduser('~/.samples')


def store_file(content):
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
    e = Engine()
    e.update()
    for feed, url in e.read():
        await q.put(url)

    await q.put(None)


async def download_samples(q):
    while True:
        url = await q.get()
        if url is None:
            break

        print("URL: %s" % url)
        r = get(url, stream=True)
        store_file(r.content)
        q.task_done()


if __name__ == '__main__':
    try:
        ioloop = asyncio.get_event_loop()
        q = asyncio.Queue(loop=ioloop)
        producer = download_from_feeds(q)
        consumer = download_samples(q)
        ioloop.run_until_complete(asyncio.gather(producer, consumer))
        ioloop.close()
    except KeyboardInterrupt:
        sys.exit()
    except SystemExit:
        pass
