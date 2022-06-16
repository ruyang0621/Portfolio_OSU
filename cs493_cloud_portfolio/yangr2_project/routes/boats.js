var router = require('express').Router();

const {Datastore} = require('@google-cloud/datastore');
const datastore = new Datastore();

const jwt = require('express-jwt');
const jwksRsa = require('jwks-rsa');
const client_info = require('../client_info.json');

const BOAT = "Boat";
const LOAD = "Load";
const USER = "User";
const DOMAIN = client_info.domain;

const checkJwt = jwt({
    secret: jwksRsa.expressJwtSecret({
      cache: true,
      rateLimit: true,
      jwksRequestsPerMinute: 5,
      jwksUri: `https://${DOMAIN}/.well-known/jwks.json`
    }),
  
    // Validate the audience and the issuer.
    issuer: `https://${DOMAIN}/`,
    algorithms: ['RS256']
});

function fromDatastore(item){
    item.id = item[Datastore.KEY].id;
    return item;
}


/* ------------- Begin boat Model Functions ------------- */
// Get a user by user_id.
function get_user(userId) {
    const query = datastore.createQuery(USER).filter('user', '=', userId);
    return datastore.runQuery(query).then(entity => {
        if (entity[0].length == 0) {
            // No entity found. Don't try to add the id attribute
            return entity;
        } else {
            return entity[0].map(fromDatastore);
        }
    });
}


// Verify input values.
 async function boat_vali(requestBody, boatId = null) {
    const name = requestBody.name, type = requestBody.type, length = requestBody.length;
    const q = datastore.createQuery(BOAT).filter('name', '=', name);
    const result = await datastore.runQuery(q).then(entity => {
        // If if the name already existed.
        const obj = entity[0].map(fromDatastore);
        if (obj[0] && obj[0].id != boatId) {
            return "duplication";
        } else {
            // Check the length of the name and type.
            if (name.length > 33 || name.length == 0 || type.length == 0 || type.length > 45) {
                return false;
            }
            // Check if the name or type contain any invalid character.
            if (!(/^[A-Za-z ]*$/.test(name)) || !(/^[A-Za-z ]*$/.test(type))) {
                return false;
            }
            // Check if the name or type start or end with space.
            if (name[0] == ' ' || name[name.length - 1] == ' ' || type[0] == ' ' || type[type.length - 1] == ' ') {
                return false;
            }
            // Check if the length is a number and less or equal to 1504.
            if ((typeof length) != "number" || length > 1504 || length <= 0) {
                return false;
            }
            return true;
        }
    });
    return result;
}


// Add a boat.
function post_boat(req) {
    const key = datastore.key(BOAT);
    const new_boat = { "name": req.body.name, "type": req.body.type, 
                       "length": req.body.length, "owner": req.user.sub, 
                       "loads": [], "self": null };
    // Create a new boat in the datastore.
    return datastore.save({ "key": key, "data": new_boat }).then(() => { 
        const self = req.protocol + "://" + req.get("host") + req.baseUrl + "/" + key.id;
        const new_boat_url = { "name": req.body.name, "type": req.body.type, 
                               "length": req.body.length, "owner": req.user.sub, 
                               "loads": [], "self": self };
        // update the self porperty.
        return datastore.save({ "key": key, "data": new_boat_url }).then(() => {
            return { "key": key, "data": new_boat_url };
        });
    });
}


// Get all boats by user_id.
async function get_all_boats_by_owner(req) {
    // Check how many boats in the boat collection.
    const q1 = datastore.createQuery(BOAT).filter('owner', '=', req.user.sub);
    let all_entities = await datastore.runQuery(q1);
    const results = {"total": all_entities[0].length};

    // Get all boats with pagination
    let q2 = datastore.createQuery(BOAT).filter('owner', '=', req.user.sub).limit(5);
    if(Object.keys(req.query).includes("cursor")) {
        q2 = q2.start(req.query.cursor);
    }
    return datastore.runQuery(q2).then(boats => {
        let boats_list = boats[0].map(fromDatastore);
        for (let i = 0; i < boats_list.length; i++) {
            boats_list[i].id = parseInt(boats_list[i].id, 10);
        }
        results.boats = boats_list
        if (boats[1].moreResults !== Datastore.NO_MORE_RESULTS) {
            results.next = req.protocol + "://" + req.get("host") + req.baseUrl + "?cursor=" + boats[1].endCursor;
        }
        return results;
    })
}


// Get a boat by id.
function get_boat(boatId){
    const key = datastore.key([BOAT, boatId]);
    return datastore.get(key).then(boat => {
        if (boat[0] === undefined || boat[0] === null) {
            return boat;
        } else {
            return boat.map(fromDatastore);
        }
    })
}


// The function is used to update a boat by PUT.
function update_boat(newBoat, id, oldBoat) {
    const key = datastore.key([BOAT, parseInt(id, 10)]);
    const new_boat = { "name": newBoat.name, "type": newBoat.type, 
                       "length": newBoat.length, "owner": oldBoat.owner, 
                       "loads": [], "self": oldBoat.self };
    return datastore.save({ "key": key, "data": new_boat }).then(() => { return { "key": key, "data": new_boat } });
}


// Delete a boat.
function delete_boat(boatId) {
    const key = datastore.key([BOAT, parseInt(boatId, 10)]);
    return datastore.delete(key);
}


// The function is used to get a load by id. 
function get_load(loadId) {
    const key = datastore.key([LOAD, loadId]);
    return datastore.get(key).then(load => {
        if (load[0] === undefined || load[0] === null) {
            return load;
        } else {
            return load.map(fromDatastore);
        }
    })
}


// The function is used to assign a load to a boat.
function assign_load(boat_obj, load_obj) {
    const boat_key = datastore.key([BOAT, parseInt(boat_obj.id)]);
    boat_obj.loads.push({"id": parseInt(load_obj.id), "self": load_obj.self});
    const updated_boat = { "name": boat_obj.name, 
                           "type": boat_obj.type, 
                           "length": boat_obj.length,
                           "owner":  boat_obj.owner,
                           "loads": boat_obj.loads,
                           "self": boat_obj.self 
                        };
    return datastore.save({ "key": boat_key, "data": updated_boat }); 
}


// The function is used to assign a carrier to a load.
function assign_carrier(boat_obj, load_obj) {
    const load_key = datastore.key([LOAD, parseInt(load_obj.id)]);
    const updated_load = { "volume": load_obj.volume, 
                           "weight": load_obj.weight, 
                           "carrier": {"id": parseInt(boat_obj.id), "name": boat_obj.name, "self": boat_obj.self}, 
                           "item": load_obj.item, 
                           "self": load_obj.self };
    return datastore.save({ "key": load_key, "data": updated_load });
}


// The function is used to remove a load to a boat.
function remove_load(boat_obj, load_obj) {
    const boat_key = datastore.key([BOAT, parseInt(boat_obj.id)]);
    const index = boat_obj.loads.indexOf({"id": parseInt(load_obj.id), "self": load_obj.self});
    boat_obj.loads.splice(index, 1);
    const updated_boat = { "name": boat_obj.name, 
                           "type": boat_obj.type, 
                           "length": boat_obj.length,
                           "owner":  boat_obj.owner,
                           "loads": boat_obj.loads,
                           "self": boat_obj.self 
                        };
    return datastore.save({ "key": boat_key, "data": updated_boat }); 
    
}


// The function is used to remove a carrier from a load.
function remove_carrier(load_obj) {
    const load_key = datastore.key([LOAD, parseInt(load_obj.id)]);
    const updated_load = { "volume": load_obj.volume, 
                           "weight": load_obj.weight, 
                           "carrier": null, 
                           "item": load_obj.item, 
                           "self": load_obj.self };
    return datastore.save({ "key": load_key, "data": updated_load });
}


// Remove all loads from a boat.
async function remove_all_load(boat_obj) {
    for (const load_on_boat of boat_obj.loads) {
        await get_load(load_on_boat.id).then(load => {
            return remove_carrier(load[0]);
        });
    }
    const boat_key = datastore.key([BOAT, parseInt(boat_obj.id)]);
    const updated_boat = { "name": boat_obj.name, 
                           "type": boat_obj.type, 
                           "length": boat_obj.length,
                           "owner":  boat_obj.owner,
                           "loads": [],
                           "self": boat_obj.self 
                        };
    return datastore.save({ "key": boat_key, "data": updated_boat }); 
}
/* ------------- End boat Model Functions ------------- */


/* ------------- Begin Controller Functions ------------- */
// Create a boat.
router.post('/', checkJwt, function(err, req, res, next) {
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        // Check if the user exist.
        const user = await get_user(req.user.sub);
        if (user[0] === undefined || user[0] === null) {
            res.status(403).json({"Error": "The user is not a registered user for this app."});
        } else {
            // A middleware to post a boat data into database.
            const accepts = req.accepts('application/json');
            if (!accepts) {
                // The endpoint cannot offers a MIME type required by the user.
                res.status(406).json({"Error": "The server only returns application/json data."});
            } else if (req.get('content-type') !== 'application/json') {
                // The user sends an unsupported MIME type to the endpoint.
                res.status(415).json({"Error": "The server only accepts application/json data."})
            } else {
                if (Object.keys(req.body).length > 3) {
                    // If user provids attributes more than required.
                    res.status(400).json({ "Error": "The attributes in the request object is more than required." });
                } else if(!req.body.name || !req.body.type || !req.body.length) {
                    // If request body is invalid.
                    res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
                } else {
                    const result = await boat_vali(req.body);
                    if (result == "duplication") {
                        // If the name already exist in the database.
                        res.status(403).json({ "Error": "The name attribute in the request object has existed in the datastore."});
                    } else if (!result) {
                        // If the inputs' value in request body is invlid.
                        res.status(400).json({ "Error": "At least one of the attributes in request object is invalid."});
                    } else {
                        post_boat(req)
                        .then(obj => {
                            res.location(obj.data.self);
                            res.status(201).json({
                                id : parseInt(obj.key.id, 10),
                                name : obj.data.name,
                                type : obj.data.type,
                                length : obj.data.length,
                                owner : obj.data.owner,
                                loads : obj.data.loads,
                                self : obj.data.self
                            })
                        })
                    }
                }
            }
        }
});


// Get all boat of current user.
router.get('/', checkJwt, function(err, req, res, next) {
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, (req, res) => {
        const accepts = req.accepts('application/json');
        if (!accepts) {
            // The endpoint cannot offers a MIME type required by the user.
            res.status(406).json({"Error": "The server only returns application/json data."});
        } else {
            get_all_boats_by_owner(req)
            .then(boats => {
                res.status(200).json(boats);
            });
        }
});


// let "/boats" reject DELETE method 
router.delete('/', function (req, res) {
    res.set('Allow', 'GET', 'POST');
    res.status(405).json({ "Error": "This endpoint only allows GET & POST method."});
});

// let "/boats" reject PUT method 
router.put('/', function (req, res) {
    res.set('Allow', 'GET', 'POST');
    res.status(405).json({ "Error": "This endpoint only allows GET & POST method."});
});


// let "/boats" reject PATCH method 
router.patch('/', function (req, res) {
    res.set('Allow', 'GET', 'POST');
    res.status(405).json({ "Error": "This endpoint only allows GET & POST method."});
});


// Get a boat by boat id.
router.get('/:boat_id', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, (req, res) => {
        const accepts = req.accepts('application/json');
        if (!accepts) {
            // The endpoint cannot offers a MIME type required by the user.
            res.status(406).json({"Error": "The server only returns application/json data."});
        } else {
            const parsed = parseInt(req.params.boat_id, 10);
            if (isNaN(parsed) || parsed === 0) {
                res.status(404).json({'Error': 'No boat with this boat_id exists.'})
            } else {
                get_boat(parsed).then(boat => {
                    if (boat[0] === undefined || boat[0] === null) {
                        // If the boat with boat id is not found.
                        res.status(404).json({ 'Error': 'No boat with this boat_id exists' });
                    } else {
                        if (boat[0].owner != req.user.sub) {
                            res.status(403).json({ 'Error': 'The user does not have permission to view this boat info.' });
                        } else {
                            boat[0].id = parseInt(boat[0].id);
                            res.status(200).json(boat[0]);
                        }
                    }
                })
            }
        }
})


// Edit a boat by put.
router.put('/:boat_id', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        const accepts = req.accepts('application/json');
        if (!accepts) {
            // The endpoint cannot offers a MIME type required by the user.
            res.status(406).json({"Error": "The server only returns application/json data."});
        } else if (req.get('content-type') !== 'application/json') {
            // The user sends an unsupported MIME type to the endpoint.
            res.status(415).json({"Error": "The server only accepts application/json data."})
        } else {
            if (Object.keys(req.body).length > 3) {
                // If user provids attributes more than required.
                res.status(400).json({ "Error": "The attributes in the request object is more than required." });
            } else if(!req.body.name || !req.body.type || !req.body.length) {
                // If request body is invalid.
                res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
            } else {
                const parsed = parseInt(req.params.boat_id, 10);
                if (isNaN(parsed) || parsed === 0) {
                    res.status(404).json({'Error': 'No boat with this boat_id exists.'})
                } else {
                    const result = await boat_vali(req.body, req.params.boat_id);
                    if (result == "duplication") {
                        // If the name already exist in the database.
                        res.status(403).json({ "Error": "The name attribute in the request object has existed in the datastore."});
                    } else if (!result) {
                        // If the inputs' value in request body is invlid.
                        res.status(400).json({ "Error": "At least one of the attributes in request object is invalid."});
                    } else {
                        const old_boat = await get_boat(parsed);
                        // If invalid id.
                        if (old_boat[0] === undefined || old_boat[0] === null) {
                            res.status(404).json({"Error": "No boat with this boat_id exists."});
                        } else {
                            // If the boat is not own by the current user.
                            if (old_boat[0].owner != req.user.sub) {
                                res.status(403).json({ 'Error': 'The user does not have permission to update the boat.' });
                            } else if (old_boat[0].loads.length != 0 ) {
                                // The boat has been loaded.
                                res.status(403).
                                json({"Error": "The boat has been loaded. Please unload all loads before updating."});
                            } else {
                                update_boat(req.body, req.params.boat_id, old_boat[0])
                                .then(obj => {
                                    res.status(200).json({
                                        id : parseInt(obj.key.id, 10),
                                        name : obj.data.name,
                                        type : obj.data.type,
                                        length : obj.data.length,
                                        owner : obj.data.owner,
                                        loads : obj.data.loads,
                                        self : obj.data.self
                                    })
                                })
                            }
                        }
                    }
                }
            }
        }
})


// Edit a boat by patch.
router.patch('/:boat_id', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        const accepts = req.accepts('application/json');
        if (!accepts) {
            // The endpoint cannot offers a MIME type required by the user.
            res.status(406).json({"Error": "The server only returns application/json data."});
        } else if (req.get('content-type') !== 'application/json') {
            // The user sends an unsupported MIME type to the endpoint.
            res.status(415).json({"Error": "The server only accepts application/json data."})
        } else {
            if (Object.keys(req.body).length > 3) {
                // If user provids attributes more than required.
                res.status(400).json({ "Error": "The attributes in the request object is more than required." });
            } else {
                let new_boat = {};
                const properties = ['name', 'type', 'length']
                for (const property in req.body) {
                    if (!properties.includes(property)) {
                        // The property not in the data model.
                        res.status(400).json({ "Error": "At least one of the attributes in request object is invalid." });
                        return;
                    } else {
                        new_boat[property] = req.body[property];
                    }
                }
                const parsed = parseInt(req.params.boat_id, 10);
                if (isNaN(parsed) || parsed === 0) {
                    res.status(404).json({'Error': 'No boat with this boat_id exists.'})
                } else {
                    const old_boat = await get_boat(parsed);
                    // If invalid id.
                    if (old_boat[0] === undefined || old_boat[0] === null) {
                        res.status(404).json({"Error": "No boat with this boat_id exists."});
                    } else {
                        // If the boat is not own by the current user.
                        if (old_boat[0].owner != req.user.sub) {
                            res.status(403).json({ 'Error': 'The user does not have permission to update the boat.' });
                        } else if (old_boat[0].loads.length != 0 ) {
                            // The boat has been loaded.
                            res.status(403).
                            json({"Error": "The boat has been loaded. Please unload all loads before updating."});
                        } else {
                            for (const property of properties) {
                                if (!Object.keys(new_boat).includes(property)) {
                                    new_boat[property] = old_boat[0][property]
                                }
                            }
                            const result = await boat_vali(new_boat, req.params.boat_id);
                            if (result == "duplication") {
                                // If the name already exist in the database.
                                res.status(403).json({ "Error": "The name attribute in the request object has existed in the datastore."});
                            } else if (!result) {
                                // If the inputs' value in request body is invlid.
                                res.status(400).json({ "Error": "At least one of the attributes in request object is invalid."});
                            } else {
                                update_boat(new_boat, req.params.boat_id, old_boat[0])
                                .then(obj => {
                                    res.status(200).json({
                                        id : parseInt(obj.key.id, 10),
                                        name : obj.data.name,
                                        type : obj.data.type,
                                        length : obj.data.length,
                                        owner : obj.data.owner,
                                        loads : obj.data.loads,
                                        self : obj.data.self
                                    })
                                })
                            }
                        }                        
                    }
                }
            }
        }
})


// Delete a boat by id.
router.delete('/:boat_id', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        const parsed = parseInt(req.params.boat_id, 10);
        if (isNaN(parsed) || parsed === 0) {
            res.status(404).json({ 'Error': 'No boat with this boat_id exists' });
        } else {
            get_boat(parsed)
            .then(boat => {
                // If invalid id.

                if (boat[0] === undefined || boat[0] === null) {
                    res.status(404).json({"Error": "No boat with this boat_id exists."});
                } else {
                    // If the boat is not own by the current user.
                    if (boat[0].owner != req.user.sub) {
                        res.status(403).json({ 'Error': 'The user does not have permission to delete the boat.' });
                    } else if (boat[0].loads.length != 0 ) {
                        // The boat has been loaded.
                        res.status(403).
                        json({"Error": "The boat has been loaded. Please unload all loads before deleting."});
                    } else {
                        delete_boat(req.params.boat_id).then(res.status(204).end()); 
                    }
                }
            })
        }
})


// let "/boats/:boat_id" reject POST method 
router.post('/:boat_id', function (req, res) {
    res.set('Allow', 'GET', 'PUT', 'PATCH', 'DELETE');
    res.status(405).json({ "Error": "This endpoint does not allow the POST method."});
});


// Assign a load to a boat
router.put('/:boat_id/loads/:load_id', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        const parsedBoatId = parseInt(req.params.boat_id, 10);
        if (isNaN(parsedBoatId) || parsedBoatId === 0) {
            res.status(404).json({ 'Error': 'The specified boat and/or load does not exist.' });
        } else {
            const parsedLoadId = parseInt(req.params.load_id, 10);
            if (isNaN(parsedLoadId) || parsedLoadId === 0) {
                res.status(404)
                .json({ 'Error': 'The specified boat and/or load does not exist.' });
            } else {
                get_boat(parsedBoatId)
                .then(boat => {
                    if (boat[0] === undefined || boat[0] === null) {
                        res.status(404).json({"Error": "The specified boat and/or load does not exist."});
                    } else {
                        // If the boat is not own by the current user.
                        if (boat[0].owner != req.user.sub) {
                            res.status(403).json({ 'Error': 'The user does not have permission to assign the load on this boat.' });
                        } else {
                            get_load(parsedLoadId)
                            .then(load => {
                                if (load[0] === undefined || load[0] === null) {
                                    // If the load with load_id is not found.
                                    res.status(404).json({ 'Error': 'The specified boat and/or load does not exist.' });
                                } else {
                                    if (load[0].carrier != null) {
                                        // IF the load has been assigned to a boat.
                                        res.status(403).json({ 'Error': 'The load has been loaded. Please unload it before re-assigning.' });
                                    } else {
                                        assign_load(boat[0], load[0])
                                        .then(assign_carrier(boat[0], load[0]).then(res.status(204).end()));
                                    }
                                }
                            })
                        }
                    }
                })
            }
        }
})


// Remove a load on a boat
router.delete('/:boat_id/loads/:load_id', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        const parsedBoatId = parseInt(req.params.boat_id, 10);
        if (isNaN(parsedBoatId) || parsedBoatId === 0) {
            res.status(404).json({ 'Error': 'The specified boat and/or load does not exist.' });
        } else {
            const parsedLoadId = parseInt(req.params.load_id, 10);
            if (isNaN(parsedLoadId) || parsedLoadId === 0) {
                res.status(404)
                .json({ 'Error': 'The specified boat and/or load does not exist.' });
            } else {
                get_boat(parsedBoatId)
                .then(boat => {
                    if (boat[0] === undefined || boat[0] === null) {
                        res.status(404).json({"Error": "The specified boat and/or load does not exist."});
                    } else {
                        // If the boat is not own by the current user.
                        if (boat[0].owner != req.user.sub) {
                            res.status(403).json({ 'Error': 'The user does not have permission to remove the load from this boat.' });
                        } else {
                            get_load(parsedLoadId)
                            .then(load => {
                                if (load[0] === undefined || load[0] === null) {
                                    // If the load with load_id is not found.
                                    res.status(404).json({ 'Error': 'The specified boat and/or load does not exist.' });
                                } else {
                                    if (!load[0].carrier || load[0].carrier.id != parsedBoatId) {
                                        // IF the load has been assigned to a boat.
                                        res.status(404).json({ 'Error': 'No boat with this boat_id is loaded with the load with this load_id' });
                                    } else {
                                        remove_load(boat[0], load[0])
                                        .then(remove_carrier(load[0]).then(res.status(204).end()));
                                    }
                                }
                            })
                        }
                    }
                })
            }
        }
})


// let "/:boat_id/loads/:load_id" reject PATCH method 
router.patch('/:boat_id/loads/:load_id', function (req, res) {
    res.set('Allow', 'PUT', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows PUT & DELETE method."});
});


// let "/:boat_id/loads/:load_id" reject GET method 
router.get('/:boat_id/loads/:load_id', function (req, res) {
    res.set('Allow', 'PUT', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows PUT & DELETE method."});
});


// let "/:boat_id/loads/:load_id" reject POST method 
router.post('/:boat_id/loads/:load_id', function (req, res) {
    res.set('Allow', 'PUT', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows PUT & DELETE method."});
});


// Remove all load on a boat
router.delete('/:boat_id/loads', checkJwt, function(err, req, res, next){
    // A middleware to handle the unauthorized error.
    if (err.name === "UnauthorizedError") {
        res.status(401).json({'Error': 'Invalid token...'})
    } else next()}, async (req, res) => {
        const parsedBoatId = parseInt(req.params.boat_id, 10);
        if (isNaN(parsedBoatId) || parsedBoatId === 0) {
            res.status(404).json({ 'Error': 'The specified boat does not exist.' });
        } else {
            get_boat(parsedBoatId)
            .then(boat => {
                if (boat[0] === undefined || boat[0] === null) {
                    res.status(404).json({"Error": "The specified boat does not exist."});
                } else {
                    // If the boat is not own by the current user.
                    if (boat[0].owner != req.user.sub) {
                        res.status(403).json({ 'Error': 'The user does not have permission to delete the boat.' });
                    } else {
                        remove_all_load(boat[0]).then(res.status(204).end());
                    }
                }
            })
        }
})


// let "/:boat_id/loads" reject PATCH method 
router.patch('/:boat_id/loads', function (req, res) {
    res.set('Allow', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows DELETE method."});
});


// let "/:boat_id/loads" reject POST method 
router.post('/:boat_id/loads', function (req, res) {
    res.set('Allow', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows DELETE method."});
});


// let "/:boat_id/loads" reject PUT method 
router.put('/:boat_id/loads', function (req, res) {
    res.set('Allow', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows DELETE method."});
});


// let "/:boat_id/loads" reject GET method 
router.get('/:boat_id/loads', function (req, res) {
    res.set('Allow', 'DELETE');
    res.status(405).json({ "Error": "This endpoint only allows DELETE method."});
});
/* ------------- End Controller Functions ------------- */

module.exports = router;