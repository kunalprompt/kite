# Kite - A Py3 Logging System

## Features

1. Python 3

2. Simple Text/HTML Messages/Templates for logs

3. Buffer to store log messages

----------------------
## Sample Kite Email

![Sample Kite EMail](https://raw.githubusercontent.com/kunalprompt/kite/master/kite_email.png)
----------------------


## Tech

1. Python 3

    `python3 -m venv env`

    `source env/bin/activate`

    As this system only uses Python 3 Standard Library, you'll find `requirements.txt` empty.

2. Main Modules (Logger, Log Buffer with Email Sending Capability)

    `logger` is the module which takes care of management of loggings.

    `log_buffer` is the module which is specially designed to handle log ERRORS. Its basic
     job to send all log errors (+/CRITICAL) to users in simple text/html templates.

3. Unit tested

    To find examples on how to use this refer to `tests/`.

Please feel free to write PRs.
