#include <catch2/catch.hpp>
#include "../backend/core/database/db_manager.h"

TEST_CASE("DBManager initializes schema", "[DBManager]") {
    DBManager db("dbname=medisys_test user=postgres password=secret host=localhost sslmode=verify-full");
    REQUIRE_NOTHROW(db.initializeSchema());

    pqxx::work txn(db.getConnection());
    auto result = txn.exec("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')");
    REQUIRE(result[0][0].as<bool>());
}

TEST_CASE("DBManager sets audit context", "[DBManager]") {
    DBManager db("dbname=medisys_test user=postgres password=secret host=localhost sslmode=verify-full");
    REQUIRE_NOTHROW(db.setAuditContext(1, "192.168.1.1", "session_123"));

    pqxx::work txn(db.getConnection());
    auto result = txn.exec("SELECT current_setting('medisys.user_id')");
    REQUIRE(result[0][0].as<std::string>() == "1");
}