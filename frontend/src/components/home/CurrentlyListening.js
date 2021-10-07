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
    Heading,
    Flex,
} from "@chakra-ui/react";

// Spotracks

function CurrentlyListening(props) {
    const containerbg = useColorModeValue("#ededed", "#302f32");
    const subheader = useColorModeValue("gray.900", "#D2D2D2");
    return (
        <Box>
            <Heading
                display="inline-block"
                align="left"
                mt="20"
                ml="2"
                color="#D2D2D2"
                fontWeight="300"
                fontSize="22px"
                borderBottom="1px solid #D2D2D2"
                paddingBottom="2px"
            >
                Your current jam
            </Heading>
            <Box mt="8" p="4" width="100%" maxWidth="325px" bg={containerbg} borderRadius="8">
                <Stat color={subheader}>
                    <StatLabel>Now playing: </StatLabel>
                    <Flex align="center" justify="center" p="3">
                        <Image boxSize="200px" src={props.current_image} alt="Album Cover" />
                    </Flex>

                    <StatNumber>
                        <Text color="white" isTruncated>
                            {props.song}
                        </Text>
                    </StatNumber>
                    <StatHelpText>by {props.artist}</StatHelpText>
                </Stat>
            </Box>
        </Box>
    );
}

export default CurrentlyListening;
