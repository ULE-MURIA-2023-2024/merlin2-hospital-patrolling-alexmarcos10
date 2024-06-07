# TODO: write the PDDL domain

from merlin2_basic_actions.merlin2_basic_types import wp_type
from kant_dto import PddlTypeDto, PddlPredicateDto


room_type = PddlTypeDto("room") # room, representa una habitacion
room_patrolled = PddlPredicateDto("room_patrolled", [room_type]) # room_patrolled(room), indica si la habitacion ha sido patrullada
room_at = PddlPredicateDto("room_at", [room_type, wp_type]) # room_at(room, wp), indica en que waypoint esta la habitacion