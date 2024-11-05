/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./application/**/*.{html,js}", "./components/**/*.{html,js,jinja}"],
  safelist: [
    // Background colors for violet, indigo, green, yellow, and red
    {
      pattern: /bg-(violet|indigo|green|yellow|red)-(.*)/,
      variants: ['hover']
    },

    // Border colors for violet, indigo, green, yellow, and red
    {
      pattern: /border-(violet|indigo|green|yellow|red)-(.*)/,
    },

    // Specific flash classes
    'flash-success',
    'flash-danger',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'hero-pattern': "url('/static/img/bg.jpg')",
      }
    }
  },
  plugins: [],
}

