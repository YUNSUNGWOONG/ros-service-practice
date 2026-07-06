# 🚢 ROS 2 Service Practice — 항만 AGV 이동 구역 안전 승인 서비스

ROS 2의 **서비스(Service) 통신**을 손으로 익히는 실습 교육용 프로젝트입니다.
항만 자율주행 물류 로봇(AGV)이 목적지로 이동하기 전, 관제 시스템에 좌표의
이동 가능 여부를 질의하고 승인받는 시나리오를 커스텀 `.srv` + 비동기
서버/클라이언트로 구현합니다.

> **환경**: ROS 2 Humble · Python(`rclpy`) · **난이도**: ⭐⭐⭐ 중급 · **소요**: 60~90분

---

## 🎯 이 실습에서 배우는 것

- 커스텀 서비스 인터페이스(`.srv`)의 요청/응답 구조 설계 및 빌드
- `create_service` 기반 **서비스 서버** 구현 (좌표 검증 로직)
- `create_client` + `call_async` 기반 **비동기 클라이언트** 구현
- `spin_once` / `future.done()` 폴링으로 **비차단(Non-blocking) 응답 처리**
- `try/except/else` 를 이용한 서비스 호출 **예외 처리**

---

## 📂 저장소 구조

```text
ros-service-practice/
├── README.md                  # 지금 이 파일
├── WORKSHEET.md               # ⭐ 실습과제 워크시트 (여기서 시작하세요)
├── LICENSE
├── .gitignore
├── docs/
│   └── OVERVIEW.md            # 프로젝트 설계 배경 / 상세 개요
├── agv_nav_service/           # 👉 학생용 스켈레톤 패키지 (TODO 채우기)
│   ├── package.xml
│   ├── CMakeLists.txt
│   ├── srv/CheckNavGoal.srv
│   └── scripts/
│       ├── nav_server.py      #   TODO(1)~(5)
│       └── nav_client.py      #   TODO(1)~(6)
└── solution/                  # ✅ 완성된 정답 패키지 (막힐 때 참고)
    └── agv_nav_service/
        ├── package.xml
        ├── CMakeLists.txt
        ├── srv/CheckNavGoal.srv
        └── scripts/
            ├── nav_server.py
            └── nav_client.py
```

> **핵심**: `agv_nav_service/` 는 미완성 스켈레톤입니다. `TODO` 를 직접 채워
> 완성하는 것이 과제이며, 완성본은 `solution/` 에서 확인할 수 있습니다.

---

## 🚀 빠른 시작 (Quick Start)

```bash
# 1) 워크스페이스 준비
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone <이-저장소-URL> ros-service-practice

# 2) 실습 패키지를 src 아래로 복사
cp -r ros-service-practice/agv_nav_service ~/ros2_ws/src/agv_nav_service
#    (정답으로 바로 돌려보려면 solution/agv_nav_service 를 복사)

# 3) WORKSHEET.md 를 따라 TODO 를 채운 뒤 빌드
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select agv_nav_service
source install/setup.bash

# 4) 실행 — 터미널 2개
ros2 run agv_nav_service nav_server          # 터미널 1 (서버)
ros2 run agv_nav_service nav_client 50 50    # 터미널 2 (승인 케이스)
ros2 run agv_nav_service nav_client 45 110   # 터미널 2 (거부 케이스)

# 5) CLI 로 직접 호출
ros2 service call /check_goal agv_nav_service/srv/CheckNavGoal "{target_x: 50.0, target_y: 50.0}"
```

기대 동작: 좌표가 안전 구역(0~100)이면 **승인 + 예상 소요 시간**, 벗어나면 **거부**.

---

## 📝 실습 진행 방법

1. **[WORKSHEET.md](WORKSHEET.md) 를 엽니다** — 개념 워밍업 → Task 1~6 → 도전 과제 순.
2. `agv_nav_service/scripts/` 의 `TODO` 를 채웁니다.
3. 각 Task 의 **확인 명령**으로 검증하고 체크리스트를 채웁니다.
4. 막히면 `solution/` 의 정답과 비교합니다.

강의/스터디에서 쓴다면 `solution/` 폴더를 배포 직전까지 감춰 두고
`agv_nav_service/` 만 학생에게 주는 방식으로 운영할 수 있습니다.

---

## 🧩 빌드 방식 참고

이 패키지는 **커스텀 인터페이스(`.srv`)와 파이썬 노드를 한 패키지에서** 다루기 위해
`ament_cmake` + `rosidl_generate_interfaces` 로 srv 를 생성하고, 파이썬 노드는
`install(PROGRAMS ... RENAME)` 으로 실행 파일로 설치합니다. 덕분에
`ros2 run agv_nav_service nav_server` 처럼 확장자 없이 실행할 수 있습니다.

---

## 📄 라이선스

Apache-2.0 — 자유롭게 학습·수정·재배포할 수 있습니다.
