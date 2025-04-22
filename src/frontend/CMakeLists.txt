# Install Python files and resources
install(DIRECTORY python/ DESTINATION ${CMAKE_INSTALL_PREFIX}/medisys/frontend
        FILES_MATCHING PATTERN "*.py" PATTERN "*.png" PATTERN "*.qss")