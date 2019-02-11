import os
from bs4 import BeautifulSoup


def class_list(path: str, student: str) -> list:
    full_path = os.path.join(path, student)
    class_list = []

    for f in os.listdir(full_path):
        if f.endswith(".html"):
            class_list.append(f)

    return class_list


def assignment_list(path: str, student: str, filename: str) -> list:
    full_path = os.path.join(path, student, filename)
    assignment_list = []

    with open(full_path, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp)
        # print(soup)

        tag_list = soup.findAll("div", {"class": ["graded_item_row", "upcoming_item_row", "submitted_item_row"]})

        for tag in reversed(tag_list):
            assignment_list.append(ItemRow(tag).dict_row())
    return assignment_list


class ItemRow:
    def __init__(self, tag):
        self.submitted_item_row = 'submitted_item_row' in tag['class']
        self.upcoming_item_row = 'upcoming_item_row' in tag['class']
        self.graded_item_row = 'graded_item_row' in tag['class']

        self.id = tag["id"]
        self.duedate = tag["duedate"]
        self.lastactivity = tag["lastactivity"]
        self.position = tag["position"]
        self.rowindex = tag["rowindex"]

        self.cell_gradable = tag.find(class_="cell gradable").contents[0].strip()

        gradable = tag.find(class_="gradable")  # intermediate value
        self.itemCat = str(gradable.find(class_="itemCat").string)

        if tag.find(class_="lastActivityDate").string:
            self.lastActivityDate = str(tag.find(class_="lastActivityDate").string)
        else:
            self.lastActivityDate = None

        self.activityType = tag.find(class_="activityType").contents[0].strip()

        cell_grade = tag.find(class_="grade")  # intermediate value
        self.grade = str(cell_grade.find(class_="grade").string)
        if self.grade == '-':
            self.grade = None
        else:
            self.grade = float(self.grade)

        # the possible text includes the '/' when displaying the fraction
        if cell_grade.find(class_="pointsPossible"):
            self.possible = float(str(cell_grade.find(class_="pointsPossible").string).replace('/', ''))
        else:
            self.possible = None

    def __repr__(self):
        return '<ItemLine> %s' % self.id

    # TODO - Loop through instance variables and print them
    def dump(self):
        print('self.id %s %s' % (type(self.id), self.id))
        print('self.submitted_item_row %s %s' % (type(self.submitted_item_row), self.submitted_item_row))
        print('self.upcoming_item_row %s %s' % (type(self.upcoming_item_row), self.upcoming_item_row))
        print('self.graded_item_row %s %s' % (type(self.graded_item_row), self.graded_item_row))

        print('self.duedate %s %s' % (type(self.duedate), self.duedate))
        print('self.lastactivity %s %s' % (type(self.lastactivity), self.lastactivity))
        print('self.position %s %s' % (type(self.position), self.position))
        print('self.rowindex %s %s' % (type(self.rowindex), self.rowindex))
        print('self.cell_gradable %s %s' % (type(self.cell_gradable), self.cell_gradable))
        print('self.itemCat %s %s' % (type(self.itemCat), self.itemCat))
        print('self.lastActivityDate %s %s' % (type(self.lastActivityDate), self.lastActivityDate))
        print('self.activityType %s %s' % (type(self.activityType), self.activityType))
        print('self.grade %s %s' % (type(self.grade), self.grade))
        print('self.possible %s %s' % (type(self.possible), self.possible))

    def dict_row(self) -> dict:
        d = {}
        d['id'] = self.id
        d['submitted_item_row'] = self.submitted_item_row
        d['upcoming_item_row'] = self.upcoming_item_row
        d['graded_item_row'] = self.graded_item_row
        d['duedate'] = self.duedate
        d['lastactivity'] = self.lastactivity
        d['position'] = self.position
        d['rowindex'] = self.rowindex
        d['cell_gradable'] = self.cell_gradable
        d['itemCat'] = self.itemCat
        d['lastActivityDate'] = self.lastActivityDate
        d['activityType'] = self.activityType
        d['grade'] = self.grade
        d['possible'] = self.possible
        return d
