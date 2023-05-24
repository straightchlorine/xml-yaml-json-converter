#!/bin/bash

pip_installed() {
  command -v pip >/dev/null 2>&1

  if [ $? -eq 0 ]; then
      echo "pip is installed."
  else
      echo "pip is not installed, proceeding to installation..."
      python -m ensurepip --upgrade
  fi
}

module_installed() {
  # name of the module, required for installation
  module=$1

  # import <module> in python code
  import=$2

  # checking whether import is any different than module
  if [ -z "$2" ]; then
    import=$module
  fi

  python -c "import ${import}" >/dev/null 2>&1

  # checking if the last command returned 0, if so then installed
  if [ $? -eq 0 ]; then
        echo "${module} is installed, skipping the installation."
  else
      echo "${module} is not installed, proceeding to installation..."
      pip install ${module}
  fi
}

generate_executable() {
  # check if the executable exists
  if [ -f ./dist/markupconverter ]; then
    echo "Executable present, skipping the generation."
  else
    echo "Proceeding to generation of an executable..."

    # generate
    pyinstaller --onefile -noconsole markupconverter.py -n markupconverter.exe 2>&1

    if [ $? -eq 0 ]; then
      echo "Generation finished successfuly."
    else
      echo "Failed to generate executable."
    fi
  fi
}

# required modules
pip_installed
module_installed pyinstaller PyInstaller
module_installed xmltodict
module_installed pyyaml yaml
module_installed PyQt5

sudo apt-get update
sudo apt-get install -y '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev build-essential qtbase5-dev

generate_executable
