import React from "react";
import {
    useColorModeValue,
    Box,
    Stat,
    StatLabel,
    StatNumber,
    StatHelpText,
} from "@chakra-ui/react";

// Spotracks

function CurrentlyListening(props) {
    const subheader = useColorModeValue("grey.900", "gray.100");
    return (
        <Box mt="6">
            <Stat color={subheader}>
                <StatLabel>Currently Listening To</StatLabel>
                <StatNumber>{props.song}</StatNumber>
                <StatHelpText>by {props.artist}</StatHelpText>
            </Stat>
        </Box>
    );
}

export default CurrentlyListening;
