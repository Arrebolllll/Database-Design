const NodePolyfillPlugin = require('node-polyfill-webpack-plugin')



configureWebpack: (config) => {
  const plugins = []
  plugins.push(new NodePolyfillPlugin())
  externals: {
    fs: require('fs')
  }
}

const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true,
//   lintOnSave: false
// })
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  configureWebpack: {
    plugins: [new NodePolyfillPlugin()]
  },
  devServer: {
    host: '0.0.0.0',
    // https:true,
    port: 8080,
    client: {
      webSocketURL: 'ws://0.0.0.0:8080/ws',
    },
    headers: {
      'Access-Control-Allow-Origin': '*',
    }
  },
})
