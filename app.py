# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import os

# app initialization
app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))
# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

# Models


class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    analysis = db.relationship('Analysis', backref='author')

    def __repr__(self):
        return '<User %r>' % self.username


class Analysis(db.Model):
    __tablename__ = 'analysis'
    uuid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))

    def __repr__(self):
        return '<Post %r>' % self.title

# Schema Objects


class AnalysisObject(SQLAlchemyObjectType):
    class Meta:
        model = Analysis
        interfaces = (graphene.relay.Node, )


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_analysis = SQLAlchemyConnectionField(AnalysisObject)
    all_users = SQLAlchemyConnectionField(UserObject)


schema = graphene.Schema(query=Query)

# Routes
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)


@app.route('/')
def index():
    return '<p>Navigate to 127.0.0.1:5000/graphql to see the GraphQLi view</p>'


if __name__ == '__main__':
    app.run()
