import { Link } from "react-router-dom";
import "./NavBar.css";
import { useState } from "react";
import MenuRoundedIcon from "@mui/icons-material/MenuRounded";

// reference: https://www.w3schools.com/howto/howto_js_topnav_responsive.asp
function NavBar() {
  // adding the states
  const [isActive, setIsActive] = useState(false);

  const toggleActiveClass = () => {
    setIsActive(!isActive);
  };

  const removeActiveClass = () => {
    setIsActive(false);
  };

  return (
    <div className='nav-bar'>
      <div className='name'>
        <strong>UBC</strong>CoursePlanner
      </div>
      <button className='btn-menu'>
        <MenuRoundedIcon onClick={toggleActiveClass} />
      </button>
      <ul className={isActive ? "active-item" : ""}>
        <li
          onClick={removeActiveClass}
          className={isActive ? "active-item" : ""}
        >
          <Link
            to='/'
            className='link'
          >
            Eligibility Tool
          </Link>
        </li>
        <li
          onClick={removeActiveClass}
          className={isActive ? "active-item" : ""}
        >
          <Link
            to='/degreetracker'
            className='link'
          >
            Degree Tracker
          </Link>
        </li>
        <li
          onClick={removeActiveClass}
          className={isActive ? "active-item" : ""}
        >
          <Link
            to='/about'
            className='link'
          >
            About
          </Link>
        </li>
        <li
          onClick={removeActiveClass}
          className={isActive ? "active-item" : ""}
        >
          <Link
            to='/contact'
            className='link'
          >
            Contact
          </Link>
        </li>
      </ul>
    </div>
  );
}
export default NavBar;
