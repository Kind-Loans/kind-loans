import { useQuery } from "@tanstack/react-query";

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

  return isLoading ? (
    <p>Loading...</p>
  ) : error ? (
    <p>Error: {error.message}</p>
  ) : (
    <ul>
      {data?.map((loanProfile) => (
        <li key={loanProfile.id}>{loanProfile.business_type}</li>
      ))}
    </ul>
  );
}

export default Requests;
