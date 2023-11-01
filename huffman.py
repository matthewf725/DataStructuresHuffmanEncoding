from ordered_list import OrderedList
from huffman_bit_writer import HuffmanBitWriter
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if type(self) == HuffmanNode and type(other) == HuffmanNode and self.char == other.char:
            return True
        return False
        
        
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        elif self.freq == other.freq:
            return self.char < other.char
        else:
            return False
    

def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    char_freq = [0] * 256
    with open(filename) as file:
        fileData = file.read()
        for char in fileData:
            char_freq[ord(char)] += 1
    
    file.close()
    return char_freq

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    
    
    nodes = OrderedList()
    for char, freq in enumerate(char_freq):
        if freq > 0:
            leaf_node = HuffmanNode(char, freq)
            nodes.add(leaf_node)
    
    while nodes.size() > 1:
        leftChild = nodes.pop(0)
        rightChild = nodes.pop(0)
        newInternalNode = HuffmanNode(min(leftChild.char, rightChild.char), leftChild.freq + rightChild.freq)
        newInternalNode.left = leftChild
        newInternalNode.right = rightChild
        nodes.add(newInternalNode)

    return nodes.pop(0)
        
def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    def traverse(node, code, result):
        if node is not None:
            if node.left is None and node.right is None and node.char is not None:  
                huffman_codes[node.char] = code
                return 
            traverse(node.left, code + '0', result)
            traverse(node.right, code + '1', result)
    huffman_codes = ['' for _ in range(256)]  # Initialize an array with 256 empty strings
    traverse(node, '', huffman_codes)
    return huffman_codes

def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    header = []    
    for char, freq in enumerate(freqs):
        if freq != 0:
            #header.append("char:")
            header.append(str(char))
            #header.append("freq:")
            header.append(str(freq))
    header = ' '.join(header)                
    return header
       
def testEmpty(in_file, out_file):
    try:
        with open(in_file, 'r') as fileInput:
            fileString = fileInput.read()
            if not fileString:
                fileString = open(out_file, 'w')
                fileString.write('')

                compressedFile = out_file.replace('.txt', '_compressed.txt')
                bitWriter = HuffmanBitWriter(compressedFile)
                bitWriter.write_code('')
                bitWriter.close()
                fileInput.close()
                return None
            return fileString    
    except FileNotFoundError:
        raise FileNotFoundError  
      
def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    
    try:
        fileString = testEmpty(in_file, out_file)
        if fileString is None:
            return
    except FileNotFoundError:
        raise FileNotFoundError
    compressedFile = out_file.replace('.txt', '_compressed.txt')
    bitWriter = HuffmanBitWriter(compressedFile)
    outputFile = open(out_file, 'w')
    outputFileWriter = HuffmanBitWriter(out_file)    

    frequencies = cnt_freq(in_file)
    header = create_header(frequencies)
    rootNode = create_huff_tree(frequencies)
    codeKey = create_code(rootNode)
    
    codeList = []
    if codeKey is not None:
        for char in fileString:
            if char != "":
                codeList.append(codeKey[ord(char)])
    code = "".join(codeList)

    outputFileWriter.write_str(header + "\r\n")
    outputFileWriter.write_str(code)
    outputFileWriter.close()
    outputFile.close()

    bitWriter.write_str(header + "\n")
    bitWriter.write_code(code)
    bitWriter.close()




    # try:
    #     with open(in_file, 'r') as file:
    #         fileData = file.read()
    #         if fileData:  
    #             frequencies = cnt_freq(in_file)
    #             rootNode = create_huff_tree(frequencies)
    #             codeKey = create_code(rootNode)
    #             header = create_header(frequencies)
                
    #             compressed_file = out_file.replace('.txt', '_compressed.txt')
    #             bitwriter = HuffmanBitWriter(compressed_file)
    #             outFileWrite = HuffmanBitWriter(out_file)

    #             code = ''
    #             if code is not None:
    #                 for char in fileData:
    #                     if (char is not None and ord(char) is not None and char != ''):
    #                         code += codeKey[ord(char)]
                
    #             outFileWrite.write_str(header)
    #             outFileWrite.write_str("\r\n")
    #             outFileWrite.write_str(code)
    #             outFileWrite.close()

    #             bitwriter.write_str(str(header) + "\n")
    #             bitwriter.write_code(code)
    #             bitwriter.close()
       
    #         else: #if file is empty
    #             file_out = open(out_file, 'w')
    #             file_out.write('')
    #             compressed_file = out_file.replace('.txt', '_compressed.txt')
    #             bitwriter = HuffmanBitWriter(compressed_file)
    #             bitwriter.write_code('')
    #             bitwriter.close()
    #             file_out.close()
    # except FileNotFoundError:
    #     raise FileNotFoundError
    
