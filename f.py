from atlassian import Bitbucket
import requests
import os
import argparse
import logging
import json

from pprint import pprint, pformat
# from urllib.parse import urljoin

def get_env(env_url: str, env_username: str, env_password: str) -> (str, str, str):
    url = os.getenv(env_url)
    username = os.getenv(env_username)
    password = os.getenv(env_password)
    return url, username, password
# /def init


def get_bitbucket(url: str, username: str, password: str):
    # s = requests.Session()
    # s.headers['Authorization'] = 'Bearer {}'.format(token)
    bitbucket = Bitbucket(
        url=url,
        username=username,
        password=password
    )
    return bitbucket
# /def


def parse_args(default_name_prefix: str, default_description_prefix: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Create an Archive BitBucket Project'
    )
    parser.add_argument(
        '--dry-run',
        help='Enable dry-run (defaults to "false")',
        action='store_const',
        dest='dry_run',
        const=True, default=False,
    )
    parser.add_argument(
        '-s', '--source',
        dest='source_key',
        required=True,
        help=f'(required) Source Bitbucket project key'
    )
    parser.add_argument(
        '-d', '--destination',
        dest='destination_key',
        required=True,
        help=f'(required) Destination Bitbucket project key'
    )
    # parser.add_argument(
    #     '-k', '--key-append',
    #     dest='key_append',
    #     help=f'Character(s) to append to the end of the project\'s "key" (defaults to "{str_archive_project_key_append}")',
    #     default=str_archive_project_key_append,
    # )
    parser.add_argument(
        '--overwrite',
        help='Continue if Bitbucket source project already exists',
        action='store_const',
        dest='overwrite',
        const=True, default=False,
    )
    parser.add_argument(
        '--name-prefix',
        dest='name_prefix',
        help=f'String to prefix at the beginning of the project\'s name (defaults to "{default_name_prefix}")',
        default=default_name_prefix,
    )
    parser.add_argument(
        '--description-prefix',
        dest='description_prefix',
        help=f'Character(s) to append to the end of the project\'s description (defaults to "{default_description_prefix}")',
        default=default_description_prefix,
    )
    parser.add_argument(
        '--debug',
        help='Display "debugging" in output (defaults to "info")',
        action='store_const', dest='verbosity',
        const=logging.DEBUG, default=logging.INFO,
    )
    parser.add_argument(
        '--warning',
        help='Display "warning" in output only (no "info" messages)',
        action='store_const', dest='verbosity',
        const=logging.WARNING,
    )

    args = parser.parse_args()
    return args
# /def


def move_repo(token, headers, url_base, url_append, key):
    url = '/'.join(s.strip('/') for s in [url_base, url_append, key])
    logging.info(f'Bitbucket API URL: "{url}"')

    logging.info(f'Bitbucket API headers:\n{pformat(headers)}')

    payload = json.dumps({
        "key": key,
    })
    logging.info(f'Bitbucket API payload:\n{pformat(payload)}')


    response = requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers
    )
    # result = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    return response
# /def
