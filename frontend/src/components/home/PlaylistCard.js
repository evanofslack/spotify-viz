import React from "react";
import { Flex, Box, useColorModeValue, Image, Text } from "@chakra-ui/react";

function PlaylistCard(props) {
    const containerbg = useColorModeValue("#ededed", "#302f32");
    const subheader = useColorModeValue("gray.900", "gray.100");

    return (
        <Flex align="center" justify="center" direction="column">
            <Box m="4" p="4" width="100%" bg={containerbg} borderRadius="8">
                <Box m="3">
                    <Image boxSize="300px" src={props.playlist_cover_image} alt="Album Cover" />
                </Box>
                <Text color="white" fontSize="md" isTruncated>
                    {props.playlist_name}
                </Text>
            </Box>
        </Flex>
    );
}

export default PlaylistCard;

<Box boxSize="sm">
    <Image src="https://bit.ly/sage-adebayo" alt="Segun Adebayo" />
</Box>;
