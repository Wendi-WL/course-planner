import { NavLink } from "react-router-dom";
import "./NavBar.css";
import { useState, useRef } from "react";
import { useClickAway } from "react-use";
import MenuRoundedIcon from "@mui/icons-material/MenuRounded";

// reference: https://www.w3schools.com/howto/howto_js_topnav_responsive.asp
function NavBar() {
  // adding the states for mobile menu
  const [isOpen, setisOpen] = useState(false);
  const ref = useRef(null);

  // user click outside of menu to close
  useClickAway(ref, () => setisOpen(false));

  // useClickAway(ref, () => setisOpen(false));

  const toggleOpenClass = () => {
    setisOpen(!isOpen);
  };

  const removeOpenClass = () => {
    setisOpen(false);
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
        <MenuRoundedIcon onClick={toggleOpenClass} />
      </button>
      <ul className={isOpen ? "open-item open-list" : ""}>
        <li onClick={removeOpenClass}>
          <NavLink
            to='/'
            className={({ isActive }) =>
              isActive ? "link active-link" : "link"
            }
          >
            Eligibility Tool
          </NavLink>
        </li>
        <li onClick={removeOpenClass}>
          <NavLink
            to='/degree-tracker'
            className={({ isActive }) =>
              isActive ? "link active-link" : "link"
            }
          >
            Degree Tracker
          </NavLink>
        </li>
        <li onClick={removeOpenClass}>
          <NavLink
            to='/about'
            className={({ isActive }) =>
              isActive ? "link active-link" : "link"
            }
          >
            About
          </NavLink>
        </li>
        <li onClick={removeOpenClass}>
          <NavLink
            to='/contact'
            className={({ isActive }) =>
              isActive ? "link active-link" : "link"
            }
          >
            Contact
          </NavLink>
        </li>
      </ul>
    </div>
  );
}
export default NavBar;
