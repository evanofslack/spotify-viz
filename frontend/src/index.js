import { ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import React, { StrictMode } from "react";
import ReactDOM from "react-dom";
import App from "./App";
import theme from "./themes/theme";

ReactDOM.render(
    <StrictMode>
        <ChakraProvider theme={theme}>
            <ColorModeScript />
            <App />
        </ChakraProvider>
    </StrictMode>,
    document.getElementById("root")
);
