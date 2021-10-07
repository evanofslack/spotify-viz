import React from "react";
import { HStack, Box } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Icon } from "@chakra-ui/react";
import { RiNeteaseCloudMusicLine } from "react-icons/ri";

function NavBar() {
    return (
        <HStack
            px="2"
            pt="1"
            background=""
            width="100%"
            flexDirection="row"
            justify="space-between"
        >
            <Box fontWeight="600">
                <Icon as={RiNeteaseCloudMusicLine} w={6} h={6} />
                &nbsp;mixtake
            </Box>
            <ColorModeSwitcher />
        </HStack>
    );
}

export default NavBar;
