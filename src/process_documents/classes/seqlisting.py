import string
import re
import xml.etree.ElementTree as et
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def find_all(tree, element):
    elems = tree.findall(element)
    res = []
    for elem in elems:
        res.append(elem.text)
    return res



class SeqListing:
    def __init__(self, full_document_path, patent_id):
        self.patentNumber = patent_id
        self.full_document_path = full_document_path
        self.__process_listings_xml()
        
    def __process_listings_xml(self):
        tree = et.parse(self.full_document_path)
        root = tree.getroot()
        logger.info("in __process_listings_xml")
        sequencesRaw = find_all(root, './/s400')
        self.sequences = []
        for seq in sequencesRaw:
            from string import digits
            remove_digits = str.maketrans('', '', digits)
            sequence = seq.translate(remove_digits)
            sequence = sequence.replace(" ", "")
            self.sequences.append(sequence)

        self.seqCount = len(self.sequences)
        # try parsing the new format
        if(len(self.sequences) == 0):
            entries = find_all(root, './/entry')
            for entry in entries:
                if entry == None or entry == '' or '<' in entry or '0' in entry or '1' in entry or entry.startswith(" "):
                    continue;
                sequence = entry
                self.sequences.append(sequence)
        self.seqCount = len(self.sequences)