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
            bg: mode("#f5f5f5", "#212022")(props), // atom_grey#282c34 # 25272B
        },
    }),
};

const theme = extendTheme({
    styles,
});

export default theme;
