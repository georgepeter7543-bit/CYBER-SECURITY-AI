/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: '#0A0A0C',
        surface: '#101217',
        card: '#161922',
        borderDark: '#1E2330',
        neonGreen: '#00FF66',
        neonBlue: '#00D2FF',
        cyberCyan: '#06B6D4',
        cyberPurple: '#A855F7',
        cyberGold: '#FACC15',
      },
    },
  },
  plugins: [],
}
