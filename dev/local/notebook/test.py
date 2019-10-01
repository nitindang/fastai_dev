#AUTOGENERATED! DO NOT EDIT! File to edit: dev/94_notebook_test.ipynb (unless otherwise specified).

__all__ = ['check_all_flag', 'NoExportPreprocessor']

#Cell
from ..imports import *
from .core import *
from .export import *
import nbformat,inspect
from nbformat.sign import NotebookNotary
from nbconvert.preprocessors import ExecutePreprocessor
from ..test import *
from ..core import *

#Cell
def check_all_flag(cells):
    for cell in cells:
        if check_re(cell, _re_all_flag): return check_re(cell, _re_all_flag).groups()[0]

#Cell
def _add_import_cell(mod):
    "Return an import cell for `mod`"
    return {'cell_type': 'code',
            'execution_count': None,
            'metadata': {'hide_input': True},
            'outputs': [],
            'source': f"\nfrom local.{mod} import *"}

#Cell
from .export import _re_mod_export

class NoExportPreprocessor(ExecutePreprocessor):
    "An `ExecutePreprocessor` that executes not exported cells"
    @delegates(ExecutePreprocessor.__init__)
    def __init__(self, flags, **kwargs):
        self.flags = flags
        super().__init__(**kwargs)

    def preprocess_cell(self, cell, resources, index):
        if 'source' not in cell or cell['cell_type'] != "code": return cell, resources
        if _re_mod_export.search(cell['source']):               return cell, resources
        for f in get_cell_flags(cell):
            if f not in self.flags:                             return cell, resources
        print(cell["source"])
        return super().preprocess_cell(cell, resources, index)