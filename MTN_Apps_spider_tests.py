import unittest, csv
from MTN_Apps_spiderV2 import scrapAppData, retreiveAppData, placeAppData

class TestRetrieveAppData(unittest.TestCase):
    def test_isURL(self):
        urls = retreiveAppData('test.csv')
        url = urls[0]
        self.assertEqual(
            url,'https://play.google.com/store/apps/details?id=biz.lgr.consumer')


class TestScrapAppData(unittest.TestCase):
    def test_isStringData(self):
        testJSONfile = scrapAppData('test.json')[0]
        self.assertEqual(testJSONfile[0], "Music Plus is your personal")
        self.assertEqual(testJSONfile[1], "Free")
        self.assertEqual(testJSONfile[2], "4.2")
        self.assertEqual(testJSONfile[3], "313")
        self.assertEqual(testJSONfile[4], "Music & Audio")
        self.assertEqual(testJSONfile[5], "September 4, 2017")
        self.assertEqual(testJSONfile[6], "  50,000 - 100,000  ")

listData = [["Music Plus is your personal","Free" ,"4.2" ,"313" , "Music & Audio",
            "September 4, 2017", "  50,000 - 100,000  "]]

def scrapLineInCSV():
    with open('testOut.csv', 'r') as testOutFile:
        readCSV = csv.reader(testOutFile, delimiter = ',')
        testOutFile.readline()
        row = testOutFile.readline()
        row = row.split(',')
        return row

class TestPlaceAppData(unittest.TestCase):
    def test_isStringData(self):
        testOutfile = placeAppData(listData,'testOut.csv')
        row = scrapLineInCSV()
        self.assertEqual(row[1], listData[0][0])
##        self.assertEqual(row[1], listData[0])
##        self.assertEqual(row[1], listData[0])
##        self.assertEqual(row[1], listData[0])
##        self.assertEqual(row[1], listData[0])
##        self.assertEqual(row[1], listData[0])
##        self.assertEqual(row[1], listData[0])



if __name__ == '__main__':
    unittest.main()
