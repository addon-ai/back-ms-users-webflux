#!/usr/bin/env python3

"""
Architect Documentation Generator Entry Point
Generates architectural diagrams from generated Java projects
"""

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
lib_dir = project_root / 'libs' / 'pyarchitect-docs-generator'

# Add to Python path
sys.path.insert(0, str(lib_dir))

# Change to the library directory to fix relative imports
os.chdir(str(lib_dir))

# Override default arguments to use absolute paths
sys.argv.extend(['--projects-dir', str(project_root / 'projects'), '--output-dir', str(project_root / 'docs')])

from main import main

if __name__ == "__main__":
    main()