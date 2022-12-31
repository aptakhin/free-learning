import Link from "next/link";

export default function MiroBlockView({ content }) {
    return <div>Miro open: <a href={ content } target='_blank'>{content}</a>
    </div>
}
