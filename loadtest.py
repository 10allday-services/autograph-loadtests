#!/usr/bin/env python
"""

Molotov loadtest script for autograph server

"""

import os
import json
import shutil
import aiohttp
import tempfile
from base64 import b64encode, b64decode
from signing_clients.apps import JarExtractor

from asynchawk import Signer
from molotov import scenario

GUID = 'tests@tests.mozilla.org'
PATH_XPI = './test-addon.xpi'
SIGNER = os.environ['SIGNER']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
TARGET = 'https://{0}:{1}/sign/data'.format(HOST, PORT)
HAWK_ID = os.environ['HAWK_ID']
HAWK_KEY = os.environ['HAWK_KEY']


@scenario(1)
async def call_signing(session):
    """Get the jar signature and send it to the signing server to be signed."""

    # We only want the (unique) temporary file name.
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_filename = temp_file.name

    # Extract jar signature.
    jar = JarExtractor(path=PATH_XPI)
    signed_manifest = jar.signatures

    # create the signing request
    sigreq = [{
        "input": bytes(b64encode(str(jar.signatures).encode("utf-8"))).decode("utf-8"), # noqa
        "keyid": SIGNER,
        "options": {
            "id": GUID,
        },
    }]

    # post the request
    signer = Signer(id=HAWK_ID, key=HAWK_KEY)
    async with aiohttp.ClientSession() as session:
        session = signer(session)
        resp = await session.post(TARGET, data=sigreq)
        try:
            sigresp = await resp.json()
        except Exception:
            sigresp = {'error': (await resp.text())}

        assert resp.status == 201, \
            'Posting to add-on signing failed:{0}'.format(json.dumps(sigresp))

        # convert the base64 encoded pkcs7 signature back to binary
        pkcs7 = b64decode(sigresp[0]["signature"])
        jar.make_signed(
            signed_manifest=str(signed_manifest).encode("utf-8"),
            signature=pkcs7,
            sigpath=u'mozilla',
            outpath=temp_filename)

        shutil.move(temp_filename, PATH_XPI)

        print("{0} signed!".format(PATH_XPI))
