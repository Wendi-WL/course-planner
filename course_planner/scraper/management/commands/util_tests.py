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

        str = "[CHEM498]"
        reqs = util.req_dict(str)
        expected = {"all of" : ["CHEM 498"]}
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

        str = "One of CHEM 211, CHEM 215 and all of CHEM 208, CHEM 213, CHEM 245."
        reqs = util.req_dict(str)
        expected = {"one of" : ["CHEM 221", "CHEM 215"],
                    "all of" : ["CHEM 208", "CHEM 213", "CHEM 245"]}

    def test_atypicalOptions(self):
        str = "Either (a) BIOL 201 or (b) all of BIOL 200, BIOL 260 and one of BIOL 233, BIOL 234."
        reqs = util.req_dict(str)
        expected = {"one of" : {"(a)" : ["BIOL 201"],
                                "(b)" : [{"all of" : ["BIOL 200", "BIOL 260"]},
                                         {"one of" : ["BIOL 233", "BIOL 234"]}]}}
        self.assertEqual(reqs, expected)

        str = "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001. or (c) 8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry."
        reqs = util.req_dict(str)
        expected = {"one of" : {"(a)" : {"all of" : ["BIOL 112", "BIOL 121"]},
                                "(b)" : ["SCIE 001"],
                                "(c)" : ["8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry"]}}
        self.assertEqual(reqs, expected)

        str = "Either (a) SCIE 001 or (b) one of MATH 100, MATH 102, MATH 104, MATH 110, MATH 120, MATH 180, MATH 184 and one of CHEM 130, CHEM 123, CHEM 154."
        reqs = util.req_dict(str)
        expected = {"one of" : {"(a)" : ["SCIE 001"],
                                "(b)" : {"all of" : {"one of" : ["MATH 100", "MATH 102", "MATH 104", "MATH 110", "MATH 120", "MATH 180", "MATH 184"],
                                                     "one of 0" : ["CHEM 130", "CHEM 123","CHEM 154"]}}}}
        self.assertEqual(reqs, expected)

        str = "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001 ; (c) a corequisite of one of CHEM 203 or CHEM 223 and one of BIOL 112 or BIOL 121; or (d) 8 transfer credits of first-year BIOL."
        reqs = util.req_dict(str)
        expected = {"one of" : {"(a)" : {"all of" : ["BIOL 112", "BIOL 121"]},
                                "(b)" : ["SCIE 001"],
                                "(c)" : [{"a corequisite of one of" : ["CHEM 203", "CHEM 223"]},
                                         {"one of" : ["BIOL 112", "BIOL 121"]}],
                                "(d)" : ["8 transfer credits of first-year BIOL"]}}
        self.assertEqual(reqs, expected)

class testGetInfo(unittest.TestCase):

    def test_onlyDesc(self):
        str = "Meaning and impact of computational thinking. Solving problems using computational thinking, testing, debugging. How computers work. No prior computing experience required. Not for students with existing credit for or exemption from CPSC 107, CPSC 110 or APSC 160. [3-1-0]"
        info = util.course_info(str)
        expected = {"description" : "Meaning and impact of computational thinking. Solving problems using computational thinking, testing, debugging. How computers work. No prior computing experience required. Not for students with existing credit for or exemption from CPSC 107, CPSC 110 or APSC 160. [3-1-0]"}
        self.assertEqual(info, expected)

    def test_descAndPrereq(self):
        str = "Fundamental computation and program structures. Continuing systematic program design from CPSC 103. [3-2-0] Prerequisite: CPSC 103."
        info = util.course_info(str)
        expected = {"description" : "Fundamental computation and program structures. Continuing systematic program design from CPSC 103. [3-2-0]",
                    "Prerequisite" : "CPSC 103."}
        self.assertEqual(info, expected)

        str = "Overview of relational and non-relational database systems, role and usage of a database when querying data, data modelling, query languages, and query optimization. [3-0-1] Prerequisite: One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221."
        info = util.course_info(str)
        expected = {"description" : "Overview of relational and non-relational database systems, role and usage of a database when querying data, data modelling, query languages, and query optimization. [3-0-1]",
                    "Prerequisite" : "One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221."}
        self.assertEqual(info, expected)


    def test_descAndPrereqAndCDF(self):
        str = "An interdisciplinary conservation course with a solutions-oriented approach to marine issues, drawing from natural sciences, social sciences, business, law, and communication. [2-0-3] Prerequisite: Fourth-year standing. This course is not eligible for Credit/D/Fail grading."
        info = util.course_info(str)
        expected = {"description" : "An interdisciplinary conservation course with a solutions-oriented approach to marine issues, drawing from natural sciences, social sciences, business, law, and communication. [2-0-3] This course is not eligible for Credit/D/Fail grading.",
                    "Prerequisite" : "Fourth-year standing."}
        self.assertEqual(info, expected)

    def test_descPrereqAndEquivalency(self):
        str = "Biology and physiology of selected plant-microbe relationships. Impacts of plant-microbe relationships on society. [3-0-2] Prerequisite: BIOL 200 and one of BIOC 202, BIOC 203, BIOL 201, BIOL 233, BIOL 234, BIOL 260. Equivalency: APBI 426"
        info = util.course_info(str)
        expected = {"description" : "Biology and physiology of selected plant-microbe relationships. Impacts of plant-microbe relationships on society. [3-0-2] Equivalency: APBI 426",
                    "Prerequisite" : "BIOL 200 and one of BIOC 202, BIOC 203, BIOL 201, BIOL 233, BIOL 234, BIOL 260."} 
        self.assertEqual(info, expected)

    def test_descPrereqAndCoreq(self):
        str = "Physical and mathematical structures of computation. Boolean algebra and combinations logic circuits; proof techniques; functions and sequential circuits; sets and relations; finite state machines; sequential instruction execution. [3-2-1] Prerequisite: Principles of Mathematics 12 or Pre-calculus 12. Corequisite: One of CPSC 107, CPSC 110."
        info = util.course_info(str)
        expected = {"description" : "Physical and mathematical structures of computation. Boolean algebra and combinations logic circuits; proof techniques; functions and sequential circuits; sets and relations; finite state machines; sequential instruction execution. [3-2-1]",
                    "Prerequisite" : "Principles of Mathematics 12 or Pre-calculus 12.",
                    "Corequisite" : "One of CPSC 107, CPSC 110."}
        self.assertEqual(info, expected)

if __name__ == '__main__':
    unittest.main()