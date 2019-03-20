const NavUserMenu = (props) => {
  return (
    <li className="nav-item dropdown">
      <a className="nav-link dropdown-toggle" id="userNavbarDropdown" role="button" href="#" data-toggle="dropdown"
         aria-haspopup="true" aria-expanded="false">{props.username}</a>
      <div className="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
        <a className="dropdown-item" href={props.urlComicCreate}>Create New Comic</a>
        <div className="dropdown-divider"></div>
        <a className="dropdown-item" href={props.urlLogout}>Logout</a>
      </div>
    </li>
  );
}

const NavNonUserMenu = (props) => {
  return <React.Fragment>
    <li className="nav-item">
      <a className="btn btn-outline-success" role="button" href={props.urlSignup}>Sign Up</a>
    </li>
    <li className="nav-item">
      <a className="btn btn-info ml-2" role="button" href={props.urlLogin}>Login</a>
    </li>
  </React.Fragment>
}

const GenreItem = (props) => {
  return <a className="dropdown-item" href={props.genre.url}>{props.genre.name}</a>
}

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      homepageUrl: '/',
      genres: [],
      isAuthenticated: props.isAuthenticated,
      username: props.username,
      urlLogin: '/login/',
      urlLogout: '/logout/',
      urlSignup: '/signup/',
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
    let navRightMenu;
    if (this.state.isAuthenticated) {
      navRightMenu = <NavUserMenu username={this.state.username} urlComicCreate={this.state.urlComicCreate}
                           urlLogout={this.state.urlLogout}/>
    } else {
      navRightMenu = <NavNonUserMenu urlSignup={this.state.urlSignup} urlLogin={this.state.urlLogin}/>
    }

    const genreItems = this.state.genres.map((genre) =>
      <GenreItem key={genre.slug} genre={genre}/>
    )

    return (
      <nav className="navbar navbar-expand-sm navbar-light" id="navbar">
        <div className="container">
          <a className="navbar-brand" href={this.state.homepageUrl}>Webcomic</a>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarContent"
                  aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarContent">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" id="genreNavbarDropdown" role="button" href="#" data-toggle="dropdown"
                   aria-haspopup="true" aria-expanded="false">Genre</a>
                <div className="dropdown-menu" id="navGenre" aria-labelledby="genreDropdown">
                    {genreItems}
                </div>
              </li>
            </ul>
            <ul className="navbar-nav ml-auto">
              {navRightMenu}
            </ul>
          </div>
        </div>
      </nav>
    )
  }
}