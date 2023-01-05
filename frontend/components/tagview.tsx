
export default function TagView({ tag }) {
    let tagView = ''
    if (tag.typ == 'com.freelearning.base.alias') {
        tagView = <div>#{tag.space}-{tag.id}</div>
    }
    // const tagView = <div>#{tag.label} {tag.space}-{tag.id}</div>
    return <>{tagView}</>
}
