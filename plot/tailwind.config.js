const plugin = require('tailwindcss/plugin')

module.exports = {
    content: ["./templates/*.{html,js}"],
    theme: {
      extend: {},
    },
    plugins: [
      plugin(function({ addBase, theme }) {
        addBase({
          'h1': { fontSize: theme('fontSize.2xl') },
          'h2': { fontSize: theme('fontSize.xl') },
          'h3': { fontSize: theme('fontSize.lg') },
        })
      })
    ]
}