import string
import re
import xml.etree.ElementTree as et
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SeqListing:
    def __init__(self, patent_id):
        self.patentNumber = patent_id
        self.__process_listings_xml()
        
    def __process_listings_xml(self):
        tree = et.parse(self.patentNumber + '.xml')
        root = tree.getroot()
        logger.info("in __process_listings_xml")
        sequencesRaw = [' '.join(el.itertext()) for el in root.findall('.//s400')]
        pattern = r'[0-9]'
        self.sequences = []
        for seq in sequencesRaw:
            seq = (re.sub(pattern, '', seq))
            self.sequences.append(seq.strip())
        self.seqCount = len(self.sequences)