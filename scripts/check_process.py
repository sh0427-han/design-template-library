"""Check only #2: six viewports, real maps/fonts, alignment and 12 fault/reuse cases."""
from pathlib import Path
from validate_references import main
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    main(['--templates','process','--report',str(root/'previews/review/process-validation.json'),
          '--evidence-dir','/tmp/process-refinement-review'])
