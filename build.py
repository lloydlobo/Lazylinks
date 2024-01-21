"""
 **To create a standalone executable from this Python script:**

1. **Install PyInstaller:** `pip install pyinstaller`

2. **Build the executable:**
   - Single file: `pyinstaller --onefile lazylinks.py`
   - GUI without console: `pyinstaller --onefile --noconsole lazylinks.py`
   - Specific name: `pyinstaller --onefile --noconsole --name Lazylinks lazylinks.py`
   - `pyinstaller --onefile --noconsole --name Lazylinks lazylinks.py`

3. **Copy configuration file:** Place `config.json` (or similar) into the `dist` folder alongside the executable.

**Dependencies:**

# requirements.txt

altgraph==0.17.4
packaging==23.2
pefile==2023.2.7
pyinstaller==6.3.0
pyinstaller-hooks-contrib==2024.0
pywin32-ctypes==0.2.2
setuptools==69.0.3
"""

import os
import shutil
import subprocess


def run_pyinstaller(script_name, exe_name):
    subprocess.run(f"pyinstaller --onefile --noconsole --name {exe_name} {script_name}")


def copy_config_file(config_path, dist_path):
    shutil.copy(config_path, dist_path)


def clean_up(exe_name):
    shutil.rmtree("build", ignore_errors=True)
    os.remove(f"{exe_name}.spec")


def main():
    script_name = "lazylinks.py"
    exe_name = "Lazylinks"
    config_path = "config.json"

    run_pyinstaller(script_name, exe_name)
    copy_config_file(config_path, "dist/")
    if (F_PRODUCTION := True):
        clean_up(exe_name)


if __name__ == '__main__':
    main()
