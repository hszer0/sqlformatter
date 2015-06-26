import unittest
import sqlformatter


class sqlformatterTests(unittest.TestCase):

    def test_EmptyStringInFormatter(self):
        self.assertEqual(sqlformatter.format(""), "")

    def test_NoneInFormatter(self):
        self.assertEqual(sqlformatter.format(None), "")

    def test_SimpleQueryInFormatter(self):
        self.assertEqual(
            sqlformatter.format("select * from folders"), "SELECT * \nFROM folders")

    def test_JoinQueryInFormatter(self):
        self.assertEqual(
            sqlformatter.format(
                "select * from folders f join iter i on i.id = f.id"),
            "SELECT * \nFROM folders f\nJOIN iter i ON i.id = f.id")

    def test_OperatorSpacing(self):
        self.assertEqual(sqlformatter.format("8*8 *8* 8"), "8 * 8 * 8 * 8")

    def test_AndQueryInFormatter(self):
        self.assertEqual(
            sqlformatter.format(
                "select * from folders f join iter i on i.id = f.id and i.id > 0 where f.name is not null and f.udefval1>0"),
            "SELECT * \nFROM folders f\nJOIN iter i ON i.id = f.id\nAND i.id > 0\nWHERE f.name IS NOT NULL\n  AND f.udefval1 > 0")

if __name__ == '__main__':
    unittest.main()
