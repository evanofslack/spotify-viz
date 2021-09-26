import React from "react";
import {
    useColorModeValue,
    Image,
    Box,
    Stat,
    StatLabel,
    StatNumber,
    StatHelpText,
    Text,
} from "@chakra-ui/react";

// Spotracks

function CurrentlyListening(props) {
    const containerbg = useColorModeValue("#ededed", "#302f32");
    const subheader = useColorModeValue("gray.900", "gray.100");
    return (
        <Box mt="8" p="4" width="100%" maxWidth="400px" bg={containerbg} borderRadius="8">
            <Stat color={subheader}>
                <StatLabel fontSize="18">Currently listening to: </StatLabel>
                <Box p="3">
                    <Image boxSize="180px" src={props.current_image} alt="Album Cover" />
                </Box>

                <StatNumber fontSize="32">
                    <Text isTruncated>{props.song}</Text>
                </StatNumber>
                <StatHelpText>by {props.artist}</StatHelpText>
            </Stat>
        </Box>
    );
}

export default CurrentlyListening;
