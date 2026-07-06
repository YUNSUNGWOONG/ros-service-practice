#!/usr/bin/env python3
"""
nav_server.py  —  항만 AGV 이동 구역 안전 승인 서비스 [서버] (정답)
"""
import rclpy
from rclpy.node import Node
from agv_nav_service.srv import CheckNavGoal   # 커스텀 서비스 타입

# 안전(승인) 구역 경계
SAFE_MIN = 0.0
SAFE_MAX = 100.0


class NavServer(Node):
    def __init__(self):
        super().__init__('nav_server')
        # 'check_goal' 서비스 서버 생성
        self.srv = self.create_service(CheckNavGoal, 'check_goal', self.goal_callback)
        self.get_logger().info('관제 서버(nav_server) 준비 완료. 승인 요청 대기 중...')

    def goal_callback(self, request, response):
        in_x = SAFE_MIN <= request.target_x <= SAFE_MAX
        in_y = SAFE_MIN <= request.target_y <= SAFE_MAX

        if in_x and in_y:
            response.is_approved = True
            response.estimated_time = (request.target_x + request.target_y) * 0.1
        else:
            response.is_approved = False
            response.estimated_time = 0.0

        self.get_logger().info(
            f'좌표 승인 요청: ({request.target_x}, {request.target_y}) '
            f'-> 결과: {response.is_approved}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = NavServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
