/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    fontFamily: {
      sans: ["var(--font-sans)", "sans-serif"],
      code: ["var(--font-code)", "monospace"],
    },
    colors: {
      transparent: "transparent",
      "ac-1": "#833FFF",
      "ac-2": "#0A9F19",
      "ac-3": "#767676",
      "ac-4": "#D80B30",
      "fg-1": "#EDE3FF",
      "fg-2": "#D9FFDD",
      "fg-3": "#EBEBEB",
      "fg-4": "#FFD9E0",
      "bd-1": "#E3E3E3",
      "ft-1": "#000000",
      "ft-2": "#A0A0A0",
      "bg-1": "#FFFFFF",
      "bg-2": "#F7F7F7",
      "bg-3": "#F5F5F5",
      "bg-lt": "#FAFAFA",
    },
    extend: {
      backgroundImage: {
        "gr-1": "linear-gradient(#8A4EF4, #5100E3)",
      },
      boxShadow: {
        article: "inset 3px 3px 15px rgba(0, 0, 0, 0.03)",
        section: "inset 1px 1px 8px rgba(0, 0, 0, 0.05)",
      },
      animation: {
        "bounce-fast": "bounce 300ms ease-in-out infinite",
        "spin-fast": "spin 300ms ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
