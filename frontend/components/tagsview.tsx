import TagView from "./tagview";
import { ReactNode } from "react";
import styles from './tagsview.module.css';
import { PlusCircleIcon } from '@heroicons/react/24/outline'

// type TagsProps = React.PropsWithChildren<{}>;
// interface TagsDataMapProps {
//     data?: ReactNode
//     // any props that come into the component
// }
interface TagsDataProps {
    data?: Array<ReactNode>
}
interface TagsProps {
    tags?: TagsDataProps
}

export default function TagsView({ tags }: TagsProps) {
    const tagsView = tags?.data?.map(tagItem => {
        return <TagView tag={tagItem} />
    })
    return <span className={styles.container}>{tagsView} <PlusCircleIcon className="h-5 w-5 text-black-500 cursor-pointer inline"/></span>
}
