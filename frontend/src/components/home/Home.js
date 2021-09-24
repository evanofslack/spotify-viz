import React from "react";
import { useQuery } from "react-query";
import { Flex, Box } from "@chakra-ui/react";
import NavBar from "../common/NavBar";
import HomeBlurb from "./HomeBlurb";
import CurrentlyListening from "./CurrentlyListening";
import LastListening from "./LastListening";

function Home() {
    const { isLoading, error, data } = useQuery("repoData", () =>
        fetch("/overview").then((res) => res.json())
    );

    if (isLoading) return "Loading...";

    if (error) return "An error has occurred: " + error.message;

    return (
        <Flex align="center" justify="center" direction="column">
            <NavBar />
            <Box m="10">
                <HomeBlurb name={data.display_name} />
                {data.current_song && (
                    <CurrentlyListening song={data.current_song} artist={data.current_artist} />
                )}
                {!data.current_song && (
                    <LastListening
                        song={data.last_song}
                        artist={data.last_artist}
                        elapsedTime={data.elapsed_time}
                        timeUnits={data.time_units}
                    />
                )}
            </Box>
        </Flex>
    );
}

export default Home;
