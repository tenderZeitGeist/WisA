
#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace algorithm {

namespace heap {
void sort(std::vector<int>& container);
void sort(std::vector<float>& container);
void sort(std::vector<std::string>& container);
}

namespace quick {
void sort(std::vector<int>& container);
void sort(std::vector<float>& container);
void sort(std::vector<std::string>& container);
}

namespace insertion {
void sort(std::vector<int>& container);
void sort(std::vector<float>& container);
void sort(std::vector<std::string>& container);
}

}