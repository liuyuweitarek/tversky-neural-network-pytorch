import pytest
import torch
from tversky_neural_network.tversky_neural_network import (
    TverskyProjectionLayer, 
    tversky_similarity,
    _tversky_prepare,
    _tversky_intersection,
    _tversky_difference
)

device = "cuda" if torch.cuda.is_available() else "cpu"

@pytest.fixture
def sample_tensors():
    torch.manual_seed(0)
    input = torch.randn(4, 16)             # (N, d)
    prototype_bank = torch.randn(6, 16)    # (P, d)
    feature_bank = torch.randn(8, 16)      # (F, d)
    return input, prototype_bank, feature_bank

def test_prepare_shapes(sample_tensors):
    a, b, feature_bank = sample_tensors
    _a, _b = _tversky_prepare(a, b, feature_bank)
    assert _a.shape == (4, 1, 8)
    assert _b.shape == (1, 6, 8)

def test_intersection_shapes(sample_tensors):
    a, b, feature_bank = sample_tensors
    _a, _b = _tversky_prepare(a, b, feature_bank)

    for psi in ["min", "max", "product", "mean", "gmean", "softmin"]:
        out = _tversky_intersection(_a, _b, psi=psi)
        assert out.shape == (4, 6, 8)
        assert torch.isfinite(out).all()

    # callable
    out2 = _tversky_intersection(_a, _b, psi=lambda x, y: (x + y) / 2)
    assert out2.shape == (4, 6, 8)

def test_difference_shapes(sample_tensors):
    a, b, feature_bank = sample_tensors
    _a, _b = _tversky_prepare(a, b, feature_bank)

    for match_type in ["ignore", "subtract"]:
        diff_a_b, diff_b_a = _tversky_difference(_a, _b, match_type=match_type)
        assert diff_a_b.shape == (4, 6, 8)
        assert diff_b_a.shape == (4, 6, 8)

def test_readme():
    model = TverskyProjectionLayer(
        in_features = 32,
        out_features = 16,
        num_features = 8,
        alpha = 0.5,
        beta = 0.5,
        theta = 1.0,
        eps = 1e-8,
        psi = "softmin",
        softmin_tau = 0.8,
        match_type = "subtract",
        device = device,
        dtype = torch.float32
    )
    x = torch.randn(10, 32, device=device)
    out = model(x)

    assert out.shape == (10, 16)
    assert torch.isfinite(out).all()

    loss = out.sum()
    print(loss.shape)
    loss.backward()
    for p in model.parameters():
        assert p.grad is not None