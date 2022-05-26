import pytest

from navigation import paths_keeper
from pyfiles.compare import StructuralSimilarity

@pytest.mark.parametrize(
    "baseline_path, subject_path",
    paths_keeper.get_paths("jpg"),
    ids=paths_keeper.get_ids("jpg"),
)
def test_jpg(baseline_path, subject_path):
    compare = StructuralSimilarity(baseline_path, subject_path)
    assert compare.score == 1
