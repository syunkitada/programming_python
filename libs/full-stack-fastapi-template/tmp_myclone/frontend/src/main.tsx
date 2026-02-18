import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";

import { client } from "./client/sdk.gen";

client.setConfig({
  baseURL: import.meta.env.VITE_API_URL,
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
