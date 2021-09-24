import React from "react";
import {
    useColorModeValue,
    Box,
    Stat,
    StatLabel,
    StatNumber,
    StatHelpText,
} from "@chakra-ui/react";

function LastListening(props) {
    const containerbg = useColorModeValue("#ededed", "#302f32");
    const subheader = useColorModeValue("gray.900", "gray.100");
    return (
        <Box mt="8" p="4" width="100%" bg={containerbg} borderRadius="8">
            <Stat color={subheader}>
                <StatLabel>
                    {props.elapsedTime} {props.timeUnits} ago{" "}
                </StatLabel>
                <StatNumber>{props.song}</StatNumber>
                <StatHelpText>by {props.artist}</StatHelpText>
            </Stat>
        </Box>
    );
}

export default LastListening;