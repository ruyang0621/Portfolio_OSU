var express = require('express');
var mysql = require('./dbcon.js');
var app = express();
var cors = require('cors');
app.set('port', 4949);
app.use(express.static('public'));
app.use(express.urlencoded());
app.use(express.json());

// this may able to remove later
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});

app.use(cors({origin:true,credentials:true}));

app.get('/',function(req, res){
    fetchAll(res);
});

app.post('/',function(req, res){
    mysql.pool.query('INSERT INTO workouts (`name`, `reps`, `weight`, `lbs`, `date`) VALUES (?, ?, ?, ?, ?)', 
    [req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date], 
    function (err, rows, fields){
        if(err){
            next(err);
            return;
        }
        fetchAll(res);
    });
});

app.put('/',function(req, res){
    mysql.pool.query('UPDATE workouts set name = ?, reps = ?, weight = ?, lbs = ?, date = ? WHERE id = ?', 
    [req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date, req.body.id],
    function (err, rows, fields){
        if(err){
            next(err);
            return;
        }
        fetchAll(res);
    });
});

app.delete('/',function(req, res){
    mysql.pool.query('DELETE FROM workouts WHERE id = ?',
    [req.body.id],
    function (err, rows, fields){
        if(err){
            next(err);
            return;
        }
        fetchAll(res);
    });
});


app.get('/reset-table', function(req, res, next){
    let context = {};
    mysql.pool.query('DROP TABLE IF EXISTS workouts', function(err){
        let createString = "CREATE TABLE workouts("+
        "id INT PRIMARY KEY AUTO_INCREMENT,"+
        "name VARCHAR(255) NOT NULL,"+
        "reps INT,"+
        "weight INT,"+
        "date DATE,"+
        "lbs BOOLEAN)";
        mysql.pool.query(createString, function(err){
            res.send('remove-successfully');
        });
    });
});


app.use(function(req, res){
    res.status(404);
    res.send('404 - Not Found');
});
  
app.use(function(err, req, res, next){
    console.error(err.stack);
    res.status(500);
    res.send('500 - Server Error');
});

app.listen(app.get('port'), function(){
    console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
})

function fetchAll(res){
    var context = {};
    mysql.pool.query('SELECT * FROM workouts', function (err, rows, fields){
        if(err){
            next(err);
            return;
        }
        context.data = rows;
        res.send(context);
    });
}