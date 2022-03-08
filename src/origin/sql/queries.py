from sqlalchemy import orm
from abc import abstractmethod


class SqlQuery(object):
    """ORM-level SQL construction class."""

    def __init__(self, session: orm.Session, query: orm.Query = None):
        self.session = session
        self.query = query or self._get_base_query()

    @abstractmethod
    def _get_base_query(self) -> orm.Query:
        """Handle the error if the Query is bad."""
        raise NotImplementedError

    def __iter__(self):
        """Iterate though the query."""

        return iter(self.query)

    def __getattr__(self, name):
        """Get the name attribute for the object."""

        return getattr(self.query, name)

    def filter(self, *filters):
        """
        Apply the given filtering criterion (keyword) to a copy of the Query.

        Example usage::
            filter(Model.age==35, Model.country=='Denmark')

        :param filters: filtering criterion
        :return: Result of the filtering criterion
        """
        return self.__class__(self.session, self.query.filter(*filters))

    def filter_by(self, **filters):
        """
        Apply the given filtering criteria (keywords) to a copy of the Query.

        Example usage::
            filter_by(age=35, country='Denmark')

        :param filters: filtering criteria
        :return: Result of the filtering criteria
        """
        return self.__class__(self.session, self.query.filter_by(**filters))

    def only(self, *fields):
        """
        Narrows down the columns to select.

        TODO Example usage

        :param fields:
        :return:
        """
        return self.__class__(self.session, self.query.options(
            orm.load_only(*fields)
        ))

    def get(self, field):
        """
        TODO.

        TODO Example usage

        :param field:
        :return: value for the field from the first result.
        """
        return self.only(field).scalar()

    def exists(self):
        """
        TODO.

        :return: True if result count is >= 1
        """
        return self.count() > 0
