
"""[summary]
"""

from src.app import home


def test_home_enpoint():
    """[summary]`
    """
    res = home()
    assert res.message == "Hello, World."
    assert res.code == "200"
