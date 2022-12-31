import MarkdownBlockView from "./markdownBlockView";

export default function BaseEntityView({ label, id, properties }) {
    console.log('Got data', id, properties)

    const renderedBlocks = properties?.main?.blocks?.items.map((block) => {
        console.log('DD', block, block.typ, block.typ == 'com.freelearning.base.markdown_content')
        if (block.typ == 'com.freelearning.base.markdown_content') {
            return <MarkdownBlockView {...block} />
        } else {

        }
    });
    return <div>#{id}: {renderedBlocks}</div>
}
