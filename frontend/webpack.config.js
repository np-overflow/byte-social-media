module.exports = {
    context: __dirname,
    entry: './src/client.js',
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-react', '@babel/preset-env'],
                    plugins: [
                        '@babel/plugin-syntax-dynamic-import',
                        'react-css-modules'
                    ]
                }
            },
            {
                test: /\.css$/,
                exclude: /node_modules/,
                use: ['style-loader', 'css-loader?modules']
            }
        ]
    },
    output: {
        path: __dirname + '/assets/js/',
        publicPath: '/assets/js/',
        filename: 'client.min.js'
    }
}