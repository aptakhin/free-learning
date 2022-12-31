from typing import Any

from base.parser import MarkdownParser


def prepare_view_inplace(entity: dict[str, Any]) -> dict:
    main_block = entity.get('properties', {}).get('main', {})
    if not main_block:
        return entity

    parser_block = main_block.get('parser')
    if not parser_block:
        return entity

    if parser_block['name'] == 'com.freelearning.base.markdown_parser':
        parser = MarkdownParser()
        blocks = parser.parse(main_block['content'], main_block.get('context', {}))
        entity['properties']['main']['blocks'] = blocks.json()

    return entity
