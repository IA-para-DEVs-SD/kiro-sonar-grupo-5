"""Unit tests for src.prompt_builder module."""

from src.prompt_builder import _sanitize_user_content, build_prompt


class TestSanitizeUserContent:
    """Tests for _sanitize_user_content."""

    def test_removes_markers_case_insensitive(self) -> None:
        text = "hello [System] world [INST] end"
        result = _sanitize_user_content(text)
        assert "[System]" not in result
        assert "[INST]" not in result
        assert "hello" in result

    def test_removes_backticks(self) -> None:
        assert "```" not in _sanitize_user_content("code ```here```")

    def test_clean_text_unchanged(self) -> None:
        assert _sanitize_user_content("normal code") == "normal code"


class TestBuildPrompt:
    """Tests for build_prompt."""

    def test_includes_diff_section_when_diff_provided(self) -> None:
        result = build_prompt("@@ -1 +1 @@", "code", "rules", "f.py")
        assert "PESO MÁXIMO" in result

    def test_excludes_diff_section_when_empty(self) -> None:
        result = build_prompt("", "code", "rules", "f.py")
        assert "PESO MÁXIMO" not in result
