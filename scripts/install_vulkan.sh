#!/bin/bash
set -e

echo "Installing Vulkan dependencies..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS. Please install Vulkan manually."
    exit 1
fi

# Install Vulkan based on OS
case $OS in
    ubuntu|debian)
        apt-get update
        apt-get install -y libvulkan1 vulkan-tools libvulkan-dev
        ;;
    fedora|rhel|centos)
        dnf install -y vulkan vulkan-tools vulkan-loader-devel
        ;;
    arch|manjaro)
        pacman -Sy --noconfirm vulkan-icd-loader vulkan-tools vulkan-headers
        ;;
    *)
        echo "Unsupported OS: $OS. Please install Vulkan manually."
        exit 1
        ;;
esac

echo "Vulkan dependencies installed successfully!"
