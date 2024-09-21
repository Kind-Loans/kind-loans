import BottomNavBar from "../../components/BottomNavBar";
import { Box, Container } from "@mui/material";

function CreateRequest() {

  return (
    <Container
      maxWidth="sm"
      sx={{
        minHeight: "100dvh",
        display: "flex",
        flexDirection: "column",
        margin: "0",
      }}
    >
      <h1>Create Request</h1>
      <Box sx={{ flexGrow: 1 }} />
      <BottomNavBar />
    </Container>
  );
}

export default CreateRequest;
