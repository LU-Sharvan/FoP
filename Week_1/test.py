
from start_compiler.import_start import *


try:
    local_vars['value'] = start()
    StartError.lineNumber = 2
    check_events()
    _set('value', local_vars, None)['value'] = number(9)
    StartError.lineNumber = 3
    check_events()
    _print(_get('value', local_vars, None)['value'])
except Exception as e:
    print(f'Start runtime error in line {StartError.lineNumber}: {e}')
finally:
    listener.stop()
