"""Check #3: six viewports, real maps/fonts, paired geometry and live resize."""
from pathlib import Path
from validate_references import main
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    main(['--templates','comparison','--report',str(root/'previews/review/comparison-validation.json'),
          '--evidence-dir','/tmp/comparison-refinement-review'])
