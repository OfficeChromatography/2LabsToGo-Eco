#!/usr/bin/python3
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Manage Docker Compose for 2LabsToGo-Eco"
    )
    parser.add_argument(
        "--build", action="store_true", help="Rebuild the app before starting"
    )
    args = parser.parse_args()

    subprocess.run(["sudo", "docker", "compose", "pause"], stderr=subprocess.PIPE)
    subprocess.run(["sudo", "docker", "compose", "unpause"], stderr=subprocess.PIPE)

    if args.build:
        subprocess.run(["sudo", "docker", "compose", "up", "--build"])
    else:
        subprocess.run(["sudo", "docker", "compose", "up"])


if __name__ == "__main__":
    main()
