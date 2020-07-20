
if __name__ == '__main__':
    try:
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv())
    except ImportError:
        pass
    from . import cli
    cli()
