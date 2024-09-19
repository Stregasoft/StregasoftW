const path = require('path');
const PurgeCSSPlugin = require('purgecss-webpack-plugin');
const glob = require('glob-all');

module.exports = {
  entry: './src/index.js', // Ajusta esto a tu archivo de entrada principal
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  plugins: [
    new PurgeCSSPlugin({
      paths: glob.sync([
        path.join(__dirname, '**/*.html'),
        path.join(__dirname, '**/*.js'),
        // Agrega más rutas si es necesario
      ], { nodir: true }),
      safelist: [], // Opcional: puedes añadir clases CSS que quieras preservar
    }),
  ],
};
