import string
import re
import xml.etree.ElementTree as et
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def find(tree, element):
    elem = tree.find(element)
    if elem == None:
        return ''
    return elem.text

def find_all_nested(tree, parent, element):
    parents = tree.findall(parent)
    res = []
    for parent in parents:
        elements = parent.findall(element)
        if elements != None:
            for elem in elements:
                if elem != None and elem.text != None:
                    res.append(elem.text)
                
    return ', '.join(res)

def find_all(tree, element):
    elements = tree.findall(element)
    res = []
    for elem in elements:
        if elem.text != None:
            res.append(elem.text)
        
    return ', '.join(res)

def find_names(tree, parent):
    parents = tree.findall(parent)
    res = []
    for parent in parents:
        first = parent.find('.//first-name')
        last = parent.find('.//last-name')
        if first == None or last == None:
            continue
        full_name = first.text + ' ' + last.text
        res.append(full_name)
    return ', '.join(res)       


class Patent:
    def __init__(self, full_document_path, patent_id):
        self.patentNumber = patent_id
        self.full_document_path = full_document_path
        self.__process_xml()
        #Extract epitope information
        self.__extract_epitope_info()
      
        
    def __process_xml(self):
        tree = et.parse(self.full_document_path)
        root = tree.getroot()
        logger.info('processing xml file {}'.format(self.full_document_path))
    
        self.patentName = find(root, './/invention-title')
        self.patentDate = find_all_nested(root, './/publication-reference', './/date')
        self.abstract = find_all_nested(root, './/abstract', './/p')
        self.description = find_all_nested(root, './/description', './/p')
        self.claims = find_all(root, './/claim-text')
        self.inventors = find_names(root, './/inventor')
        self.patentAssignees = find_all_nested(root, './/assignee', './/orgname')

        self.applicants = find_all_nested(root, './/us-applicant', './/orgname')
        self.applicants += find_names(root, './/us-applicant')
        
        self.examiners = find_names(root, './/primary-examiner')
        self.claimsCount = find(root, './/number-of-claims')
        self.appNumber = find_all_nested(root, './/application-reference', './/doc-number')
        self.appDate = find_all_nested(root, './/application-reference', './/date')


    #Extract epitope information
    def __extract_epitope_info(self):
        patterns = [
            r'''([^.]*?antibody(.*)binds(.*)residues[^.]*\.)''',
            r'''([^.]*?antibody(.*)binds(.*)residue[^.]*\.)''',
            r'((epitope[s\s])(.{0,250})(residue[s|\s])(.{0,250})(([A-Z][0-9]{1,5})+(,|and|to|\s?)?([A-Z][0-9]{1,5})?)+(.{0,30})(SEQ ID NO: ([0-9])))',
        ]
        # TODO: ENHANCE
        #Regex
        regex_patterns = [re.compile(p) for p in patterns]
        self.mentionedResidues = []
        # TODO: Handle negation
        claims_sentences = self.claims.split('.')
        description_sentences = self.description.split('.')
        claimsMatchDict = {}
        descriptionMatchDict = {}
        
        #--------------------- PARSE THE CLAIMS --------------------- #
        for sentence in claims_sentences:
            for pattern in patterns:
                match = re.search(pattern, sentence)
                if match:
                    full_match = match.group(0)
                    sequence_id_regex = r'(SEQ ID NO[:]?\s?)([0-9]{1,5})'
                    matching_seq_id_no = re.search(sequence_id_regex, full_match).group(2)
                    if matching_seq_id_no not in claimsMatchDict:
                        claimsMatchDict[matching_seq_id_no] = {}
                    # get the epitope sequences
                    epitope_seq_ranges = [r'([A-Z])?([0-9]{1,5})(-|([\s]?to[\s]?))([A-Z])?([0-9]{1,5})',
                                          r'(between\s)?([A-Z])?([0-9]{1,5})\s(and)\s([A-Z])?([0-9]{1,5})',
                                          r'(from\s)?([A-Z])?([0-9]{1,5})\s(to)\s([A-Z])?([0-9]{1,5})'
                                        ]
                    epitope_numbers_statements = [r'([A-Z])?([0-9]{1,5})(\s|,|and)?([A-Z])?([0-9]{1,5})?(?=.*SEQ)']
                    for range_regex in epitope_seq_ranges:
                         # group 2 and group 6
                         # TODO: Iterate from the small range to the large range
                        ranges = re.search(range_regex, full_match)
                        if ranges == None:
                            continue
                        claimsMatchDict[matching_seq_id_no][ranges.group(2)] = True
                        claimsMatchDict[matching_seq_id_no][ranges.group(6)] = True
                    
                    for epitope_numbers_regex in epitope_numbers_statements:
                         # group 2 and group 6
                         # TODO: Iterate from the small range to the large range
                        ranges = re.search(epitope_numbers_regex, full_match)
                        # 
                        for num in re.finditer(epitope_numbers_regex, full_match):
                            claimsMatchDict[matching_seq_id_no][num.group(2)] = True
                            
        # logger.info(claimsMatchDict)
        
        for seq_no in claimsMatchDict.keys():
            seq_object = {}
            seq_object['seqId'] = seq_no
            seq_object['claimedResidues'] = []
            seq_object['location'] = 'claim'
            for claimed_residue in claimsMatchDict[seq_no]:
                seq_object['claimedResidues'].append(claimed_residue)
            self.mentionedResidues.append(seq_object)

        #--------------------- PARSE THE DESCRIPTION --------------------- #

        self.mentionedResiduesCount = len(self.mentionedResidues)
        for sentence in description_sentences:
            for pattern in patterns:
                match = re.search(pattern, sentence)
                if match:
                    full_match = match.group(0)
                    sequence_id_regex = r'(SEQ ID NO[:]?\s?)([0-9]{1,5})'
                    matching_seq_id_no = re.search(sequence_id_regex, full_match).group(2)
                    if matching_seq_id_no not in descriptionMatchDict:
                        descriptionMatchDict[matching_seq_id_no] = {}
                    # get the epitope sequences
                    epitope_seq_ranges = [r'([A-Z])?([0-9]{1,5})(-|([\s]?to[\s]?))([A-Z])?([0-9]{1,5})',
                                          r'(between\s)?([A-Z])?([0-9]{1,5})\s(and)\s([A-Z])?([0-9]{1,5})',
                                          r'(from\s)?([A-Z])?([0-9]{1,5})\s(to)\s([A-Z])?([0-9]{1,5})'
                                        ]
                    epitope_numbers_statements = [r'([A-Z])?([0-9]{1,5})(\s|,|and)?([A-Z])?([0-9]{1,5})?(?=.*SEQ)']
                    for range_regex in epitope_seq_ranges:
                         # group 2 and group 6
                         # TODO: Iterate from the small range to the large range
                        ranges = re.search(range_regex, full_match)
                        if ranges == None:
                            continue
                        descriptionMatchDict[matching_seq_id_no][ranges.group(2)] = True
                        descriptionMatchDict[matching_seq_id_no][ranges.group(6)] = True
                    
                    for epitope_numbers_regex in epitope_numbers_statements:
                         # group 2 and group 6
                         # TODO: Iterate from the small range to the large range
                        ranges = re.search(epitope_numbers_regex, full_match)
                        # 
                        for num in re.finditer(epitope_numbers_regex, full_match):
                            descriptionMatchDict[matching_seq_id_no][num.group(2)] = True
                            
        # logger.info(descriptionMatchDict)
        
        for seq_no in descriptionMatchDict.keys():
            seq_object = {}
            seq_object['seqId'] = seq_no
            seq_object['claimedResidues'] = []
            seq_object['location'] = 'description'
            for claimed_residue in descriptionMatchDict[seq_no]:
                seq_object['claimedResidues'].append(claimed_residue)
            self.mentionedResidues.append(seq_object)
        logger.info(self.mentionedResidues)