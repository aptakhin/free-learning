
export default function MiroEntityView({ label, id, properties }) {
    return <div>#{id}: Miro open <a link="{properties.url}">{properties.url}</a></div>
}
