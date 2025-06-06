import { NavLink } from "react-router-dom";
import "./NavBar.css";
import { useState, useRef } from "react";
import { useClickAway } from "react-use";
import MenuRoundedIcon from "@mui/icons-material/MenuRounded";

// reference: https://www.w3schools.com/howto/howto_js_topnav_responsive.asp
function NavBar() {
  const routes = [
    {
      path: "/",
      name: "Degree Tracker",
    },
    {
      path: "/eligibility-tool",
      name: "Eligibility Tool",
    },
    {
      path: "/about",
      name: "About",
    },
    {
      path: "/contact",
      name: "Contact",
    },
  ];
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
        {routes.map((route) => (
          <li onClick={removeOpenClass}>
            <NavLink
              to={route.path}
              className={({ isActive }) =>
                isActive ? "link active-link" : "link"
              }
            >
              {route.name}
            </NavLink>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default NavBar;
