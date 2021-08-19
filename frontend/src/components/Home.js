import React, { useState, useEffect } from "react";
import { ChakraProvider, Flex } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import HomeBlurb from "./HomeBlurb";
import CurrentlyListening from "./CurrentlyListing";
import theme from ".././themes/theme";

function Home() {
    const [data, setData] = useState({
        display_name: null,
        current_song: null,
        current_artist: null,
    });

    useEffect(() => {
        fetch("/home").then((response) =>
            response.json().then((data) => {
                setData({
                    display_name: data.display_name,
                    current_song: data.current_song,
                    current_artist: data.current_artist,
                });
            })
        );
    }, []);

    const { display_name, current_song, current_artist } = data;

    return (
        <ChakraProvider theme={theme}>
            <Flex align="center" justify="center" direction="column">
                <ColorModeSwitcher justifySelf="flex-end" />
                <HomeBlurb name={display_name} />
                {current_song && <CurrentlyListening song={current_song} artist={current_artist} />}
            </Flex>
        </ChakraProvider>
    );
}

export default Home;
