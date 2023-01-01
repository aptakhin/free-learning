// import styles from './layout.module.css';

import { useState } from "react";

export default function TextEditor({ initOpenState, onTextSubmit }) {
    const [openState, setOpenState] = useState(initOpenState || false)
    const [content, setContent] = useState('')

    const replyButton = !openState && (<div onClick={() => setOpenState(true)}class="underline decoration-dashed cursor-pointer">Reply</div>)
    const textForm = openState && (<>
        <textarea class="
            mt-1
            block
            w-full
            rounded-md
            border-gray-300
            shadow-sm
            focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50
        " rows="3" spellcheck="false" onChange={ev => setContent(ev.target.value)}>{content}</textarea>
        <div onClick={() => setOpenState(false)} class="underline decoration-dashed cursor-pointer text-left">X</div>
        <div onClick={() => onTextSubmit(content)} class="underline decoration-dashed cursor-pointer text-right">Submit</div>

    </>)
    return <>{replyButton} {textForm}</>
}
