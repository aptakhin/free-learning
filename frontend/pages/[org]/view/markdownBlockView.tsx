
export default function MarkdownBlockView({ content }) {
    return <div dangerouslySetInnerHTML={{ __html: content }} />
}
