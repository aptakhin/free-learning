import TagsView from "../../../components/tagsview";
import MarkdownBlockView from "./markdownBlockView";
import MiroBlockView from "./miroBlockView";

import { HashtagIcon } from '@heroicons/react/24/outline'

export default function BaseEntityView({ label, id, properties, onAddTag, onRemoveTag }) {
    const renderedBlocks = properties?.main?.blocks?.items.map((block) => {
        if (block.typ == 'com.freelearning.base.markdown_html') {
            return <MarkdownBlockView {...block} />
        } else if (block.typ == 'com.freelearning.miro.block') {
            return <MiroBlockView {...block} />
        }
    });
    // const tagView = <TagsView tags={} onAddTag={onAddTag} onRemoveTag={onRemoveTag} />
    const tagsData = { 'data': [{ 'typ': 'com.freelearning.base.alias', 'space': 'DOM', 'id': 23 }, { 'typ': 'com.freelearning.base.team', 'driver': 'Alex Ptakhin', 'and': [12313, 123231]}] }
    const tagsView = <TagsView tags={tagsData} />

    const linkTag = <HashtagIcon className="h-4 w-4 text-blue-600 cursor-pointer inline relative bottom-0.5" />

    return <p class='pt-4'>{linkTag}{id}: {tagsView} {renderedBlocks}</p>
}
