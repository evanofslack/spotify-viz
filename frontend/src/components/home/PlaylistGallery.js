import React from "react";
import { useQuery } from "react-query";
import { Flex, Box, CircularProgress, Heading } from "@chakra-ui/react";
import PlaylistCard from "./PlaylistCard";

function PlaylistGallery() {
    const { isLoading, error, data } = useQuery("playlists", () =>
        fetch("/playlists").then((res) => res.json())
    );

    if (isLoading) return <CircularProgress isIndeterminate color="green.300" />;

    if (error) return "An error has occurred: " + error.message;

    return (
        <Flex align="center" justify="center" direction="column">
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
                    Your mixes
                </Heading>

                {data.map((playlist, index) => {
                    return (
                        <PlaylistCard
                            key={index}
                            playlist_name={playlist.playlist_name}
                            playlist_cover_image={playlist.playlist_cover_image}
                        />
                    );
                })}
            </Box>
        </Flex>
    );
}

export default PlaylistGallery;
