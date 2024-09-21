import { useQuery } from "@tanstack/react-query";
import BottomNavBar from "../../components/BottomNavBar";
import { Box, Container } from "@mui/material";

interface LoanProfile {
  id: number;
  business_type: string;
}
function Requests() {
  const { data, error, isLoading } = useQuery<LoanProfile[]>({
    queryKey: ["loan-profiles"],
    queryFn: async () => {
      const response = await fetch("api/loanprofile/");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
  });

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
      <h1>Loan Requests</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error.message}</p>
      ) : (
        <ul>
          {data?.map((loanProfile) => (
            <li key={loanProfile.id}>{loanProfile.business_type}</li>
          ))}
        </ul>
      )}
      <Box sx={{ flexGrow: 1 }} />
      <BottomNavBar />
    </Container>
  );
}

export default Requests;
