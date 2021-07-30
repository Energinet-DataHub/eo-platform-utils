from abc import abstractmethod
from typing import Dict, Optional


class Context(object):
    """
    Context for a single incoming HTTP request.
    """

    @property
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        """
        Returns request headers.
        """
        raise NotImplementedError

    @property
    def token(self) -> Optional[str]:
        """
        Returns request Bearer token.
        """
        if 'Authorization' in self.headers:
            value = self.headers['Authorization']
            if value.startswith('Bearer: '):
                return value.split('Bearer: ')[1]
        return None
