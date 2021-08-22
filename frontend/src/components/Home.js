import React, { useState, useEffect } from "react";
import { Flex, Box } from "@chakra-ui/react";
import NavBar from "./NavBar";
import HomeBlurb from "./HomeBlurb";
import CurrentlyListening from "./CurrentlyListening";
import LastListening from "./LastListening";

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
                    last_song: data.last_song,
                    last_artist: data.last_artist,
                    elapsed: data.elapsed,
                });
            })
        );
    }, []);

    const { display_name, current_song, current_artist, last_song, last_artist, elapsed } = data;

    return (
        <Flex align="center" justify="center" direction="column">
            <NavBar />
            <Box>
                <HomeBlurb name={display_name} />
                {current_song && <CurrentlyListening song={current_song} artist={current_artist} />}
                {!current_song && (
                    <LastListening song={last_song} artist={last_artist} elapsed={elapsed} />
                )}
            </Box>
        </Flex>
    );
}

export default Home;
