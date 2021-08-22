import React from "react";
import { Flex } from "@chakra-ui/react";
import NavBar from "./NavBar";
import LoginButton from "./LoginButton";
import LoginBlurb from "./LoginBlurb";

function Home() {
    return (
        <Flex direction="column" justify="center" align="center">
            <NavBar />
            <LoginBlurb />
            <LoginButton />
        </Flex>
    );
}

export default Home;
