import xlwt
import xlrd
from xlutils.copy import copy
import os

rb = xlrd.open_workbook(os.path.join(MEDIA_ROOT, 'report.xls'), formatting_info=True, on_demand=True)