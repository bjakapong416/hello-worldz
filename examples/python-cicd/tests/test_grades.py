import pytest

from grades import average, grade


@pytest.mark.parametrize(
    "score, expected",
    [(100, "A"), (80, "A"), (79, "B"), (70, "B"), (60, "C"), (50, "D"), (49, "F"), (0, "F")],
)
def test_grade(score, expected):
    assert grade(score) == expected


@pytest.mark.parametrize("score", [-1, 101])
def test_grade_out_of_range(score):
    with pytest.raises(ValueError):
        grade(score)


def test_average():
    assert average([80, 70, 60]) == 70


def test_average_rounds_to_2_digits():
    assert average([1, 2, 2]) == pytest.approx(1.67)


def test_average_empty_list():
    with pytest.raises(ValueError, match="อย่างน้อย 1 ค่า"):
        average([])
