# RPGenerator


## Environment requirements
MacOS Mojave produces errors with Pygame. Known issue seen here: https://github.com/pygame/pygame/issues/555
Requirement: Download Python 3.7.2 from https://www.python.org with macOS 64-bit installer. 
Then run:
```
pip3 install pygame
pip3 install pygame-menu
python3 gameview.py
```

### Windows Install Instructions
Requirement: Download Python 3.7.2 from https://www.python.org for Windows 10.
Note that the MAX_PATH limitation should be expanded (see https://docs.python.org/3/using/windows.html#installation-steps)

Then run in Windows Powershell:
```
py -m pip install -U pygame --user
```
Test by running:
```
py -m pygame.examples.aliens
```