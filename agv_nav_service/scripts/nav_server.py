#!/usr/bin/env python3
"""
nav_server.py  —  항만 AGV 이동 구역 안전 승인 서비스 [서버] (실습용 스켈레톤)

[역할]
클라이언트(물류 로봇)가 보낸 목표 좌표(target_x, target_y)가 안전 구역 안에 있는지
검증하고, 승인 여부(is_approved)와 예상 소요 시간(estimated_time)을 응답으로 돌려준다.

아래 TODO 를 순서대로 채워 서버를 완성하세요.
정답은 ../../solution/agv_nav_service/scripts/nav_server.py 에서 확인할 수 있습니다.
"""
import rclpy
from rclpy.node import Node

# =========================================================================
# TODO(1): 커스텀 서비스 타입을 import 하세요.
#   힌트) from <패키지명>.srv import <서비스명>
# =========================================================================
# from agv_nav_service.srv import CheckNavGoal


class NavServer(Node):
    def __init__(self):
        super().__init__('nav_server')

        # =================================================================
        # TODO(2): create_service 로 'check_goal' 서비스를 생성하세요.
        #   힌트) self.create_service(<서비스타입>, '<서비스이름>', <콜백함수>)
        # =================================================================
        # self.srv = self.create_service(CheckNavGoal, 'check_goal', self.goal_callback)

        self.get_logger().info('관제 서버(nav_server) 준비 완료. 승인 요청 대기 중...')

    def goal_callback(self, request, response):
        # =================================================================
        # TODO(3): request.target_x, request.target_y 가
        #          0.0 ~ 100.0 범위(안전 구역)인지 검사하세요.
        # TODO(4): 범위 안이면
        #             response.is_approved   = True
        #             response.estimated_time = (target_x + target_y) * 0.1
        # TODO(5): 범위 밖이면
        #             response.is_approved   = False
        #             response.estimated_time = 0.0
        # =================================================================
        pass  # <- TODO 를 채운 뒤 이 줄을 지우세요.

        self.get_logger().info(
            f'좌표 승인 요청: ({request.target_x}, {request.target_y}) '
            f'-> 결과: {response.is_approved}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = NavServer()
    try:
        rclpy.spin(node)          # 서버는 요청을 계속 대기
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
