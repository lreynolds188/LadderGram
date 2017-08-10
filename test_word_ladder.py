#!/usr/bin/python

from word_ladder import *
import unittest


# application information
__author__ = 'Jordan Schurmann, Luke Reynolds'
__email__ = 'jordan.schurmann@gmail.com, lreynolds188@gmail.com'
__version__ = '1.0.5'
__website__ = 'http://lukereynolds.net/'


class TestValidFile(unittest.TestCase):

    #Test valid file
    def test_1_valid_file(self):
        fname = 'dictionary.txt'
        self.assertEqual(valid_file(fname), '0')

    # Test file is empty
    def test_2_emptyfile(self):
        fname = 'empty.txt'
        self.assertEqual(valid_file(fname), 'Selected file is empty....please reenter')

    # Test file name can not be found - invalid file name or doesn't exist
    def test_3_badfilename(self):
        fname = 'no such file'
        self.assertEqual(valid_file(fname), 'Can not find the file....please reenter')

    # Test enter pressed and no file name entered
    def test_4_nulls(self):
        fname = ''
        self.assertEqual(valid_file(fname), 'Can not find the file....please reenter')


class TestMakeWordFile(unittest.TestCase):

    #Test empty exclusion file
    def test_5_excluded_empty(self):
        start = 'side'
        lines = ['bats', 'cats', 'dogs', 'side']
        excluded = []
        self.assertEqual(make_word_list(start, lines, excluded), ['bats', 'cats', 'dogs', 'side'])

    # Test exclusion file does not exclude start word
    def test_6_startnotexcluded(self):
        start = 'side'
        lines = ['bats', 'cats', 'dogs', 'side']
        excluded = ['bats', 'side']
        self.assertEqual(make_word_list(start, lines, excluded), ['cats', 'dogs', 'side'])

    # Test exclusion file no matching words
    def test_7_noexcluded(self):
        start = 'side'
        lines = ['bats', 'cats', 'dogs', 'side']
        excluded = ['bots', 'sits']
        self.assertEqual(make_word_list(start, lines, excluded), ['bats', 'cats', 'dogs', 'side'])


class TestValidStart(unittest.TestCase):

    #Test start word exists in list of words
    def test_8_start_valid(self):
        start = 'hide'
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(valid_start(start, lines), '0')

    # Test start word not in list of words
    def test_9_start_notinwordlist(self):
        start = 'hide'
        lines = ['cide', 'seek', 'smith']
        self.assertEqual(valid_start(start, lines), 'Start word not in list of words....please reenter')

    # Test start word only has one character
    def test_10_start_oneletter(self):
        start = 'a'
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(valid_start(start, lines), 'Start word must contain more than one letter....please reenter')

    # Test start word that is not alphabetic
    def test_11_start_notalpha(self):
        start = 'h1de'
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(valid_start(start, lines), 'Start word must contain only letters....please reenter')

    # Test enter pressed an no start word entered
    def test_12_start_null(self):
        start = ''
        lines = ['hide', 'seek', 'smith']
        self.assertEqual(valid_start(start, lines ), 'Start word must contain only letters....please reenter')


class TestValidTarget(unittest.TestCase):

    #Test target word exists in list of words
    def test_13_target_valid(self):
        start = 'hide'
        target = 'seek'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), '0')

    # Test target word not in list of words
    def test_14_target_notinwordlist(self):
        start = 'hide'
        target = 'seke'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word not in list of words....please reenter')

    # Test target word is not the same as the start word
    def test_15_target_notdifftostart(self):
        start = 'hide'
        target = 'hide'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word must be different from Start word....please reenter')

    # Test target word only has one character
    def test_16_target_oneletter(self):
        start = 'hide'
        target = 's'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word must be same length as Start word....please reenter')

    # Test target word is not longer than start word
    def test_17_target_greaterthanstart(self):
        start = 'hide'
        target = 'seeks'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word must be same length as Start word....please reenter')

    # Test target word is not less than start word
    def test_18_target_lessthanstart(self):
        start = 'hide'
        target = 'sek'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word must be same length as Start word....please reenter')

    # Test target word that is not alphabetic
    def test_19_target_notalpha(self):
        start = 'hide'
        target = 's3ek'
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word must contain only letters....please reenter')

    # Test enter pressed an no target word entered
    def test_20_target_null(self):
        start = 'hide'
        target = ''
        words = ['hide', 'seek', 'smith']
        self.assertEqual(valid_target(start, target, words), 'Target word must contain only letters....please reenter')


class TestValidFlag(unittest.TestCase):

    # Test valid y flag entered - note case is converted to lower and all front and back spaces are stripped on input
    def test_21_flag_valid_yes(self):
        flag = 'y'
        self.assertEqual(valid_yn(flag), 'y')

    # Test valid n flag entered
    def test_22_flag_valid_no(self):
        flag = 'n'
        self.assertEqual(valid_yn(flag), 'n')

    # Test alphabetic character other than y or n entered
    def test_23_flag_invalid_notYN(self):
        flag = 'w'
        self.assertEqual(valid_yn(flag), 'Please enter Y or N only')

    # Test numeric character entered
    def test_24_flag_invalid_numeric(self):
        flag = '1'
        self.assertEqual(valid_yn(flag), 'Please enter letters Y or N only')

    # Test more than 1 character entered- alphabetic
    def test_25_flag_invalid_mutliplealpha3(self):
        flag = 'aa'
        self.assertEqual(valid_yn(flag), 'Please enter only one character')

    # Test more than 1 character entered- numeric
    def test_26_flag_invalid_multiplenumeric(self):
        flag = '123'
        self.assertEqual(valid_yn(flag), 'Please enter only one character')

    # Test enter pressed and no flag entered
    def test_27_flag_invalid_nodata(self):
        flag = ''
        self.assertEqual(valid_yn(flag), 'Please enter a character')


class TestSame(unittest.TestCase):

    # Test no matching letters
    def test_28_no_letters_match(self):
        item = 'hide'
        target = 'seek'
        self.assertEqual(same(item, target), 0)

    # Test 1 matching letters
    def test_29_one_letter_match(self):
        item = 'hide'
        target = 'sits'
        self.assertEqual(same(item, target), 1)

    # Test 2 matching letters
    def test_30_two_letters_match(self):
        item = 'hide'
        target = 'hits'
        self.assertEqual(same(item, target), 2)

    # Test all matching letters
    def test_31_all_letters_match(self):
        item = 'hide'
        target = 'hide'
        self.assertEqual(same(item, target), 4)


class TestBuild(unittest.TestCase):

    # Test 0 matching word - 0 Seen - 0 in list
    def test_32_build1(self):
        pattern = '.ode'
        words = ['dogs', 'side', 'site', 'tide']
        seen = {'ride': True}
        list = ['farm', 'lamb']
        self.assertEqual(build(pattern, words, seen, list), [])

    # Test 2 matching words - 0 Seen - 0 in list
    def test_33_build2(self):
        pattern = '.ide'
        words = ['dogs', 'side', 'site', 'tide']
        seen = {'ride': True}
        list = ['farm', 'lamb']
        self.assertEqual(build(pattern, words, seen, list), ['side', 'tide'])

    # Test 2 matching words - 1 Seen - 0 in list
    def test_34_build3(self):
        pattern = '.ide'
        words = ['dogs', 'side', 'site', 'tide']
        seen = {'side': True}
        list = ['farm', 'lamb']
        self.assertEqual(build(pattern, words, seen, list), ['tide'])

    # Test 2 matching words - 1 Seen - 1 in list
    def test_35_build4(self):
        pattern = '.ide'
        words = ['dogs', 'fide', 'ride', 'side', 'tide']
        seen = {'side': True}
        list = ['farm', 'lamb', 'fide']
        self.assertEqual(build(pattern, words, seen, list), ['ride', 'tide'])


class TestFind(unittest.TestCase):
     # Test path found, Return = True
    def test_36_path_found(self):
        start = 'lead'
        words = ['load', 'goad']
        seen = {'lead': True}
        target = 'gold'
        path = ['lead']
        self.assertTrue(find(start, words, seen, target, path))

    # Test no path found, Return = False
    def test_37_no_path_found(self):
        start = 'lead'
        words = ['load', 'goss']
        seen = {'lead': True}
        target = 'gold'
        path = ['lead']
        self.assertFalse(find(start, words, seen, target, path))


if __name__ == '__main__':
    unittest.main()
