var router = require('express').Router();

const {Datastore} = require('@google-cloud/datastore');
const datastore = new Datastore();

const USER = "User";

function fromDatastore(item){
    item.id = item[Datastore.KEY].id;
    return item;
}

// Get all users from datastore.
function get_users() {
    const query = datastore.createQuery(USER);
    return datastore.runQuery(query).then(entities => {
        let users_list = entities[0].map(fromDatastore);
        for (let i = 0; i < users_list.length; i++) {
            users_list[i].id = parseInt(users_list[i].id, 10);
        }
        return users_list;
    });
}

/* ------------- Begin Controller Functions ------------- */
// let "/users" reject DELETE method 
router.delete('/', function (req, res) {
    res.set('Allow', 'GET');
    res.status(405).json({ "Error": "This endpoint only allows GET method."});
});

// let "/users" reject POST method 
router.post('/', function (req, res) {
    res.set('Allow', 'GET');
    res.status(405).json({ "Error": "This endpoint only allows GET method."});
});

// let "/users" reject PUT method 
router.put('/', function (req, res) {
    res.set('Allow', 'GET');
    res.status(405).json({ "Error": "This endpoint only allows GET method."});
});

// let "/users" reject PATCH method 
router.patch('/', function (req, res) {
    res.set('Allow', 'GET');
    res.status(405).json({ "Error": "This endpoint only allows GET method."});
});

// Get all users.
router.get('/', async function(req, res) {
    const accepts = req.accepts('application/json')
    if (!accepts) {
        // The endpoint cannot offers a MIME type required by the user.
        res.status(406).json({"Error": "The server only returns application/json data."})
    } else {
        get_users()
        .then(users => {
            res.status(200).json(users);
        })
    }
});
/* ------------- End Controller Functions ------------- */

module.exports = router;