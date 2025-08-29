/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../**/templates/**/*.html',  // Scan all app templates
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',  // Custom blue for buttons
        secondary: '#6b7280',  // Gray for text
      },
    },
  },
  plugins: [],
}