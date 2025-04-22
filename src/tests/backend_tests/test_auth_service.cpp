#include <catch2/catch.hpp>
#include "../backend/core/services/auth_service.h"
#include "../backend/core/database/db_manager.h"

TEST_CASE("AuthService authenticates valid user", "[AuthService]") {
    auto db = std::make_shared<DBManager>("dbname=medisys_test user=postgres password=secret host=localhost sslmode=verify-full");
    db->initializeSchema();
    AuthService auth(db);

    // Insert test user
    pqxx::work txn(db->getConnection());
    txn.exec("INSERT INTO users (username, password_hash, role) VALUES ('testuser', '" + auth.hashPassword("testpass") + "', 'admin')");
    txn.commit();

    REQUIRE(auth.authenticate("testuser", "testpass") > 0);
}

TEST_CASE("AuthService rejects invalid password", "[AuthService]") {
    auto db = std::make_shared<DBManager>("dbname=medisys_test user=postgres password=secret host=localhost sslmode=verify-full");
    AuthService auth(db);

    REQUIRE_THROWS_AS(auth.authenticate("testuser", "wrongpass"), std::runtime_error);
}