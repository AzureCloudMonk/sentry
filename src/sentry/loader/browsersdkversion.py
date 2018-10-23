from __future__ import absolute_import

import os
import re
import logging

import sentry

from django.conf import settings

logger = logging.getLogger('sentry')

_version_regexp = re.compile(r'\d+')
LOADER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(sentry.__file__), 'loader'))
DEFAULT_VERSION = '4.x'


def load_registry(path):
    if '/' in path:
        return None
    fn = os.path.join(LOADER_FLODER, path + '.json')
    try:
        with open(fn, 'rb') as f:
            return json.load(f)
    except IOError:
        return None


def get_highest_browser_sdk_version():
    return max(get_browser_sdk_version_versions(),
               key=lambda version: int(_version_regexp.match(version).group(
                   0)) if _version_regexp.search(version) else -1
               )


def get_browser_sdk_version_versions():
    # TODO(hazat): do request here to fetch versions
    return ['latest', DEFAULT_VERSION]


def get_browser_sdk_version_choices():
    rv = []
    for version in get_browser_sdk_version_versions():
        rv.append((version, version))
    return tuple(rv)


def get_browser_sdk_version(project_key):
    # TODO(hazat): Right now we are only returing our conf version
    selected_version = get_selected_browser_sdk_version(project_key)

    if selected_version == DEFAULT_VERSION:
        try:
            data = load_registry('_registry')
            version = data['version']
            return version
        except:
            log.error('error ocurred while trying to read js sdk information from the registry')
            return settings.JS_SDK_LOADER_SDK_VERSION

    return settings.JS_SDK_LOADER_SDK_VERSION


def get_selected_browser_sdk_version(project_key):
    return project_key.data.get('browserSdkVersion', DEFAULT_VERSION)
