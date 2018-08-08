# MOE

Morse Over Ethernet  

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgitlab.com%2Fcegal%2FMOE.svg?type=shield)](https://app.fossa.io/projects/git%2Bgitlab.com%2Fcegal%2FMOE?ref=badge_shield)

# Overview

Small DIY Raspberry Pi project for hobbyists who want to put their unused boards to good use.  
`MOE` is inteded to be lightweight with respect to resource usage so that even the first generation boards can be used.

At its core, `MOE` is a morse machine:
  - It can record a morse message through a button and send it to another `MOE` over the internet.
  - It can play a received morse message through a beeper.

### Goals
- __Cheap__

    The MOE project aims to be as cost effective as possible in terms of operation, i.e not paying for server instances of any kind.  
    MOE leverages the Gmail service and its API to deliver and store the messages. The only operational costs are the internet connection and the power consumption of the Raspberry Pi.

- __Modular__

    I/O devices must be added/swapped in a `MOE` without much trouble.  
    For example: a printer can be added so that morse messages are printed too, a light can be added so that morse messages are blinked too.

- __Easy to setup__

    The software must be easily installable and well documented so that anyone can modify as they wish.  
    The hardware must provide a basic set of downloadable schemas for 3d printing or cardboard-cutting must be available for those who want to dress up their `MOE`.

# Contribution guidelines

I am completely open to suggestions, criticism, and collaborators. Feel free to open issues and label them accordingly.  
Please read the [Contribution Guide](CONTRIBUTING.md) for more information.

# Documentation

For more information on the materials, the architecture, the usage and more, visit the [Wiki](https://gitlab.com/cegal/MOE/wikis/home).

# Licensing

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgitlab.com%2Fcegal%2FMOE.svg?type=large)](https://app.fossa.io/projects/git%2Bgitlab.com%2Fcegal%2FMOE?ref=badge_large)