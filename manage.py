from main import app, db, User


def ensure_doctor(email: str = 'doctor@example.com', password: str = 'doctor123', name: str = 'Doctor'):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            user.name = name
            user.is_doctor = True
            db.session.commit()
            print(f"Updated existing doctor: {email}")
        else:
            user = User(email=email, name=name, is_doctor=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Created new doctor: {email}")


def list_users():
    with app.app_context():
        users = User.query.all()
        for u in users:
            print(f"id={u.id} email={u.email} is_doctor={u.is_doctor} name={u.name}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Manage Triage System users')
    sub = parser.add_subparsers(dest='cmd')

    s1 = sub.add_parser('ensure_doctor')
    s1.add_argument('--email', default='doctor@example.com')
    s1.add_argument('--password', default='doctor123')
    s1.add_argument('--name', default='Doctor')

    sub.add_parser('list_users')

    args = parser.parse_args()

    if args.cmd == 'ensure_doctor':
        ensure_doctor(args.email, args.password, args.name)
    elif args.cmd == 'list_users':
        list_users()
    else:
        parser.print_help()

