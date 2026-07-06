요청하신 유튜브 영상의 내용을 바탕으로, ROS 2 서비스 프로그래밍의 핵심을 직접 손으로 익힐 수 있는 맞춤형 실습 프로젝트를 설계해 드립니다.

### 1. 영상 핵심 개념 및 기술 스택 요약

* **핵심 개념**: 클라이언트의 요청(Request)을 받아 서버가 로직을 처리한 후 응답(Response)을 반환하는 ROS 2의 1:1 통신 구조입니다.
* **기술 스택**: ROS 2, Python (`rclpy`) 기반 서비스 서버 및 클라이언트 프로그래밍.
* **주요 구성요소**: 사용자 정의 서비스 인터페이스(`.srv`), `create_service`, `create_client` 함수 활용.
* **통신 제어**: `call_async`를 통한 비동기식 요청 및 상태 폴링(`spin_once`, `future.done()`)을 통한 비차단(Non-blocking) 응답 처리.
* **안정성 확보**: `try-except` 구문을 통한 서비스 통신 예외 처리 기법.

---

### 2. 실습 프로젝트 제안: "항만 물류 로봇(AGV) 이동 구역 안전 승인 서비스"

항만 내에서 수출입 차량을 적재하거나 화물을 운반하는 자율주행 물류 로봇이 특정 목적지로 이동하기 전, 관제 시스템(서버)에 해당 좌표의 이동 가능 여부를 질의하고 승인을 받는 시스템을 구현합니다.

---

### 3. 프로젝트 상세 정리

**프로젝트 목표**

* 커스텀 `.srv` 파일을 생성하여 요청과 응답 메시지 구조를 이해합니다.
* 파이썬을 이용해 서비스 서버와 비동기식 클라이언트 노드를 구현합니다.
* 관제 서버가 로봇의 목표 좌표를 검증하고, 클라이언트가 예외 처리와 함께 결과를 수신하는 전체 파이프라인을 완성합니다.

**사전 준비물**

* **ROS 버전**: ROS 2 Humble
* **필요 패키지**: `rclpy`, `rosidl_default_generators` (커스텀 메시지 빌드용)
* **시뮬레이터**: 별도 물리 시뮬레이터(Isaac Sim 등) 불필요 (순수 노드 간 통신 테스트)

**프로젝트 구조**

```text
agv_nav_service/
├── package.xml
├── CMakeLists.txt (또는 setup.py, 패키지 구성 방식에 따라 선택)
├── srv/
│   └── CheckNavGoal.srv         # 커스텀 서비스 파일
└── agv_nav_service/
    ├── __init__.py
    ├── nav_server.py            # 관제 시스템 (서버)
    └── nav_client.py            # 물류 로봇 (클라이언트)

```

**단계별 구현 순서**

* **Step 1**: `CheckNavGoal.srv` 작성 (요청: `x`, `y` 좌표 / 응답: `is_approved` 상태, `estimated_time` 예상 시간)
* **Step 2**: 서비스 메시지 빌드 설정 (`package.xml` 및 `CMakeLists.txt` 의존성 추가 후 `colcon build`)
* **Step 3**: `nav_server.py` 구현 (요청된 x, y 좌표가 허용된 하역/이동 구역 내에 있는지 조건문으로 검증 후 응답 반환)
* **Step 4**: `nav_client.py` 구현 (`call_async` 비동기 호출 및 `while` 루프 내 `spin_once`, `try-except` 예외 처리 구현)
* **Step 5**: 두 노드를 실행하여 서비스 통신 정상 작동 여부 확인

**핵심 코드 뼈대 (Skeleton Code)**

*`srv/CheckNavGoal.srv`*

```text
float64 target_x
float64 target_y
---
bool is_approved
float64 estimated_time

```

*`nav_server.py`*

```python
import rclpy
from rclpy.node import Node
from agv_nav_service.srv import CheckNavGoal # 생성한 커스텀 패키지 경로

class NavServer(Node):
    def __init__(self):
        super().__init__('nav_server')
        # 서비스 서버 생성
        self.srv = self.create_service(CheckNavGoal, 'check_goal', self.goal_callback)
        
    def goal_callback(self, request, response):
        # 영상에서 소개된 것처럼 요청 파라미터를 받아 로직 수행
        # 예: x, y가 0~100 범위의 안전 구역인지 확인
        if 0.0 <= request.target_x <= 100.0 and 0.0 <= request.target_y <= 100.0:
            response.is_approved = True
            response.estimated_time = (request.target_x + request.target_y) * 0.1
        else:
            response.is_approved = False
            response.estimated_time = 0.0
            
        self.get_logger().info(f"좌표 승인 요청: ({request.target_x}, {request.target_y}) -> 결과: {response.is_approved}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NavServer()
    rclpy.spin(node) # 서버는 지속적으로 대기
    rclpy.shutdown()

```

*`nav_client.py`*

```python
import rclpy
from rclpy.node import Node
from agv_nav_service.srv import CheckNavGoal

class NavClient(Node):
    def __init__(self):
        super().__init__('nav_client')
        # 서비스 클라이언트 생성
        self.cli = self.create_client(CheckNavGoal, 'check_goal')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('관제 서비스 서버 대기 중...')
        self.req = CheckNavGoal.Request()

    def send_request(self, x, y):
        self.req.target_x = x
        self.req.target_y = y
        # 비동기 서비스 호출
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    node = NavClient()
    
    # 임의의 목적지 좌표 전송 테스트
    node.send_request(45.0, 110.0)
    
    # 비동기 응답 대기 및 예외 처리 로직 (영상 핵심 내용)
    while rclpy.ok():
        rclpy.spin_once(node)
        if node.future.done():
            try:
                response = node.future.result()
            except Exception as e:
                node.get_logger().error(f'서비스 호출 실패: {e}')
            else:
                node.get_logger().info(f'이동 승인 여부: {response.is_approved}, 예상 소요 시간: {response.estimated_time}')
            break

    node.destroy_node()
    rclpy.shutdown()

```

**완료 후 확인할 수 있는 테스트/검증 방법**

1. **터미널 1**: `ros2 run agv_nav_service nav_server` 를 실행하여 서버 구동
2. **터미널 2**: `ros2 run agv_nav_service nav_client` 를 실행
3. **결과 확인**: 클라이언트 터미널에 예상 소요 시간 또는 거부 메시지가 출력되는지 확인하고, 서버 터미널에는 들어온 좌표 값 로그가 정상적으로 찍히는지 확인.
4. **CLI 테스트**: 코드를 수정하지 않고 직접 터미널에서 서비스를 호출해 봅니다.
`ros2 service call /check_goal agv_nav_service/srv/CheckNavGoal "{target_x: 50.0, target_y: 50.0}"`

---

### 4. 난이도

* **[중급]** (초급 과정인 단순 Topic 통신을 넘어 사용자 정의 srv 빌드 및 비동기 처리, 예외 처리를 모두 포함하고 있기 때문입니다.)

### 5. ROS 버전

* **ROS 2 Humble** 기준

### 6. 실습 예상 소요 시간

* **약 1시간 ~ 1시간 30분** (패키지 구성 및 CMake/setup 빌드 설정에 익숙할 경우 40분 이내 가능)