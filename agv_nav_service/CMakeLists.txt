cmake_minimum_required(VERSION 3.8)
project(agv_nav_service)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 1) 커스텀 서비스 인터페이스 생성 -> 파이썬에서 agv_nav_service.srv.CheckNavGoal 로 import 가능
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/CheckNavGoal.srv"
)
ament_export_dependencies(rosidl_default_runtime)

# 2) 파이썬 노드를 실행 파일로 설치 (확장자 없이 ros2 run 되도록 RENAME)
install(PROGRAMS scripts/nav_server.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME nav_server
)
install(PROGRAMS scripts/nav_client.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME nav_client
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
