import Paper from "@mui/material/Paper";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import HomeIcon from "@mui/icons-material/Home";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import ListAltIcon from "@mui/icons-material/ListAlt";
import { Link, useLocation } from "react-router-dom";

export default function BottomNavBar() {
  const location = useLocation();

  return (
    <Paper
      sx={{ position: "fixed", bottom: 0, left: 0, right: 0 }}
      elevation={3}
    >
      <BottomNavigation showLabels value={location.pathname}>
        <BottomNavigationAction
          label="Home"
          icon={<HomeIcon />}
          component={Link}
          to="/"
          value="/"
        />
        <BottomNavigationAction
          label="Requests"
          icon={<ListAltIcon />}
          component={Link}
          to="/requests"
          value="/requests"
        />
        <BottomNavigationAction
          label="Add Request"
          icon={<AddCircleOutlineIcon />}
          component={Link}
          to="/create-request"
          value="/create-request"
        />
      </BottomNavigation>
    </Paper>
  );
}
