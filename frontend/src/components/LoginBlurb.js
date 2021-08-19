import React from "react";
import { useColorModeValue, Box, Heading } from "@chakra-ui/react";

// Spotracks

function LoginBlurb() {
    const header = useColorModeValue("gray.700", "green.400");
    const subheader = useColorModeValue("teal.600", "#abb2bf");
    return (
        <Box mt="40" mb="10" textAlign="center">
            <Heading fontWeight="900" color={header} fontSize="36px">
                Visualize Your Tracks
            </Heading>

            <Box mt="6">
                <Heading color={subheader} fontWeight="400" fontSize="20px">
                    See listening trends from the past <br />
                    and discover new tracks for the future
                </Heading>
            </Box>
        </Box>
    );
}

export default LoginBlurb;
