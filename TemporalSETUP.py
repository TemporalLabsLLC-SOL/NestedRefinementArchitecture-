#!/usr/bin/env python3

import subprocess
import sys
import os

def run_command(command, sudo=False, check=True, shell=False):
    """
    Runs a shell command.
    
    :param command: List of command arguments or string if shell=True
    :param sudo: Whether to run the command with sudo
    :param check: Whether to check for errors
    :param shell: Whether to execute the command through the shell
    :return: CompletedProcess instance
    """
    if sudo:
        if shell:
            command = f"sudo {command}"
        else:
            command = ['sudo'] + command
    print(f"Running command: {' '.join(command) if not shell else command}")
    return subprocess.run(command, check=check, shell=shell)

def main():
    try:
        print("Updating package lists...")
        run_command(['apt', 'update', '-y'], sudo=True)

        print("Installing software-properties-common...")
        run_command(['apt', 'install', 'software-properties-common', '-y'], sudo=True)

        print("Adding deadsnakes PPA...")
        run_command(['add-apt-repository', 'ppa:deadsnakes/ppa', '-y'], sudo=True)

        print("Updating package lists after adding PPA...")
        run_command(['apt', 'update', '-y'], sudo=True)

        print("Installing Python 3.10 and related packages...")
        run_command(['apt', 'install', 'python3.10', 'python3.10-venv', 'python3.10-dev', '-y'], sudo=True)

        print("Installing Python 3.12 and related packages...")
        run_command(['apt', 'install', 'python3.12', 'python3.12-venv', 'python3.12-dev', '-y'], sudo=True)

        print("Installing Tkinter for Python 3...")
        run_command(['apt', 'install', 'python3-tk', '-y'], sudo=True)

        print("Downloading get-pip.py script...")
        run_command(['curl', '-sS', 'https://bootstrap.pypa.io/get-pip.py', '-o', 'get-pip.py'])

        print("Installing pip for Python 3.10...")
        run_command(['python3.10', 'get-pip.py'], sudo=True)

        print("Installing pip for Python 3.12...")
        run_command(['python3.12', 'get-pip.py'], sudo=True)

        print("Cleaning up get-pip.py...")
        os.remove('get-pip.py')

        print("Installing ffmpeg...")
        run_command(['apt', 'install', 'ffmpeg', '-y'], sudo=True)

        print("Installing Ollama...")
        # Safely downloading and executing the Ollama install script
        run_command(['curl', '-fsSL', 'https://ollama.com/install.sh', '-o', 'install_ollama.sh'], sudo=True)
        run_command(['sh', 'install_ollama.sh'], sudo=True)
        os.remove('install_ollama.sh')

        print("Configuring tomcat9 service...")

        print("Copying tomcat9.service to /etc/systemd/system/...")
        run_command(['cp', '/lib/systemd/system/tomcat9.service', '/etc/systemd/system/'], sudo=True)

        print("Modifying tomcat9.service to include GUACAMOLE_HOME environment variable...")
        # Use sudo and sed to append the environment variable
        sed_command = r'/Environment=/ s/$/ GUACAMOLE_HOME=\/etc\/temporal/'
        run_command(['sed', '-i', sed_command, '/etc/systemd/system/tomcat9.service'], sudo=True)

        print("Reloading systemd daemon...")
        run_command(['systemctl', 'daemon-reload'], sudo=True)

        print("Restarting tomcat9 service...")
        run_command(['systemctl', 'restart', 'tomcat9'], sudo=True)

        print("Verifying tomcat9 environment variables...")
        # Filtering Environment variables
        run_command(['systemctl', 'show', 'tomcat9', '--property=Environment'], sudo=True)

        print("Verifying installation...")
        run_command(['python3.10', '--version'])
        run_command(['python3.12', '--version'])
        run_command(['python3.10', '-m', 'pip', '--version'])
        run_command(['python3.12', '-m', 'pip', '--version'])
        run_command(['ffmpeg', '-version'])
        run_command(['ollama', 'version'])

        print("\nOptional: Updating default python3 to Python 3.10")
        print("WARNING: This may cause issues with system scripts that rely on Python 3.8.")
        user_input = input("Do you want to update the default python3 to Python 3.10? [y/N]: ").strip().lower()
        if user_input == 'y':
            print("Removing existing python3 symlink...")
            run_command(['rm', '/usr/bin/python3'], sudo=True)
            print("Creating new symlink for python3.10...")
            run_command(['ln', '-s', 'python3.10', '/usr/bin/python3'], sudo=True)
            print("Verifying new python3 version...")
            run_command(['python3', '--version'])
        else:
            print("Skipping update of default python3.")

        print("Installing CUDA Toolkit 12.6.3...")
        # Download the CUDA pin file
        run_command(['wget', 'https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin'], sudo=False)
        run_command(['sudo', 'mv', 'cuda-ubuntu2004.pin', '/etc/apt/preferences.d/cuda-repository-pin-600'], sudo=True)

        # Download the CUDA repository package
        run_command(['wget', 'https://developer.download.nvidia.com/compute/cuda/12.6.3/local_installers/cuda-repo-ubuntu2004-12-6-local_12.6.3-560.35.05-1_amd64.deb'], sudo=False)
        run_command(['sudo', 'dpkg', '-i', 'cuda-repo-ubuntu2004-12-6-local_12.6.3-560.35.05-1_amd64.deb'], sudo=True)

        # Add the CUDA GPG key
        run_command(['sudo', 'cp', '/var/cuda-repo-ubuntu2004-12-6-local/cuda-*-keyring.gpg', '/usr/share/keyrings/'], sudo=True)

        print("Updating package lists for CUDA...")
        run_command(['sudo', 'apt-get', 'update'], sudo=True)

        print("Installing CUDA Toolkit 12.6...")
        run_command(['sudo', 'apt-get', '-y', 'install', 'cuda-toolkit-12-6'], sudo=True)

        print("Verifying CUDA installation...")
        run_command(['nvcc', '--version'])

        print("\nAll done! Python 3.10, Python 3.12, Tkinter, ffmpeg, Ollama, tomcat9, and CUDA Toolkit are installed and configured.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running command: {' '.join(e.cmd) if isinstance(e.cmd, list) else e.cmd}")
        print(f"Error message: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Command not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the script is run with root privileges
    if os.geteuid() != 0:
        print("This script requires administrative privileges. Please run as root or use sudo.")
        sys.exit(1)
    main()
