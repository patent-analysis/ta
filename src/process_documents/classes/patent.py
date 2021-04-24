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
        res.append(first.text + ' '+ last.text)
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
        self.claimsCount = len(self.claims)
        self.appNumber = find_all_nested(root, './/application-reference', './/doc-number')
        self.appDate = find_all_nested(root, './/application-reference', './/date')


    #Extract epitope information
    def __extract_epitope_info(self):
        bindingString = r'''([^.]*?antibody(.*)binds(.*)residues[^.]*\.)'''
        pattern_1 = r'''((residue[s|\s])(.{0,150})(([A-Z][0-9]{1,5})+(,|and|to|\s?)?([A-Z][0-9]{1,5})?)+(.{0,30})(SEQ ID NO: ([0-9]))\.)'''
        # TODO: ENHANCE ENHANCE ENHANCE


        bindingString4 = r'''([^.]*?antibody(.*)binds(.*)residue[^.]*\.)'''
        
        #Regex
        bindingPattern = [re.compile(p) for p in [pattern_1, bindingString, bindingString4]]

        #claimedResidues array of dictionaries
        self.claimedResidues = []
        keysForSequences = ["seqNoId", "values"]
        keysForValues = ["num", "code"]
        
        lines = iter(self.claims)
        
        #Claimed as string
        for claimed in lines:
            #Find the required sentence with epitope info
            sentenceToEvaluate = ''
            for regex in bindingPattern:
                if re.findall(regex, claimed):
                    sentenceToEvaluate = re.findall(regex, claimed)
            
            #If pattern not found - return
            if not sentenceToEvaluate:
                next(lines, None)
                continue
            
            sequencesDict = dict.fromkeys(keysForSequences)
            sentenceToEvaluate = ','.join(str(v) for v in sentenceToEvaluate)
            
            #Extract Seq ID
            extractedSeqID = ''.join(sentenceToEvaluate)
            if re.search(r'\bresidues\b', extractedSeqID):
                extractedSeqID = extractedSeqID.split("SEQ ID NO:")[1].split(".")[0].strip()
                extractedSeqID = extractedSeqID.split(",")[0].strip()
            else:
                extractedSeqID = extractedSeqID.split("(SEQ ID NO:")[1].split(").")[0].strip()

            listings = extractedSeqID.split()
            for l in listings:
                if l.isdigit():
                    sequencesDict["seqNoId"] = l
            
            sequencesDict["values"] = []
            
            #Extract string with residues info
            extractedString = ''.join(sentenceToEvaluate)
            if re.search(r'\bresidues\b', extractedString):
                extractedString = extractedString.split("residues")[1].split("SEQ ID")[0]
            else:
                extractedString = extractedString.split("residue")[1].split("SEQ ID")[0]
            words = extractedString.split()
            for i in words:
                i = i.replace(',','')
                #if punctuation
                if i in string.punctuation:
                    i = i.replace(':','')
                #if range of sequences
                elif i.find("-") != -1:
                    rangeList = i.split("-")
                    for n in range(int(rangeList[0]), int(rangeList[-1]) + 1):
                        valuesDict = dict.fromkeys(keysForValues)
                        valuesDict["num"] = int(n)
                        sequencesDict["values"].append(valuesDict)
                #if mix of letters and digits
                elif (i.isalpha() == False) and (i.isdigit() == False) and (len(i) < 5 ):
                    i = i[1:]
                    valuesDict = dict.fromkeys(keysForValues)
                    valuesDict["num"] = int(i)
                    sequencesDict["values"].append(valuesDict)
                #if digital
                elif i.isdigit():
                    valuesDict = dict.fromkeys(keysForValues)
                    valuesDict["num"] = int(i)
                    sequencesDict["values"].append(valuesDict)
            self.claimedResidues.append(sequencesDict)
