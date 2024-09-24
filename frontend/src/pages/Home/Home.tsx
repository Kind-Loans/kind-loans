import { useQuery } from "@tanstack/react-query";

interface LoanProfile {
  id: number;
  title: string;
  description: string;
  user_name: string;
  business_type: string;
}
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
    <div>
      {data?.map((loanProfile) => (
        <div key={loanProfile.id}>
          <h2>{loanProfile.title}</h2>
          <p>{loanProfile.description}</p>
          <p>{loanProfile.user_name}</p>
          <p>{loanProfile.business_type}</p>
        </div>
      ))}
    </div>
  );
}

export default Home;
