from sqlalchemy import orm
from abc import abstractmethod


class SqlQuery(object):
    """TODO."""

    def __init__(self, session: orm.Session, query: orm.Query = None):
        """
        TODO.
        :param session:
        :param query:
        """

        self.session = session
        self.query = query or self._get_base_query()

    @abstractmethod
    def _get_base_query(self) -> orm.Query:
        """TODO Describe with example."""

        raise NotImplementedError

    def __iter__(self):
        """TODO."""

        return iter(self.query)

    def __getattr__(self, name):
        """TODO."""

        return getattr(self.query, name)

    def filter(self, *filters):
        """
        TODO.

        TODO Describe with example

        Example usage::

            filter(Model.age==35, Model.country=='Denmark')

        :param filters:
        :return:
        """
        return self.__class__(self.session, self.query.filter(*filters))

    def filter_by(self, **filters):
        """
        TODO.

        TODO Describe with example

        Example usage::

            filter_by(age=35, country='Denmark')

        :param filters:
        :return:
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
