---
id: getting_started
title: Getting Started
# sidebar_label: Example Page
---


## Prerequisites

Its a good idea to start by reading about the **[architecture](https://moe.readthedocs.io/en/latest/architecture.html)** of `MOE`.

This tutorial assumes you are working on a Linux distribution, you have Python3+ and an internet connection.

## Software

Before getting to physically build `MOE`, we have to get comfortable with its software.

1.  Download the project and install its dependencies
    ```bash
    git clone https://github.com/CamiloGarciaLaRotta/MOE.git
    cd MOE
    # activate your virtual environment
    pip install -r config/requirements.txt
    ```

2. Now we can tiker with `moe/daemon.py`. Let's start by adding a new cypher code to it:
    ```python
    #moe/daemon.py
    from encoder import Encoder

    # create an encoder for the Morse code
    MORSER = Encoder('examples/MORSE.csv')

    morse_code = MORSER.encode('THE ANSWER IS 42')
    plain_text = MORSER.decode(morse_code)
    print(morse_code)
    print(plain_text)
    ```

3. Next we could delegate outputting the strings to a **Writer**, for example **Echoer**:
    ```python
    #moe/daemon.py
    from encoder import Encoder
    from writer.echoer import Echoer

    # create an encoder for the Morse code
    MORSER = Encoder('examples/MORSE.csv')

    # create an echoer
    ECHOER = Echoer()

    morse_code = MORSER.encode('THE ANSWER IS 42')
    plain_text = MORSER.decode(morse_code)
    ECHOER.write(f'{morse_code}\n')
    ECHOER.write(f'{plain_text}\n')
    ```

    While its a dummy example, it suffises to change **Echoer** for any other **Writer** and the code would continue to work. Next, I will replace it with a **Mailer**, which is also a **Writer**.

4. Let's configure the **Mailer** **Gmailer**, it is both a **Reader** and a **Writer**. It adds extra functions so that messages can be sent through the internet to other `MOE`'s:
    - **[Enable the Gmail API](https://developers.google.com/gmail/api/quickstart/python)** (step #1 in the officla Gmail API tutorial). If it's your first time using a Google API, you might find this **[guide](https://medium.com/@pablo127/google-api-authentication-with-oauth-2-on-the-example-of-gmail-a103c897fd98)** useful.

    - If you don't have it already, download `client_secrets.json`, which can be found in the **[Google API Console](https://console.cloud.google.com/apis/credentials)**.

    - Then go ahead an play with it:
        ```python
        #moe/daemon.py
        from encoder import Encoder
        from writer.echoer import Echoer
        from mailer.gmailer import Gmailer

        # create an encoder for the Morse code
        MORSER = Encoder('examples/MORSE.csv')

        # create an echoer
        ECHOER = Echoer()

        # create a gmailer
        MAILER = Gmailer(user='<YOUR_GMAIL>', 
                         destination='<YOUR_GMAIL>',
                         secret='path/to/your/client_secrets.json')

        morse_code = MORSER.encode('THE ANSWER IS 42')

        # you see, we replaced ECHOER by MAILER!
        MAILER.write(morse_code)

        body_of_latest_email = MAILER.read()['content']

        # the encoded message
        ECHOER.write(f'{body_of_latest_email}\n')

        # the decoded message
        ECHOER.write(f'{MORSER.decode(body_of_latest_email)}\n')
        ```

        If its your first time using `MOE`, it will open up a browser tab for you to authorize it to access your Gmail account.
        It does the following: __create/delete {labels,filters} create/read/send/delete {emails}__.
        All of `MOE`'s actions happen only withing its labeled inbox, hence it won't clutter your personal inbox.

        **Note** You can change the destination email address to anyone else's. This is just for demo purposes.

5. A more intensive Gmailer Use Case:
    ```python
    #moe/daemon.py
    from encoder import Encoder
    from writer.echoer import Echoer
    from mailer.gmailer import Gmailer

    # create an encoder for the Morse code
    MORSER = Encoder('examples/MORSE.csv')

    # create an echoer
    ECHOER = Echoer()

    # create a gmailer
    MAILER = Gmailer(user='<YOUR_GMAIL>', 
                     destination='<YOUR_GMAIL>',
                     secret='path/to/your/client_secrets.json')

    morse_code = MORSER.encode('THE ANSWER IS 42')
    plain_text = MORSER.decode(morse_code)

    # if its your first time using MOE, there are no emails with MOE's label in your inbox
    print(MAILER.read())

    # lets send an email
    MAILER.write('tis not encoded')

    # lets read new unread email, this is the email dict used across MOE
    print(MAILER.read())

    # Because read() marks email as read, calling read() again will return nothing
    print(MAILER.read())

    # send 2 new emails
    MAILER.write('A')
    MAILER.write('B')

    # lets see all unread MOE emails
    print(MAILER.fetch_unread())

    # lets see all MOE emails
    print(MAILER.fetch_all())
    ```


## Hardware
**TODO**

## Next Steps

If you like the project, feel free to contribute to it by adding new **Readers**, **Writers**, **Mailers** and **Hardware**

The **[API documentation](https://moe.readthedocs.io/en/latest/)** is a good place to continue.
