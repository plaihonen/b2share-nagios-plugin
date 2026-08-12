# B2SHARE Monitoring probe for ARGO

## Setting up environment

This probe has been written for Python 3 and tested with Python 3.12.
You may need to install (using e.g. `pip3`) the following Python modules as they do not come with original distribution:

- requests
- jsonschema

## Overview

The B2SHARE probe for ARGO does the following interaction
with B2SHARE REST API:

- Both, B2SHARE v2 and v3 (Release 3.0.2 and above) are supported.
- Search for records
- Fetch record's metadata from search results
- Fetch record's metadata schema
- Validate record's metadata agains record's metadata schema
- If a record with file is available, check that a file
  should be able to be downloaded (HTTP HEAD request)

B2SHARE ARGO probe:

- makes HTTP requests (GET, HEAD) to B2SHARE's REST API
- parses JSON responses obtained from B2SHARE's REST API

## Pre-requisites:

- None

## Package dependences

Python modules "requests" and "jsonschema" have the following dependencies (02/2026):

```python
requests==2.32.5
├── charset-normalizer [required: >=2,<4, installed: 3.4.4]
├── idna [required: >=2.5,<4, installed: 3.11]
├── urllib3 [required: >=1.21.1,<3, installed: 2.6.3]
└── certifi [required: >=2017.4.17, installed: 2026.1.4]

jsonschema==4.25.1
├── attrs [required: >=22.2.0, installed: 25.4.0]
├── jsonschema-specifications [required: >=2023.03.6, installed: 2025.9.1]
│   └── referencing [required: >=0.31.0, installed: 0.36.2]
│       ├── attrs [required: >=22.2.0, installed: 25.4.0]
│       ├── rpds-py [required: >=0.7.0, installed: 0.27.1]
│       └── typing_extensions [required: >=4.4.0, installed: 4.15.0]
├── referencing [required: >=0.28.4, installed: 0.36.2]
│   ├── attrs [required: >=22.2.0, installed: 25.4.0]
│   ├── rpds-py [required: >=0.7.0, installed: 0.27.1]
│   └── typing_extensions [required: >=4.4.0, installed: 4.15.0]
└── rpds-py [required: >=0.7.1, installed: 0.27.1]
```

## How it works?

```bash
./check_b2share.py --help
usage: check_b2share.py [-h] -u URL [-t TIMEOUT] [-v] [--verify-tls-cert] [--no-verify-tls-cert] [--error-if-no-records-present] [--use-proxy] [--debug-metadata] [--metadata-report]

B2SHARE Nagios probe

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Base URL of B2SHARE instance
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds as positive integer. (default: 15)
  -v, --verbose         Increase output verbosity (-v, -vv, -vvv)
  --verify-tls-cert     Verify TLS certificate (default: enabled)
  --no-verify-tls-cert  Disable TLS verification (NOT recommended)
  --error-if-no-records-present
                        Return CRITICAL if no public records are present
  --use-proxy           Allow requests to use environment proxies.
  --debug-metadata      (v3 Only). Print ignored vocabulary fields during validation
  --metadata-report     (v3 Only). Print a summary report of vocabulary-like keys
```

Example:

```bash
14:26 $ ./check_b2share.py -u https://b2share.eudat.eu:443 -vvv
Verbosity level: 3
Timeout: 15 seconds
B2SHARE URL: https://b2share.eudat.eu:443
Starting B2SHARE Probe...
---------------------------
Making a search.
Making a HTTP GET request to https://b2share.eudat.eu:443/api/records?access_status=open&sort=newest&size=10
hits: 11718
A record with files was found.
Making a HTTP GET request to https://b2share.eudat.eu/api/records/h4rf8-38964
Fetching record metadata schema.
Making a HTTP GET request to https://b2share.eudat.eu/api/schemas/records/record-v10.0.0.json/jsonschema
Accessing file bucket.
Making a HTTP GET request to https://b2share.eudat.eu/api/records/h4rf8-38964/files
Validating parent schema (draft-07).
Building metadata-only schema.
Validating metadata (vocabulary fields ignored).
Fetching first file of bucket (HEAD).
---------------------------
OK: records, metadata schemas and files are accessible.
```

Extra usage examples for B2SHARE v3:

```bash
# See what was ignored:
./check_b2share.py -u https://b2share.eudat.eu:443 -vvv --metadata-report

# Debug each stripped key (chatty; stderr):
./check_b2share.py -u https://b2share.eudat.eu:443 -vvv --debug-metadata
```

## How the timeout calculations work

* Each individual request uses "time remaining" as its timeout
* But every request can take up to that long
* And you can have multiple requests in sequence (search → record → schema → bucket → file HEAD)

This means the script’s total runtime may exceed the user‑specified timeout.

Why?

Because each request gets a fresh timeout based on the remaining window, not the original timeout.

Example:

* User sets --timeout 15
* First request uses ~0 seconds, so timeout ~14.9s
* Second request gets ~14s
* Third request gets ~13.5s
* and so on...

In the worst case:

If several requests hang until their individual timeout, The total script runtime might reach 2-4× the requested timeout.

## How to run the code in a container

In the root folder of the project, build the container:

```bash
docker build -t <name_of_the_image>:<tag_of_the_image> .
```

Then run the code in the container

```bash
docker run --rm <name_of_the_image>:<tag_of_the_image> ./check_b2share.py -u https://b2share.eudat.eu:443 -t 15 -vvv
# OR inside the container (Follow instructions)
docker run -it --rm <name_of_the_image>:<tag_of_the_image> bash
```

## Credits

This code is based on [EUDAT-B2ACCESS/b2access-probe](https://github.com/EUDAT-B2ACCESS/b2access-probe)
