---
title: Towards v0.0.1
author: Camilo Garcia La Rotta
authorURL: https://camilogarcialarotta.github.io/
authorImageURL: https://i.imgur.com/DvQtOyL.png
---

# What it is
Although initially planned as a Morse machine, early in development I realized there was no need to bind `MOE` only to Morse code. 
The project is best summarized as: a P2P service to transmit encoded messages over any transport medium.

There is both a software component and an optional hardware component to the project. You may run the service directly from the terminal or build a little box with the IO of your liking (e.g. buttons, thermal printer, LEDs, buzzer)

# What it isn't
`MOE` is not an app in the sense most people expect it to work. There is no account you have to create with us. Think of it more as a your network in which you define the receivers and how to connect to them. Of course you can have a single node in the network, in which case you send a message to yourself. 


# Why?

`MOE` was conceived to encourage the usage of P2P architectures over centralized server applications. 

Use the right architecture for the problem at hand. If your service does not require to store user data, why do you want to burden yourself with the complexity and responsibility of handling user credentials. I would be happy to see more business models that are not based on the extraction of user data.

Complementary, `MOE` serves as a project where I can sharpen software design skills. Plus the added bonus of learning a couple new technologies and collaborating in an open source project.

# How?
By having a modular service which has simple input, output and transportation interfaces.

By using a free transportation medium such as an email service (e.g. Gmail) the operational cost of the project in terms of cloud service providers is nil. 

By leaving the freedom of choice to the users:
- to add only the people they want to their `MOE` networks. 
- to use the IO, transportation medium of their choice
- to develop their own implementations of the interfaces
- to use `MOE` as a software or as software + hardware

# When
Brainstorming for this project had begun since late Summer 2017. But the first official development sprint began August 1st, 2018 and the MVP milestone is set for September 3rd, 2018. 

From there, further iterations will be made to improve existing functionalities and implement new ones.

Cheers.

![Nicollete Groom](https://media.giphy.com/media/3rgXBsmYd60rL3w7sc/giphy.gif)
> GIF by Nicolette Groom
