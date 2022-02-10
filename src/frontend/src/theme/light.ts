import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
    palette: {
        primary: {
            main: '#005ea2',
            light: '#73b3e7',
            dark: '#1a4480',
        },
        secondary: {
            main: '#d83933',
            light: '#f2938c',
            dark: '#b50909',
        },
        background: {
            paper: '#fcfcfc',
            default: '#fcfcfc',
        },
        text: {
            primary: '#1b1b1b',
            secondary: '#171717',
            disabled: '#454545',
        },
        error: {
            main: '#e52207',
        },
        success: {
            main: '#7d9b4e',
            light: '#b8d293',
            dark: '#4c6424',
        },
        info: {
            main: '#59b9de',
        },
    },
    typography: {
        fontFamily: 'PublicSans',
    },
});