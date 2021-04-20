var db = connect("mongodb://admin:syllabuddy@localhost:27017/admin");

db = db.getSiblingDB("syllabuddy");

db.createUser(
    {
	user: "syllabuddy",
	pwd: "syllabuddy123",
	roles: [ { role:"readWrite", db: "syllabuddy"} ],
	passwordDigestor: "server",
    }
)
