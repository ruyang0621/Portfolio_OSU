var router = require('express').Router();

const {Datastore} = require('@google-cloud/datastore');
const datastore = new Datastore();

const LOAD = "Load";

function fromDatastore(item){
    item.id = item[Datastore.KEY].id;
    return item;
}


/* ------------- Begin load Model Functions ------------- */
//Verify the input load values.
function load_vali(requestBody) {
    const volume = requestBody.volume, weight = requestBody.weight, item = requestBody.item;
    // Check if the volume is valid.
    if ((typeof volume) != "number" || volume > 93000 || volume <= 0) {
        return false;
    }
    // Check if the weight is valid
    if ((typeof weight) != "number" || weight > 4600 || weight <= 0) {
        return false;
    }
    // Check if the item contain any invalid character.
    if (!(/^[A-Za-z ]*$/.test(item))) {
        return false;
    }
    // Check if the length of the item is invalid.
    if (item.length > 55 || item.length == 0) {
        return false;
    }
    // Check if the item start or end with space.
    if (item[0] == ' ' || item[item.length - 1] == ' ') {
        return false;
    }
    return true;
}


// The function is used to add a load to datastore.
function post_load(req) {
    const key = datastore.key(LOAD);
    const new_load = {"volume": req.body.volume, "weight": req.body.weight, 
                      "item": req.body.item, "carrier": null, "self": null};
    // Create a new load in the datastore.
    return datastore.save({ "key": key, "data": new_load }).then(() => {
        const self = req.protocol + "://" + req.get("host") + req.baseUrl + "/" + key.id;
        const new_load_url = {"volume": req.body.volume, "weight": req.body.weight, 
                              "item": req.body.item, "carrier": null, "self": self};
        // update the self porperty.
        return datastore.save({ "key": key, "data": new_load_url }).then(() => {
            return { "key": key, "data": new_load_url };
        });
    })
}


// The function is used to get a load by id. 
function get_load(id) {
    const key = datastore.key([LOAD, parseInt(id, 10)]);
    return datastore.get(key).then(load => {
        if (load[0] === undefined || load[0] === null) {
            return load;
        } else {
            return load.map(fromDatastore);
        }
    })
}


// The function is used to get all loads with pagination.
async function get_loads(req) {
    // Check how many loads in the load collection.
    const q1 = datastore.createQuery(LOAD);
    let all_entities = await datastore.runQuery(q1);
    const results = {"total": all_entities[0].length};

    // Get all laods with pagination
    let q2 = datastore.createQuery(LOAD).limit(5);
    if(Object.keys(req.query).includes("cursor")) {
        q2 = q2.start(req.query.cursor);
    }
    return datastore.runQuery(q2).then(loads => {
        let loads_list = loads[0].map(fromDatastore);
        for (let i = 0; i < loads_list.length; i++) {
            loads_list[i].id = parseInt(loads_list[i].id, 10);
        }
        results.loads = loads_list
        if (loads[1].moreResults !== Datastore.NO_MORE_RESULTS) {
            results.next = req.protocol + "://" + req.get("host") + req.baseUrl + "?cursor=" + loads[1].endCursor;
        }
        return results;
    })
}


// The function is used to update a load by PATCH.
function patch_load(newLoad, id) {
    const key = datastore.key([LOAD, parseInt(id, 10)]);
    const load = {"volume": newLoad.volume, "weight": newLoad.weight, 
                  "item": newLoad.item, "carrier": null, "self": newLoad.self};
    return datastore.save({ "key": key, "data": load }).then(() => { return { "key": key, "data": load } });
}


// The function is used to update a load by PUT.
function put_load(newLoad, id, self) {
    const key = datastore.key([LOAD, parseInt(id, 10)]);
    const load = {"volume": newLoad.volume, "weight": newLoad.weight, 
                  "item": newLoad.item, "carrier": null, "self": self};
    return datastore.save({ "key": key, "data": load }).then(() => { return { "key": key, "data": load } });
}


// Delete a load.
function delete_load(id) {
    const key = datastore.key([LOAD, parseInt(id, 10)]);
    return datastore.delete(key);
}
/* ------------- End load Model Functions ------------- */



/* ------------- Begin Controller Functions ------------- */
// Create a load
router.post('/', async function(req, res) {
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
        } else if(!req.body.volume || !req.body.weight || !req.body.item) {
            // If request body is invalid.
            res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
        } else {
            const result = await load_vali(req.body);
            if (!result) {
                // If the inputs' value in request body is invlid.
                res.status(400).json({ "Error": "At least one of the attributes in request object is invalid."});
            } else {
                post_load(req)
                .then(obj => {
                    res.location(obj.data.self);
                    res.status(201).json({
                        id : parseInt(obj.key.id, 10),
                        volume : obj.data.volume,
                        weight : obj.data.weight,
                        item : obj.data.item,
                        carrier : obj.data.carrier,
                        self : obj.data.self
                    })
                })
            }
        }
    }
})


// Get all loads
router.get('/', function(req, res) {
    const accepts = req.accepts('application/json');
    if (!accepts) {
        // The endpoint cannot offers a MIME type required by the user.
        res.status(406).json({"Error": "The server only returns application/json data."});
    } else {
        get_loads(req)
        .then(loads => {
            res.status(200).json(loads);
        })
    }
})


// let "/loads" reject DELETE method 
router.delete('/', function (req, res) {
    res.set('Allow', 'GET', 'POST');
    res.status(405).json({ "Error": "This endpoint only allows GET & POST method."});
});


// let "/loads" reject PUT method 
router.put('/', function (req, res) {
    res.set('Allow', 'GET', 'POST');
    res.status(405).json({ "Error": "This endpoint only allows GET & POST method."});
});


// let "/loads" reject PATCH method 
router.patch('/', function (req, res) {
    res.set('Allow', 'GET', 'POST');
    res.status(405).json({ "Error": "This endpoint only allows GET & POST method."});
});


// View a load
router.get('/:load_id', function (req, res) {
    const accepts = req.accepts('application/json');
    if (!accepts) {
        // The endpoint cannot offers a MIME type required by the user.
        res.status(406).json({"Error": "The server only returns application/json data."})
    } else {
        const parsed = parseInt(req.params.load_id, 10);
        if (isNaN(parsed) || parsed === 0) {
            res.status(404).json({ 'Error': 'No load with this load_id exists' });
        } else {
            const parsed = parseInt(req.params.load_id, 10);
            if (isNaN(parsed) || parsed === 0) {
                res.status(404).json({ 'Error': 'No load with this load_id exists' });
            } else {
                get_load(req.params.load_id)
                .then(load => {
                    if (load[0] === undefined || load[0] === null) {
                        // If the load with load id is not found.
                        res.status(404).json({ 'Error': 'No load with this load_id exists' });
                    } else {
                        load[0].id = parseInt(load[0].id);
                        res.status(200).json(load[0]);
                    }
                })
            }
        }
    }
})


// Update a load by PATCH
router.patch('/:load_id', async function (req, res) {
    const accepts = req.accepts('application/json');
    if (!accepts) {
        // The endpoint cannot offers a MIME type required by the user.
        res.status(406).json({"Error": "The server only returns application/json data."})
    } else if (req.get('content-type') !== 'application/json') {
        // The user sends an unsupported MIME type to the endpoint.
        res.status(415).json({"Error": "The server only accepts application/json data."})
    } else {
        if (Object.keys(req.body).length == 0) {
            // If user no attribute provided.
            res.status(400).json({ "Error": "The request object is empty." });
        } else if (Object.keys(req.body).length > 3) {
            // If user provids attributes more than required.
            res.status(400).json({ "Error": "The attributes in the request object is more than required." });
        } else {
            let new_load = {};
            const properties = ['volume', 'weight', 'item']
            for (const property in req.body) {
                if (!properties.includes(property)) {
                    // The property not in the data model.
                    res.status(400).json({ "Error": "At least one of the attributes in request object is invalid." });
                    return;
                } else {
                    new_load[property] = req.body[property];
                }
            }
            const parsed = parseInt(req.params.load_id, 10);
            if (isNaN(parsed) || parsed === 0) {
                res.status(404).json({ 'Error': 'No load with this load_id exists' });
            } else {
                const old_load = await get_load(req.params.load_id);
                if (old_load[0] === undefined || old_load[0] === null) {
                    res.status(404).json({"Error": "No load with this load_id exists."});
                } else {
                    if(old_load[0].carrier != null ) {
                        res.status(403).
                        json({"Error": "The load with load_id has been loaded. It needs to be unloaded by the boat owner before updating."});
                    } else {
                        for (const property of properties) {
                            if (!Object.keys(new_load).includes(property)) {
                                new_load[property] = old_load[0][property]
                            }
                        }
                        // Valid input value.
                        const result = await load_vali(new_load);
                        if (!result) {
                            // If the inputs' value in request body is invlid.
                            res.status(400).json({ "Error": "At least one of the attributes in request object is invalid."});
                        } else {
                            new_load.self = old_load[0].self
                            patch_load(new_load, req.params.load_id)
                            .then(obj => {
                                res.status(200).json({
                                    id : parseInt(obj.key.id, 10),
                                    volume : obj.data.volume,
                                    weight : obj.data.weight,
                                    item : obj.data.item,
                                    carrier : obj.data.carrier,
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


// Update a load by PUT
router.put('/:load_id', async function (req, res) {
    const accepts = req.accepts('application/json');
    if (!accepts) {
        // The endpoint cannot offers a MIME type required by the user.
        res.status(406).json({"Error": "The server only returns application/json data."})
    } else if (req.get('content-type') !== 'application/json') {
        // The user sends an unsupported MIME type to the endpoint.
        res.status(415).json({"Error": "The server only accepts application/json data."})
    } else {
        if (Object.keys(req.body).length > 3) {
            // If user provids attributes more than required.
            res.status(400).json({ "Error": "The attributes in the request object is more than required." });
        } else if(!req.body.volume || !req.body.weight || !req.body.item) {
            // If request body is invalid.
            res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
        } else {
            const result = await load_vali(req.body);
            if (!result) {
                // If the inputs' value in request body is invlid.
                res.status(400).json({ "Error": "At least one of the attributes in request object is invalid."});
            } else {
                const parsed = parseInt(req.params.load_id, 10);
                if (isNaN(parsed) || parsed === 0) {
                    res.status(404).json({ 'Error': 'No load with this load_id exists' });
                } else {
                    const old_load = await get_load(req.params.load_id);
                    if (old_load[0] === undefined || old_load[0] === null) {
                        res.status(404).json({"Error": "No load with this load_id exists."});
                    } else {
                        if(old_load[0].carrier != null ) {
                            res.status(403).
                            json({"Error": "The load with load_id has been loaded. It needs to be unloaded by the boat owner before updating."});
                        } else {
                            put_load(req.body, req.params.load_id, old_load[0].self)
                            .then(obj => {
                                res.status(200).json({
                                    id : parseInt(obj.key.id, 10),
                                    volume : obj.data.volume,
                                    weight : obj.data.weight,
                                    item : obj.data.item,
                                    carrier : obj.data.carrier,
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


// Delete a load
router.delete('/:load_id', function(req, res) {
    const parsed = parseInt(req.params.load_id, 10);
    if (isNaN(parsed) || parsed === 0) {
        res.status(404).json({ 'Error': 'No load with this load_id exists' });
    } else {
        get_load(req.params.load_id)
        .then(load => {
            if (load[0] === undefined || load[0] === null) {
                // If the load with load_id is not found.
                res.status(404).json({ 'Error': 'No load with this load_id exists.' });
            } else {
                if (load[0].carrier != null) {
                    res.status(403).
                    json({"Error": "The load with load_id has been loaded. It needs to be unloaded by the boat owner before deleting."});
                } else {
                    delete_load(req.params.load_id).then(res.status(204).end()); 
                }
            }
        })
    }
})


// let "/loads/:load_id" reject POST method 
router.post('/:load_id', function (req, res) {
    res.set('Allow', 'GET', 'PUT', 'PATCH', 'DELETE');
    res.status(405).json({ "Error": "This endpoint does not allow the POST method."});
});
/* ------------- End Controller Functions ------------- */

module.exports = router;