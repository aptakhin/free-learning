import TagView from "./tagview";

export default function TagsView({ tags, onAddTag, onRemoveTag }) {
    const tagsView = tags?.map((tag) => {
        return <TagView tag={tag} onAddTag={onAddTag} onRemoveTag={onRemoveTag} />
    })
    return <>Tags: {tagsView}</>
}
