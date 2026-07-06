# 🛠️ 실습과제 워크시트 — 항만 AGV 이동 구역 안전 승인 서비스

> **주제**: ROS 2 커스텀 서비스(`.srv`) + 비동기 서버/클라이언트 프로그래밍
> **난이도**: ⭐⭐⭐ 중급 · **예상 소요 시간**: 60~90분 · **환경**: ROS 2 Humble / Python(`rclpy`)

이 워크시트는 스켈레톤 코드(`agv_nav_service/`)의 `TODO` 를 직접 채워
서비스 통신 파이프라인을 완성하는 **채움형(fill-in) 실습**입니다.
막히면 `solution/` 폴더의 정답을 참고하세요.

---

## 0. 학습 목표 (체크리스트)

실습을 마치면 다음을 설명·구현할 수 있어야 합니다.

- [ ] 서비스(Service) 통신과 토픽(Topic) 통신의 **차이**를 말할 수 있다.
- [ ] 커스텀 `.srv` 파일의 **요청/응답(`---`) 구조**를 작성할 수 있다.
- [ ] `package.xml` / `CMakeLists.txt` 에 **인터페이스 빌드 의존성**을 추가할 수 있다.
- [ ] `create_service` 로 서버를, `create_client` 로 클라이언트를 만들 수 있다.
- [ ] `call_async` + `spin_once` + `future.done()` 으로 **비차단(Non-blocking) 응답**을 처리할 수 있다.
- [ ] `try/except/else` 로 서비스 호출 **예외를 안전하게** 처리할 수 있다.

---

## 1. 사전 준비 (Setup)

```bash
# 1) 워크스페이스 생성
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 2) 이 저장소를 clone (또는 압축 해제)
git clone <이-저장소-URL> ros-service-practice

# 3) 실습 패키지를 src 아래에 둔다
#    colcon 은 src 안의 package.xml 을 자동 탐색한다.
cp -r ros-service-practice/agv_nav_service ~/ros2_ws/src/agv_nav_service
```

> 💡 **왜 복사하나요?** `agv_nav_service/` 만 실제 빌드 대상(ROS 패키지)이고,
> 저장소 루트에는 워크시트·정답·문서가 함께 들어 있기 때문입니다.
> 정답으로 실습하려면 `solution/agv_nav_service` 를 대신 복사하세요.

**환경 점검**

```bash
printenv ROS_DISTRO        # -> humble 이 나와야 함
source /opt/ros/humble/setup.bash
```

---

## 2. 개념 워밍업 (빈칸 채우기)

> 코드를 짜기 전에 개념을 정리합니다. 답은 자유롭게 적어보세요.

| # | 질문 | 나의 답 |
|---|------|---------|
| Q1 | 토픽은 (①______) 통신, 서비스는 (②______) 통신이다. | |
| Q2 | `.srv` 파일에서 요청과 응답을 나누는 구분자는? | |
| Q3 | `call_async` 가 즉시 반환하는 객체의 이름은? | |
| Q4 | 응답이 도착했는지 확인하는 메서드는 `future.____()` ? | |
| Q5 | 서버 노드는 왜 `spin()`, 클라이언트는 왜 `spin_once()` 를 주로 쓰나? | |

<details>
<summary>정답 보기</summary>

- Q1: ① 단방향/발행-구독(다:다) · ② 요청-응답(1:1)
- Q2: `---` (세 개의 하이픈)
- Q3: `future` (미래 결과 핸들)
- Q4: `done`
- Q5: 서버는 요청을 **계속** 대기해야 하므로 `spin()`, 클라이언트는 응답 1건만 폴링하면 되므로 루프 안에서 `spin_once()` 로 제어권을 잠깐씩 넘겨준다.
</details>

---

## 3. 단계별 과제 (Tasks)

각 Task 를 끝낼 때마다 ✅ 체크하고, **확인 명령**으로 검증하세요.

### ✅ Task 1 — 커스텀 서비스 인터페이스 이해

`agv_nav_service/srv/CheckNavGoal.srv` 를 열어 구조를 확인합니다.

```text
float64 target_x     # 요청: 목표 x
float64 target_y     # 요청: 목표 y
---
bool    is_approved  # 응답: 승인 여부
float64 estimated_time  # 응답: 예상 소요 시간
```

**미니 과제**: 아래 표를 채우세요.

| 필드 | 요청/응답 | 타입 | 의미 |
|------|-----------|------|------|
| `target_x` | | | |
| `is_approved` | | | |
| `estimated_time` | | | |

---

### ✅ Task 2 — 서버 완성 (`nav_server.py`)

`agv_nav_service/scripts/nav_server.py` 의 **TODO(1)~(5)** 를 채웁니다.

| TODO | 할 일 |
|------|-------|
| (1) | `from agv_nav_service.srv import CheckNavGoal` import |
| (2) | `create_service(CheckNavGoal, 'check_goal', self.goal_callback)` |
| (3) | `target_x`, `target_y` 가 `0.0~100.0` 인지 검사 |
| (4) | 통과 시 `is_approved=True`, `estimated_time=(x+y)*0.1` |
| (5) | 실패 시 `is_approved=False`, `estimated_time=0.0` |

> ⚠️ **함정**: `pass` 로 남겨둔 자리 표시 줄을 지웠나요? 응답 필드를 채우지 않으면 승인 결과가 항상 기본값이 됩니다.

---

### ✅ Task 3 — 클라이언트 완성 (`nav_client.py`)

`agv_nav_service/scripts/nav_client.py` 의 **TODO(1)~(6)** 를 채웁니다.

| TODO | 할 일 |
|------|-------|
| (1) | 커스텀 서비스 타입 import |
| (2) | `create_client(CheckNavGoal, 'check_goal')` |
| (3) | `wait_for_service(timeout_sec=1.0)` 로 서버 대기 |
| (4) | `CheckNavGoal.Request()` 생성 |
| (5) | 좌표 채우고 `call_async` 호출 → `future` 반환 |
| (6) | `spin_once` 폴링 + `future.done()` + `try/except/else` 로 결과 처리 |

> 💡 **핵심 학습 포인트(TODO 6)**: 왜 `spin_once` 를 루프로 돌릴까요?
> `call_async` 는 응답을 기다리지 않고 즉시 반환하므로, 노드를 계속 스핀시키며
> `future.done()` 을 폴링해야 응답을 받을 수 있습니다. 이렇게 하면 응답을 기다리는
> 동안에도 노드가 멈추지 않습니다(Non-blocking).

---

### ✅ Task 4 — 빌드

```bash
cd ~/ros2_ws
colcon build --packages-select agv_nav_service
source install/setup.bash          # ← 빌드 후 반드시 source!
```

**확인**: 인터페이스가 생성됐는지 검사

```bash
ros2 interface show agv_nav_service/srv/CheckNavGoal
# 위에서 본 요청/응답 구조가 그대로 출력되면 성공
```

<details>
<summary>🚑 빌드가 안 될 때 자주 하는 실수</summary>

- `source /opt/ros/humble/setup.bash` 를 안 함 → `colcon` / 의존성 없음
- 빌드 후 `source install/setup.bash` 를 안 함 → `ros2 run` 이 노드를 못 찾음
- `package.xml` 에 `member_of_group>rosidl_interface_packages` 누락 → 인터페이스 미생성
- 패키지를 `~/ros2_ws/src/` 아래에 안 둠 → colcon 이 탐색 못 함
</details>

---

### ✅ Task 5 — 실행 & 검증

**터미널 1 — 서버**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run agv_nav_service nav_server
```

**터미널 2 — 클라이언트 (승인 케이스: 구역 안)**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run agv_nav_service nav_client 50 50
```

**터미널 2 — 거부 케이스 (구역 밖)**
```bash
ros2 run agv_nav_service nav_client 45 110
```

**기대 결과 표** — 직접 채워보세요.

| 입력 (x, y) | is_approved | estimated_time | 승인/거부 |
|-------------|-------------|----------------|-----------|
| (50, 50)   | | | |
| (45, 110)  | | | |
| (0, 0)     | | | |
| (100, 100) | | | |
| (-1, 50)   | | | |

<details>
<summary>정답 보기</summary>

| 입력 (x, y) | is_approved | estimated_time | |
|---|---|---|---|
| (50, 50) | True | 10.0 | 승인 |
| (45, 110) | False | 0.0 | 거부(y 초과) |
| (0, 0) | True | 0.0 | 승인(경계값) |
| (100, 100) | True | 20.0 | 승인(경계값) |
| (-1, 50) | False | 0.0 | 거부(x 음수) |
</details>

---

### ✅ Task 6 — CLI 로 직접 호출 (코드 수정 없이)

```bash
ros2 service call /check_goal agv_nav_service/srv/CheckNavGoal "{target_x: 50.0, target_y: 50.0}"
```

**미니 과제**: `ros2 service list`, `ros2 service type /check_goal` 명령의 출력을 적어보세요.

---

## 4. 제출/완료 기준 (Definition of Done)

- [ ] `ros2 interface show` 로 커스텀 srv 가 정상 출력된다.
- [ ] 승인 케이스와 거부 케이스가 **서버·클라이언트 로그 양쪽에** 올바르게 찍힌다.
- [ ] `ros2 service call` CLI 호출이 성공한다.
- [ ] Task 5 의 기대 결과 표 5개 행이 모두 정답과 일치한다.
- [ ] (개념) 워밍업 Q1~Q5 를 자기 말로 설명할 수 있다.

---

## 5. 도전 과제 (Stretch Goals) — 선택

난이도를 한 단계 올리고 싶다면 시도해 보세요.

1. **🟡 다중 안전 구역**: 사각형 하나가 아니라 여러 허용 구역(리스트)을 검사하도록 서버를 확장.
2. **🟡 응답 메시지 추가**: `.srv` 응답에 `string reason`(거부 사유)을 추가하고 빌드 → 클라이언트에서 출력.
3. **🟠 타임아웃 처리**: 클라이언트에서 N초 안에 응답이 없으면 `timeout` 로그를 남기고 종료.
4. **🟠 파라미터화**: 안전 구역 경계(`SAFE_MIN/MAX`)를 ROS 파라미터로 선언해 실행 시 변경.
5. **🔴 launch 파일**: 서버·클라이언트를 한 번에 띄우는 `launch/agv.launch.py` 작성.

> 도전 과제 2번을 하면 `.srv` 를 바꾼 뒤 **반드시 다시 `colcon build`** 해야 함을 체감할 수 있습니다.

---

## 6. 자주 겪는 오류 & 해결 (Troubleshooting)

| 증상 | 원인 | 해결 |
|------|------|------|
| `No module named 'agv_nav_service.srv'` | 빌드/소싱 안 됨 | `colcon build` 후 `source install/setup.bash` |
| `ros2 run` 이 실행 파일을 못 찾음 | 소싱 누락 / 설치 안 됨 | 새 터미널에서 `source install/setup.bash` |
| 클라이언트가 무한 대기 | 서버 미실행 | 터미널 1에서 서버 먼저 실행 |
| 승인 결과가 항상 False | TODO(4) 미완성 / `pass` 미삭제 | 서버 콜백의 응답 필드 채우기 |
| CLI 호출 시 타입 에러 | 좌표를 정수로 입력 | `50.0` 처럼 `float` 로 입력 |

---

### 📎 참고

- 설계 배경/전체 개요: [`README.md`](README.md)
- 정답 코드: [`solution/`](solution/)
- ROS 2 공식 튜토리얼: *Writing a simple service and client (Python)* — docs.ros.org (Humble)
