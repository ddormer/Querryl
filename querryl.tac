from querryl.deployment import deploy

config = {}
exec file('config.py', 'rb') in config
del config['__builtins__']

application = deploy(**config)
