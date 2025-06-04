import { Link } from "react-router-dom";

function NavBar() {
  return (
    <div className='nav-bar'>
      <div className='name'>
        <strong>UBC</strong>CoursePlanner
      </div>
      <ul>
        <li>
          <Link to='/'>
            <button>Eligibility Tool</button>
          </Link>
        </li>
        <li>
          <Link to='/degreetracker'>
            <button>Degree Tracker</button>
          </Link>
        </li>
        <li>
          <Link to='/about'>
            <button>About</button>
          </Link>
        </li>
        <li>
          <Link to='/contact'>
            <button>Contact</button>
          </Link>
        </li>
      </ul>
    </div>
  );
}
export default NavBar;
