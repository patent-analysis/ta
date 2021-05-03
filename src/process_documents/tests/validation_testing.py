import os
import json
import sys

mocks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks')
sys.path.insert(0, mocks_dir + '/../../classes/')

from patent import Patent

data_path = os.path.join(mocks_dir, 'validation_data.json')
data_file = open(data_path)
data = json.load(data_file)

for datum in data:
    patent_xml_path = os.path.join(mocks_dir, datum['patentNumber'] + '.xml')
    patent = Patent(patent_xml_path, datum['patentNumber'])
    for key in datum:
        if (datum[key].lower() != patent.__dict__[key].lower()):
            print(key + "is incorrect")
            print("Extracted: " + patent.__dict__[key])
    print(patent.mentionedResidues)