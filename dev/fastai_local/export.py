#AUTOGENERATED! DO NOT EDIT! File to edit: dev/99_export.ipynb (unless otherwise specified).

__all__ = [is_export, find_default_export, notebook2script]

from fastai_local.core import *
import json,re,os,shutil,glob
from textwrap import TextWrapper

def _check_re(cell, pat):
    if cell['cell_type'] != 'code': return False
    src = cell['source']
    if len(src) == 0: return False
    return re.match(pat, src[0], re.IGNORECASE)

def is_export(cell, default):
    "Check if `cell` is to be exported and returns the name of the module."
    if _check_re(cell, r'^\s*#\s*exports?\s*$'):
        if default is None: print(f"This cell doesn't have an export destination and was ignored:\n{cell['source'][1]}")
        return default
    tst = _check_re(cell, r'^\s*#\s*exports?\s*(\S+)\s*$')
    return os.path.sep.join(tst.groups()[0].split('.')) if tst else None

def find_default_export(cells):
    "Find in `cells` the default export module."
    for cell in cells:
        tst = _check_re(cell, r'^\s*#\s*default_exp\s*(\S*)\s*$')
        if tst: return tst.groups()[0]

def _create_mod_file(fname, nb_path):
    "Create a module file for `fname`."
    os.makedirs(fname.parent, parents=True, exist_ok=True)
    with open(fname, 'w') as f:
        f.write(f"#AUTOGENERATED! DO NOT EDIT! File to edit: dev/{nb_path.name} (unless otherwise specified).")
        f.write('\n\n__all__ = []')

def _func_class_names(code):
    names = re.findall(r'^(?:def|class)\s+([^\(]*)\(', code, re.MULTILINE)
    return [n for n in names if not n.startswith('_')]

def _notebook2script(fname):
    "Finds cells starting with `#export` and puts them into a new module"
    fname = Path(fname)
    nb = json.load(open(fname,'r'))
    default = find_default_export(nb['cells'])
    if default is not None:
        default = os.path.sep.join(default.split('.'))
        _create_mod_file(Path.cwd()/'fastai_local'/f'{default}.py', fname)
    exports = [is_export(c, default) for c in nb['cells']]
    cells = [(c,e) for (c,e) in zip(nb['cells'],exports) if e is not None]
    for (c,e) in cells:
        fname_out = Path.cwd()/'fastai_local'/f'{e}.py'
        orig = '' if e==default else f'#Comes from {fname.name}.\n'
        code = '\n\n' + orig + ''.join(c['source'][1:])
        # remove trailing spaces
        _add2add(fname_out, _func_class_names(code))
        code = re.sub(r' +$', '', code, flags=re.MULTILINE)
        with open(fname_out, 'a') as f: f.write(code)
    print(f"Converted {fname}.")

def _get_sorted_files(all_fs: Union[bool,str], up_to=None):
    "Return the list of files corresponding to `g` in the current dir."
    if (all_fs==True): ret = glob.glob('*.ipynb') # Checks both that is bool type and that is True
    else: ret = glob.glob(all_fs) if isinstance(g,str) else []
    if len(ret)==0: print('WARNING: No files found')
    if up_to is not None: ret = [f for f in ret if str(f)<=str(up_to)]
    return sorted(ret)

def notebook2script(fname=None, all_fs:Optional[Union[bool,str]]=None, up_to=None):
    # initial checks
    assert fname or all_fs
    if (all_fs is None) and (up_to is not None): all_fs=True # Enable allFiles if upTo is present
    fnames = _get_sorted_files(all_fs, up_to=up_to) if all_fs else [fname]
    [_notebook2script(f) for f in fnames]