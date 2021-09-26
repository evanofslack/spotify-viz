import React from "react";
import { Button } from "@chakra-ui/react";

function LoginButton() {
    async function getRedirect() {
        await fetch("/login").then((response) =>
            response.json().then((data) => {
                window.location.href = data.url;
            })
        );
    }

    return (
        <Button
            bg="#1db954"
            color="white"
            borderRadius="80px"
            margin={16}
            maxWidth={80}
            fontWeight="600"
            fontSize="16"
            onClick={() => getRedirect()}
        >
            CONNECT WITH SPOTIFY
        </Button>
    );
}

export default LoginButton;
