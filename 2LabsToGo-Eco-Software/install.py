import subprocess


# FUNCTIONS
def check_error(process):
    # Print the result of a process execution
    if process.returncode == 0:
        print("-----------------------\tSUCCESS!-----------------------\t")
    else:
        print("-----------------------\tERROR!-----------------------\t")


def execute_command(command_list):
    # Receive the list that conforms a command and execute it
    process = subprocess.run(command_list)
    check_error(process)
    print("\n")


class InstallationProcess:

    def __init__(self) -> object:
        self.version = 1.0
        self.main_title = "\n\t WELCOME TO 2LabsToGo-Eco-Software INSTALLATION PROCESS\n"
        # The commands should be written as a list of strings, otherwise could fail.
        # Don't try to run RAW strings instead of list, if your string uses user input,
        # as they may inject arbitrary code!
        # https://queirozf.com/entries/python-3-subprocess-examples#run-raw-string-as-a-shell-command-line
        self.command = {
            "update": ["sudo", "apt-get", "update"],
            "upgrade": ["sudo", "apt-get", "upgrade", "-y"],
            "pip3": ['sudo', 'apt-get', 'install', 'python3-pip', '-y'],
            "curl": ['sudo', 'apt-get', 'install', 'curl', '-y'],
            "docker download": ["sudo", "curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"],
            "docker installation": ["sudo", "sh", "get-docker.sh"],
            "install_docker_compose": ["sudo", "pip3", "install", "docker-compose"],
            "install_libraries": ["sudo", "apt-get", "install", "-y", "libffi-dev", "libssl-dev"],
            "autoremove": ["sudo", "apt-get", "autoremove", "-y"],
        }

        print(self.main_title)
        self.installation_process()

    def __str__(self):
        print(self.version)

    def installation_process(self):
        # Executes each of the commands in the dictionary 'commands'
        for key, value in self.command.items():
            print(f"-----------------------\t{key.upper()}\t-----------------------")
            execute_command(value)


if __name__ == "__main__":
    InstallationProcess()
