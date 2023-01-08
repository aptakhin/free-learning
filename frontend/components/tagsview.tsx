import TagView from "./tagview";
import styles from './tagsview.module.css';
import { PlusCircleIcon } from '@heroicons/react/24/outline'

export default function TagsView({ tags }) {
    const tagsView = tags.data?.map(tagItem => {
        return <TagView tag={tagItem} />
    })
    return <span className={styles.container}>{tagsView} <PlusCircleIcon className="h-5 w-5 text-black-500 cursor-pointer inline"/></span>
}
