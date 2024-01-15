import environ

@environ.config(prefix='')
class AppConfig:

    @environ.config(prefix='ALLEGRO')
    class Allegro:
        client_id = environ.var()
        client_secret = environ.var()
        user_name = environ.var()
        api_base_url=environ.var()

    allegro = environ.group(Allegro)

config = AppConfig.from_environ()

if __name__ == '__main__':

    print(config.allegro.client_id)
    print(config.allegro.client_secret)
    print(config.allegro.user_name)
    print(config.allegro.api_base_url)