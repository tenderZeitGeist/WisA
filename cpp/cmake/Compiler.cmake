if (CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    # Debug: No optimizations, extra warnings
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG -O0 -Wall -Wextra -Wconversion -Wpedantic")
    # Release: Maximum performance, aggressive optimizations
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -flto -fvisibility=hidden")
    # MinSize: Optimize for minimum binary size, stripping symbols, removing unused functions, etc.
    set(CMAKE_CXX_FLAGS_MINSIZEREL "${CMAKE_CXX_FLAGS_MINSIZEREL} -Os -s -flto -fdata-sections -fvisibility=hidden")
    set(CMAKE_EXE_LINKER_FLAGS_MINSIZEREL "${CMAKE_EXE_LINKER_FLAGS_MINSIZEREL} -Wl,--gc-sections")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
    # Debug: No optimizations, extra warnings
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /DDEBUG /Od /W4 /WX /permissive-")
    # Release: Maximum performance, aggressive optimizations
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /O2 /GL /Gy /Zc:inline /fp:fast /D NDEBUG")
    # MinSize: Optimize for minimum binary size, stripping symbols, removing unused functions, etc.
    set(CMAKE_CXX_FLAGS_MINSIZEREL "${CMAKE_CXX_FLAGS_MINSIZEREL} /O1 /GL /Gy /Zc:inline /fp:fast /D NDEBUG")
    set(CMAKE_EXE_LINKER_FLAGS_MINSIZEREL "${CMAKE_EXE_LINKER_FLAGS_MINSIZEREL} /LTCG /OPT:REF /OPT:ICF")
else()
    message(FATAL_ERROR "Unknown compiler ID. Aborting CMake process.")
endif()
