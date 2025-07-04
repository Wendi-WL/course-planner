import unittest
import re
import prereq_utility as util


class testOptionSplit(unittest.TestCase):
    
    def test_noSplit(self):
        str = "Meaning and impact of computational thinking. Solving problems using computational thinking, testing, debugging. How computers work. No prior computing experience required. Not for students with existing credit for or exemption from CPSC 107, CPSC 110 or APSC 160. [3-1-0]"

        info = util.course_info(str)
        self.assertEqual(info[0], str)
        self.assertEqual(info[1], None)
        self.assertEqual(info[2], None)

    def test_onePrereq(self):
        str = "Fundamental computation and program structures. Continuing systematic program design from CPSC 103. [3-2-0] Prerequisite: CPSC 103."

        info = util.course_info(str)
        self.assertEqual(info[0], "Fundamental computation and program structures. Continuing systematic program design from CPSC 103. [3-2-0]")
        self.assertEqual(info[1], "CPSC 103.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "CPSC 103."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        for op, req in prereqs.items():
            all_of = re.split("and", req)
            self.assertEqual(all_of, ["CPSC 103."])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["CPSC 103"]}}
        self.assertEqual(expected, prereqs)

    def test_multiOneOf(self):
        str = "Overview of relational and non-relational database systems, role and usage of a database when querying data, data modelling, query languages, and query optimization. [3-0-1] Prerequisite: One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221."

        info = util.course_info(str)
        self.assertEqual(info[0], "Overview of relational and non-relational database systems, role and usage of a database when querying data, data modelling, query languages, and query optimization. [3-0-1]")
        self.assertEqual(info[1], "One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        for op, req in prereqs.items():
            all_of = re.split("and", req)
            self.assertEqual(all_of, ["One of CPSC_V 203, CPSC_V 210, CPEN_V 221, DSCI_V 221."])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"one of" : ["CPSC_V 203", "CPSC_V 210", "CPEN_V 221", "DSCI_V 221"]}}
        self.assertEqual(expected, prereqs)

    def test_multiAllOf(self):
        str = "Ecological adaptation and evolutionary processes in contemporary populations; natural selection, variation, optimization, foraging theory, coevolution, arms races; life history theory, evolution of sex, sexual selection, evolution in managed populations. [2-2-0] Prerequisite: BIOL 336 and BIOL 230."

        info = util.course_info(str)
        self.assertEqual(info[0], "Ecological adaptation and evolutionary processes in contemporary populations; natural selection, variation, optimization, foraging theory, coevolution, arms races; life history theory, evolution of sex, sexual selection, evolution in managed populations. [2-2-0]")
        self.assertEqual(info[1], "BIOL 336 and BIOL 230.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "BIOL 336 and BIOL 230."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, ["BIOL 336", "BIOL 230."])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 336", "BIOL 230"]}}
        self.assertEqual(expected, prereqs)

    def test_multiAllOf(self):
        str = "Ecological adaptation and evolutionary processes in contemporary populations; natural selection, variation, optimization, foraging theory, coevolution, arms races; life history theory, evolution of sex, sexual selection, evolution in managed populations. [2-2-0] Prerequisite: BIOL 336 and BIOL 230."

        info = util.course_info(str)
        self.assertEqual(info[0], "Ecological adaptation and evolutionary processes in contemporary populations; natural selection, variation, optimization, foraging theory, coevolution, arms races; life history theory, evolution of sex, sexual selection, evolution in managed populations. [2-2-0]")
        self.assertEqual(info[1], "BIOL 336 and BIOL 230.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "BIOL 336 and BIOL 230."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, ["BIOL 336", "BIOL 230."])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 336", "BIOL 230"]}}
        self.assertEqual(expected, prereqs)


    def test_mixAllOfOneOf(self):
        str = "Design, execution, and analysis of ecological surveys and experiments. Practical field methods for estimating population metrics and describing community structure. Computer techniques for the statistical analysis of ecological data. [2-4-0] Prerequisite: BIOL 230 and one of BIOL 300, STAT 200."

        info = util.course_info(str)
        self.assertEqual(info[0], "Design, execution, and analysis of ecological surveys and experiments. Practical field methods for estimating population metrics and describing community structure. Computer techniques for the statistical analysis of ecological data. [2-4-0]")
        self.assertEqual(info[1], "BIOL 230 and one of BIOL 300, STAT 200.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "BIOL 230 and one of BIOL 300, STAT 200."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, ["BIOL 230", "one of BIOL 300, STAT 200."])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 230"],
                             "one of" : ["BIOL 300", "STAT 200"]}}
        self.assertEqual(expected, prereqs)



        str = "Introduction to the structure and function of the nervous system, excitable membranes, and synaptic signaling using representative vertebrate and invertebrate species. Please consult the Faculty of Science Credit Exclusion Lists: https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/facult… [3-0-0] Prerequisite: BIOL 200 and one of BIOL 260, NSCI 200, PSYC 270, PSYC 271, PSYC 304, CAPS 301."
        
        info = util.course_info(str)
        self.assertEqual(info[0], "Introduction to the structure and function of the nervous system, excitable membranes, and synaptic signaling using representative vertebrate and invertebrate species. Please consult the Faculty of Science Credit Exclusion Lists: https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/facult… [3-0-0]")
        self.assertEqual(info[1], "BIOL 200 and one of BIOL 260, NSCI 200, PSYC 270, PSYC 271, PSYC 304, CAPS 301.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "BIOL 200 and one of BIOL 260, NSCI 200, PSYC 270, PSYC 271, PSYC 304, CAPS 301."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, ["BIOL 200", "one of BIOL 260, NSCI 200, PSYC 270, PSYC 271, PSYC 304, CAPS 301."])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 200"],
                             "one of" : ["BIOL 260", "NSCI 200", "PSYC 270", "PSYC 271", "PSYC 304", "CAPS 301"]}}
        self.assertEqual(expected, prereqs)

    def test_twoOptions(self):
        str = "Animal development and its underlying causal principles; introductory embryology. [3-5-0] Prerequisite: Either (a) BIOL 201 or (b) all of BIOL 200, BIOL 260 and one of BIOL 233, BIOL 234."

        info = util.course_info(str)
        self.assertEqual(info[0], "Animal development and its underlying causal principles; introductory embryology. [3-5-0]")
        self.assertEqual(info[1], "Either (a) BIOL 201 or (b) all of BIOL 200, BIOL 260 and one of BIOL 233, BIOL 234.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "BIOL 201",
                   "(b)" : "all of BIOL 200, BIOL 260 and one of BIOL 233, BIOL 234."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        split = {"(a)" : ["BIOL 201"],
                 "(b)" : ["all of BIOL 200, BIOL 260", "one of BIOL 233, BIOL 234."]}
        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, split[op])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 201"]},
                    "(b)" : {"all of" : ["BIOL 200", "BIOL 260"],
                             "one of" : ["BIOL 233", "BIOL 234"]}}
        self.assertEqual(expected, prereqs)

    def test_multiOptions_atypReq(self):
        str = "Principles of cellular and organismal physiology illustrated with examples from unicellular organisms, plants and animals, focusing on transport processes, water balance, nutrient acquisition and communication. [3-0-0] Prerequisite: Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001. or (c) 8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry."

        info = util.course_info(str)
        self.assertEqual(info[0], "Principles of cellular and organismal physiology illustrated with examples from unicellular organisms, plants and animals, focusing on transport processes, water balance, nutrient acquisition and communication. [3-0-0]")
        self.assertEqual(info[1], "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001. or (c) 8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "all of BIOL 112, BIOL 121",
                   "(b)" : "SCIE 001.",
                   "(c)" : "8 transfer credits of 1st year BIOL and 6 credits of 1st year chemistry."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        split = {"(a)" : ["all of BIOL 112, BIOL 121"],
                 "(b)" : ["SCIE 001."],
                 "(c)" : ["8 transfer credits of 1st year BIOL", "6 credits of 1st year chemistry."]}
        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, split[op])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 112", "BIOL 121"]},
                    "(b)" : {"all of" : ["SCIE 001"]},
                    "(c)" : {"all of" : ["8 transfer credits of 1st year BIOL",
                                         "6 credits of 1st year chemistry"]}}
        self.assertEqual(expected, prereqs)



        str = "Genotype and phenotype, mechanisms of inheritance, genetic analysis. Please consult the Faculty of Science Credit Exclusion Lists: https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/facult…. [3-0-2] Prerequisite: Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001 ; (c) a corequisite of one of CHEM 203 or CHEM 223 and one of BIOL 112 or BIOL 121; or (d) 8 transfer credits of first-year BIOL."

        info = util.course_info(str)
        self.assertEqual(info[0], "Genotype and phenotype, mechanisms of inheritance, genetic analysis. Please consult the Faculty of Science Credit Exclusion Lists: https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/facult…. [3-0-2]")
        self.assertEqual(info[1], "Either (a) all of BIOL 112, BIOL 121 or (b) SCIE 001 ; (c) a corequisite of one of CHEM 203 or CHEM 223 and one of BIOL 112 or BIOL 121; or (d) 8 transfer credits of first-year BIOL.")
        self.assertEqual(info[2], None)

        prereqs = {"(a)" : "all of BIOL 112, BIOL 121",
                   "(b)" : "SCIE 001 ;",
                   "(c)" : "a corequisite of one of CHEM 203 or CHEM 223 and one of BIOL 112 or BIOL 121;",
                   "(d)" : "8 transfer credits of first-year BIOL."}
        self.assertEqual(util.split_by_option(info[1]), prereqs)

        split = {"(a)" : ["all of BIOL 112, BIOL 121"],
                 "(b)" : ["SCIE 001 ;"],
                 "(c)" : ["a corequisite of one of CHEM 203 or CHEM 223", "one of BIOL 112 or BIOL 121;"],
                 "(d)" : ["8 transfer credits of first-year BIOL."]}
        for op, req in prereqs.items():
            all_of = re.split(" and ", req)
            self.assertEqual(all_of, split[op])

            prereqs[op] = util.req_dict(all_of)
        
        expected = {"(a)" : {"all of" : ["BIOL 112", "BIOL 121"]},
                    "(b)" : {"all of" : ["SCIE 001"]},
                    "(c)" : {"a corequisite of one of" : ["CHEM 203", "CHEM 223"],
                             "one of" : ["BIOL 112", "BIOL 121"]},
                    "(d)" : {"all of" : ["8 transfer credits of first-year BIOL"]}}
        self.assertEqual(expected, prereqs)
    
if __name__ == '__main__':
    unittest.main()