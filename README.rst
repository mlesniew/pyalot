******
pyalot
******

The pyalot package allows sending push notifications to Windows and Windows 
Phone devices using pushalot.com_.

.. _pushalot.com: http://www.pushalot.com

Notifications can be sent from the **command line** or from **Python code**.

|pypi| |license| |build|

Basic command line usage
------------------------

Sending a text notification from the command line is simple:

.. code-block:: bash

    pyalot --token 11234567890abcdef234567890abcdef "Hello world"

The text doesn't have to be quoted, pyalot will accept any number of positional
arguments and combine them into a notification text.

.. code-block:: bash

    pyalot --token 11234567890abcdef234567890abcdef Hello world

In some cases it may be more convenient to pass the notification text through
stdin instead of using parameters:

.. code-block:: bash

    uptime | pyalot --token 11234567890abcdef234567890abcdef --pipe

Don't like passing the auth token every time?  You can store your auth token in
``~/.pushalot-token`` as simple text.  This will allow you to omit the
``--token`` parameter:

.. code-block:: bash

    echo 11234567890abcdef234567890abcdef > ~/.pushalot-token
    pyalot Hello world

We can also use pyalot to set other, optional notification parameters.  We can
set the title or source, add a link or set a time-to-live value.

.. code-block:: bash

    pyalot --title "Important notification!" "Did you notice the title?"
    pyalot --source "Raspberry Pi" "This notification is from my Raspberry"
    pyalot --link "http://github.com" "Check out this link"
    pyalot --ttl 10 "This notification will disappear after 10 minutes"


Installation
------------

pyalot can be installed using pip:

.. code-block:: bash

    pip install pyalot

.. |pypi| image:: https://img.shields.io/pypi/v/pyalot.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pyalot

.. |license| image:: https://img.shields.io/pypi/l/pyalot.svg?style=flat-square

.. |build| image:: https://img.shields.io/travis/mlesniew/pyalot.svg?style=flat-square
    :target: https://travis-ci.org/mlesniew/pyalot
