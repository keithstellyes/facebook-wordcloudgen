# Parses a settings.cfg that is a series of key-value pairs.
# key="value"
# Comments can either begin with a #
# or a [

def process_settings(s):
    s = s.split('\n')
    d = {}
    for line in s:
        line = line.strip()

        k = ''
        v = ''
        if line.startswith('[') or line.startswith('#'):
            continue
        for c in line:
            print(c,end='')
            if c.isalnum() or c == '_':
                k += c
            elif c.isspace():
                raise Exception("No space is allowed between key and =.")
            elif c == '=':
                for _c in line[line.find('=')+1:]:
                    v += _c
                d[k] = v
                break
            else:
                exceptstr = "Unrecognized character where a key was expected:"
                raise Exception(exceptstr + c)
    return d
