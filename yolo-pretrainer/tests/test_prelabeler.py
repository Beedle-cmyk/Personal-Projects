import pytest
import torch
from prelabeler import Prelabeler
from unittest.mock import patch
from unittest.mock import MagicMock

@pytest.fixture
def prelabeler():
    return Prelabeler.__new__(Prelabeler)

##############################################
#             TESTING setters                #
##############################################
def test_set_confidence_valid(prelabeler):
    prelabeler.set_confidence(0.2, 0.8)

    assert prelabeler.min_conf == 0.2
    assert prelabeler.max_conf == 0.8

def test_set_confidence_invalid(prelabeler):
    with pytest.raises(ValueError):
        prelabeler.set_confidence(-1, 0.8)

###############################################
#               INITIALIZATION                #
###############################################

@patch("prelabeler.YOLO")
def test_initialize_yolo(mock_yolo, prelabeler):
    prelabeler._initialize_model("model.pt")
    mock_yolo.assert_called_once_with("model.pt")

def test_initialize_model_none(prelabeler):
    with pytest.raises(ValueError):
        prelabeler._initialize_model(None)

def test_initialize_model_invalid_extension(prelabeler):
    with pytest.raises(ValueError):
        prelabeler._initialize_model("model.xyz")

##################################################
#               Calculations                     #
##################################################

def test_no_mask_overlap(prelabeler):
    tensor1 = torch.tensor([
        [0.6, 0.0, 0.5],
        [0.0, 0.0, 0.3],
        [0.5, 0.3, 0.0]
    ])

    tensor2 = torch.tensor([
        [0.0, 0.1, 0.0],
        [0.9, 0.4, 0.0],
        [0.0, 0.0, 0.1]
    ])

    assert prelabeler._mask_overlap(tensor1, tensor2) == 0

def test_partial_mask_overlap(prelabeler):
    tensor1 = torch.tensor([
        [0, 1],
        [0, 1],
        [1, 0]
    ])
    
    tensor2 = torch.tensor([
        [0, 0],
        [1, 1],
        [0, 0]
    ])
    assert prelabeler._mask_overlap(tensor1, tensor2) == 0.5  # one intersection

def test_full_mask_overlap(prelabeler):
    tensor1 = torch.tensor([
        [1, 1],
        [1, 1],
        [1, 1]
    ])

    tensor2 = torch.tensor([
        [1, 1],
        [1, 1],
        [1, 1]
    ])
    assert prelabeler._mask_overlap(tensor1, tensor2) == 1

##################################################
#               Test predict                     #
##################################################

