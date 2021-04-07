import xml.etree.ElementTree as et
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Patent:
    def __init__(self, patent_id):
        self.patent_id = patent_id
        self.__process_xml()
      
        
    def __process_xml(self):
        tree = et.parse(self.patent_id + '.xml')
        root = tree.getroot()
        logger.info("in __process_xml")
        self.title = root.find('.//invention-title').text
        self.date = root.find('.//publication-reference').find('.//date').text
        self.inventors = [el.find('.//first-name').text + ' ' + 
                            el.find('.//last-name').text
                            for el in root.findall('.//inventor')]
        self.abstract = ' '.join([' '.join(el.itertext()) 
                            for el in root.findall('.//abstract')])
        self.description = ' '.join([' '.join(el.itertext()) 
                            for el in root.findall('.//description')])
        self.claims = [' '.join(el.itertext()) 
                            for el in root.findall('.//claim')]
        self.assignees = [el.find('.//orgname').text 
                            for el in root.findall('.//assignee')]
