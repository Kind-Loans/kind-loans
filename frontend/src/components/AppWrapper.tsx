import { Container } from "@mui/material";
import BottomNavBar from "./BottomNavBar";
import Header from "./Header";

export default function AppWrapper({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <>
      <Header sectionTitle={title} />
      <Container maxWidth="lg" sx={{ minHeight: "calc(100dvh - 120px)" }}>
        {children}
      </Container>
      <BottomNavBar />
    </>
  );
}
