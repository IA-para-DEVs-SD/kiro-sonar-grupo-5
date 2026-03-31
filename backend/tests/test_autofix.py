"""Unit tests for src.autofix module."""

from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.autofix import _validate_path, apply_fix, extract_refactored_code


class TestValidatePath:
    """Tests for _validate_path."""

    @patch("src.autofix.get_repo_root", return_value="/home/user/repo")
    def test_raises_for_path_outside_repo(self, mock_root: MagicMock) -> None:
        with pytest.raises(ValueError, match="Caminho fora do repositório"):
            _validate_path("/etc/passwd")

    @patch("src.autofix.get_repo_root", return_value="/home/user/repo")
    def test_accepts_path_inside_repo(self, mock_root: MagicMock) -> None:
        _validate_path("/home/user/repo/src/app.py")


class TestExtractRefactoredCode:
    """Tests for extract_refactored_code."""

    def test_extracts_code_between_tags(self) -> None:
        response = "## Código\n[START]\nprint('hello')\n[END]\n"
        assert extract_refactored_code(response) == "print('hello')"

    def test_returns_none_when_tags_absent(self) -> None:
        response = "## Bugs\n- Nenhum bug encontrado."
        assert extract_refactored_code(response) is None

    def test_extracts_multiline_code(self) -> None:
        response = "[START]\ndef foo():\n    return 1\n[END]"
        assert extract_refactored_code(response) == "def foo():\n    return 1"


class TestApplyFix:
    """Tests for apply_fix."""

    @patch("builtins.input", return_value="s")
    @patch("builtins.open", mock_open())
    def test_applies_fix_when_user_accepts(self, mock_inp) -> None:
        response = "[START]\nprint('fixed')\n[END]"
        assert apply_fix(response, "file.py") is True

    @patch("builtins.input", return_value="n")
    def test_does_not_apply_when_user_declines(self, mock_inp) -> None:
        response = "[START]\nprint('fixed')\n[END]"
        assert apply_fix(response, "file.py") is False

    def test_returns_false_when_no_refactored_code(self) -> None:
        response = "## Bugs\n- Nenhum"
        assert apply_fix(response, "file.py") is False
