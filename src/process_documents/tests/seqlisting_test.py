import pytest
import os
from classes.seqlisting import SeqListing
mock_xml_document1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mocks', 'seq_US8829165B2.xml')

def test_xml_parsing_1():
    seq_listing = SeqListing(mock_xml_document1,'US8828405B2')
    # print(seq_listing.sequences)
    print(len(seq_listing.sequences))