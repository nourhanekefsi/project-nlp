/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      keyframes: {
        scroll: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
      },
      animation: {
        scroll: "scroll 30s linear infinite",
      },
    },
    colors: {
      cream: "#F4F2E9",
      white:"#ffffff",
      green:"#C6E1C5",
      Green:"#1A8917",
      lightGreen : "#26B922",
      yellow: {
        200: "#F3EFDA",
      },
    }
  },
  plugins: [],
};
