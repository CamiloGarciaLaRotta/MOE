# MOE

Morse Over Ethernet 

[![Documentation Status](https://readthedocs.org/projects/moe/badge/?version=latest)](https://moe.readthedocs.io/en/latest/?badge=latest)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgitlab.com%2Fcegal%2FMOE.svg?type=shield)](https://app.fossa.io/projects/git%2Bgitlab.com%2Fcegal%2FMOE?ref=badge_shield)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2111/badge)](https://bestpractices.coreinfrastructure.org/projects/2111)
  
<img src="https://gitlab.com/cegal/MOE/raw/pages/website/static/img/BMO_flat.jpg" width=380 />
  
# Overview

P2P encoded messaging service with a focus on customizable input, output and transportation modules.

It is primarily a CLI application, but also includes documentation to build a  DIY Raspberry Pi Device.

At its core, `MOE` can:
  - Read a message from the user through any of its **[Reader](https://moe.readthedocs.io/en/latest/architecture.html#architecture)** interface implementations.

  - Encode/decode a message to any given dictionnary fed to it.

  - Send/receive a message over the Internet through any of its **[Mailers](https://moe.readthedocs.io/en/latest/architecture.html#architecture)** interface implementations.

  - Output a received message through any of its **[Writer](https://moe.readthedocs.io/en/latest/architecture.html#architecture)** interface implementations.

# Goals
- __Modular__
    Simple and clear interfaces for its software components so that users can easily code their own implementations.

- __Hardware Agnostic__
    It's core functionality does not depend on any hardware. Any microcontroller or IO device that can be wired up can be used as Hardware to build up a `MOE`.

- __P2P__
    While users may implement their own **Mailers** in a server-client pattern, `MOE` aims to showcase that P2P is a very useful architectural pattern for recreational projects:
    - **Operational Cost**
    A `MOE` network does not cost anything to deploy (there is no need to pay for server instances of any kind).

    - **Secutiry**
    No credentials or private data leave your `MOE` (there is no `MOE` server on the Internet).
    Only you give `MOE` access to the **Readers**, **Writers** and **Mailers** of your choice.
    Only you choose who to add to your `MOE` network.

# Contribution guidelines

I am completely open to suggestions, criticism, and collaborators. Feel free to open issues and label them accordingly.
Please read the **[Contribution Guide](CONTRIBUTING.md)** for more information.

# Documentation

For setup/usage documentation and the current status of the project, visit the `MOE`'s **[HomePage](http://cegal.gitlab.io/MOE/)**.

For the API interface and software architecture, visit `MOE`'s **[API documentation](https://moe.readthedocs.io/en/latest/)**.


# Licensing

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgitlab.com%2Fcegal%2FMOE.svg?type=large)](https://app.fossa.io/projects/git%2Bgitlab.com%2Fcegal%2FMOE?ref=badge_large)
