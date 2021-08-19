import React from "react";
import { ChakraProvider, Flex } from "@chakra-ui/react";

import { ColorModeSwitcher } from "./ColorModeSwitcher";
import LoginButton from "./LoginButton";
import LoginBlurb from "./LoginBlurb";
import theme from ".././themes/theme";

function Home() {
    return (
        <ChakraProvider theme={theme}>
            <Flex direction="column" justify="center" align="center">
                <ColorModeSwitcher justifySelf="flex-end" />
                <LoginBlurb />
                <LoginButton />
            </Flex>
        </ChakraProvider>
    );
}

export default Home;
