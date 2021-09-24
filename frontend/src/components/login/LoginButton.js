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
            margin={16}
            maxWidth={80}
            fontWeight="600"
            fontSize="22"
            onClick={() => getRedirect()}
        >
            Log In with Spotify
        </Button>
    );
}

export default LoginButton;
