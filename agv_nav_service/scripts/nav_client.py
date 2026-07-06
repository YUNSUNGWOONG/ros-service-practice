#!/usr/bin/env python3
"""
nav_client.py  —  항만 AGV 이동 구역 안전 승인 서비스 [클라이언트] (실습용 스켈레톤)

[역할]
목표 좌표를 관제 서버에 비동기(call_async)로 요청하고,
spin_once 폴링 + try/except 로 응답을 안전하게(Non-blocking) 수신한다.

실행 예)  ros2 run agv_nav_service nav_client 45 110
정답은 ../../solution/agv_nav_service/scripts/nav_client.py 에서 확인할 수 있습니다.
"""
import sys
import rclpy
from rclpy.node import Node

# =========================================================================
# TODO(1): 커스텀 서비스 타입을 import 하세요.
# =========================================================================
# from agv_nav_service.srv import CheckNavGoal


class NavClient(Node):
    def __init__(self):
        super().__init__('nav_client')

        # =================================================================
        # TODO(2): create_client 로 'check_goal' 클라이언트를 생성하세요.
        # =================================================================
        # self.cli = self.create_client(CheckNavGoal, 'check_goal')

        # =================================================================
        # TODO(3): 서버가 켜질 때까지 wait_for_service 로 대기하세요.
        # =================================================================
        # while not self.cli.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('관제 서비스 서버 대기 중...')

        # =================================================================
        # TODO(4): 요청(Request) 객체를 생성하세요.
        # =================================================================
        # self.req = CheckNavGoal.Request()

    def send_request(self, x, y):
        # =================================================================
        # TODO(5): self.req 에 좌표(x, y)를 채우고 call_async 로 호출한 뒤
        #          future 객체를 반환하세요.
        # =================================================================
        # self.req.target_x = x
        # self.req.target_y = y
        # return self.cli.call_async(self.req)
        return None  # <- TODO 를 채운 뒤 이 줄을 지우세요.


def main(args=None):
    rclpy.init(args=args)
    node = NavClient()

    # 명령행 인자로 목표 좌표를 받는다 (기본값: 45.0, 110.0 → 거부 케이스)
    x = float(sys.argv[1]) if len(sys.argv) > 1 else 45.0
    y = float(sys.argv[2]) if len(sys.argv) > 2 else 110.0
    node.get_logger().info(f'목표 좌표 요청 전송: ({x}, {y})')

    future = node.send_request(x, y)

    # =================================================================
    # TODO(6): while rclpy.ok() 루프에서 spin_once 로 폴링하고,
    #          future.done() 이 True 가 되면 try/except/else 로 결과를 처리하세요.
    #   - 성공(else): is_approved, estimated_time 를 로그로 출력
    #   - 실패(except): get_logger().error 로 예외 메시지 출력
    #   - 처리 후 break
    # =================================================================
    # while rclpy.ok():
    #     rclpy.spin_once(node)
    #     if future.done():
    #         try:
    #             response = future.result()
    #         except Exception as e:
    #             node.get_logger().error(f'서비스 호출 실패: {e}')
    #         else:
    #             node.get_logger().info(
    #                 f'이동 승인 여부: {response.is_approved}, '
    #                 f'예상 소요 시간: {response.estimated_time:.1f}s'
    #             )
    #         break

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
