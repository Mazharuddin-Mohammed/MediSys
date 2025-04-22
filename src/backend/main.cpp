#include <iostream>
#include "db_manager.h"

int main() {
    try {
        DBManager db("dbname=medisys user=postgres password=secret host=localhost");
        db.initializeSchema();
        std::cout << "MediSys backend initialized successfully" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}