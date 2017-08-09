import word_ladder
import unittest

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.16"
__website__ = "http://lukereynolds.net/"


class TestValidFile(unittest.TestCase):

    #Test valid file
    def test_1_validfile(self):
        self.assertEqual(word_ladder.valid_file("dictionary.txt"), "0")

    # Test file is empty
    def test_2_emptyfile(self):
        self.assertEqual(word_ladder.valid_file("empty.txt"), "Selected file is empty....please reenter")

    # Test file name can not be found - invalid file name or doesn't exist
    def test_3_badfilename(self):
        self.assertEqual(word_ladder.valid_file("no such file"), "Can not find the file....please reenter")

    # Test enter pressed and no file name entered
    def test_4_nulls(self):
        self.assertEqual(word_ladder.valid_file(""), "Can not find the file....please reenter")


class TestMakeWordFile(unittest.TestCase):

    #Test empty exclusion file
    def test_5_exclusions1(self):
        self.assertEqual(word_ladder.make_word_list("side", ["bats", "cats", "dogs", "side"], []), ["bats", "cats", "dogs", "side"])

    # Test exclusion file does not exclude start word
    def test_6_exclusions2(self):
        self.assertEqual(word_ladder.make_word_list("side", ["bats", "cats", "dogs", "side"], ["bats", "side"]), ["cats", "dogs", "side"])

    # Test exclusion file no matching words
    def test_7_exclusions3(self):
        self.assertEqual(word_ladder.make_word_list("side", ["bats", "cats", "dogs", "side"], ["bots", "sits"]), ["bats", "cats", "dogs", "side"])


class TestValidStart(unittest.TestCase):

    #Test start word exists in list of words
    def test_8_validstartword(self):
        self.assertEqual(word_ladder.valid_start("hide", ["hide", "seek", "smith"]), "0")

    # Test start word not in list of words
    def test_9_startwordnotinfileinput(self):
        self.assertEqual(word_ladder.valid_start("hide", ["cide", "seek", "smith"]), "Start word not in list of words....please reenter")

    # Test start word only has one character
    def test_10_startwordlength(self):
        self.assertEqual(word_ladder.valid_start("a", ["hide", "seek", "smith"]), "Start word must contain more than one letter....please reenter")

    # Test start word that is not alphabetic
    def test_11_startwordnotalphabetic(self):
        self.assertEqual(word_ladder.valid_start("h1de", ["hide", "seek", "smith"]), "Start word must contain only letters....please reenter")

    # Test enter pressed an no start word entered
    def test_12_startnull(self):
        self.assertEqual(word_ladder.valid_start("", ["hide", "seek", "smith"]), "Start word must contain only letters....please reenter")


class TestValidTarget(unittest.TestCase):

    #Test target word exists in list of words
    def test_13_validtargetword(self):
        self.assertEqual(word_ladder.valid_target("hide", "seek", ["hide", "seek", "smith"]), "0")

    # Test start word not in list of words
    def test_14_targetwordnotinfileinput(self):
        self.assertEqual(word_ladder.valid_target("hide", "seke", ["hide", "seek", "smith"]), "Target word not in list of words....please reenter")

    # Test target word is not the same as the start word
    def test_15_targetdifftostart(self):
        self.assertEqual(word_ladder.valid_target("hide", "hide", ["hide", "seek", "smith"]), "Target word must be different from Start word....please reenter")

    # Test target word only has one character
    def test_16_targetwordlength(self):
        self.assertEqual(word_ladder.valid_target("hide", "s", ["hide", "seek", "smith"]), "Target word must be same length as Start word....please reenter")

    # Test target word is not longer than start word
    def test_17_targetwordgreaterthanstart(self):
        self.assertEqual(word_ladder.valid_target("hide", "seeks", ["hide", "seek", "smith"]), "Target word must be same length as Start word....please reenter")

    # Test target word is not less than start word
    def test_18_targetwordlessthanstart(self):
        self.assertEqual(word_ladder.valid_target("hide", "sek", ["hide", "seek", "smith"]), "Target word must be same length as Start word....please reenter")

    # Test target word that is not alphabetic
    def test_19_targetwordnotalphabetic(self):
        self.assertEqual(word_ladder.valid_target("hide", "s3ek", ["hide", "seek", "smith"]), "Target word must contain only letters....please reenter")

    # Test enter pressed an no target word entered
    def test_20_targetnull(self):
        self.assertEqual(word_ladder.valid_target("hide", "", ["hide", "seek", "smith"]), "Target word must contain only letters....please reenter")


class TestValidFlag(unittest.TestCase):

    # Test valid y flag entered - note case is converted to lower and all front and back spaces are stripped on input
    def test_21_flagyvalid(self):
        self.assertEqual(word_ladder.valid_yn("y"), "y")

    # Test valid n flag entered
    def test_22_flagnyvalid(self):
        self.assertEqual(word_ladder.valid_yn("n"), "n")

    # Test alphabetic character other than y or n entered
    def test_23_flaginvalid1(self):
        self.assertEqual(word_ladder.valid_yn("w"), "Please enter Y or N only")

    # Test numeric character entered
    def test_24_flaginvalid2(self):
        self.assertEqual(word_ladder.valid_yn("1"), "Please enter letters Y or N only")

    # Test more than 1 character entered- alphabetic
    def test_25_flaginvalid3(self):
        self.assertEqual(word_ladder.valid_yn("aa"), "Please enter only one character")

    # Test more than 1 character entered- numeric
    def test_26_flaginvalid4(self):
        self.assertEqual(word_ladder.valid_yn("123"), "Please enter only one character")

    # Test enter pressed and no flag entered
    def test_27_flaginvalid5(self):
        self.assertEqual(word_ladder.valid_yn(""), "Please enter a character")


class TestSame(unittest.TestCase):

    # Test no matching letters
    def test_28_same1(self):
        self.assertEqual(word_ladder.same("hide", "seek"), 0)

    # Test 1 matching letters
    def test_29_same2(self):
        self.assertEqual(word_ladder.same("hide", "sits"), 1)

    # Test 2 matching letters
    def test_30_same3(self):
        self.assertEqual(word_ladder.same("hide", "hits"), 2)

    # Test all matching letters
    def test_31_same4(self):
        self.assertEqual(word_ladder.same("hide", "hide"), 4)


class TestBuild(unittest.TestCase):

    # Test 0 matching word - 0 Seen - 0 in list
    def test_32_build1(self):
        self.assertEqual(word_ladder.build(".ode", ["dogs", "side", "site", "tide"], {"ride" : True}, ["farm", "lamb"]), [])

    # Test 2 matching words - 0 Seen - 0 in list
    def test_33_build2(self):
        self.assertEqual(word_ladder.build(".ide", ["dogs", "side", "site", "tide"], {"ride" : True}, ["farm", "lamb"]), ["side", "tide"])

    # Test 2 matching words - 1 Seen - 0 in list
    def test_34_build3(self):
        self.assertEqual(word_ladder.build(".ide", ["dogs", "side", "site", "tide"], {"side" : True}, ["farm", "lamb"]), ["tide"])

    # Test 2 matching words - 1 Seen - 1 in list
    def test_35_build4(self):
        self.assertEqual(word_ladder.build(".ide", ["dogs", "fide", "ride", "side", "tide"], {"side" : True}, ["farm", "lamb", "fide"]), ["ride", "tide"])


class TestFind(unittest.TestCase):
# this does not work assertion error
    # Test correct path found
    def test_36_find1(self):
        start = "lead"
        words = ["lead", "load", "goad", "gold"]
        target = "gold"
        seen = {"lead": True}
        path = ["lead"]
        self.assertEqual(word_ladder.find(start, words, seen, target, path), ['lead', 'load', 'goad', 'gold'])




if __name__ == '__main__':
    unittest.main()
