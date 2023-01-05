import TagsView from "../../../components/tagsview";
import MarkdownBlockView from "./markdownBlockView";
import MiroBlockView from "./miroBlockView";

export default function BaseEntityView({ label, id, properties, onAddTag, onRemoveTag }) {
    const renderedBlocks = properties?.main?.blocks?.items.map((block) => {
        if (block.typ == 'com.freelearning.base.markdown_html') {
            return <MarkdownBlockView {...block} />
        } else if (block.typ == 'com.freelearning.miro.block') {
            return <MiroBlockView {...block} />
        }
    });
    const tagView = <TagsView tags={[{ 'typ': 'com.freelearning.base.alias', 'space': 'DOM', 'id': 23 }, { 'typ': 'com.freelearning.base.alias', 'space': 'WOWOW', 'id': 34233 }]} onAddTag={onAddTag} onRemoveTag={onRemoveTag} />
    return <p class='pt-4'>#{id}: {tagView} {renderedBlocks}</p>
}
