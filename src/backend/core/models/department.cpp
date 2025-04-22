#include "department.h"

bool DepartmentModel::isValidName(const std::string& name) {
    return !name.empty() && name.length() <= 100;
}

bool DepartmentModel::isValidDescription(const std::string& description) {
    return description.length() <= 1000; // Allow empty or long descriptions
}