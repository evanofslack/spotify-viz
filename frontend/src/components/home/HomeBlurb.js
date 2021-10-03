import React from "react";
import { useColorModeValue, Box, Heading, Text, Icon, keyframes } from "@chakra-ui/react";
import { BsChevronDoubleDown } from "react-icons/bs";

function LoginBlurb(props) {
    const header = useColorModeValue("blue.800", "#FDD855");
    const subheader = useColorModeValue("teal.600", "#D2D2D2");

    const bounce = keyframes`
    0%,  100% {transform: translateY(0);}
    50% {transform: translateY(-7px);}
  `;

    const bounceAnimation = `${bounce} infinite 3s linear`;

    return (
        <Box>
            <Box mt="36" mb="16" width="100%">
                <Heading align="left" m="6" color={subheader} fontWeight="300" fontSize="26px">
                    Hi
                    <Text as="span" fontWeight="300" color={subheader}>
                        &nbsp;{props.name} <br />
                    </Text>
                </Heading>
                <Heading align="left" m="6" color={subheader} fontWeight="300" fontSize="26px">
                    Let's get your
                    <Text as="span" fontWeight="400" color={header}>
                        &nbsp;mixtake
                    </Text>
                </Heading>
                <Box mt="32" align="center">
                    <Icon as={BsChevronDoubleDown} w={7} h={7} animation={bounceAnimation} />
                </Box>
            </Box>
        </Box>
    );
}

export default LoginBlurb;
