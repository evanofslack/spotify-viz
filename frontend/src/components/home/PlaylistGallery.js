import React from "react";
import { useQuery } from "react-query";
import { Flex, Box, Text } from "@chakra-ui/react";
import PlaylistCard from "./PlaylistCard";

function PlaylistGallery() {
    const { isLoading, error, data } = useQuery("playlists", () =>
        fetch("/playlists").then((res) => res.json())
    );

    if (isLoading) return "Loading...";

    if (error) return "An error has occurred: " + error.message;

    return (
        <Flex align="center" justify="center" direction="column">
            <Box>
                <Text fontSize="lg" isTruncated>
                    Your Playlists:
                </Text>

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
