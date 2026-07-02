/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        medical: {
          blue: "#2563EB",
          ink: "#111827",
          mist: "#F3F4F6"
        }
      }
    }
  },
  plugins: []
};
