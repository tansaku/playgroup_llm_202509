from representations import make_grid_csv_english_words, make_grid_plain



def test_make_grid_plain():
    """Test the make_grid_plain function"""
    # Test cases from test_utils.py
    test_cases = [
        ([[1, 0, 0], [0, 0, 0], [0, 0, 0]], "100\n000\n000"),
        ([[0, 0, 0], [0, 1, 0], [1, 2, 3]], "000\n010\n123"),
    ]

    for input_grid, expected in test_cases:
        result = make_grid_plain(input_grid)
        assert result == expected, f"Expected {expected}, got {result}"

    print("All make_grid_plain tests passed!")


def test_make_grid_csv_english_words():
    """Test the make_grid_csv_english_words function"""
    # Test case 1: Simple 2x2 grid
    input_grid = [[1, 2], [3, 4]]
    expected = "one, two\nthree, four"
    result = make_grid_csv_english_words(input_grid)
    assert result == expected
    print("Test 1 passed: Simple 2x2 grid")

    # Test case 2: Grid with zeros
    input_grid = [[0, 1], [2, 0]]
    expected = "zero, one\ntwo, zero"
    result = make_grid_csv_english_words(input_grid)
    assert result == expected
    print("Test 2 passed: Grid with zeros")

    # Test case 3: Single cell grid
    input_grid = [[8]]
    expected = "eight"
    result = make_grid_csv_english_words(input_grid)
    assert result == expected
    print("Test 3 passed: Single cell grid")

    # Test case 4: Larger grid with various numbers
    input_grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected = "one, zero, zero\nzero, zero, zero\nzero, zero, zero"
    result = make_grid_csv_english_words(input_grid)
    assert result == expected
    print("Test 4 passed: Larger grid with various numbers")

    print("All tests passed!")


if __name__ == "__main__":
    test_make_grid_plain()
    test_make_grid_csv_english_words()
