"""Tests for pb-tomarkdown's HTML-to-Markdown conversion."""

import pytest
from conftest import load_script

mod = load_script("pb-tomarkdown")
html_to_markdown = mod.html_to_markdown


class TestHeadings:
    def test_h1(self) -> None:
        assert html_to_markdown("<h1>Title</h1>") == "# Title\n"

    def test_h1_through_h6(self) -> None:
        for level in range(1, 7):
            tag = "h%d" % level
            result = html_to_markdown("<%s>X</%s>" % (tag, tag))
            assert result == "%s X\n" % ("#" * level)


class TestInlineFormatting:
    def test_bold_strong(self) -> None:
        assert html_to_markdown("<p><b>bold</b></p>") == "**bold**\n"
        assert html_to_markdown("<p><strong>bold</strong></p>") == "**bold**\n"

    def test_italic_em(self) -> None:
        assert html_to_markdown("<p><i>italic</i></p>") == "_italic_\n"
        assert html_to_markdown("<p><em>italic</em></p>") == "_italic_\n"

    def test_strikethrough(self) -> None:
        assert html_to_markdown("<p><s>gone</s></p>") == "~~gone~~\n"
        assert html_to_markdown("<p><del>gone</del></p>") == "~~gone~~\n"

    def test_inline_code(self) -> None:
        assert html_to_markdown("<p><code>x = 1</code></p>") == "`x = 1`\n"

    def test_nested_formatting(self) -> None:
        result = html_to_markdown("<p><b>bold <i>and italic</i></b></p>")
        assert result == "**bold _and italic_**\n"

    def test_link(self) -> None:
        result = html_to_markdown('<p><a href="https://example.com">text</a></p>')
        assert result == "[text](https://example.com)\n"

    def test_link_with_bold_inside(self) -> None:
        result = html_to_markdown('<p><a href="https://x.com"><b>Bold</b></a></p>')
        assert result == "[**Bold**](https://x.com)\n"

    def test_image(self) -> None:
        result = html_to_markdown('<p><img src="https://x.com/a.png" alt="alt"></p>')
        assert result == "![alt](https://x.com/a.png)\n"

    def test_line_break(self) -> None:
        result = html_to_markdown("<p>one<br>two</p>")
        assert result == "one  \ntwo\n"


class TestParagraphsAndWhitespace:
    def test_multiple_paragraphs(self) -> None:
        result = html_to_markdown("<p>First</p><p>Second</p>")
        assert result == "First\n\nSecond\n"

    def test_internal_whitespace_collapsed(self) -> None:
        result = html_to_markdown("<p>a   b\n\tc</p>")
        assert result == "a b c\n"

    def test_whitespace_only_nodes_ignored(self) -> None:
        result = html_to_markdown("<h1>A</h1>\n   \n<p>B</p>")
        assert result == "# A\n\nB\n"

    def test_empty_input(self) -> None:
        assert html_to_markdown("") == "\n"


class TestLists:
    def test_unordered_list(self) -> None:
        result = html_to_markdown("<ul><li>One</li><li>Two</li></ul>")
        assert result == "- One\n- Two\n"

    def test_ordered_list(self) -> None:
        result = html_to_markdown("<ol><li>One</li><li>Two</li></ol>")
        assert result == "1. One\n2. Two\n"

    def test_nested_list_indented_for_ordered_parent(self) -> None:
        # A 2-space indent isn't enough for CommonMark to nest content under
        # an "1. " marker (3 chars wide); it must be indented at least that far.
        result = html_to_markdown(
            "<ol><li>Top<ul><li>Sub</li></ul></li></ol>"
        )
        assert result == "1. Top\n    - Sub\n"

    def test_deeply_nested_mixed_list(self) -> None:
        result = html_to_markdown(
            "<ul><li>A<ol><li>A1</li></ol></li><li>B</li></ul>"
        )
        assert result == "- A\n    1. A1\n- B\n"


class TestCodeBlocks:
    def test_pre_code_preserves_newlines_and_indentation(self) -> None:
        result = html_to_markdown("<pre><code>def foo():\n    return 42\n</code></pre>")
        assert result == "```\ndef foo():\n    return 42\n```\n"

    def test_pre_without_code_child(self) -> None:
        result = html_to_markdown("<pre>line one\nline two</pre>")
        assert result == "```\nline one\nline two\n```\n"


class TestTables:
    def test_simple_table(self) -> None:
        html = (
            "<table><tr><th>A</th><th>B</th></tr>"
            "<tr><td>1</td><td>2</td></tr></table>"
        )
        result = html_to_markdown(html)
        assert result == "| A | B |\n| --- | --- |\n| 1 | 2 |\n"

    def test_table_with_thead_tbody(self) -> None:
        html = (
            "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
            "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
        )
        result = html_to_markdown(html)
        assert result == "| A | B |\n| --- | --- |\n| 1 | 2 |\n"


class TestBlockquotes:
    def test_single_paragraph_blockquote(self) -> None:
        result = html_to_markdown("<blockquote><p>Quoted.</p></blockquote>")
        assert result == "> Quoted.\n"

    def test_multi_paragraph_blockquote_keeps_paragraphs_separate(self) -> None:
        html = "<blockquote><p>First.</p><p>Second.</p></blockquote>"
        result = html_to_markdown(html)
        assert result == "> First.\n>\n> Second.\n"


class TestMisc:
    def test_horizontal_rule(self) -> None:
        assert html_to_markdown("<p>A</p><hr><p>B</p>") == "A\n\n---\n\nB\n"

    def test_html_entities_decoded(self) -> None:
        result = html_to_markdown("<p>Caf&eacute; &amp; friends</p>")
        assert result == "Caf\u00e9 & friends\n"


class TestEscaping:
    def test_markdown_special_chars_escaped(self) -> None:
        result = html_to_markdown("<p>1 * 2 [x] _y_ `z` #tag</p>")
        assert result == "1 \\* 2 \\[x\\] \\_y\\_ \\`z\\` \\#tag\n"

    def test_angle_bracket_escaped_to_avoid_inline_html(self) -> None:
        result = html_to_markdown("<p>a &lt;tag&gt; b</p>")
        assert result == "a \\<tag> b\n"

    def test_code_span_not_escaped(self) -> None:
        # Content inside a <code> span is rendered verbatim between backticks,
        # not run through the general text escaper.
        result = html_to_markdown("<p><code>a[b]*c*</code></p>")
        assert result == "`a[b]*c*`\n"


class TestMalformedHtml:
    def test_unclosed_tag_does_not_raise(self) -> None:
        # Real-world clipboard HTML is sometimes malformed; conversion should
        # degrade gracefully rather than raising.
        html_to_markdown("<p>Unclosed <b>bold")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
