BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "User" (
	"userID"	INTEGER,
	"password"	TEXT,
	"nickname"	TEXT,
	"gender"	TEXT,
	"age"	INTEGER,
	"reputationScore"	NUMERIC,
	"cellphone"	TEXT,
	"email"	TEXT UNIQUE,
	PRIMARY KEY("userID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Activity" (
	"activityID"	INTEGER,
	"title"	TEXT,
	"time"	TEXT,
	"area"	TEXT,
	"location"	TEXT,
	"category"	TEXT,
	"peopleLimited"	INTEGER,
	"signUp"	INTEGER,
	"fee"	INTEGER,
	"expireDate"	TEXT,
	"status"	TEXT,
	"organizerUserID"	INTEGER,
	PRIMARY KEY("activityID" AUTOINCREMENT),
	FOREIGN KEY("organizerUserID") REFERENCES "User"("userID")
);
CREATE TABLE IF NOT EXISTS "Participant" (
	"participantUserID"	INTEGER,
	"participantActivityID"	INTEGER,
	"score"	INTEGER,
	PRIMARY KEY("participantUserID","participantActivityID"),
	FOREIGN KEY("participantUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("participantActivityID") REFERENCES "Activity"("activityID")
);
CREATE TABLE IF NOT EXISTS "Discussion" (
	"discussionID"	INTEGER,
	"discussionUserID"	INTEGER,
	"discussionActivityID"	INTEGER,
	"discussionTime"	TEXT,
	"discussionContent"	TEXT,
	PRIMARY KEY("discussionID" AUTOINCREMENT),
	FOREIGN KEY("discussionUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("discussionActivityID") REFERENCES "Activity"("activityID")
);
CREATE TABLE IF NOT EXISTS "Post" (
	"postID"	INTEGER,
	"postUserID"	INTEGER,
	"postTime"	TEXT,
	"postContent"	TEXT,
	PRIMARY KEY("postID" AUTOINCREMENT),
	FOREIGN KEY("postUserID") REFERENCES "User"("userID")
);
CREATE TABLE IF NOT EXISTS "Comment" (
	"commentID"	INTEGER,
	"commentPostID"	INTEGER,
	"commentUserID"	INTEGER,
	"commentTime"	TEXT,
	"commentContent"	TEXT,
	PRIMARY KEY("commentID" AUTOINCREMENT),
	FOREIGN KEY("commentPostID") REFERENCES "Post"("postID"),
	FOREIGN KEY("commentUserID") REFERENCES "User"("userID")
);
COMMIT;
