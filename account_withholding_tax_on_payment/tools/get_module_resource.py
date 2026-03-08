from os.path import join as opj

from odoo.tools import file_path


def get_module_resource(module, *parts):
    """
    Odoo 19 compatibility helper for old get_module_resource style.

    Example:
        get_module_resource("my_module", "static", "template", "file.xlsx")
    """
    return file_path(opj(module, *parts))
