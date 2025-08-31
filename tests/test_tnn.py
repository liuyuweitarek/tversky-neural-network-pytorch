import pytest

from tversky_neural_network.tnn import TverskyProjectionLayer, TverskySimilarityLayer

def test_tversky_projection_layer():
    with pytest.raises(NotImplementedError):
        TverskyProjectionLayer()

def test_tversky_similarity_layer():
    with pytest.raises(NotImplementedError):
        TverskySimilarityLayer()