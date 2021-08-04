var mysql = require('mysql');
var pool = mysql.createPool({
    connectionLimit : 10,
    host            : 'classmysql.engr.oregonstate.edu',
    user            : 'cs290_yangr2',
    password        : '20210330',
    database        : 'cs290_yangr2'
  });
  
  module.exports.pool = pool;