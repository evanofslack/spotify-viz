import React from "react";
import { useColorModeValue, Box, Heading } from "@chakra-ui/react";

// Spotracks

function LoginBlurb() {
    const header = useColorModeValue("gray.700", "green.400");
    const subheader = useColorModeValue("teal.600", "#abb2bf");
    return (
        <Box mt="55" mb="10" textAlign="center">
            <Heading fontWeight="200" color={header} fontSize="40px">
                Welcome to
            </Heading>
            <Heading fontWeight="600" color={header} fontSize="80px">
                Mixtake
            </Heading>

            <Box mt="6">
                <Heading color={subheader} fontWeight="300" fontSize="18px">
                    See listening trends from the past <br />
                    and discover new tracks for the future
                </Heading>
            </Box>
        </Box>
    );
}

export default LoginBlurb;
