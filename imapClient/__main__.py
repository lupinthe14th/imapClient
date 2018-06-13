#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import INFO, basicConfig, getLogger

import chardet
from imbox import Imbox

logger = getLogger(__name__)
basicConfig(level=INFO)


def main():
    try:
        with Imbox(
                server=server,
                username=username,
                password=password,
                ssl=True,
                ssl_context=None,
                starttls=False,
        ) as imbox:
            return check(cm=imbox)
    except Exception as err:
        logger.error("detail: {}".format(err))
        raise


def check(cm):
    # Get all folders
    status, folders_with_additional_info = cm.folders()

    # Gets all messages
    all_messages = cm.messages(
        # unread=True,
    )

    for uid, message in all_messages:
        if len(message.body['plain']) != 0:
            for body in message.body['plain']:
                if isinstance(body, str):
                    encoding = chardet.detect(body.encode())
                    logger.info("encoding: {}".format(encoding))
                    encoding_charset = encoding['encoding']
                    logger.info(
                        "encoding_charset: {}".format(encoding_charset))
                    if encoding_charset == 'ascii':
                        logger.info(body.encode().decode('unicode-escape'))
                    elif encoding_charset == 'utf-8':
                        logger.info(body)
                    else:
                        logger.info(body.encode().decode('utf-8'))


if __name__ == '__main__':
    main()

# vim fileencoding=utf-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
