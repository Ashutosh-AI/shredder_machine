from datetime import date
import xlrd
from xlwt import Workbook
from xlutils.copy import copy


def save_data(no_of_time_hand_crossed):

    try:
        today = date.today()
        today = str(today)

        rb = xlrd.open_workbook("../result.xls")
        sheet = rb.sheet_by_index(0)       # 1st sheet will be get
        sheet.cell_value(0,0)     # get value of row,column

        q = sheet.cell_value(sheet.nrows-1, 1)   # date, get last row and 1st column

        rb = xlrd.open_workbook("../result.xls")

        wb = copy(rb)

        w_sheet = wb.get_sheet(0)

        if (q == today):

            e = sheet.cell_value(sheet.nrows-1, 2)  # no of hand cros. colm
            print(e, no_of_time_hand_crossed)
            w_sheet.write(sheet.nrows-1, 2, e + no_of_time_hand_crossed)
            wb.save("result.xls")

        else:
            w_sheet.write(sheet.nrows, 0, sheet.nrows)
            w_sheet.write(sheet.nrows, 1, today)
            w_sheet.write(sheet.nrows, 2, no_of_time_hand_crossed)
            wb.save("result.xls")


    except:
        today = date.today()
        today = str(today)

        wb = Workbook()

        sheet = wb.add_sheet("Sheet 1")

        sheet.write(0, 0, "Sl.No")
        sheet.write(0, 1, "Date")
        sheet.write(0, 2, "Number of times hand crossed")

        m=1
        sheet.write(1, 0, 1)
        sheet.write(1, 1, today)
        sheet.write(1, 2, no_of_time_hand_crossed)
        wb.save("result.xls")