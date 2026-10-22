"""Compatibility entry point for final-source validation.
Shared font, math and geometry rules: validate_references.py / reference_validation.py.
"""
from validate_references import main

if __name__ == "__main__":
    main(['--templates','experiment','--report','previews/review/experiment-validation.json'])
