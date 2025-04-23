/**
 * MediSys Hospital Management System - Backend Main Entry Point
 *
 * This file contains the main entry point for the MediSys backend application.
 * It initializes the database connection and schema, serving as the standalone
 * backend process that can be used independently or with the frontend.
 *
 * Author: Mazharuddin Mohammed
 */

#include <iostream>
#include "core/database/db_manager.h"

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