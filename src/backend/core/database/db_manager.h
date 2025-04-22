#pragma once

#include <string>
#include <memory>
#include <iostream>

#ifndef MOCK_DATABASE
#include <pqxx/pqxx>
#else
// Mock pqxx namespace for when PostgreSQL is not available
namespace pqxx {
    class connection {
    public:
        connection(const std::string&) {}
        bool is_open() const { return true; }
        void close() {}
        void prepare(const std::string&, const std::string&) {}
    };

    class work {
    public:
        work(connection&) {}
        void exec(const std::string&) {}
        void exec_prepared(const std::string&, ...) {}
        void commit() {}
    };

    template<typename... Args>
    std::string to_json(Args&&...) { return "{}"; }
}
#endif

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