import pytest
import os
from classes.patent import Patent
mock_xml_document1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', '8828405.xml')
mock_xml_document2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US10787484B2.xml')
mock_xml_document3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8829165B2.xml')
mock_xml_document4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US8563698B2.xml')
mock_xml_document5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US20090246192A1.xml')


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

