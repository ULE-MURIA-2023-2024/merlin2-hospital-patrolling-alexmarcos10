# TODO: write the patrol FSM action

from merlin2_hospital_patrolling.pddl import room_at, room_patrolled, room_type
from merlin2_basic_actions.merlin2_basic_predicates import robot_at
from merlin2_basic_actions.merlin2_basic_types import wp_type
from merlin2_fsm_action import Merlin2BasicStates
from merlin2_fsm_action import Merlin2FsmAction
from typing import List
from kant_dto import PddlObjectDto, PddlConditionEffectDto
from yasmin import CbState
from yasmin import Blackboard
from yasmin_ros.basic_outcomes import SUCCEED
import rclpy
from geometry_msgs.msg import Twist
import time

class Merlin2RoomPatrolFSMAction(Merlin2FsmAction):

    def __init__(self) -> None:
        
        self._room = PddlObjectDto(room_type, "room")
        self._wp = PddlObjectDto(wp_type, "wp")
        super().__init__("room_patrol")
        
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        tts_state = self.create_state(Merlin2BasicStates.TTS)
       

        self.add_state(
            "ROTATING",
            CbState([SUCCEED], self.rotate),
            transitions={
                SUCCEED:"PREPARING_TEXT"
            }
        )

        self.add_state(
            "PREPARING_TEXT",
            CbState([SUCCEED], self.prepare_text),
            transitions={
                SUCCEED:"SPEAKING"
            }
        )

        self.add_state(
            "SPEAKING",
            tts_state
        )

    
        
    def rotate(self, blackboard: Blackboard) -> str:
        
        twist = Twist()
        twist.angular.z = 0.5

        self.publisher(twist)
        self.get_clock().sleep_for(rclpy.duration.Duration(seconds=10))

        twist.angular.z = 0.0 # stop rotating
        self.cmd_vel_publisher.publish(twist)
                          
        blackboard.text = "Rotando en la stretcher room"                  
        return SUCCEED


    def prepare_text(self, blackboard: Blackboard)->str:
        # room_name = blackboard.merlin2_action_goal.objects[0][-1]

        blackboard.text = f"Se ha patrullado la stretcher room" 
        return SUCCEED

    def create_parameters(self) -> List[PddlObjectDto]:
        return [self._room, self._wp]
    
    def create_conditions(self) -> List[PddlConditionEffectDto]:

        # cond_1 = PddlConditionEffectDto(
        #     room_patrolled,
        #     [self._room],
        #     PddlConditionEffectDto.AT_START,
        #     is_negative = True
        # )

        cond_2 = PddlConditionEffectDto(
            robot_at,
            [self._wp],
            PddlConditionEffectDto.AT_START
        )

        cond_3 = PddlConditionEffectDto(
            room_at,
            [self._room, self._wp],
            PddlConditionEffectDto.AT_START
        )
        
        return [cond_2, cond_3]
    
    def create_efects(self) -> List[PddlConditionEffectDto]:

        effect_1 = PddlConditionEffectDto(
            room_patrolled,
            [self._room],
            time=PddlConditionEffectDto.AT_END
        )

        return [effect_1]


def main():

    rclpy.init()
    node = Merlin2RoomPatrolFSMAction()
    node.join_spin()
    rclpy.shutdown()

if __name__ == "__main__":
    main()