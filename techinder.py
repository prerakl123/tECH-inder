from app import app, db
from app.models import User, Project, followers, Location, Message, Misconduct, Applied


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Project': Project,
        'followers': followers,
        'Location': Location,
        'Message': Message,
        'Misconduct': Misconduct,
        'Applied': Applied
    }


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
