import { extendTheme } from "@chakra-ui/react";
import { mode } from "@chakra-ui/theme-tools";

const styles = {
    colors: {
        primary: {
            100: "yellow.400",
            200: "green.400",
        },
    },
    global: (props) => ({
        body: {
            color: mode("green.600", "#abb2bf")(props), //LIGHT, DARK
            bg: mode("gray.50", "#282c34")(props),
        },
    }),
};

const theme = extendTheme({
    styles,
});

export default theme;
