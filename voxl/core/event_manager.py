# TODO all hooks managed by this guy.
# impl an EventManager. it will have 'listen' and 'emit'
# also a base Event (data?)class, which events (eg. MeshAdded, AssetLoaded) will inherit.
# The event classes will be in a separate core/events.py file.
# emit() will take these Event classes
# listen(event: str (eg. "MeshAdded"), callback: Callable[[Event], None]) -> None
