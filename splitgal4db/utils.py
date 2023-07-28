import openpyxl
import warnings

def get_secret(setting: str, secrets: dict):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

def get_template_cname(template: str, sheet: str = 'List of lines'):
    def suppressWarnings(f):
        warnings.simplefilter("ignore")
        return(f)
    
    @suppressWarnings
    def load_workbook(path: str):
        return openpyxl.load_workbook(path)

    wb = load_workbook(template)
    worksheet = wb[sheet]
    
    # Get column names from the template
    for row in worksheet.iter_rows():
        cnames = [cname.value for cname in row]
        break
    
    return cnames

def get_default_types(
    template: str,
    sheet: str = 'Instruction',
    skip: int = 2,
    col_spec: dict = {
        # Note that theses col IDs should be 0-based!!!
        '1': 'EFFECTORS',
        '5': 'CASSETTE_STYLE',
        '6': 'DIMERIZER_STYLE',
        '7': 'STATUS_LIST',
        '8': 'PRIVATE'
    }
):
    wb = openpyxl.load_workbook(template)
    workbook = wb[sheet]
    excel_data = list()
    header = 0
    # Iterating over the rows and
    # getting value from each cell in row
    for row in worksheet.iter_rows():
        # The first row is header;
        # the second is instruction
        if header < skip - 1:
            header = header + 1
            continue

        default_opts = {}
        for key in col_spec:
            default_opts[col_spec[key]] = []

        # Read default classes until no columns contain new classes
        all_empty = True
        for ncol, cell in enumerate(row):
            if str(ncol) in col_spec and cell.value is not None:
                default_opts[col_spec].append(cell.value)
                all_empty = False
                
            if ncol == len(row) and all_empty:
                break
            

    return 0