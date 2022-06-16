const express = require('express');
const app = express();

const bodyParser = require('body-parser');

const client_info = require('./client_info.json');

app.use(bodyParser.json());


const DOMAIN = client_info.domain;

const { auth } = require('express-openid-connect');

const config = {
    authRequired: false,
    auth0Logout: true,
    baseURL: 'https://cs493-project-351300.wn.r.appspot.com',
    clientID: client_info.client_id,
    issuerBaseURL: 'https://' + DOMAIN,
    secret: client_info.client_secret
};

app.use(auth(config));

app.set('views', './views');
app.set('view engine', 'pug');


app.enable('trust proxy');
app.use('/', require('./routes/index'));
app.use('/users', require('./routes/users'));
app.use('/boats', require('./routes/boats'));
app.use('/loads', require('./routes/loads'));

// Listen to the App Engine-specified port, or 8080 otherwise.
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});