import globals from "globals";
import pluginJs from "@eslint/js";


export default [
    {
        ignores: ['!pdf/static/js/**'],
    },
    {
        files: ["pdf/static/js/*.js"],

        languageOptions: {sourceType: "script",globals: {...globals.browser, ...globals.jquery}}
    },
    pluginJs.configs.recommended,
];
