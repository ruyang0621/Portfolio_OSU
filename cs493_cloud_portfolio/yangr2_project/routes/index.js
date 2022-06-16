var router = require('express').Router();
const { requiresAuth } = require('express-openid-connect');

const {Datastore} = require('@google-cloud/datastore');
const datastore = new Datastore();

const USER = "User";

// The function is used to add a new user into datastore. 
async function post_user(user) {
    const res = await existed_user(user.sub);
    if (res === false) {
        const key = datastore.key(USER);
        const new_user = {"user_id": user.sub, "email": user.email};
        await datastore.save({ "key": key, "data": new_user });
    }
}

// The function is used to check if a user is existing in the datastore.
function existed_user(userId) {
    const query = datastore.createQuery(USER).filter('user_id', '=', userId);
    return datastore.runQuery(query).then(user => {
        if (user[0].length == 0){
            return false;
        } else {
            return true;
        }
    })
}


/* ------------- Begin Controller Functions ------------- */
// The route to display the welcome page.
router.get('/', async function(req, res) {
    // Check if a user has logged in or not
    if (req.oidc.isAuthenticated()) {
        await post_user(req.oidc.user);
        res.render("index", {logged_in: true, user_id: req.oidc.user.sub, email: req.oidc.user.email});
    } else {
        res.render("index", {logged_in: false});
    }
});


// The route to display a user info.
router.get('/profile', requiresAuth(), (req, res) => {
    res.render("userInfo", {id_token: req.oidc.idToken, user_id: req.oidc.user.sub, email: req.oidc.user.email});
});
/* ------------- End Controller Functions ------------- */

module.exports = router;