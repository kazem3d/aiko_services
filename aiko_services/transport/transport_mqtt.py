# To Do
# ~~~~~
# * Refactor current code into ServiceDiscovery
#
# * Design Pattern for creating Actors of different types, e.g MQTT or Ray
#
# - Apply proxy automatically for ActorMQTT and not in "aloha_honua.py"
#
# - Replace Actor topic with Actor name ... and name can be the topic
#   - Will need to support multiple Actors running in the same process !
#
# * Once Service protocol matching is properly implemented ...
#     Replace Service tag "actor=actor_name" marking Actors with
#     matching via Service protocol "{AIKO_PROTOCOL_PREFIX}/actor:0"
#
#------------------------------------------------------------------------------
# def create_actor(actor_class, actor_type, actor_uuid,
#     actor_check = True, actor_init_args = {}, daemon = False,
#     max_concurrency = _MAX_CONCURRENCY, resources = None):
#
# delete_actor(actor_name, wait = False, force = False):
#
# get_actor(actor_name,
#     exit_not_found = False, fail_not_found = True, wait_time = None):

from aiko_services import *

__all__ = ["TransportMQTTActor", "ActorDiscovery"]

class TransportMQTTActor(Actor):
    def __init__(self, actor_name):
        super().__init__(actor_name)

    def terminate(self):
        self._stop()

    def topic_in_handler(self, aiko, topic, payload_in):
        command, parameters = parse(payload_in)
    #   _LOGGER.debug(f"topic_in_handler(): {command}: {parameters}")
        self._post_message(actor.Topic.IN, command, parameters)

# def _proxy_post_message(
#   proxy_name, actual_object, actual_function,
#   actual_function_name, *args, **kwargs):
#
#   actual_object._post_message.remote(
#       actor.Topic.IN, actual_function_name, args
#   )

class ServiceDiscovery:  # Move to registrar.py or share.py?
    pass                 # Refactor after ActorDiscovery starts to work properly

class ActorDiscovery(ServiceDiscovery):  # Move to actor.py or share.py ?
    def __init__(self):
        self.services_cache = service_cache_create_singleton()

    def add_handler(self, service_change_handler, filter):
        self.services_cache.add_handler(service_change_handler, filter)

    def get_actor_mqtt(self, actor_name):
        actor_topic = ".".join(actor_name.split(".")[:-1])  # WIP: Actor name
        services = self.services_cache.get_services()
        services = filter_services_by_actor_names(services, [actor_name])
        actor = services.get(actor_name)
        return actor

    def query_actor_mqtt(self, filter):
        services = self.services_cache.get_services()
        actors = filter_services_by_attributes(services, filter)
        return actors

# -----------------------------------------------------------------------------

def create_actor_mqtt(actor_class, actor_name,
    actor_init_args={}, resources=None, daemon = True):
    pass

def delete_actor_mqtt(actor):
    actor.terminate()

# -----------------------------------------------------------------------------