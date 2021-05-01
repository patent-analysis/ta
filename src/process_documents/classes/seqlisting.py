import string
import re
import xml.etree.ElementTree as et
import logging
from string import digits

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
            remove_digits = str.maketrans('', '', digits)
            sequence = seq.translate(remove_digits)
            sequence = sequence.replace(" ", "")
            self.sequences.append(sequence)

        # try parsing the new seq_listing format
        if(len(self.sequences) == 0):
            entries = find_all(root, './/entry')
            full_table_text = ''
            for entry in entries:
                if entry != None:
                    full_table_text += entry
            
            # split by the 210 to segments
            segments = full_table_text.split('<210>')

            for segment in segments:
                txt = re.findall(r"(?:SEQUENCE:)([\s\w\W]+)", segment)                                
                if len(txt) == 0:
                    continue
                full_seq = ''
                for seq in txt:
                    full_seq+=seq

                remove_digits = str.maketrans('', '', digits)
                sequence = full_seq.translate(remove_digits)
                sequence = sequence.replace(" ", "")
                self.sequences.append(sequence)
            # print(self.sequences)