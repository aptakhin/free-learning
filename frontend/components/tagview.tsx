import styles from './tagsview.module.css';

export default function TagView({ tag }) {
    let tagView = ''
    if (tag.typ == 'com.freelearning.base.alias') {
        tagView = <>#{tag.space}-{tag.id}</>
    } else if (tag.typ == 'com.freelearning.base.team') {
        tagView = <>driver: {tag.driver}</>
    }

    const stylesxx = []
    return <span className={`underline decoration-dotted ${styles.item} cursor-pointer`}>{tagView}</span>
}
