#pragma once
#include <pqxx/pqxx>
#include <string>
#include <memory>

class DBManager {
public:
    DBManager(const std::string& conn_str);
    ~DBManager();
    pqxx::connection& getConnection() { return *conn; }
    void initializeSchema();
    void setAuditContext(int user_id, const std::string& ip_address, const std::string& session_id);

private:
    std::unique_ptr<pqxx::connection> conn;
};