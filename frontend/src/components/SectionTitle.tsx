import { Box, Typography } from "@mui/material";

export default function SectionTitle({ title }: { title: string }) {
  return (
    <Box
      sx={{
        px: 2,
        backgroundColor: "secondary.main",
      }}
    >
      <Typography variant="h6" component="h6" sx={{ py: 1, color: "text.primary" }}>
        {title}
      </Typography>
    </Box>
  );
}
