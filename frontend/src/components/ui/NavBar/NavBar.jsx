import { NavLink } from "react-router-dom";
import "./NavBar.css";
import { useState, useRef } from "react";
import { useClickAway } from "react-use";
import MenuRoundedIcon from "@mui/icons-material/MenuRounded";

// reference: https://www.w3schools.com/howto/howto_js_topnav_responsive.asp
function NavBar() {
  // adding the states for mobile menu
  const [isActive, setIsActive] = useState(false);
  const ref = useRef(null);

  // user click outside of menu to close
  useClickAway(ref, () => setIsActive(false));

  // useClickAway(ref, () => setIsActive(false));

  const toggleActiveClass = () => {
    setIsActive(!isActive);
  };

  const removeActiveClass = () => {
    setIsActive(false);
  };

  return (
    <div
      className='nav-bar'
      ref={ref}
    >
      <div className='name'>
        <strong>UBC</strong>CoursePlanner
      </div>
      <button className='btn-menu'>
        <MenuRoundedIcon onClick={toggleActiveClass} />
      </button>
      <ul className={isActive ? "active-item active-list" : ""}>
        <li onClick={removeActiveClass}>
          <NavLink
            to='/'
            className='link'
          >
            Eligibility Tool
          </NavLink>
        </li>
        <li onClick={removeActiveClass}>
          <NavLink
            to='/degree-tracker'
            className='link'
          >
            Degree Tracker
          </NavLink>
        </li>
        <li onClick={removeActiveClass}>
          <NavLink
            to='/about'
            className='link'
          >
            About
          </NavLink>
        </li>
        <li onClick={removeActiveClass}>
          <NavLink
            to='/contact'
            className='link'
          >
            Contact
          </NavLink>
        </li>
      </ul>
    </div>
  );
}
export default NavBar;
