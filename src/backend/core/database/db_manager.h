#pragma once

#include <string>
#include <memory>
#include <iostream>
#include <pqxx/pqxx>

class DBManager {
public:
    DBManager(const std::string& conn_str);
    ~DBManager();
    pqxx::connection& getConnection() { return *conn; }
    void initializeSchema();
    void setAuditContext(int user_id, const std::string& ip_address, const std::string& session_id);

    // Safely prepare a statement if it doesn't already exist
    void safelyPrepare(const std::string& name, const std::string& query);

    // Check if a prepared statement exists
    bool preparedStatementExists(const std::string& name);

private:
    std::unique_ptr<pqxx::connection> conn;
};