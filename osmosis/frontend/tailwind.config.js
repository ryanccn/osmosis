/* eslint-env node */

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx,vue}", "./index.html"],
  theme: {
    extend: {
      colors: {
        fg: "rgba(var(--fg-color) / <alpha-value>)",
        bg: "rgba(var(--bg-color) / <alpha-value>)",
        surface: "rgba(var(--surface-color) / <alpha-value>)",
        "surface-hover": "rgba(var(--surface-color-hover) / <alpha-value>)",
        accent: "rgba(var(--accent-color) / <alpha-value>)",
        "accent-hover": "rgba(var(--accent-color-hover) / <alpha-value>)",
      },
    },
  },
  plugins: [],
};
