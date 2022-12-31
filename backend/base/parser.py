from dataclasses import asdict, dataclass
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


class MarkdownParser(object):
    NAME = 'com.freelearning.base.markdown_parser'

    def parse(self, text: str, context: dict) -> ParserResults:
        md = (
            MarkdownIt('gfm-like')
        )
        html_text = md.render(text)

        return ParserResults(
            items=[
                ParserBlock(
                    typ='com.freelearning.base.markdown_content',
                    content=html_text,
                ),
            ],
        )

    def install_markdown_integration(self, *, code_block: Optional[str]):
        pass
