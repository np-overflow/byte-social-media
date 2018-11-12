module.exports = {
    context: __dirname,
    entry: {
        main: './src/client.js',
        admin: './src/admin.js',
    },
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
        filename: '[name].min.js'
    }
}