# RPGenerator

*Computer Software Enginnering Capstone Project*

Written by:

Bianca Angotti, Shally Banh, Andrew McKernan, Thomas Tetz


## Environment requirements
### macOS Install Instructions
macOS Mojave produces errors with Pygame. 

Known issue seen here: https://github.com/pygame/pygame/issues/555

**Requirement**: Download Python 3.7.2 from https://www.python.org for macOS 64-bit installer. 

Run:
```
pip3 install pygame
pip3 install pygame-menu
python3 gameview.py
```

### Windows Install Instructions
**Requirement**: Download Python 3.7.2 from https://www.python.org for Windows 10.

Note that the MAX_PATH limitation should be expanded (see https://docs.python.org/3/using/windows.html#installation-steps)

Then run in Windows Powershell:
```
py -m pip install -U pygame --user
```
Test by running:
```
py -m pygame.examples.aliens
```

### Docker Image Instructions
A Docker image exists for automated testing. It does not have graphical capability.

**Requirement**: Docker must be installed.

Pull the image:
```
docker pull ttetz/capstone-docker
```
Launch a container:
```
./docker_setup.sh -li
```

### pip3 Instructions
```
pip3 install --requirement requirements.txt --user
```