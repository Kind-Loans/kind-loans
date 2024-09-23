import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Home from "./pages/Home/Home";
import Requests from "./pages/Requests/Requests";
import CreateRequest from "./pages/CreateRequest/CreateRequest";
import "./index.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import AppWrapper from "./components/AppWrapper";

const queryClient = new QueryClient();

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#e1f5fe",
    },
  },
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppWrapper children={<Home />} title="My Loan Profiles" />,
  },
  {
    path: "/requests",
    element: <AppWrapper children={<Requests />} title="Loan Requests" />,
  },
  {
    path: "/create-request",
    element: <AppWrapper children={<CreateRequest />} title="Create Loan Request" />,
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </QueryClientProvider>
  </StrictMode>
);
