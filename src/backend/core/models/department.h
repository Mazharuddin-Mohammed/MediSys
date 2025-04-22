#pragma once
#include <string>

struct Department {
    int id;
    std::string name;
    int head_id;
    std::string description;
};

class DepartmentModel {
public:
    static bool isValidName(const std::string& name);
    static bool isValidDescription(const std::string& description);
};