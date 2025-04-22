# MediSys Installation Guide

This guide will help you install and run the MediSys application.

## Prerequisites

Before you can build and run MediSys, you need to install the following dependencies:

### 1. PostgreSQL

MediSys requires PostgreSQL for its database functionality.

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib libpq-dev
```

#### Fedora/RHEL
```bash
sudo dnf install postgresql postgresql-server postgresql-contrib postgresql-devel
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS
```bash
brew install postgresql
brew services start postgresql
```

### 2. Vulkan

MediSys requires Vulkan for its rendering capabilities.

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install libvulkan1 vulkan-tools libvulkan-dev
```

#### Fedora/RHEL
```bash
sudo dnf install vulkan vulkan-tools vulkan-loader-devel
```

#### macOS
```bash
brew install molten-vk vulkan-tools
```

### 3. Python Dependencies

MediSys requires several Python packages.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Building MediSys

Once you have installed all the prerequisites, you can build MediSys:

```bash
source venv/bin/activate
./scripts/build.sh
```

## Setting up the Database

Before running MediSys, you need to set up the database:

```bash
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb medisys
./scripts/setup_db.sh
```

## Running MediSys

Finally, you can run MediSys:

```bash
source venv/bin/activate
./scripts/run.sh
```

## Troubleshooting

### PostgreSQL Issues

If you encounter issues with PostgreSQL, make sure the service is running:

```bash
sudo systemctl status postgresql
```

If it's not running, start it:

```bash
sudo systemctl start postgresql
```

### Vulkan Issues

If you encounter issues with Vulkan, check if your GPU supports Vulkan:

```bash
vulkaninfo
```

If your GPU doesn't support Vulkan, you may need to use a software renderer or update your GPU drivers.

### Python Issues

If you encounter issues with Python dependencies, make sure you're using the virtual environment:

```bash
source venv/bin/activate
```

And that all dependencies are installed:

```bash
pip install -r requirements.txt
```
