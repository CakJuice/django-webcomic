const ChapterItem = (props) => {
  return (
    <h3><a href={props.chapter.url}>{props.chapter.title}</a></h3>
  )
}

class ChapterList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      chapters: props.chapters,
    }
  }

  render() {
    const chapterItems = this.state.chapters.map((chapter) =>
      <ChapterItem key={chapter.slug} chapter={chapter}/>
    );
    return (
      <div>
        {chapterItems}
      </div>
    );
  }
}