import pytest
import os
import logging
logger = logging.getLogger()
from classes.patent import Patent
# Import the test patents
mock_xml_document1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', '8828405.xml')
mock_xml_document2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US10787484B2.xml')
mock_xml_document3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8829165B2.xml')
mock_xml_document4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8563698B2.xml')
mock_xml_document5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US20090246192A1.xml')
mock_xml_document6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8080243B2.xml') 
mock_xml_document7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8188234B2.xml') 
mock_xml_document8 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8399646B2.xml') 
mock_xml_document9 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US9175093B2.xml') 
mock_xml_document10 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US20090326202A1.xml') 
mock_xml_document11 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US20100068199A1.xml') 
mock_xml_document12 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8062640B2.xml') 
mock_xml_document13 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8357371B2.xml') 
mock_xml_document14 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8501184B2.xml') 
mock_xml_document15 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US9550837B2.xml') 
mock_xml_document16 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US9724411B2.xml') 
mock_xml_document17 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US10023654B2.xml') 
mock_xml_document18 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US20100166768A1.xml') 
mock_xml_document19 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US20120195910A1.xml') 


def test_xml_parsing_1():
    patent = Patent(mock_xml_document1,'US8828405B2')
    assert patent.patentAssignees == 'Lipoxen Technologies Limited'
    assert patent.applicants == 'Andrew David Bacon, Peter Laing, Gregory Gregoriadis, Wilson Romero Caparros-Wanderley'
    assert patent.inventors == 'Andrew David Bacon, Peter Laing, Gregory Gregoriadis, Wilson Romero Caparros-Wanderley'
    assert patent.examiners == 'Shin Lin Chen'
    assert patent.appNumber == '13292778'
    assert patent.appDate == '2011-11-09T00:00:00'
    assert patent.patentDate == '2014-09-09T00:00:00'
    assert '1. A composition for generating an immune response in a mammal, wherein said' in patent.claims
    assert 'This application is a continuation of U.S. application Ser' in  patent.description
    assert 'A composition comprising liposomes a' in patent.abstract

def test_claimed_residues1():
    patent = Patent(mock_xml_document1,'US8828405B2')
    # This is correct, no claims for this patent
    assert patent.mentionedResidues == []

def test_xml_parsing_2():
    patent = Patent(mock_xml_document2,'US10787484')
    assert patent.applicants == 'Genentech, Inc.'
    assert patent.inventors == 'Maureen Beresini, Daniel Burdick, Charles Eigenbrot, Jr., Daniel Kirchhofer, Robert Lazarus, Wei Li, John Quinn, Nicholas Skelton, Mark Ultsch, Yingnan Zhang'

def test_claimed_residues():
    patent = Patent(mock_xml_document2,'US10787484')
    # TODO: update with expected residues...
    assert patent.mentionedResidues != []

def test_claimed_residues_3():
    patent = Patent(mock_xml_document3,'US8829165B2')
    # TODO: update with expected residues...
    assert patent.mentionedResidues != []    

def test_claimed_residues_4():
    patent = Patent(mock_xml_document4,'US8563698B2')
    # TODO: update with expected residues...
    assert patent.mentionedResidues != []  

def test_claimed_residues_5():
    patent = Patent(mock_xml_document5,'US20090246192A1')
    # TODO: update with expected residues...
    assert patent.applicants == 'Jon H. Condra, Rose M. Cubbon, Holly A. Hammond, Laura Orsatti, Shilpa Pandit, Laurence B. Peterson, Joseph C. Santoro, Ayesha Sitlani, Dana D. Wood, Henryk Mach, Heidi Yoder, Sonia M. Gregory, Jeffrey T. Blue, Kevin Wang, Peter Luo, Denise K. Nawrocki, Pingyu Zhong, Feng Dong, Yan Li'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []  

def test_claimed_residues_6():
    patent = Patent(mock_xml_document6,'US8080243B2')
    assert patent.applicants == 'Hong Liang, Yasmina Noubia Abdiche, Javier Fernando Chaparro Riggers, Bruce Charles Gomes, Julie Jia Li Hawkins, Jaume Pons, Yuli Wang'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert patent.mentionedResidues[0]['claimedResidues'] == ['153', '154', '155', '194', '195', '197', '237', '238','239','367', '369', '374', '375','376', '377','378','379','381']  
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '53'

def test_claimed_residues_7():
    patent = Patent(mock_xml_document7,'US8188234B2')
    assert patent.applicants == 'Jon H. Condra, Rose M. Cubbon, Holly A. Hammond, Laura Orsatti, Shilpa Pandit, Laurence B. Peterson, Joseph C. Santoro, Ayesha Sitlani, Dana D. Wood, Henryk Mach, Heidi Yoder, Sonia M. Gregory, Jeffrey T. Blue, Kevin Wang, Peter Luo, Denise K. Nawrocki, Pingyu Zhong, Feng Dong, Yan Li'
    assert patent.inventors == patent.applicants
    # TODO: THIS IS A HARD PATENT WHERE THE RESIDUES ARE ACTUALLY SEQUENCES
    # DESCRIPTION: epitope comprising these amino acid residues is represented by SEQ ID NO: 37 and falls within the area of SEQ ID NO: 39 of human PCSK9 and SEQ ID NO: 41
    assert patent.mentionedResidues != []

def test_claimed_residues_8():
    patent = Patent(mock_xml_document8,'US8399646B2')
    assert patent.applicants == 'Hong Liang, Yasmina Noubia Abdiche, Javier Fernando Chaparro Riggers, Bruce Charles Gomes, Julie Jia Li Hawkins, Jaume Pons, Yuli Wang'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert patent.mentionedResidues[0]['claimedResidues'] == ['153', '154', '155', '194', '195', '197', '237', '238','239','367', '369', '374', '375','376', '377','378','379','381']  
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '53'

def test_claimed_residues_9():
    patent = Patent(mock_xml_document9,'US9175093B2')
    assert patent.applicants == 'RINAT NEUROSCIENCE CORP., PFIZER INC.'
    assert patent.inventors == 'Hong Liang, Yasmina Noubia Abdiche, Javier Fernando Chaparro Riggers, Bruce Charles Gomes, Julie Jia Li Hawkins, Jaume Pons, Xiayang Qiu, Pavel Strop, Yuli Wang'
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert patent.mentionedResidues[0]['claimedResidues'] == ['153', '154', '155', '194', '195', '197', '237', '238','239','367', '369', '374', '375','376', '377','378','379','381']  
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '188'

def test_claimed_residues_10():
    patent = Patent(mock_xml_document10,'US20090326202A1')
    assert patent.applicants == 'Simon Mark Jackson, Bei Shan, Wenyan Shen, Joyce Chi Yee Chan, Chadwick Terence King'
    assert patent.inventors == 'Simon Mark Jackson, Bei Shan, Wenyan Shen, Joyce Chi Yee Chan, Chadwick Terence King'
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 662
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '3'

def test_claimed_residues_11():
    patent = Patent(mock_xml_document11,'US20100068199A1')
    assert patent.applicants == 'Hong Liang, Yasmina Noubia Abdiche, Javier Fernando Chaparro Riggers, Bruce Charles Gomes, Julie Jia Li Hawkins, Jaume Pons, Xiayang Qiu, Pavel Strop, Yuli Wang'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 18
    assert patent.mentionedResidues[0]['claimedResidues'] == ['153', '154', '155', '194', '195', '197', '237', '238','239','367', '369', '374', '375','376', '377','378','379','381']  
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '53'

def test_claimed_residues_12():
    patent = Patent(mock_xml_document12,'US8062640B2')
    assert patent.applicants == 'Mark W. Sleeman, Joel H. Martin, Tammy T Huang, Douglas MacDonald'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'

def test_claimed_residues_13():
    patent = Patent(mock_xml_document13,'US8357371B2')
    assert patent.applicants == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald, Gary Swergold'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'

def test_claimed_residues_14():
    patent = Patent(mock_xml_document14,'US8501184B2')
    assert patent.applicants == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'

def test_claimed_residues_15():
    patent = Patent(mock_xml_document15,'US9550837B2')
    assert patent.applicants == 'REGENERON PHARMACEUTICALS, INC.'
    assert patent.inventors == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald'
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'

def test_claimed_residues_16():
    patent = Patent(mock_xml_document16,'US9724411B2')
    assert patent.applicants == 'Regeneron Pharmaceuticals, Inc.'
    assert patent.inventors == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald, Gary Swergold, Robert C. Pordy, William J. Sasiela'
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'

def test_claimed_residues_17():
    patent = Patent(mock_xml_document17,'US10023654B2')
    assert patent.applicants == 'REGENERON PHARMACEUTICALS, INC.'
    assert patent.inventors == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald'
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'


def test_claimed_residues_18():
    patent = Patent(mock_xml_document18,'US20100166768A1')
    assert patent.applicants == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald'
    assert patent.inventors == 'Mark W. Sleeman, Joel H. Martin, Tammy T. Huang, Douglas MacDonald'
    assert patent.mentionedResidues != []
    assert len(patent.mentionedResidues) == 1
    assert len(patent.mentionedResidues[0]['claimedResidues']) == 395
    assert patent.mentionedResidues[0]['location'] == 'description'
    assert patent.mentionedResidues[0]['seqId'] == '755'

# @pytest.mark.slow
def test_claimed_residues_19():
    patent = Patent(mock_xml_document19,'US20120195910A1')
    assert patent.applicants == 'YAN WU, CECILIA CHIU, DANIEL KIRCHHOFER, ANDREW PETERSON, GANESH KOLUMAM, MONICA KONG BELTRAN, PAUL MORAN, WEI LI'
    assert patent.inventors == patent.applicants
    assert patent.mentionedResidues == []
    # TODO: HARD PATENT
    #  (b) detecting formation of a complex between the anti-PCSK9 antibody and the PCSK9 protein., (i) at least one residue selected from the group consisting of R194 and E195 of human PCSK9,, (ii) at least one residue selected from the group consisting of D238 and A239 of human PCSK9,, (iii) at least one residue selected from the group consisting of A341 and Q342 of human PCSK9, and, (iv) at least one residue selected from the group consisting of E366, D367, I369, S376, T377, C378, F379, S381 and H391 of human PCSK9.
