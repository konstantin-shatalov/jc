"""jc - JSON CLI output utility INI Parser

Usage:

    Specify --ini as the first argument if the piped input is coming from an INI file or any
    simple key/value pair file. Delimiter can be '=' or ':'. Missing values are supported.
    Comment prefix can be '#' or ';'. Comments must be on their own line.

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ cat example.ini
    [DEFAULT]
    ServerAliveInterval = 45
    Compression = yes
    CompressionLevel = 9
    ForwardX11 = yes

    [bitbucket.org]
    User = hg

    [topsecret.server.com]
    Port = 50022
    ForwardX11 = no

    $ cat example.ini | jc --ini -p
    {
      "bitbucket.org": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "yes",
        "user": "hg"
      },
      "topsecret.server.com": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "no",
        "port": "50022"
      }
    }
"""
import jc.utils
import configparser


class info():
    version = '1.2'
    description = 'INI file parser. Also parses files/output containing simple key/value pairs'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using configparser from the standard library'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        Dictionary representing an ini document:

        {
          ini or key/value document converted to a dictionary - see configparser standard
          library documentation for more details.

          Note: Values starting and ending with quotation marks will have the marks removed.
                If you would like to keep the quotation markes, use the -r or raw=True argument.
        }
    """
    # remove quotation marks from beginning and end of values
    for heading in proc_data:
        # standard ini files with headers
        if isinstance(proc_data[heading], dict):
            for key, value in proc_data[heading].items():
                if value.startswith('"') and value.endswith('"'):
                    proc_data[heading][key] = value.lstrip('"').rstrip('"')

        # simple key/value files with no headers
        else:
            if proc_data[heading].startswith('"') and proc_data[heading].endswith('"'):
                proc_data[heading] = proc_data[heading].lstrip('"').rstrip('"')

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing the ini file
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}

    if jc.utils.has_data(data):

        ini = configparser.ConfigParser(allow_no_value=True)
        try:
            ini.read_string(data)
            raw_output = {s: dict(ini.items(s)) for s in ini.sections()}

        except configparser.MissingSectionHeaderError:
            data = '[data]\n' + data
            ini.read_string(data)
            output_dict = {s: dict(ini.items(s)) for s in ini.sections()}
            for key, value in output_dict['data'].items():
                raw_output[key] = value

    if raw:
        return raw_output
    else:
        return process(raw_output)
