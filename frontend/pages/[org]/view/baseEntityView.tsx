import MarkdownBlockView from "./markdownBlockView";
import MiroBlockView from "./miroBlockView";

export default function BaseEntityView({ label, id, properties }) {
    console.log('Got data', id, properties)

    const renderedBlocks = properties?.main?.blocks?.items.map((block) => {
        console.log('DD', block, block.typ, block.typ == 'com.freelearning.base.markdown_content')
        if (block.typ == 'com.freelearning.base.markdown_html') {
            return <MarkdownBlockView {...block} />
        } else if (block.typ == 'com.freelearning.miro.block') {
            return <MiroBlockView {...block} />
        }
    });
    return <div>#{id}: {renderedBlocks}</div>
}
