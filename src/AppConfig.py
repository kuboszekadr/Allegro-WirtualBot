import environ

@environ.config(prefix='')
class AppConfig:

    @environ.config(prefix='ALLEGRO')
    class Allegro:
        client_id = environ.var()
        client_secret = environ.var()
        device_code = environ.var()
        user_name = environ.var()

    allegro = environ.group(Allegro)

config = AppConfig.from_environ()