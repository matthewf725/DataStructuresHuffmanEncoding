import unittest
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

        
    def test_lt_and_eq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1
        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertFalse(HuffmanNode(97, 2) == None)
                    
                    
    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

      
    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

        
    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        self.assertEqual(codes[ord('z')], '')
        
    def test_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        huffman_encode("file2.txt", "file2_out.txt")
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        huffman_encode("repeating.txt", "repeating_out.txt")
        #huffman_encode("file_WAP.txt", "file_WAP_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        self.assertEqual(subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb file2_out_compressed.txt file2_compressed_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb empty_file_out.txt empty_file.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb empty_file_out_compressed.txt empty_file.txt", shell = True), 0)   
        self.assertEqual(subprocess.call("diff -wb repeating_out.txt repeating_soln.txt", shell = True), 0)
        self.assertEqual(subprocess.call("diff -wb repeating_out_compressed.txt repeating_soln.txt", shell = True), 0)          
        # self.assertEqual(subprocess.call("fc file1_out.txt file1_soln.txt", shell = True), 0)
        # self.assertEqual(subprocess.call("fc file1_out_compressed.txt file1_compressed_soln.txt", shell = True), 0)
        # self.assertEqual(subprocess.call("fc file2_out.txt file2_soln.txt", shell = True), 0)
        # self.assertEqual(subprocess.call("fc file2_out_compressed.txt file2_compressed_soln.txt", shell = True), 0)
        # self.assertEqual(subprocess.call("fc empty_file_out.txt empty_file.txt", shell = True), 0)
        # self.assertEqual(subprocess.call("fc empty_file_out_compressed.txt empty_file.txt", shell = True), 0) 
        # self.assertEqual(subprocess.call("fc repeating_out.txt repeating_soln.txt", shell = True), 0)
        # self.assertEqual(subprocess.call("fc repeating_out_compressed.txt repeating_soln.txt", shell = True), 0)       
        #self.assertEqual(subprocess.call("fc file_WAP_compressed_soln.txt file_WAP_out_compressed.txt", shell=True), 0)  
        with self.assertRaises(FileNotFoundError):
            huffman_encode("nonexistent.txt", "nonexistent_out.txt")
    #Ordered list tests
    def setUp(self):
        self.list = OrderedList()
    def test_simple(self):
        t_list = OrderedList()
        t_list.add(10)
        self.assertEqual(t_list.python_list(), [10])
        self.assertEqual(t_list.size(), 1)
        self.assertEqual(t_list.index(10), 0)
        self.assertTrue(t_list.search(10))
        self.assertFalse(t_list.is_empty())
        self.assertEqual(t_list.python_list_reversed(), [10])
        self.assertTrue(t_list.remove(10))
        t_list.add(10)
        self.assertEqual(t_list.pop(0), 10)
    def test_is_empty(self):
        self.assertTrue(self.list.is_empty())
        self.list.add(5)
        self.assertFalse(self.list.is_empty())

    def test_add(self):
        self.assertTrue(self.list.add(5))
        self.assertFalse(self.list.add(5))  # Adding the same item again should return False
        self.assertEqual(self.list.python_list(), [5])
        self.assertTrue(self.list.add(3))
        self.assertEqual(self.list.python_list(), [3, 5])
        self.assertTrue(self.list.add(7))
        self.assertEqual(self.list.python_list(), [3, 5, 7])

    def test_remove(self):
        self.assertFalse(self.list.remove(5))  # Removing from an empty list should return False
        self.list.add(5)
        self.assertTrue(self.list.remove(5))
        self.assertTrue(self.list.is_empty())
        self.assertFalse(self.list.remove(5))  # Removing the same item again should return False

    def test_index(self):
        self.assertIsNone(self.list.index(5))  # Index of an item in an empty list should be None
        self.list.add(5)
        self.assertEqual(self.list.index(5), 0)
        self.assertIsNone(self.list.index(10))  # Item not in the list should return None
        self.list.add(10)
        self.assertEqual(self.list.index(10), 1)

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.list.pop(0)  # Popping from an empty list should raise an IndexError
        self.list.add(5)
        self.assertEqual(self.list.pop(0), 5)
        self.assertTrue(self.list.is_empty())
        self.list.add(3)
        self.list.add(7)
        self.assertEqual(self.list.pop(1), 7)
        self.assertEqual(self.list.python_list(), [3])

    def test_search(self):
        self.assertFalse(self.list.search(5))  # Searching in an empty list should return False
        self.list.add(5)
        self.assertTrue(self.list.search(5))
        self.assertFalse(self.list.search(10))  # Item not in the list should return False

    def test_python_list(self):
        self.assertEqual(self.list.python_list(), [])  # Python list of an empty list should be []
        self.list.add(5)
        self.list.add(3)
        self.list.add(7)
        self.assertEqual(self.list.python_list(), [3, 5, 7])

    def test_python_list_reversed(self):
        self.assertEqual(self.list.python_list_reversed(), [])  # Reversed list of an empty list should be []
        self.list.add(5)
        self.list.add(3)
        self.list.add(7)
        self.assertEqual(self.list.python_list_reversed(), [7, 5, 3])

    def test_size(self):
        self.assertEqual(self.list.size(), 0)  # Size of an empty list should be 0
        self.list.add(5)
        self.list.add(3)
        self.list.add(7)
        self.assertEqual(self.list.size(), 3)

    def test_manipulate_list(self):
        self.list.add(5)
        self.list.add(3)
        self.list.add(7)
        self.assertEqual(self.list.python_list(), [3, 5, 7])
        self.assertEqual(self.list.python_list_reversed(), [7, 5, 3])
        self.list.remove(5)
        self.assertEqual(self.list.python_list(), [3, 7])
        self.list.add(10)
        self.assertEqual(self.list.python_list(), [3, 7, 10])
        self.assertEqual(self.list.size(), 3)
        self.assertTrue(self.list.search(7))
        with self.assertRaises(IndexError):
            self.list.pop(-1)    
if __name__ == '__main__': 
   unittest.main()
