import NavBar from "../components/ui/NavBar/NavBar.jsx";
import { Outlet } from "react-router-dom";

function Layout() {
  return (
    <>
      <NavBar />
      <main>
        <Outlet />
      </main>
    </>
  );
}
export default Layout;
