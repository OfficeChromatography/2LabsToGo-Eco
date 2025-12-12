#!/bin/bash

# Setup script for Raspberry Pi OS Bookworm Lite compatibility
# This script prepares the system for firmware flashing

set -e

echo "=== 2LabsToGo-Eco Firmware Setup for Bookworm ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash setup_bookworm.sh"
    exit 1
fi

# Update package list
echo "Updating package list..."
apt update

# Install required packages
echo "Installing required packages..."
apt install -y libgpiod2 gpiod libgpiod-dev

# Check if avrdude supports linuxgpiod
echo "Checking avrdude version and linuxgpiod support..."
if command -v avrdude &> /dev/null && avrdude -c ? 2>&1 | grep -q "linuxgpio"; then
    echo "✓ avrdude with linuxgpiod support detected"
else
    echo "Building avrdude from source with gpiod support..."

    # Install build dependencies
    apt install -y build-essential git cmake libelf-dev libusb-dev \
        libhidapi-dev libftdi1-dev libreadline-dev flex bison

    # Remove old avrdude if installed
    apt remove -y avrdude || true

    echo "Cloning avrdude repository..."
    cd /tmp
    if [ -d "avrdude" ]; then
        rm -rf avrdude
    fi

    git clone https://github.com/avrdudes/avrdude.git
    cd avrdude
    git checkout v8.1

    echo "Building avrdude..."
    mkdir -p build
    cd build
    cmake -D CMAKE_BUILD_TYPE=Release \
          -D HAVE_LINUXGPIO=1 \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          ..

    # Check if cmake found libgpiod
    if grep -q "HAVE_LINUXGPIO:BOOL=1" CMakeCache.txt; then
        echo "✓ CMake detected linuxgpio support"
    else
        echo "✗ Error: CMake did not enable linuxgpio support"
        echo "CMake cache content:"
        grep -i "gpiod\|gpio" CMakeCache.txt || echo "No GPIO-related entries found"
        exit 1
    fi

    make -j$(nproc)
    make install

    # Update library cache
    ldconfig

    # Remove any old avrdude binaries from standard paths
    rm -f /usr/bin/avrdude

    echo "✓ avrdude installed from source"

    # Verify installation
    echo "Verifying avrdude installation..."
    AVRDUDE_PATH=$(which avrdude)
    echo "Using avrdude at: $AVRDUDE_PATH"

    # Test linuxgpio support
    if /usr/local/bin/avrdude -c ?type 2>&1 | grep -q "linuxgpio"; then
        echo "✓ linuxgpio programmer support confirmed"
    else
        echo "✗ Error: linuxgpio support not found"
        echo ""
        echo "Available programmer types:"
        /usr/local/bin/avrdude -c ?type 2>&1 | grep -i gpio || echo "No GPIO programmers found"
        exit 1
    fi

    # Verify libgpiod linkage
    if ldd /usr/local/bin/avrdude | grep -q libgpiod; then
        echo "✓ avrdude is linked against libgpiod library"
    else
        echo "✗ Error: avrdude is NOT linked against libgpiod library"
        exit 1
    fi
fi

# Verify GPIO chip exists
if [ ! -e /dev/gpiochip0 ]; then
    echo "⚠ Warning: /dev/gpiochip0 not found"
    echo "GPIO device may not be accessible"
else
    echo "✓ GPIO device found"
fi

# Add current user to gpio group (if not root)
if [ -n "$SUDO_USER" ]; then
    usermod -a -G gpio "$SUDO_USER"
    echo "✓ User $SUDO_USER added to gpio group"
    echo "  (You may need to log out and back in for this to take effect)"
fi

# Create udev rule for GPIO access
echo 'SUBSYSTEM=="gpio", KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"' > /etc/udev/rules.d/90-gpio.rules
udevadm control --reload-rules
udevadm trigger

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. If you're not root, log out and back in for group changes to take effect"
echo "2. Run: sudo bash flash_firmware.sh"
echo ""
