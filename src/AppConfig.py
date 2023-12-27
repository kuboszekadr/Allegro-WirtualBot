import environ

@environ.config(prefix='')
class AppConfig:

    @environ.config(prefix='ALLEGRO')
    class Allegro:
        client_id = environ.var()
        client_secret = environ.var()
        user_name = environ.var()
        device_code = environ.var()
        prefix = "" if environ.var('ENV') == 'PROD' else '.allegrosandbox.pl'

    allegro = environ.group(Allegro)

config = AppConfig.from_environ()