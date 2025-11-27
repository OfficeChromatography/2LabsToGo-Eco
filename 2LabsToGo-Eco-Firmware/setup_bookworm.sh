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
if command -v avrdude &> /dev/null && avrdude -c ? 2>&1 | grep -q "linuxgpiod"; then
    echo "✓ avrdude with linuxgpiod support detected"
else
    echo "Building avrdude from source with gpiod support..."
    
    # Install build dependencies
    apt install -y build-essential git cmake libelf-dev libusb-dev \
        libhidapi-dev libftdi1-dev libreadline-dev flex bison libgpiod-dev
    
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
    cmake -D CMAKE_BUILD_TYPE=Release -D HAVE_LIBGPIOD=1 ..
    
    # Check if cmake found libgpiod
    if grep -q "HAVE_LIBGPIOD" CMakeCache.txt; then
        echo "✓ CMake detected libgpiod support"
    else
        echo "⚠ Warning: CMake may not have detected libgpiod"
    fi
    
    make -j$(nproc)
    make install

    # Update library cache
    ldconfig
    
    echo "✓ avrdude installed from source"
    
    # Verify installation - use full path to ensure we're testing the new installation
    echo "Verifying avrdude installation..."
    AVRDUDE_PATH=$(which avrdude)
    echo "Using avrdude at: $AVRDUDE_PATH"
    
    if /usr/local/bin/avrdude -c ? 2>&1 | grep -q "linuxgpiod"; then
        echo "✓ linuxgpiod programmer support confirmed"
    else
        echo "⚠ Warning: linuxgpiod support not found in programmer list"
        echo ""
        echo "Attempting manual verification..."
        # Try to see if the library is linked
        if ldd /usr/local/bin/avrdude | grep -q libgpiod; then
            echo "✓ avrdude is linked against libgpiod library"
        else
            echo "✗ avrdude is NOT linked against libgpiod library"
            echo "This may indicate a build configuration issue"
        fi
        echo ""
        echo "You can manually check available programmers with: avrdude -c ?"
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
