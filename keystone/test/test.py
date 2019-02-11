import unittest
from bs4 import BeautifulSoup
from keystone.parse import ItemRow


class TestSubmitted(unittest.TestCase):
    soup = BeautifulSoup(open('KeystoneClassList.html', encoding='utf8'), "html.parser")
    item_row = soup.findAll(class_="submitted_item_row")
    tag = item_row[0]
    item = ItemRow(tag)

    def test_submitted_item_row(self):
        self.assertTrue(self.item.submitted_item_row)

    def test_graded_item_row(self):
        self.assertFalse(self.item.graded_item_row)

    def test_upcoming_item_row(self):
        self.assertFalse(self.item.upcoming_item_row)


class TestUpcoming(unittest.TestCase):
    soup = BeautifulSoup(open('KeystoneClassList.html', encoding='utf8'), "html.parser")
    item_row = soup.findAll(class_="upcoming_item_row")
    tag = item_row[0]
    item = ItemRow(tag)

    def test_submitted_item_row(self):
        self.assertFalse(self.item.submitted_item_row)

    def test_graded_item_row(self):
        self.assertFalse(self.item.graded_item_row)

    def test_upcoming_item_row(self):
        self.assertTrue(self.item.upcoming_item_row)



if __name__ == '__main__':
    unittest.main()
