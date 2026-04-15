cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES C
)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

python_add_library(_claylib MODULE src/_clay_impl.c WITH_SOABI)

install(TARGETS _claylib DESTINATION pyclay)

target_include_directories(_claylib PRIVATE ${CMAKE_SOURCE_DIR}/clay)
