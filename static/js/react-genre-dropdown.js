const GenreItem = (props) => {
  return <a className="dropdown-item" href={props.genre.url}>{props.genre.name}</a>
}

class GenreDropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      genres: []
    }
  }

  componentDidMount() {
    axios.get('/ajax/genres/').then((response) => {
      const data = response.data
      if (data.success) {
        this.setState({
          genres: data.genres
        })
      }
    })
  }

  render() {
    const genreItems = this.state.genres.map((genre) =>
      <GenreItem key={genre.slug} genre={genre}/>
    )

    return (
      <div>
        {genreItems}
      </div>
    )
  }
}