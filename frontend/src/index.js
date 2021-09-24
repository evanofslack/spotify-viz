import { ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import React, { StrictMode } from "react";
import { QueryClient, QueryClientProvider } from "react-query";

import ReactDOM from "react-dom";
import App from "./App";
import theme from "./themes/theme";

const queryClient = new QueryClient();

ReactDOM.render(
    <StrictMode>
        <QueryClientProvider client={queryClient}>
            <ChakraProvider theme={theme}>
                <ColorModeScript />
                <App />
            </ChakraProvider>
        </QueryClientProvider>
    </StrictMode>,
    document.getElementById("root")
);
