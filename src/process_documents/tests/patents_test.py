import pytest
import os
from classes.patent import Patent
mock_xml_document1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', '8828405.xml')
mock_xml_document2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'US10787484B2.xml')

def test_xml_parsing_1():
    patent = Patent(mock_xml_document1,'US8828405B2')
    assert patent.patentAssignees == 'Lipoxen Technologies Limited'
    assert patent.applicants == 'Andrew David Bacon, Peter Laing, Gregory Gregoriadis, Wilson Romero Caparros-Wanderley'
    assert patent.inventors == 'Andrew David Bacon, Peter Laing, Gregory Gregoriadis, Wilson Romero Caparros-Wanderley'
    assert patent.examiners == 'Shin Lin Chen'
    assert patent.appNumber == '13292778'
    assert patent.appDate == '20111109'
    assert patent.patentDate == '20140909'
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

def test_claimed_residues():
    patent = Patent(mock_xml_document2,'US10787484')
    # TODO: update with expected residues...
    assert patent.mentionedResidues != []