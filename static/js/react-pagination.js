const PageItemInit = (props) => {
  return (
    <li className="page-item disabled">
      <span className="page-link">Page {props.current} Of {props.numPages}</span>
    </li>
  );
}

const PageItem = (props) => {
  return (
    <li className={'page-item ' + (props.active ? 'active' : '')}>
      {props.active ? (
        <span className="page-link">{props.text} <span className="sr-only">(current)</span></span>
      ) : (
        <a className="page-link" href={props.url}>{props.text}</a>
      )}
    </li>
  );
}

class Pagination extends React.Component {
  constructor(props) {
    super(props);

    let listPages = [];
    for (var i=props.pagination.start;i<=props.pagination.end;i++) {
      listPages.push(i);
    }

    this.state = {
      current: props.pagination.current,
      listPages: listPages,
      numPages: props.pagination.num_pages,
      hasPrev: props.pagination.has_prev,
      hasNext: props.pagination.has_next,
    }
  }

  render() {
    const pageItems = this.state.listPages.map((pageNum) =>
      <PageItem key={pageNum.toString()} active={pageNum == this.state.current ? true : false} url={'?page=' + pageNum} text={pageNum}/>
    );
    return (
      <nav aria-label="Pagination">
        <ul className="pagination justify-content-center">
          <PageItemInit current={this.state.current} numPages={this.state.numPages}/>

          {this.state.hasPrev && (
            <PageItem url="?page=1" text="&laquo;"/>
          )}

          {pageItems}

          {this.state.hasNext && (
            <PageItem url={'?page=' + this.state.numPages} text="&raquo;"/>
          )}
        </ul>
      </nav>
    );
  }
}
