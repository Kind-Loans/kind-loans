import { useQuery } from "@tanstack/react-query";
import LoanProfileCard from "../../components/LoanProfileCard";
import LoanProfile from "../../types/LoanProfile";
import { Box, } from "@mui/material";

function Home() {
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

  return isLoading ? (
    <p>Loading...</p>
  ) : error ? (
    <p>Error: {error.message}</p>
  ) : (
    <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
    </Box>
  );
}

export default Home;
