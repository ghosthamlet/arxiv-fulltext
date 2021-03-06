"""
Flask configuration.

Docstrings are from the `Flask configuration documentation
<http://flask.pocoo.org/docs/0.12/config/>`_.
"""
import os
import re

ON = 'yes'
OFF = 'no'

DEBUG = os.environ.get('DEBUG') == ON
"""enable/disable debug mode"""

TESTING = os.environ.get('TESTING') == ON
"""enable/disable testing mode"""

PROPAGATE_EXCEPTIONS = \
    True if os.environ.get('PROPAGATE_EXCEPTIONS') == ON else None
"""
explicitly enable or disable the propagation of exceptions. If not set or
explicitly set to None this is implicitly true if either TESTING or DEBUG is
true.
"""

PRESERVE_CONTEXT_ON_EXCEPTION = \
    True if os.environ.get('PRESERVE_CONTEXT_ON_EXCEPTION') == ON else None
"""
By default if the application is in debug mode the request context is not
popped on exceptions to enable debuggers to introspect the data. This can be
disabled by this key. You can also use this setting to force-enable it for non
debug execution which might be useful to debug production applications (but
also very risky).
"""

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf1234')
"""
the secret key
"""

SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', 'fulltext')
"""
the name of the session cookie
"""

SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN', None)
"""
the domain for the session cookie. If this is not set, the cookie will be valid
for all subdomains of SERVER_NAME.
"""

SESSION_COOKIE_PATH = os.environ.get('SESSION_COOKIE_PATH', None)
"""
the path for the session cookie. If this is not set the cookie will be valid
for all of APPLICATION_ROOT or if that is not set for '/'.
"""

SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY') != OFF
"""
controls if the cookie should be set with the httponly flag. Defaults to True.
"""

SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE') == ON
"""
controls if the cookie should be set with the secure flag. Defaults to False.
"""

PERMANENT_SESSION_LIFETIME = \
    int(os.environ.get('PERMANENT_SESSION_LIFETIME', '3600'))
"""
the lifetime of a permanent session as datetime.timedelta object. Starting with
Flask 0.8 this can also be an integer representing seconds.
"""

SESSION_REFRESH_EACH_REQUEST = \
    os.environ.get('SESSION_REFRESH_EACH_REQUEST') != OFF
"""
this flag controls how permanent sessions are refreshed. If set to True (which
is the default) then the cookie is refreshed each request which automatically
bumps the lifetime. If set to False a set-cookie header is only sent if the
session is modified. Non permanent sessions are not affected by this.
"""

USE_X_SENDFILE = os.environ.get('USE_X_SENDFILE') == ON
"""
enable/disable x-sendfile
"""

LOGGER_NAME = os.environ.get('LOGGER_NAME', 'fulltext')
"""
the name of the logger
"""

LOGGER_HANDLER_POLICY = os.environ.get('LOGGER_HANDLER_POLICY', 'always')
"""
the policy of the default logging handler. The default is 'always' which means
that the default logging handler is always active. 'debug' will only activate
logging in debug mode, 'production' will only log in production and 'never'
disables it entirely.
"""

SERVER_NAME = os.environ.get('FULLTEXT_SERVER_NAME', None)
"""
the name and port number of the server. Required for subdomain support (e.g.:
'myapp.dev:5000') Note that localhost does not support subdomains so setting
this to "localhost" does not help. Setting a SERVER_NAME also by default
enables URL generation without a request context but with an application
context.
"""

APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT', None)
"""
If the application does not occupy a whole domain or subdomain this can be set
to the path where the application is configured to live. This is for session
cookie as path value. If domains are used, this should be None.
"""

MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH', None)
"""
If set to a value in bytes, Flask will reject incoming requests with a content
length greater than this by returning a 413 status code.
"""

SEND_FILE_MAX_AGE_DEFAULT = int(os.environ.get('SEND_FILE_MAX_AGE_DEFAULT', 43200))
"""
Default cache control max age to use with send_static_file() (the default
static file handler) and send_file(), as datetime.timedelta or as seconds.
Override this value on a per-file basis using the get_send_file_max_age() hook
on Flask or Blueprint, respectively. Defaults to 43200 (12 hours).
"""

TRAP_HTTP_EXCEPTIONS = os.environ.get('TRAP_HTTP_EXCEPTIONS') == ON
"""
If this is set to True Flask will not execute the error handlers of HTTP
exceptions but instead treat the exception like any other and bubble it through
the exception stack. This is helpful for hairy debugging situations where you
have to find out where an HTTP exception is coming from.
"""

TRAP_BAD_REQUEST_ERRORS = os.environ.get('TRAP_BAD_REQUEST_ERRORS') == ON
"""
Werkzeug's internal data structures that deal with request specific data will
raise special key errors that are also bad request exceptions. Likewise many
operations can implicitly fail with a BadRequest exception for consistency.
Since it’s nice for debugging to know why exactly it failed this flag can be
used to debug those situations. If this config is set to True you will get a
regular traceback instead.
"""

PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'http')
"""
The URL scheme that should be used for URL generation if no URL scheme is
available. This defaults to http.
"""

JSON_AS_ASCII = os.environ.get('JSON_AS_ASCII') == ON
"""
By default Flask serialize object to ascii-encoded JSON. If this is set to
False Flask will not encode to ASCII and output strings as-is and return
unicode strings. jsonify will automatically encode it in utf-8 then for
transport for instance.
"""

JSON_SORT_KEYS = os.environ.get('JSON_AS_ASCII') != OFF
"""
By default Flask will serialize JSON objects in a way that the keys are ordered.
This is done in order to ensure that independent of the hash seed of the
dictionary the return value will be consistent to not trash external HTTP
caches. You can override the default behavior by changing this variable.
This is not recommended but might give you a performance improvement on the
cost of cacheability.
"""

JSONIFY_PRETTYPRINT_REGULAR = os.environ.get('JSON_AS_ASCII') != OFF
"""
If this is set to True (the default) jsonify responses will be pretty printed
if they are not requested by an XMLHttpRequest object (controlled by the
X-Requested-With header).
"""

JSONIFY_MIMETYPE = os.environ.get('JSONIFY_MIMETYPE', 'application/json')
"""
MIME type used for jsonify responses.
"""

TEMPLATES_AUTO_RELOAD = os.environ.get('TEMPLATES_AUTO_RELOAD') == ON
"""
Whether to check for modifications of the template source and reload it
automatically. By default the value is None which means that Flask checks
original file only in debug mode.
"""

EXPLAIN_TEMPLATE_LOADING = os.environ.get('EXPLAIN_TEMPLATE_LOADING') == ON
"""
If this is enabled then every attempt to load a template will write an info
message to the logger explaining the attempts to locate the template. This can
be useful to figure out why templates cannot be found or wrong templates appear
to be loaded.
"""

# SUBMISSION_DATABASE_URL = os.environ.get('SUBMISSION_DATABASE_URL')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_SHARED_CREDENTIALS_FILE = os.environ.get('AWS_SHARED_CREDENTIALS_FILE', None)
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
if (AWS_ACCESS_KEY_ID is None
        and AWS_SECRET_ACCESS_KEY is None
        and AWS_SHARED_CREDENTIALS_FILE is not None):
    try:
        with open(AWS_SHARED_CREDENTIALS_FILE) as f:
            _raw = f.read()
            _match = re.search(
                r"\[default\]\naws_access_key_id=(.*)\naws_secret_access_key=(.*)",
                _raw
            )
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = _match.groups()
            os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
            os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    except Exception as e:
        print('could not load credentials: %s' % e)
        pass

SOURCE_WHITELIST = os.environ.get('SOURCE_WHITELIST',
                                  'arxiv.org,export.arxiv.org')


FULLTEXT_DOCKER_IMAGE = os.environ.get('FULLTEXT_DOCKER_IMAGE',
                                       'arxiv/fulltext-extractor:0.3')

# Settings for the indexing agent.
KINESIS_ENDPOINT = os.environ.get('KINESIS_ENDPOINT')
"""Can be used to set an alternate endpoint, e.g. for testing."""

KINESIS_VERIFY = os.environ.get('KINESIS_VERIFY', "true")
"""Indicates whether SSL certificate verification should be enforced."""

KINESIS_STREAM = os.environ.get('KINESIS_STREAM', 'PDFIsAvailable')
"""Name of the stream to which the indexing agent subscribes."""

KINESIS_SHARD_ID = os.environ.get('KINESIS_SHARD_ID', '0')

KINESIS_CHECKPOINT_VOLUME = os.environ.get('KINESIS_CHECKPOINT_VOLUME',
                                           '/tmp')

KINESIS_START_TYPE = os.environ.get('KINESIS_START_TYPE', 'AT_TIMESTAMP')
KINESIS_START_AT = os.environ.get('KINESIS_START_AT')

KINESIS_SLEEP = os.environ.get('KINESIS_SLEEP', '0.1')
"""Amount of time to wait before moving on to the next record."""


REDIS_ENDPOINT = os.environ.get('REDIS_ENDPOINT')

BASE_SERVER = 'arxiv.org'
URLS = [
    ('submission_pdf', '/pdf/<submission_id>', BASE_SERVER),
    ('pdf', '/pdf/<paper_id>', BASE_SERVER)
]

VERSION = '0.3'
"""
The extractor version, used to sign extracted fulltext.

This should only be incremented when the extraction process itself changes,
not when the API of this web application changes.
"""

WORKDIR = os.environ.get('WORKDIR', '/tmp')
STORAGE_VOLUME = os.environ.get('STORAGE_VOLUME', '/tmp/storage')
