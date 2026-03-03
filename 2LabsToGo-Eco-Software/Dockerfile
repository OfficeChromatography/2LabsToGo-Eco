# first stage
FROM python:3.13-trixie

# Install system dependencies first
RUN apt update && apt install -y curl --no-install-recommends

# Add Raspberry Pi repository for picamera2
RUN echo "deb [signed-by=/etc/apt/keyrings/raspberrypi.gpg] http://archive.raspberrypi.org/debian/ trixie main" | tee /etc/apt/sources.list.d/raspberrypi.list
RUN curl -sSL https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | gpg --dearmor -o /etc/apt/keyrings/raspberrypi.gpg
RUN apt update && apt install -y python3-picamera2 --no-install-recommends

# Install pip dependencies
COPY requirements/base.txt /base_requirements4.txt
RUN pip install --no-cache-dir -r /base_requirements4.txt

ENV PYTHONUNBUFFERED=1

# Set PYTHONPATH to prefer pip packages over system packages
ENV PYTHONPATH=/usr/local/lib/python3.13/site-packages:/usr/lib/python3/dist-packages


WORKDIR /app

# Debugging commands:
# docker run -it <image_id> <one of the below commands>
# python -c "import sys; print('\n'.join(sys.path))"
# find /usr -name "pykms*"
# find /usr -name "libcamera*" | grep -E "\.(so|py)$"