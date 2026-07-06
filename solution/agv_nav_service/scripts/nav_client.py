#!/usr/bin/env python3
"""
nav_client.py  —  항만 AGV 이동 구역 안전 승인 서비스 [클라이언트] (정답)

실행 예)  ros2 run agv_nav_service nav_client 45 110
"""
import sys
import rclpy
from rclpy.node import Node
from agv_nav_service.srv import CheckNavGoal   # 커스텀 서비스 타입


class NavClient(Node):
    def __init__(self):
        super().__init__('nav_client')
        # 'check_goal' 서비스 클라이언트 생성
        self.cli = self.create_client(CheckNavGoal, 'check_goal')
        # 서버가 켜질 때까지 대기
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('관제 서비스 서버 대기 중...')
        self.req = CheckNavGoal.Request()

    def send_request(self, x, y):
        self.req.target_x = x
        self.req.target_y = y
        return self.cli.call_async(self.req)   # 비동기 호출 → future 반환


def main(args=None):
    rclpy.init(args=args)
    node = NavClient()

    # 명령행 인자로 목표 좌표를 받는다 (기본값: 45.0, 110.0 → 거부 케이스)
    x = float(sys.argv[1]) if len(sys.argv) > 1 else 45.0
    y = float(sys.argv[2]) if len(sys.argv) > 2 else 110.0
    node.get_logger().info(f'목표 좌표 요청 전송: ({x}, {y})')

    future = node.send_request(x, y)

    # 비동기 응답을 폴링하며 예외까지 안전하게 처리 (영상 핵심 내용)
    while rclpy.ok():
        rclpy.spin_once(node)
        if future.done():
            try:
                response = future.result()
            except Exception as e:
                node.get_logger().error(f'서비스 호출 실패: {e}')
            else:
                node.get_logger().info(
                    f'이동 승인 여부: {response.is_approved}, '
                    f'예상 소요 시간: {response.estimated_time:.1f}s'
                )
            break

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
