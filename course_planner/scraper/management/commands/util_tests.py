import unittest
import re
import utility as util


class testSplitDotAnd(unittest.TestCase):

    def test_noAndOrDot(self):
        str = "BIOL 371."
        splits = util.split_dot_and(str)
        self.assertIsNone(splits)

    def test_periodButNoAnd(self):
        str = "BIOL 230. BIOL 324 is recommended."
        splits = util.split_dot_and(str)
        expected = ["BIOL 230", "BIOL 324 is recommended."]
        self.assertEqual(splits, expected)

    def test_andButNoPeriod(self):
        str = "BIOL 230 and one of BIOL 300, STAT 200."
        splits = util.split_dot_and(str)
        expected = ["BIOL 230", "one of BIOL 300, STAT 200."]
        self.assertEqual(splits, expected)

        str = "all of BIOL 200, BIOL 260 and one of BIOL 233, BIOL 234."
        expected = ["all of BIOL 200, BIOL 260", "one of BIOL 233, BIOL 234."]

    def test_andNotInOps(self):
        str = "Third-year standing or higher in Combined Major in Science, and one of (a) BIOL 121, BIOL 180 (or BIOL 140), or (b) SCIE 001, or (c) 8 transfer credits of first-year biology."
        splits = util.split_dot_and(str)
        expected = ["Third-year standing or higher in Combined Major in Science,", "one of (a) BIOL 121, BIOL 180 (or BIOL 140), or (b) SCIE 001, or (c) 8 transfer credits of first-year biology."]
        self.assertEqual(splits, expected)

    def test_moreAtEnd(self):
        str = "Either (a) BIOL 200 and one of BIOL 233, BIOL 234; or (b) FRST 302. CHEM 233 is recommended."
        splits = util.split_dot_and(str)
        expected = ["Either (a) BIOL 200 and one of BIOL 233, BIOL 234; or (b) FRST 302", "CHEM 233 is recommended."]
        self.assertEqual(splits, expected)

    def test_andInAndOutOfOps(self):
        str = "Third-year standing or higher in Combined Major in Science, and one of (a) BIOL 121 and BIOL 180 (or BIOL 140), or (b) SCIE 001, or (c) 8 transfer credits of first-year biology."
        splits = util.split_dot_and(str)
        expected = ["Third-year standing or higher in Combined Major in Science,", "one of (a) BIOL 121 and BIOL 180 (or BIOL 140), or (b) SCIE 001, or (c) 8 transfer credits of first-year biology."]
        self.assertEqual(splits, expected)

    def test_andAndDotButNoSplit(self):
        str = "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001. or (c) 8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry."
        splits = util.split_dot_and(str)
        self.assertIsNone(splits)

    def test_splitMultiSection(self):
        str = "BIOL 230 and one of BIOL 300, STAT 200. BIOL 306 is recommended."
        splits = util.split_dot_and(str)
        expected = ["BIOL 230", "one of BIOL 300, STAT 200", "BIOL 306 is recommended."]
        self.assertEqual(splits, expected)

    def test_caseSensitive(self):
        str = "BIOL200 And fourth-year standing."
        splits = util.split_dot_and(str)
        expected = ["BIOL200", "fourth-year standing."]
        self.assertEqual(splits, expected)

class testSplitOps(unittest.TestCase):

    def test_noOps(self):
        str = "BIOL 230 and one of BIOL 300, STAT 200. BIOL 306 is recommended."
        splits = util.split_ops(str)
        self.assertIsNone(splits)

        str = "Third-year standing or higher in Combined Major in Science"
        splits = util.split_ops(str)
        self.assertIsNone(splits)

        str = "One of PHYS 101, PHYS 106, PHYS 107, PHYS 117, PHYS 131, PHYS 157, SCIE 001."
        splits = util.split_ops(str)
        self.assertIsNone(splits)

    def test_twoOps(self):
        str = "Either (a) BIOL 200 and one of BIOL 233, BIOL 234; or (b) FRST 302"
        splits = util.split_ops(str)
        expected = {"(a)" : "BIOL 200 and one of BIOL 233, BIOL 234",
                    "(b)" : "FRST 302"}
        self.assertEqual(splits, expected)

        str = "Either (a) BIOL 335 and one of BIOL 201, BIOC 202, BIOC 203; or (b) BIOT 380."
        splits = util.split_ops(str)
        expected = {"(a)" : "BIOL 335 and one of BIOL 201, BIOC 202, BIOC 203",
                    "(b)" : "BIOT 380"}
        self.assertEqual(splits, expected)

        str = "All of (a) CPSC_V 221 or DSCI_V 221, (b) at least 3 credits from COMM_V 291, BIOL_V 300, MATH or STAT at 200 level or above."
        splits = util.split_ops(str)
        expected = {"(a)" : "CPSC_V 221 or DSCI_V 221",
                    "(b)" : "at least 3 credits from COMM_V 291, BIOL_V 300, MATH or STAT at 200 level or above"}
        self.assertEqual(splits, expected)
        
    def test_multiOps(self):
        str = "one of (a) BIOL 121, BIOL 180 (or BIOL 140), or (b) SCIE 001, or (c) 8 transfer credits of first-year biology."
        splits = util.split_ops(str)
        expected = {"(a)" : "BIOL 121, BIOL 180 (or BIOL 140)",
                    "(b)" : "SCIE 001",
                    "(c)" : "8 transfer credits of first-year biology"}
        self.assertEqual(splits, expected)

        str = "All of (a) one of CPSC_V 221, DSCI_V 221 (b) one of MATH_V 152, MATH_V 221, MATH_V 223 (c) one of MATH_V 200, MATH_V 217, MATH_V 226, MATH_V 253, MATH_V 254 (d) one of STAT_V 241, STAT_V 251, ECON_V 325, ECON_V 327, MATH_V 302, STAT_V 302, MATH_V 318."
        splits = util.split_ops(str)
        expected = {"(a)" : "one of CPSC_V 221, DSCI_V 221",
                    "(b)" : "one of MATH_V 152, MATH_V 221, MATH_V 223",
                    "(c)" : "one of MATH_V 200, MATH_V 217, MATH_V 226, MATH_V 253, MATH_V 254",
                    "(d)" : "one of STAT_V 241, STAT_V 251, ECON_V 325, ECON_V 327, MATH_V 302, STAT_V 302, MATH_V 318"}
        self.assertEqual(splits, expected)

class testReqDict(unittest.TestCase):

    def test_oneCourse(self):
        str = "CPSC 103."
        reqs = util.req_dict(str)
        expected = {"all of" : ["CPSC 103"]}
        self.assertEqual(reqs, expected)

    def test_simpleOneOf(self):
        str = "One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221."
        reqs = util.req_dict(str)
        expected = {"one of" : ["CPSC 203", "CPSC 210", "CPEN 221", "DSCI 221"]}
        self.assertEqual(reqs, expected)

    def test_simpleAllOf(self):
        str = "BIOL 336 and BIOL 230."
        reqs = util.req_dict(str)
        expected = {"all of" : ["BIOL 336", "BIOL 230"]}
        self.assertEqual(reqs, expected)

    def test_allOfAndOneOf(self):
        str = "BIOL 230 and one of BIOL 300, STAT 200"
        reqs = util.req_dict(str)
        expected = {"all of" : ["BIOL 230"],
                    "one of" : ["BIOL 300", "STAT 200"]}
        self.assertEqual(reqs, expected)

        str = "BIOL 200 and one of BIOL 260, NSCI 200, PSYC 270, PSYC 271, PSYC 304, CAPS 301."
        reqs = util.req_dict(str)
        expected = {"all of" : ["BIOL 200"],
                    "one of" : ["BIOL 260", "NSCI 200", "PSYC 270", "PSYC 271", "PSYC 304", "CAPS 301"]}
        self.assertEqual(reqs, expected)

    def test_atypicalOptions(self):
        str = "Either (a) BIOL 201 or (b) all of BIOL 200, BIOL 260 and one of BIOL 233, BIOL 234."
        reqs = util.req_dict(str)
        print(reqs)
        expected = {"one of" : {"(a)" : ["BIOL 201"],
                                "(b)" : {"all of" : ["BIOL 200", "BIOL 260"],
                                         "one of" : ["BIOL 233", "BIOL 234"]}}}
        self.assertEqual(reqs, expected)

        str = "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001. or (c) 8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry."
        reqs = util.req_dict(str)
        expected = {"one of" : {"(a)" : {"all of" : ["BIOL 112", "BIOL 121"]},
                                "(b)" : {"all of" : ["SCIE 001"]},
                                "(c)" : {"all of" : ["8 transfer credits of 1st year BIOL",
                                                     "6 credits of 1st year chemistry"]}}}
        self.assertEqual(reqs, expected)

        str = "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001 ; (c) a corequisite of one of CHEM 203 or CHEM 223 and one of BIOL 112 or BIOL 121; or (d) 8 transfer credits of first-year BIOL."
        reqs = util.req_dict(str)
        expected = {"one of" : {"(a)" : {"all of" : ["BIOL 112", "BIOL 121"]},
                                "(b)" : {"all of" : ["SCIE 001"]},
                                "(c)" : {"a corequisite of one of" : ["CHEM 203", "CHEM 223"],
                                         "one of" : ["BIOL 112", "BIOL 121"]},
                                "(d)" : {"all of" : "8 transfer credits of first-year BIOL"}}}
        self.assertEqual(reqs, expected)

if __name__ == '__main__':
    unittest.main()