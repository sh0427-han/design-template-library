"""Compatibility entry point for final-source validation.
Shared font, math and geometry rules: validate_references.py / reference_validation.py.
"""
from reference_validation import GEOMETRY, check_executive
from validate_references import main

if __name__ == "__main__":
    main()
