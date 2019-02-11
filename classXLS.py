from bs4 import BeautifulSoup
from keystone.parse import ItemRow
import os
import xlsxwriter


student_list = ('nick', 'abby', 'mel',)


def main():
    for student in student_list:
        one_student(student)


class StudentXLS(xlsxwriter.Workbook):
    def __init__(self, output_file_path):
        super().__init__(output_file_path)
        self.cell_format_border = self.add_format({'border': True})
        self.cell_format_header = self.add_format({'border': True, 'bold': True})
        self.cell_format_percent = self.add_format({'border': True, 'num_format': '0.00%'})


def one_student(student):
    app_path = os.path.dirname(os.path.realpath(__file__))
    full_output_file_path = os.path.join(app_path, 'output', student + '.xlsx')
    workbook = StudentXLS(full_output_file_path)
    full_path = os.path.join(app_path, 'data', student)
    directory = os.fsencode(full_path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".html"):
            full_file_path = os.path.join(full_path, filename)
            f = GradeFile(filename, workbook, full_file_path)
            f.process()

    workbook.close()


class GradeFile:
    def __init__(self, filename, workbook, full_path):
        self.filename = filename
        self.workbook = workbook
        self.full_path = full_path

    def process(self):
        with open(self.full_path, encoding="utf-8") as fp:
            soup = BeautifulSoup(fp)
            worksheet = self.workbook.add_worksheet(name=os.path.splitext(self.filename)[0])

            worksheet.write(0, 0, "Order", self.workbook.cell_format_header)
            worksheet.write(0, 1, "Done", self.workbook.cell_format_header)
            worksheet.write(0, 2, "Grade", self.workbook.cell_format_header)
            worksheet.write(0, 3, "Possible", self.workbook.cell_format_header)
            worksheet.write(0, 4, "Percent", self.workbook.cell_format_header)
            worksheet.write(0, 5, "Assignment", self.workbook.cell_format_header)
            worksheet.write(0, 6, "Unit", self.workbook.cell_format_header)

            tag_list = soup.findAll("div", {"class": ["graded_item_row", "upcoming_item_row", "submitted_item_row"]})

            c = 0
            for tag in reversed(tag_list):
                class_obj = ItemRow(tag)

                worksheet.write(c+1, 0, int(class_obj.rowindex)-2, self.workbook.cell_format_border)
                worksheet.write(c+1, 0, c+1, self.workbook.cell_format_border)
                worksheet.write(c+1, 1, '', self.workbook.cell_format_border)

                if class_obj.grade:
                    worksheet.write_number(c+1, 2, class_obj.grade, self.workbook.cell_format_border)
                else:
                    if class_obj.submitted_item_row:
                        worksheet.write(c + 1, 2, "Submitted", self.workbook.cell_format_border)
                    else:
                        worksheet.write(c+1, 2, None, self.workbook.cell_format_border)

                if class_obj.possible:
                    worksheet.write_number(c+1, 3, class_obj.possible, self.workbook.cell_format_border)
                else:
                    worksheet.write(c+1, 3, None, self.workbook.cell_format_border)

                s = '=IF(ISNUMBER(C{0}),C{0}/D{0},"")'.format(c+2)
                worksheet.write_formula(c+1, 4, s, self.workbook.cell_format_percent)

                worksheet.write(c+1, 5, class_obj.cell_gradable, self.workbook.cell_format_border)
                worksheet.write(c+1, 6, class_obj.itemCat, self.workbook.cell_format_border)
                c += 1


if __name__ == '__main__':
    main()
