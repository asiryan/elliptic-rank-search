"""Check the Python version and the GP functions used by the search engine."""
import json
import sys

from bootstrap import gp
from runtime import GP


def main():
    if sys.version_info < (3, 10):
        raise RuntimeError('Python 3.10 or newer is required')
    required = ('ellinit', 'ellminimalmodel', 'ellheightmatrix', 'ellisdivisible',
                'elltors', 'qflllgram', 'hyperellratpoints', 'hyperellred',
                'hyperellminimalmodel', 'hyperellchangecurve', 'polrootsmod')
    script = 'print("VERSION ",version());\n'
    for name in required:
        script += f'if(type({name})!="t_CLOSURE",error("Missing GP function: {name}"));\n'
    script += 'print("GP_READY");quit;\n'
    output, _ = gp(script, 10)
    if 'GP_READY' not in output:
        raise RuntimeError('The GP capability check did not finish')
    print(json.dumps({'python': sys.version.split()[0], 'gp_executable': str(GP),
                      'gp_version': next(l[8:] for l in output.splitlines() if l.startswith('VERSION ')),
                      'required_functions': list(required), 'status': 'ready'}, indent=2))


if __name__ == '__main__':
    main()
