import React from "react";
import { useColorModeValue, Box, Heading } from "@chakra-ui/react";

// Spotracks

function LoginBlurb(props) {
    const header = useColorModeValue("blue.800", "green.400");
    const subheader = useColorModeValue("teal.700", "#abb2bf");
    //#302f32
    return (
        <Box>
            <Box width="100%" mt="12" mb="10" textAlign="center">
                <Heading fontWeight="900" color={header} fontSize="52px">
                    Welcome to <br /> SpotViz
                </Heading>
            </Box>

            <Box mt="20" mb="16" width="100%">
                <Heading align="left" m="6" color={subheader} fontWeight="400" fontSize="20px">
                    Hi {props.name} <br />
                    Let's check out your <br />
                    playback history
                </Heading>
            </Box>
        </Box>
    );
}

export default LoginBlurb;
