import word_ladder
import unittest

# application information
__author__ = 'Jordan Schurmann, Luke Reynolds'
__email__ = 'jordan.schurmann@gmail.com, lreynolds188@gmail.com'
__version__ = '1.0.16'
__website__ = 'http://lukereynolds.net/'


class TestValidFile(unittest.TestCase):

    #Test valid file
    def test_1_validfile(self):
        fname = 'dictionary.txt'
        self.assertEqual(word_ladder.valid_file(fname), '0')

    # Test file is empty
    def test_2_emptyfile(self):
        fname = 'empty.txt'
        self.assertEqual(word_ladder.valid_file(fname), 'Selected file is empty....please reenter')

    # Test file name can not be found - invalid file name or doesn't exist
    def test_3_badfilename(self):
        fname = 'no such file'
        self.assertEqual(word_ladder.valid_file(fname), 'Can not find the file....please reenter')

    # Test enter pressed and no file name entered
    def test_4_nulls(self):
        fname = ''
        self.assertEqual(word_ladder.valid_file(fname), 'Can not find the file....please reenter')


class TestMakeWordFile(unittest.TestCase):

    #Test empty exclusion file
    def test_5_exclusions1(self):
        start = 'side'
        lines = ['bats', 'cats', 'dogs', 'side']
        excluded = []
        self.assertEqual(word_ladder.make_word_list(start, lines, excluded), ['bats', 'cats', 'dogs', 'side'])

    # Test exclusion file does not exclude start word
    def test_6_exclusions2(self):
        start = 'side'
        lines = ['bats', 'cats', 'dogs', 'side']
        excluded = ['bats', 'side']
        self.assertEqual(word_ladder.make_word_list(start, lines, excluded), ['cats', 'dogs', 'side'])

    # Test exclusion file no matching words
    def test_7_exclusions3(self):
        start = 'side'
        lines = ['bats', 'cats', 'dogs', 'side']
        excluded = ['bots', 'sits']
        self.assertEqual(word_ladder.make_word_list(start, lines, excluded), ['bats', 'cats', 'dogs', 'side'])


class TestValidStart(unittest.TestCase):

    #Test start word exists in list of words
    def test_8_validstartword(self):
        start = 'hide'
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_start(start, lines), '0')

    # Test start word not in list of words
    def test_9_startwordnotinfileinput(self):
        start = 'hide'
        lines = ['cide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_start(start, lines), 'Start word not in list of words....please reenter')

    # Test start word only has one character
    def test_10_startwordlength(self):
        start = 'a'
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_start(start, lines), 'Start word must contain more than one letter....please reenter')

    # Test start word that is not alphabetic
    def test_11_startwordnotalphabetic(self):
        start = 'h1de'
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_start(start, lines), 'Start word must contain only letters....please reenter')

    # Test enter pressed an no start word entered
    def test_12_startnull(self):
        start = ''
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_start(start, lines ), 'Start word must contain only letters....please reenter')


class TestValidTarget(unittest.TestCase):

    #Test target word exists in list of words
    def test_13_validtargetword(self):
        start = 'hide'
        target = 'seek'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), '0')

    # Test target word not in list of words
    def test_14_targetwordnotinfileinput(self):
        start = 'hide'
        target = 'seke'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word not in list of words....please reenter')

    # Test target word is not the same as the start word
    def test_15_targetdifftostart(self):
        start = 'hide'
        target = 'hide'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word must be different from Start word....please reenter')

    # Test target word only has one character
    def test_16_targetwordlength(self):
        start = 'hide'
        target = 's'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word must be same length as Start word....please reenter')

    # Test target word is not longer than start word
    def test_17_targetwordgreaterthanstart(self):
        start = 'hide'
        target = 'seeks'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word must be same length as Start word....please reenter')

    # Test target word is not less than start word
    def test_18_targetwordlessthanstart(self):
        start = 'hide'
        target = 'sek'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word must be same length as Start word....please reenter')

    # Test target word that is not alphabetic
    def test_19_targetwordnotalphabetic(self):
        start = 'hide'
        target = 's3ek'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word must contain only letters....please reenter')

    # Test enter pressed an no target word entered
    def test_20_targetnull(self):
        start = 'hide'
        target = ''
        words = ['hide', 'seek', 'smith']
        self.assertEqual(word_ladder.valid_target(start, target, words), 'Target word must contain only letters....please reenter')


class TestValidFlag(unittest.TestCase):

    # Test valid y flag entered - note case is converted to lower and all front and back spaces are stripped on input
    def test_21_flagyvalid(self):
        flag = 'y'
        self.assertEqual(word_ladder.valid_yn(flag), 'y')

    # Test valid n flag entered
    def test_22_flagnyvalid(self):
        flag = 'n'
        self.assertEqual(word_ladder.valid_yn(flag), 'n')

    # Test alphabetic character other than y or n entered
    def test_23_flaginvalid1(self):
        flag = 'w'
        self.assertEqual(word_ladder.valid_yn(flag), 'Please enter Y or N only')

    # Test numeric character entered
    def test_24_flaginvalid2(self):
        flag = '1'
        self.assertEqual(word_ladder.valid_yn(flag), 'Please enter letters Y or N only')

    # Test more than 1 character entered- alphabetic
    def test_25_flaginvalid3(self):
        flag = 'aa'
        self.assertEqual(word_ladder.valid_yn(flag), 'Please enter only one character')

    # Test more than 1 character entered- numeric
    def test_26_flaginvalid4(self):
        flag = '123'
        self.assertEqual(word_ladder.valid_yn(flag), 'Please enter only one character')

    # Test enter pressed and no flag entered
    def test_27_flaginvalid5(self):
        flag = ''
        self.assertEqual(word_ladder.valid_yn(flag), 'Please enter a character')


class TestSame(unittest.TestCase):

    # Test no matching letters
    def test_28_same1(self):
        item = 'hide'
        target = 'seek'
        self.assertEqual(word_ladder.same(item, target), 0)

    # Test 1 matching letters
    def test_29_same2(self):
        item = 'hide'
        target = 'sits'
        self.assertEqual(word_ladder.same(item, target), 1)

    # Test 2 matching letters
    def test_30_same3(self):
        item = 'hide'
        target = 'hits'
        self.assertEqual(word_ladder.same(item, target), 2)

    # Test all matching letters
    def test_31_same4(self):
        item = 'hide'
        target = 'hide'
        self.assertEqual(word_ladder.same(item, target), 4)


class TestBuild(unittest.TestCase):

    # Test 0 matching word - 0 Seen - 0 in list
    def test_32_build1(self):
        pattern = '.ode'
        words = ['dogs', 'side', 'site', 'tide']
        seen = {'ride': True}
        list = ['farm', 'lamb']
        self.assertEqual(word_ladder.build(pattern, words, seen, list), [])

    # Test 2 matching words - 0 Seen - 0 in list
    def test_33_build2(self):
        pattern = '.ide'
        words = ['dogs', 'side', 'site', 'tide']
        seen = {'ride': True}
        list = ['farm', 'lamb']
        self.assertEqual(word_ladder.build(pattern, words, seen, list), ['side', 'tide'])

    # Test 2 matching words - 1 Seen - 0 in list
    def test_34_build3(self):
        pattern = '.ide'
        words = ['dogs', 'side', 'site', 'tide']
        seen = {'side': True}
        list = ['farm', 'lamb']
        self.assertEqual(word_ladder.build(pattern, words, seen, list), ['tide'])

    # Test 2 matching words - 1 Seen - 1 in list
    def test_35_build4(self):
        pattern = '.ide'
        words = ['dogs', 'fide', 'ride', 'side', 'tide']
        seen = {'side': True}
        list = ['farm', 'lamb', 'fide']
        self.assertEqual(word_ladder.build(pattern, words, seen, list), ['ride', 'tide'])


class TestFind(unittest.TestCase):
     # Test path found = True
    def test_36_find1(self):
        start = 'lead'
        words = ['load', 'goad']
        seen = {'lead': True}
        target = 'gold'
        path = ['lead']
        self.assertTrue(word_ladder.find(start, words, seen, target, path))

    # Test no path found = False
    def test_37_find2(self):
        start = 'lead'
        words = ['load', 'goss']
        seen = {'lead': True}
        target = 'gold'
        path = ['lead']
        self.assertFalse(word_ladder.find(start, words, seen, target, path))

    # assertEqual fails  NEED TO KNOW WHAT TRUE EQUALS
    def test_38_find3(self):
        start = 'lead'
        words = ['lead', 'load', 'goad', 'gold']
        seen = {'lead': True}
        target = 'gold'
        path = ['lead']
        self.assertEqual((word_ladder.find(start, words, seen, target, path)), ['lead', 'load', 'goad'])

if __name__ == '__main__':
    unittest.main()
