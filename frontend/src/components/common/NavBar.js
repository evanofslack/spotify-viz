import React from "react";
import { Box } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";

function NavBar() {
    return (
        <Box width="100%" textAlign="right">
            <ColorModeSwitcher />
        </Box>
    );
}

export default NavBar;
