from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with 
from flask_sqlalchemy import SQLAlchemy 
# abort help us to send error message if the input id is not present in database
# reqparse make sure when we pass the request we pass the required information with the request

app = Flask(__name__)
api = Api(app)  # wreapping our app in api
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.database' # location of database. it' a relative database in the current directory we're in. so we make a db file in the current direcory we're in
# if you want to make the database file in a folder in the current directory you're on then sqlite///temp/db.database
db = SQLAlchemy(app)


# creating the database 
class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):  # this function is made so that if we print something out we should get something
		return f"Video(name = {name}, views = {views}, likes = {likes})"


# create database, only used once when we initially run the program so that it should not override the database again and again each time it runs
# db.create_all() 

# we are making a request parser object and what this going to do is automatically parse throught the request automatially parse through teh request sent and it fits teh guideline we're about to define below and has correct informationin it
video_put_args = reqparse.RequestParser()
# making the guideline fro the information we want
# we have request parser in which these three arguments are mandatory             
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True) 
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views on the video is required", required=True)   

# this we are making so that we can get input from user what he wants to change in and existing video stats
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required") 
video_update_args.add_argument("likes", type=int, help="Likes on the video is required")
video_update_args.add_argument("views", type=int, help="Views on the video is required")

# resource_field is a way of how an object should be serialize
resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}


class Video(Resource):
    # what this actually means is that when we get result from teh get function then serialize it using teh resource field for the client to read properly
    @marshal_with(resource_fields)
    # the below function give reponse for GET requests
    def get(video, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()  # getting the information of the video with video_id as it's id and it will give instances of videomodel taht matches teh videoid
        if not result:
            abort(404, message="Video doesn't exist...")
        return result  # this result will be an instance of videomodel class
    
    # to store the video information in the object creating new video information [Request argument parser]
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args() # this will get all the arguments from the parser object above. it's also a dictionary
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video already exists...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video) # temporarily add in databse session
        db.session.commit() # it will commit any changes i have made in the session and make them permanent
        return  video, 201  # 201 is status code for created
    
    # an http method for update in the db
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist...")
        # since it already replace unpass arguments with none, we check whether the key value is not none, then only we updtae
        if args['name']:
            result.name=args['name']
        if args['views']:
            result.views=args['views']
        if args['likes']:
            result.likes=args['likes']

        db.session.commit()
        return result
    
    # to delete video and it's inforamation
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exists...")
        # video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.delete(result)
        db.session.commit()
        return "", 204 # 204 stands fro deleted successfully
 


api.add_resource(Video, "/video/<int:video_id>")

if __name__=="__main__":
    # this starts our server and flask application 
    # also this is in debug mode so if anything goes wrong we'll see why, but debug mode is only used for development process not in the production environment
    app.run(debug=True)