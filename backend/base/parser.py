from dataclasses import asdict, dataclass
import re
from typing import Optional, Any

from markdown_it import MarkdownIt


@dataclass
class ParserBlock(object):
    typ: str
    content: str


@dataclass
class ParserResults(object):
    items: list[ParserBlock]

    def json(self) -> dict[str, Any]:
        return {'items': [asdict(it) for it in self.items]}


class ExtractRule(object):
    def __init__(self, regex, typ) -> None:
        self.regex = regex
        self.typ = typ

    def extract(self, blocks: list[ParserBlock]) -> list[ParserBlock]:
        """The trivial regex blocks extraction from text."""
        new_blocks = []

        default_block = 'com.freelearning.base.markdown_raw'
        for block in blocks:
            if block.typ != default_block:
                continue

            new_adds = re.split(self.regex, block.content)

            for new_block in new_adds:
                if not new_block:
                    continue

                make_typ = default_block
                if re.match(self.regex, new_block):
                    make_typ = self.typ

                new_blocks.append(
                    ParserBlock(
                        typ=make_typ,
                        content=new_block,
                    )
                )

        return new_blocks


class MarkdownParser(object):
    NAME = 'com.freelearning.base.markdown_parser'

    def __init__(self) -> None:
        self._extract_rules = [
            ExtractRule(
                '(https://miro.com/app/board/\S+)',
                typ='com.freelearning.miro.block',
            )
        ]

    def parse(self, text: str, context: dict) -> ParserResults:
        blocks = [
            ParserBlock(
                typ='com.freelearning.base.markdown_raw',
                content=text,
            ),
        ]

        for rule in self._extract_rules:
            blocks = rule.extract(blocks)

        return ParserResults(items=blocks)

    def export_html(self, parser_results: ParserResults) -> ParserResults:
        blocks = []
        for block in parser_results.items:
            if block.typ == 'com.freelearning.base.markdown_raw':
                md = MarkdownIt('gfm-like')
                html_text = md.render(block.content)

                blocks.append(
                    ParserBlock(
                        typ='com.freelearning.base.markdown_html',
                        content=html_text,
                    )
                )
            else:
                blocks.append(block)

        return ParserResults(items=blocks)

    def install_markdown_integration(self, *, code_block: Optional[str]):
        pass
