
# Debug: No optimizations, extra warnings
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG -O0 -Wall -Wextra -Wconversion -Wpedantic")
# Release: Maximum performance, aggressive optimizations
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -flto -fvisibility=hidden")
# MinSize: Optimize for minimum binary size, stripping symbols, removing unused functions, etc.
set(CMAKE_CXX_FLAGS_MINSIZEREL "${CMAKE_CXX_FLAGS_MINSIZEREL} -Os -s -flto -fdata-sections -fvisibility=hidden")
set(CMAKE_EXE_LINKER_FLAGS_MINSIZEREL "${CMAKE_EXE_LINKER_FLAGS_MINSIZEREL} -Wl,--gc-sections")

