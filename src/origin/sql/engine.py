from wrapt import decorator
from typing import Dict, Any
from sqlalchemy import orm, engine
from functools import cached_property


class SqlEngine(object):
    """Class to create the Sql Engine."""

    # Shortcut/alias
    Session = orm.Session

    def __init__(self, uri: str, pool_size: int = 1):
        self.uri = uri
        self.pool_size = pool_size
        self._uri = None
        self._engine = None

    @property
    def settings(self) -> Dict[str, Any]:
        """Parameter settings for the Engine instance."""

        return {
            'echo': False,
            'pool_pre_ping': True,
            'pool_size': self.pool_size,
        }

    @property
    def engine(self) -> engine.Engine:
        """Create a new Engine instance."""

        if self.uri != self._uri:
            self._uri = self.uri
            self._engine = engine.create_engine(self.uri, **self.settings)
        return self._engine

    @property
    def session_class(self) -> orm.scoped_session:
        """Create the session with the new Engine."""

        orm.configure_mappers()
        factory = orm.sessionmaker(bind=self.engine, expire_on_commit=False)
        session_class = orm.scoped_session(factory)
        return session_class

    @cached_property
    def registry(self) -> orm.registry:
        """
        Registry to maintaining a collection of mappings.

        The registry serves as the basis for maintaining a collection of
        mappings, and provides configurational hooks used to map classes.
        """

        return orm.registry()

    @cached_property
    def ModelBase(self) -> orm.declarative_base:
        """Metaclass that produces appropriate Table objects."""

        return self.registry.generate_base()

    def make_session(self) -> orm.Session:
        """
        Create a new database session.

        :rtype: sqlalchemy.orm.Session
        """
        return self.session_class()

    def apply_schema(self):
        """Create all tables stored in the metadata."""

        self.ModelBase.metadata.create_all(self.engine)

    def session(self):
        """
        Make a connection from an Engine that is associated with the Session.

        Function decorator which injects a "session" named parameter
        if it doesn't already exists.
        """
        @decorator
        def session_decorator(wrapped, instance, args, kwargs):
            # pylint: disable=unused-argument
            session = kwargs.setdefault(
                'session', self.make_session())

            try:
                return wrapped(*args, **kwargs)
            finally:
                session.close()

        return session_decorator

    def atomic(self):
        """
        Wrap the function in an atomic transaction.

        The decorator which injects a "session" named parameter if it
        doesn't  already exists, and wraps the function in an atomic
        transaction.
        """
        @decorator
        def atomic_wrapper(wrapped, instance, args, kwargs):
            # pylint: disable=unused-argument
            session: orm.Session = kwargs.setdefault(
                'session', self.make_session())

            session.begin()

            try:
                return_value = wrapped(*args, **kwargs)
            except:  # noqa: E722
                session.rollback()
                raise
            else:
                session.commit()
                return return_value
            finally:
                session.close()

        return atomic_wrapper
