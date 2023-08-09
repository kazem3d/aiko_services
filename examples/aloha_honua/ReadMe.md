# Aiko Services examples: AlohaHonua (Hello World)

These examples require the Aiko Services [framework](https://en.wikipedia.org/wiki/Software_framework) to be installed and the Core [Services](https://en.wikipedia.org/wiki/Service-oriented_architecture) to be started.

* Installing Aiko Services framework *[TBC]*
* Starting and stopping Core Services *[TBC]*
* Using Aiko Dashboard for monitoring and control *[TBC]*
* More AlohaHonua examples *[TBC]*

![Diagram: AlohaHonua example](aloha_honua_0.png)

The Aiko Services framework relies on (at least) these two Core Services ...

* [MQTT server](https://en.wikipedia.org/wiki/MQTT#MQTT_broker) for passing messages between Services (Actors)
* Aiko Registrar for discovering what Services (Actors) are available

Other Services (Actors), like AlohaHonua and the Aiko Dashboard can then send messages via the [MQTT](https://mqtt.org) protocol to communicate with each other.

## A minimal Actor: aloha\_honua\_0.py

In computer science, it is traditional to start with an example [hello world program](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program).  For a programming language, that example program may be just a single line of code or a few lines of code.  The simpliest Aiko Services equivalent is currently around 14 lines of code.  Clearly, there is a lot more going on here than just printing "Hello World !".

The AlohaHonua [Actor](https://en.wikipedia.org/wiki/Actor_model) below is a distributed Service that can be discovered, [receive and send messages](https://en.wikipedia.org/wiki/Actor_model#Fundamental_concepts), perform distributed logging and be inspected via the Aiko Dashboard.  Subsequent examples will extend this basic building block to do much more.

*Source code: [aloha\_honua\_0.py](aloha_honua_0.py)*

    from aiko_services import *

    _LOGGER = aiko.logger(__name__)

    class AlohaHonua(Actor):
        def __init__(self, implementations, name, protocol, tags, transport):
            implementations["Actor"].__init__(self,
                implementations, name, protocol, tags, transport)
            print(f"MQTT topic: {self.topic_in}")

        def get_logger(self):
            return _LOGGER

        def aloha(self, name):
            _LOGGER.info(f"AlohaHonua {name} !")

    if __name__ == "__main__":
        init_args = actor_args("aloha_honua", "*")
        aloha_honua = compose_instance(AlohaHonua, init_args)
        aiko.process.run()

### Running the AlohaHonua Actor with a local MQTT server

After the Aiko Services framework has been installed, you'll need to start the Core Services, which are the [mosquitto](https://mosquitto.org) ([MQTT server](https://en.wikipedia.org/wiki/MQTT#MQTT_broker)) and the Aiko Registrar on your computer.  The Aiko Dashboard will also be started, which provides interactive monitoring and control.

    # Current working directory should be the top-level of the Aiko Services repository
    # The first command starts mosquitto, Aiko Registrar and Aiko Dashboard
    ./scripts/system_start.sh
        Starting: /usr/sbin/mosquitto
        Starting: aiko_registrar

    # Use another terminal session, also starting at the top-level of the repository
    cd examples/aloha_honua
    ./aloha_honua_0.py
        MQTT topic: aiko/nomad.local/123/1/in

Whilst the AlohaHonua Actor is running, the Aiko Dashboard will show a list of the available Services / Actors and selecting `aloha_honua` will show further details ...

![Aiko Dashboard](aiko_dashboard_0a.png)

* AIKO DASHBOARD LOG PAGE *[TBC]*
* MQTT PUBLISH *[TBC]*
* SCREEN SNAPSHOT OF THE LOG MESSAGE "aiko_dashboard_0b.png" *[TBC]*


### Running the AlohaHonua Actor with a remote MQTT server

*[TBC]*

### Stopping the AlohaHonua Actor and Core Services

The AlohaHonua Actor example, Core Services and Aiko Dashboard can be stopped, as follows ...

    # Type Control-C to stop the ./aloha_honua_0.py program

    # Select the terminal session running the Aiko Dashboard and press the "x" key

    # Then stop the Core Services
    ../../scripts/system_stop.sh
        Stopping: aiko_registrar
        Stopping: /usr/sbin/mosquitto

### Examining the AlohaHonua Actor source code

*Source code: [aloha\_honua\_0.py](aloha_honua_0.py)*

Start by importing the Aiko Services [module](https://www.w3schools.com/python/python_modules.asp) and creating a [logger](https://en.wikipedia.org/wiki/Logging_(computing)) [instance](https://en.wikipedia.org/wiki/Instance_(computer_science)#Object-oriented_programming) for this Actor.

    from aiko_services import *

    _LOGGER = aiko.logger(__name__)

The `_LOGGER` variable is specific to each Actor instance, so that log records can be shown for just that Actor instance.  The logging level can be independently changed on-the-fly by the Aiko Dashboard or given an initial value via the command line ...

`AIKO_LOG_LEVEL=DEBUG ./aloha_honua_0.py`

By default, the `_LOGGER` instance will use distributed logging (via MQTT) that makes it easier to diagnose background or remote Actors via the Aiko Dashboard.  Alternatively, the log records can be sent directly to the terminal console ...

`AIKO_LOG_MQTT=false ./aloha_honua_0.py`

The AlohaHonua Actor is defined as a Python class that inherits from the Aiko Actor class.  The class constructor method `__init__()` is required, but don't worry about its implementation for the moment.  The `print()` statement shows the automagically generated MQTT topic path (input) for communicating with this Actor.

    class AlohaHonua(Actor):
        def __init__(self, implementations, name, protocol, tags, transport):
            implementations["Actor"].__init__(self,
                implementations, name, protocol, tags, transport)
            print(f"MQTT topic: {self.topic_in}")

Actors are required to create their own logger instance and provide an accessor method.

        def get_logger(self):
            return _LOGGER

Actors can define functions that can be invoked directly by other Actors (via MQTT messages).

        def aloha(self, name):
            _LOGGER.info(f"AlohaHonua {name} !")

When coding in Python, Aiko Actors can be discovered and their functions invoked via a regular Python function call.  For testing and diagnosis, MQTT CLI tools can also used to *publish* hand-crafted messages and *subscribe* to observe one or more Actor's output.

The standard Python `__main__` code defines the AlohaHonua class constructor method` __init__()` arguments, e.g the Actor `name` and `protocol`.  Then creates (*composes*) the AlohaHonua Actor instance.  Finally, the Aiko Process main event loop can be run (which is a blocking call).

    if __name__ == "__main__":
        init_args = actor_args("aloha_honua", "*")
        aloha_honua = compose_instance(AlohaHonua, init_args)
        aiko.process.run()

The Aiko Services framework uses the [Inversion of Control (IoC)](https://en.wikipedia.org/wiki/Inversion_of_control) design pattern, which enables an extensible, event-driven programming model.

The Aiko Services framework also utilizes [Design by Composition](https://en.wikipedia.org/wiki/Composition_over_inheritance) and [Interfaces](https://en.wikipedia.org/wiki/Interface_(object-oriented_programming)), which promotes code reuse ([DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)) and enables [Aspect Oriented Programming (AOP)](https://en.wikipedia.org/wiki/Aspect-oriented_programming) to deal with cross-cutting concerns.

*Note: About 6 lines of code above are [boilerplate](https://en.wikipedia.org/wiki/Boilerplate_code), i.e the `aiko.logger()`, `__init__()` and `get_logger()` methods.  Over time, the aim is to eliminate as much boilerplate code as possible.*