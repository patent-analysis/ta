import xml.etree.ElementTree as et
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Patent:
    def __init__(self, patent_id):
        self.patentNumber = patent_id
        self.__process_xml()
      
        
    def __process_xml(self):
        tree = et.parse(self.patentNumber + '.xml')
        root = tree.getroot()
        logger.info("in __process_xml")
        self.patentName = root.find('.//invention-title').text
        self.patentDate = root.find('.//publication-reference').find('.//date').text
        self.inventors = [el.find('.//first-name').text + ' ' + 
                            el.find('.//last-name').text
                            for el in root.findall('.//inventor')]
        self.abstract = ' '.join([' '.join(el.itertext()) 
                            for el in root.findall('.//abstract')])
        self.description = ' '.join([' '.join(el.itertext()) 
                            for el in root.findall('.//description')])
        self.claims = [' '.join(el.itertext()) 
                            for el in root.findall('.//claim')]
        self.patentAssignees = [el.find('.//orgname').text 
                            for el in root.findall('.//assignee')]
        self.applicants = [el.find('.//orgname').text 
                                for el in root.findall('.//us-applicant')]
        self.examiners = root.find('.//primary-examiner').find('.//first-name').text + ' ' + root.find('.//primary-examiner').find('.//last-name').text
        self.claimsCount = len(self.claims)
        self.appNumber = root.find('.//application-reference').find('.//doc-number').text
        self.appDate = root.find('.//application-reference').find('.//date').text
